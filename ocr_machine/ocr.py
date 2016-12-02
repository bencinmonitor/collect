import cv2
from PIL import Image
from tesserocr import PyTessBaseAPI
from fuzzywuzzy import process
import re, itertools

TESSEDIT_CHAR_WHITELIST = "čČabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321-.,:/"
PHRASES_LIST = ['Kurilno', 'olje', 'EL', 'OMV', 'Petrol', 'Diesel', 'MaxxMotion', 'EUR', 'Datum/Čas',
                'Max', 'LPG', 'futurPlus', 'futur', 'Plus', 'Q', 'Q Max', 'OMV Diesel', 'Max Diesel']
WORDS_LIST = list(set(itertools.chain(*map(lambda w: w.split(), PHRASES_LIST))))


def ocr_pipeline(image_paths):
    """ OCR pipeline with pre and post-processing. """
    return post_process(ocr(pre_process(image_paths)))


def pre_process(image_paths, min_f=2.40, max_f=2.30):
    """ Execures pre-processing stage"""
    return [pre_process_image(path, min_f=2.40, max_f=2.30) for path in image_paths]


def pre_process_image(path, min_f=2.40, max_f=2.30):
    """ Removes noise and imperfections from images. """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    original_width = image.shape[1]
    if original_width < 400:
        base_width = int(original_width * min_f)
    else:
        base_width = int(original_width * max_f)

    w_ratio = float(base_width) / float(image.shape[1])
    h_size = int((float(image.shape[0]) * float(w_ratio)))

    image_resized = cv2.resize(image, (base_width, h_size), interpolation=cv2.INTER_NEAREST)
    _, image_resized = cv2.threshold(image_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return Image.fromarray(image_resized)


def ocr(images):
    """ Executes OCR on text and returns words, text and confidence numbers. """
    results = []
    with PyTessBaseAPI(lang='slv') as api:
        api.SetVariable("tessedit_char_whitelist", TESSEDIT_CHAR_WHITELIST)
        api.SetVariable("classify_enable_learning", "0")
        api.SetVariable("classify_enable_adaptive_matcher", "0")
        api.SetVariable("load_system_dawg", "0")
        api.SetVariable("load_freq_dawg", "0")

        for image in images:
            api.SetImage(image)

            results.append({
                'words_confidences': api.AllWordConfidences(),
                'words': api.AllWords(),
                'text': api.GetUTF8Text(),
            })

    return results


def should_replace(ocr_confidence, fuzzy_confidence, replacement_thresholds=(60, 60)):
    """ This method could eventually be improved with machine learning model. (or ID3) """
    ocr_confidence_threshold, fuzzy_confidence_threshold = replacement_thresholds

    ocr_beyond = ocr_confidence >= ocr_confidence_threshold
    ocr_lower = ocr_confidence < ocr_confidence_threshold

    fuzzy_beyond = fuzzy_confidence >= fuzzy_confidence_threshold
    fuzzy_lower = fuzzy_confidence < fuzzy_confidence_threshold

    if ocr_lower and fuzzy_beyond:
        return True

    if ocr_beyond and fuzzy_beyond:
        return True
    return False


def post_text_process(nodes, debug=False, word_list=WORDS_LIST):
    """ Computes confidences for OCR and fuzzy-matches end executes replacements. """
    fuzzy_confidences = [{'fuzzy_confidences': [process.extractOne(word, word_list)
                                                for word in node['words']]} for node in nodes]

    results = [{**a, **b} for a, b in list(zip(nodes, fuzzy_confidences))]

    for index, result in enumerate(results):
        replacements = [(ocr_conf, fuzzy_conf, fuzzy_word, should_replace(ocr_conf, fuzzy_conf)) for
                        (ocr_conf, (fuzzy_word, fuzzy_conf))
                        in zip(result['words_confidences'], result['fuzzy_confidences'])]
        results[index]['replacements'] = replacements

    for index, result in enumerate(results):
        out_words = [fuzzy_word if should_be_replaced else word for
                     word, (ocr_conf, fuzzy_conf, fuzzy_word, should_be_replaced)
                     in zip(result['words'], result['replacements'])]
        results[index]['post_text'] = ' '.join(out_words)

    return results


def numbers_fixing(text):
    """ Tries to fix things that look like numbers with Regular expressions. """

    # 1. Remove date to prevent future fuckups.
    text = re.sub("\d{4}-\d{2}-\d{2}\s+\d{2}\:\d{2}", "YMD-HIS", text)

    # 2. Get potential 3 digit screwups and fix them.
    pre_post = re.sub(r"\.?\,?(\d{1})\-*(\d{2,2})\s", r"\1\2 ", text + " ")

    # 3. Get 4 digit screwups and fix them.
    post_text = re.sub(r"(\d{1})\s*\.?\,?\s*(\d{3,3})\s*\b", r"\1,\2 ", pre_post + " ")

    return post_text.strip()


def post_number_fixer(nodes, debug=True):
    """ Executes number fixing and build "out_text". """
    return [{**node, **{'out_text': numbers_fixing(node['post_text'])}} for node in nodes]


def post_process(nodes, debug_text=False, debug_numbers=False, word_list=WORDS_LIST):
    """" Tries to fix OCR mistakes with fuzzy-matching. Tries to fix numbers with regex. """
    nodes = post_text_process(nodes, debug=debug_text, word_list=word_list)
    nodes = post_number_fixer(nodes, debug=debug_numbers)
    return nodes
