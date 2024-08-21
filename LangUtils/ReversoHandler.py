import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from threading import Thread
from aqt.utils import showInfo
import time

from LangUtils import utilsNData


## TODO: thread the fetch operations so we can have proper error handling


class ReversoExamplesData:
    def __init__(self, meaning, dict):
        self.meaning = meaning
        self.dict = dict


def reverso_get_dict_languages() -> list:
    return ["Arabic", "Chinese", "Dutch", "English", "French", "Hebrew", "Italian",
            "Japanese", "Korean", "Portuguese", "Romanian", "Russian", "Spanish",
            "Swedish", "Turkish", "Ukrainian"]


def reverse_lang_specifier(lang_specifier: str) -> str:
    split_specifier: str = lang_specifier.split("-")
    return split_specifier[1] + "-" + split_specifier[0]  # I feel like there's a better way to do this


reverso_response = None
# Global variables, I know, I know. This is probably the best way to do it

def reverso_get_examples(source_language: str, target_language: str, word: str):
    global reverso_response
    reverso_response = None
    thread = Thread(target=reverso_get_examples_tr, args=(source_language, target_language, word))
    elapsed = 0.0
    thread.start()
    while reverso_response is None:
        time.sleep(0.2)
        elapsed += 0.2
        if elapsed > 17:
            return None
    return reverso_response

def reverso_get_examples_tr(source_language: str, target_language: str, word: str):
    global reverso_response
    return_dict = {}
    use_word = urllib.parse.quote(word)
    source_language: str = source_language.lower()
    target_language = target_language.lower()
    lang_specifier = source_language + "-" + target_language
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    meaning = "multiple meanings, see example phrases" # if meaning cannot be found (when reverso context must be used, this will remain unchanged)
    response = requests.get('https://dictionary.reverso.net/' + lang_specifier + '/' + use_word, headers=headers)
    # print(response.content)
    parser = BeautifulSoup(response.content, "html.parser")
    items = parser.find_all(True, {'class': ["src", "tgt"]})
    meaning_temp = parser.find(True, {'id': "ID0EAC"})
    if meaning_temp is not None and len(meaning_temp.get_text()) > 1:
        meaning = meaning_temp.get_text()
    for i in range(len(items)-1):
        # This isn't the greatest set-up...
        # print(items[i].text)
        if i % 2 == 0:  # only do this on even items
            if (len(items[i].get_text())) > 4:
                return_dict[items[i].get_text()] = str(items[i+1].get_text())
        #return_list.append(ReversoExampleItem(items[i].text, items[i+1].text))
    # sometimes the big box with the examples isn't shown
    # TODO: consider removing the above and simply using reverso context for finding the example phrases
    if (len(return_dict) <= 1):
        # get from "reverso context"
        response = requests.get('https://context.reverso.net/translation/' + lang_specifier + '/' + use_word, headers=headers)
        parser = BeautifulSoup(response.content, "html.parser")
        matches = parser.find_all(True, {'class': ["src ltr", "trg ltr"]})
        # showInfo(matches[0].get_text())
        for i in range(len(matches)-1):
            if i % 2 == 0:
                return_dict[matches[i].get_text()] = matches[i+1].get_text()
    #print(items)
    #print(return_list[0].result_text)
    reverso_response = ReversoExamplesData(meaning, return_dict)
