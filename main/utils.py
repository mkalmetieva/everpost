from PIL import Image
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError

VALID_TAGS = ['b', 'i', 'u', 'strike', 'a', 'ul', 'ol', 'li', 'a', 'img', 'br', 'div']
VALID_ATTRS = ["href", "title", "target", "src", "alt"]

MAX_IMG_WIDTH = 750
MAX_IMG_HEIGHT = 3000


def sanitize_html(value):
    soup = BeautifulSoup(value)

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.decompose()
        else:
            clean_attrs(tag.attrs)

    return soup.renderContents()


def clean_attrs(attrs):
    for attribute in list(attrs):
        if attribute not in VALID_ATTRS:
            del attrs[attribute]


def resize_if_needed(file):
    img_data = Image.open(file)
    if img_data.size[1] > MAX_IMG_HEIGHT:
        raise ValidationError('Too large image')
    if img_data.size[0] > MAX_IMG_WIDTH:
        wpercent = (MAX_IMG_WIDTH / float(img_data.size[0]))
        hsize = int((float(img_data.size[1]) * float(wpercent)))
        img_data = img_data.resize((MAX_IMG_WIDTH, hsize), Image.ANTIALIAS)
        img_data.save(file.name)
