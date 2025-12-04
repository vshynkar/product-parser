from bs4 import BeautifulSoup, Comment
from bs4.element import Tag
from markdownify import markdownify as md

UNWANTED_TAGS = ['script', 'link', 'style', 'picture', 'svg', 'source', 'iframe', 'noscript', 'use',
                             'button', 'footer', 'header']

UNWRAP_TAGS = ['a', 'span', 'b', 'strong', 'i', 'em', 'u', 'font']

WHITELIST_ATTR_GLOBAL = ["id", "class", "title", "lang", "dir", "hidden", "translate", "accesskey", "contenteditable"]
WHITELIST_ATTR_META = ['content', 'charset', 'http-equiv', 'itemprop', 'itemscope', 'itemtype']
WHITELIST_ATTR_IMG = ['alt']
WHITELIST_ATTR_FORM = ['name', 'value', 'disabled', 'checked', 'selected', 'step']
WHITELIST_ATTR_INPUT = ['type', 'for']
WHITELIST_ATTR_TABLE = ['colspan', 'rowspan', 'headers', 'scope']

WHITELIST_ATTR_ALL = (WHITELIST_ATTR_GLOBAL + WHITELIST_ATTR_META, WHITELIST_ATTR_IMG
                      + WHITELIST_ATTR_FORM + WHITELIST_ATTR_INPUT + WHITELIST_ATTR_TABLE)

def remove_unwanted_tags(soup: BeautifulSoup) -> None:
    for tag_name in UNWANTED_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()


def remove_comments(soup: BeautifulSoup) -> None:
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()


def filter_attributes(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(True):
        for attr in list(tag.attrs.keys()):
            if attr not in WHITELIST_ATTR_ALL:
                del tag.attrs[attr]


def unwrap_and_cleanup_tags(soup: BeautifulSoup) -> None:
    for tag in list(soup.find_all()):
        tag_name = tag.name.lower()
        if '-' in tag_name:
            # Unwrap custom elements (tags containing '-') — keep inner content
            tag.unwrap()
        elif tag_name in UNWRAP_TAGS:
            # Unwrap all tags from UNWRAP_TAGS list
            tag.unwrap()
        elif tag_name == "img":
            alt = tag.get("alt")
            if alt is not None and str(alt).strip() == "":
                tag.decompose()


def remove_empty_div(soup: BeautifulSoup, empty_div_passes: int = 5) -> None:
    # handle nested empty divs (stop early if no removals on a pass).
    for _ in range(max(0, int(empty_div_passes))):
        removed_any = False
        for div in list(soup.find_all("div")):
            # Consider a div non-empty if it has any non-div tag descendant
            # (e.g., <img>, <p>, etc.) or contains non-whitespace text.
            has_text = div.get_text(strip=True) != ""
            has_non_div_descendant = any(
                isinstance(d, Tag) and d.name != "div" for d in div.descendants
            )
            if not has_text and not has_non_div_descendant:
                div.decompose()
                removed_any = True
        if not removed_any:
            break


def html_cleanup(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")

    # 1. Remove scripts and styles and other
    remove_unwanted_tags(soup)

    # 2. Remove HTML comments
    remove_comments(soup)

    # 3. Remove all attributes that are not in WHITELIST_ATTR_ALL
    filter_attributes(soup)

    # 4. Unwrap UI framework and formatting tags
    unwrap_and_cleanup_tags(soup)

    # Finally: remove empty <div> tags. Repeat up to `empty_div_passes` times
    remove_empty_div(soup)

    return str(soup)


def html_to_markdown(cleaned_html: str) -> str:
    markdown_text = md(
        cleaned_html,
        heading_style="ATX",  # # H1, ## H2, etc.
        strip=["style", "script", "img", "video"],  # вже вирізано, але на всяк випадок
        # convert=["p", "br", "ul", "ol", "li", "table", "tr", "th", "td", "strong", "em"]
    )

    # Optional: нормалізувати зайві пусті рядки
    lines = [line.rstrip() for line in markdown_text.splitlines()]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    markdown_text = "\n".join(lines)

    return markdown_text

