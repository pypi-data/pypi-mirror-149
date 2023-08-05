import re

CLEAN_UP_PATTERNS = [
    ('\n', ''),
    ('-<br />', '<lb break="no"/>'),
    ('<br />', '<lb />\n'),
    ('</p>', '</p>\n'),
    ('‚', ','),
    ('ı', 'i')
]


def clean_markup(source, patterns=CLEAN_UP_PATTERNS):
    """ applies search and replace
    :param source: A string to clean
    :type source: str
    :param patterns: a list of tuples `[('-<br />', '<lb break="no"/>'),`]
    :type patterns: list

    :return: the cleaned string
    :rtype: str

    """
    for x in patterns:
        source = source.replace(x[0], x[1])
    return source


def normalize_white_space(source):
    """ removes all superfluos whitespaces
    :param source: A string to clean
    :type source: str

    :return: the cleaned string
    :rtype: str

    """
    source = ' '.join(source.split())
    return source


def extract_page_nr(some_string):
    """ extracts the page number from a string like `Seite 21`

    :param some_string: e.g. `Seite 21`
    :type some_string: str

    :return: The page number e.g. `21`
    :rtype: str
    """

    page_nr = re.findall(r'\d+', some_string)
    if len(page_nr) > 0:
        return "-".join(page_nr)
    else:
        return some_string


def always_https(url):
    """ ensures that urls are always using HTTPS

    :param url: An URL (as string)
    :type url: str

    :return: The passed in URL with HTTPS
    :rtrype: str

    """

    if not url.startswith('http'):
        return url
    elif url.startswith('https'):
        return url
    else:
        https_url = url.replace('http://', 'https://')
        return https_url
