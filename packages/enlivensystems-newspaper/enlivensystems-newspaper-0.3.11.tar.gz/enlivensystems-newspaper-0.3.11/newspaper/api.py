# -*- coding: utf-8 -*-
"""
Ignore the unused imports, this file's purpose is to make visible
anything which a user might need to import from newspaper.
View newspaper/__init__.py for its usage.
"""
__title__ = 'newspaper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
__version__ = '0.3.4.2'

import feedparser

from .article import Article, ArticleException
from .configuration import Configuration
from .settings import POPULAR_URLS, TRENDING_URL
from .source import Source
from .utils import extend_config, print_available_languages
import json
import sys
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def build(url='', dry=False, config=None, **kwargs) -> Source:
    """Returns a constructed source object without
    downloading or parsing the articles
    """
    config = config or Configuration()
    config = extend_config(config, kwargs)
    url = url or ''
    s = Source(url, config=config)
    if not dry:
        s.build()
    return s


def build_article(url='', config=None, **kwargs) -> Article:
    """Returns a constructed article object without downloading
    or parsing
    """
    config = config or Configuration()
    config = extend_config(config, kwargs)
    url = url or ''
    a = Article(url, config=config)
    return a


def languages():
    """Returns a list of the supported languages
    """
    print_available_languages()


def popular_urls():
    """Returns a list of pre-extracted popular source urls
    """
    with open(POPULAR_URLS) as f:
        urls = ['http://' + u.strip() for u in f.readlines()]
        return urls


def hot():
    """Returns a list of hit terms via google trends
    """
    try:
        listing = feedparser.parse(TRENDING_URL)['entries']
        trends = [item['title'] for item in listing]
        return trends
    except Exception as e:
        print('ERR hot terms failed!', str(e))
        return None


def fulltext(html, language='en'):
    """Takes article HTML string input and outputs the fulltext
    Input string is decoded via UnicodeDammit if needed
    """
    from .cleaners import DocumentCleaner
    from .configuration import Configuration
    from .extractors import ContentExtractor
    from .outputformatters import OutputFormatter

    config = Configuration()
    config.language = language

    extractor = ContentExtractor(config)
    document_cleaner = DocumentCleaner(config)
    output_formatter = OutputFormatter(config)

    doc = config.get_parser().fromstring(html)
    doc = document_cleaner.clean(doc)

    top_node = extractor.calculate_best_node(doc)
    top_node = extractor.post_cleanup(top_node)
    text, article_html = output_formatter.get_formatted(top_node)
    return text

class Request(BaseModel):
    link: str
    content: str
    language: Optional[str] = None

def extract(request: Request, language = None):
    try:
        if language == None:
            if request.language is not None:
                language = request.language
            else:
                language = 'hu'
        article = Article(request.link, language=language)
        article.download(input_html=request.content)
        article.parse()
        if article.publish_date:
                publish_date_str = article.publish_date.strftime("%Y%m%d-%H:%M:%S")
        else:
                publish_date_str = 'None'
        result = {
                'title': article.title,
                'text': article.text,
                'publish_date': publish_date_str,
                'status': 0
                }
    except ArticleException:
        result = {
                'status': 1,
                'error': str(sys.exc_info()[1].with_traceback(
                        sys.exc_info()[2])) + ' Maybe content is empty?',
                'type': str('ArticleException')
                }
    except TypeError:
        result = {
                'status': 1,
                'error': 'The type of an argument is not correct. ' +
                    str(sys.exc_info()[1].with_traceback(sys.exc_info()[2])),
                'type': 'TypeError'
                }
    except KeyError:
        result = {
                'status': 1,
                'error': 'A key is missing from the request. ' +
                    str(sys.exc_info()[1].with_traceback(sys.exc_info()[2])),
                'type': str('KeyError')
                }
    except AttributeError:
        result = {
                'status': 1,
                'error': str(sys.exc_info()[1].with_traceback(sys.exc_info()[2])),
                'type': str('AttributeError')
                }
    except:
        result = {
                'status': 1,
                'error': str(sys.exc_info()[1].with_traceback(sys.exc_info()[2])),
                'type': str(sys.exc_info()[0])
                }
    return JSONResponse(content=jsonable_encoder(result))