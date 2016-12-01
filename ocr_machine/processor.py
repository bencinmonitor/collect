from json import loads, load
import cv2
from PIL import Image
from tesserocr import PyTessBaseAPI
from fuzzywuzzy import fuzz, process
import itertools
from os import getenv
import re

TESSEDIT_CHAR_WHITELIST = "čČabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321-.,:/"
PHRASES_LIST = ['Kurilno', 'olje', 'EL', 'OMV', 'Petrol', 'Diesel', 'MaxxMotion', 'EUR', 'Datum/Čas',
                'Max', 'LPG', 'futurPlus', 'futur', 'Plus', 'Q', 'Q Max', 'OMV Diesel', 'Max Diesel']
WORDS_LIST = list(set(itertools.chain(*map(lambda w: w.split(), PHRASES_LIST))))


def process_station(station_as_json):
    station = loads(station_as_json, 'utf8')
    print("Processing station: \"%s\"" % station['name'])
    r = 10 / 0


def ocr_pipeline(image_paths):
    return post_process(ocr(pre_process(image_paths)))


def pre_process(image_paths, min_f=2.40, max_f=2.30):
    return [pre_process_image(path, min_f=2.40, max_f=2.30) for path in image_paths]


def pre_process_image(path, min_f=2.40, max_f=2.30):
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


from pprint import pprint


def should_replace(ocr_confidence, fuzzy_confidence, replacement_thresholds=(60, 60)):
    """ This method could eventually be improved with machine learning model (or ID3) """
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
    fuzzy_confidences = [{'fuzzy_confidences': [process.extractOne(word, word_list) for word in node['words']]} for
                         node in nodes]
    results = [{**a, **b} for a, b in list(zip(nodes, fuzzy_confidences))]

    for index, result in enumerate(results):
        replacements = [(ocr_conf, fuzzy_conf, fuzzy_word, should_replace(ocr_conf, fuzzy_conf)) for
                        (ocr_conf, (fuzzy_word, fuzzy_conf)) in
                        zip(result['words_confidences'], result['fuzzy_confidences'])]
        results[index]['replacements'] = replacements

    if debug or (getenv("DEBUG_POST_PROCESS", "0") is "1"):
        print("----- post_process DEBUG START -----")

        for result in results:
            for word, replacement in zip(result['words'], result['replacements']):
                out_word = word

                if replacement[3]:
                    out_word = replacement[2]

                print("%s\t%d\t%d\t%s\t%s" % (
                    out_word.strip(), replacement[0], replacement[1], replacement[2], replacement[3]))

        print("----- post_process DEBUG STOP -----")

    for index, result in enumerate(results):
        out_words = [fuzzy_word if should_be_replaced else word for
                     word, (ocr_conf, fuzzy_conf, fuzzy_word, should_be_replaced) in zip(result['words'],
                                                                                         result['replacements'])]

        results[index]['post_text'] = ' '.join(out_words)

    return results


def numbers_fixing(text):
    return re.sub(r"(\d{1})\s*[\.\,]?(\d{3,3})\s\b", r"\1,\2 ", text)


def post_number_fixer(nodes, debug=True):
    return [{**node, **{'out_text': numbers_fixing(node['post_text'])}} for node in nodes]


def post_process(nodes, debug_text=False, debug_numbers=False, word_list=WORDS_LIST):
    nodes = post_text_process(nodes, debug=debug_text, word_list=word_list)
    nodes = post_number_fixer(nodes, debug=debug_numbers)
    return nodes
