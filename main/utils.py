from bs4 import BeautifulSoup

VALID_TAGS = ['b', 'i', 'u', 'strike', 'a', 'ul', 'ol', 'li', 'a', 'img', 'br', 'div']
VALID_ATTRS = ["href", "title", "target", "src", "alt"]


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
