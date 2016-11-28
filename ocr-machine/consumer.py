import argparse
from kafka import KafkaConsumer
from collector.settings import *
from PIL import *
from PIL import Image, ImageFilter
import tesserocr
from tesserocr import PyTessBaseAPI, PSM
import re

PSM.

def start_kafka_consumer():
    consumer = KafkaConsumer(KAFKA_SCRAPED_ITEMS_TOPIC, **{
        'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
        'group_id': 'ocr'
    })

    for msg in consumer:
        print(msg)


def clean_text(text):
    # out = re.sub('\s+', ' ', text).strip()
    # out = re.sub(r"\n(?=[^\n\t])", " ", text)
    out = text.strip()
    # out = out.replace("\n\n", '\n')
    print(out)


def process_image(path):
    print("Processing %s" % path)
    image = Image.open(path).convert("L")

    basewidth = 1000
    wpercent = float(basewidth) / float(image.size[0])
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.QUAD)  # Bicubic # LIBIMAGEQUANT

    # f = 1.1
    # nx, ny = image.size
    # image = image.resize((int(nx * f), int(ny * f)), Image.ADAPTIVE)

    # image.save("to-ts.tiff", format="tiff")

    # image5 = image.filter(ImageFilter.BLUR)
    # image5.save("f-5.jpg", format='JPEG', subsampling=0, quality=10)

    # image4 = image.filter(ImageFilter.EDGE_ENHANCE)
    # image4.save("f-0.jpg", format='JPEG', subsampling=0, quality=10)

    image = image.filter(ImageFilter.EDGE_ENHANCE)
    # image3.save("f-1.tiff")
    # image = image.filter(ImageFilter.EDGE_ENHANCE)
    # image2.save("f-2.jpg", format='JPEG', subsampling=0, quality=10)

    # image.save("to-ts.tiff", format="tiff")

    text = tesserocr.image_to_text(image, lang="slv")
    clean_text(text)

    # with PyTessBaseAPI(lang="slv") as api:
    #    api.SetImage(image)
    # api.Recognize()
    # api.SetVariable("user_words", "/Users/otobrglez/bencinmonitor/collect/user-words.txt")

    #   clean_text(api.GetUTF8Text())


    # print(api.AllWordConfidences())

    # it = api.AnalyseLayout()
    # orientation, direction, order, deskew_angle = it.Orientation()
    # print(orientation, direction, orientation, deskew_angle)

    # image.save('test.tiff', format='tiff')
    # print("Format %s", image)
    # text = tesserocr.image_to_text(image, lang='eng+deu+slv', psm=tesserocr.PSM.AUTO)
    # print(text)

    # print(tesserocr.tesseract_version())  # print tesseract-ocr version
    # print(tesserocr.get_languages())
    # image.save("test.jpg", format='JPEG', )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Image to use instead of stream", type=str)
    args = parser.parse_args()

    if args.image:
        process_image(args.image)
    else:
        start_kafka_consumer()
