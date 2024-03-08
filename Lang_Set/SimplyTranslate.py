import requests
import html
import re


simply_homepage_text = None

## TODO: thread the fetch operations so we can have proper error handling;

def simply_extract_result(response: requests.Response):  # I'm not going to use html parser, this is easier, but, I may live to regret it
    final_return_data = ""                               # TODO: now that bs4 is included in source anyway, rewrite code to include it
    body = response.text
    search_regex = re.compile("<textarea id=\"output\"[^>]*>[^<]*</textarea>*", re.MULTILINE)
    res = search_regex.findall(body)
    if len(res) == 0:
        return "TRANSLATION ERROR"
    res = res[0]
    res = re.sub("(</textarea>|<textarea[^>]*>)", "", res)
    return html.unescape(res)


def simply_get_target_language_list():
    global simply_homepage_text
    return {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bambara': 'bm', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chichewa': 'ny', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dhivehi': 'dv', 'Dogri': 'doi', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Filipino': 'tl', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Ilocano': 'ilo', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Konkani': 'gom', 'Korean': 'ko', 'Krio': 'kri', 'Kurdish (Kurmanji)': 'ku', 'Kurdish (Sorani)': 'ckb', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luganda': 'lg', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Maithili': 'mai', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Meiteilon (Manipuri)': 'mni-Mtei', 'Mizo': 'lus', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Odia (Oriya)': 'or', 'Oromo': 'om', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Quechua': 'qu', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Sanskrit': 'sa', 'Scots Gaelic': 'gd', 'Sepedi': 'nso', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Tsonga': 'ts', 'Turkish': 'tr', 'Turkmen': 'tk', 'Twi': 'ak', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}
    # this is the best way to go about it tbh, I don't want to load the page every goddamn time
    def get_friendly_lang_name_from_options(line):
        return re.sub("<.*?>", "", line)
    def get_lang_code_from_options(line):
        get_value_pattern = re.compile('value="[\\w\\-()]*"')
        lang_code_value = get_value_pattern.findall(line)
        if len(lang_code_value) > 0:
            lang_code_value = lang_code_value[0]
            lang_code_value = lang_code_value.replace('value="', "")
            lang_code_value = lang_code_value.replace('"', "")
            return lang_code_value
        else:
            return ""

    lang_dict = {}
    if simply_homepage_text is None:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'engine': 'google',
        }
        response = requests.get('https://simplytranslate.org/', params=params, headers=headers)
        simply_homepage_text = response.text
    find_select_pattern = re.compile("<select name=\"to\" aria-label=\"Target language\">.*?</select>", re.MULTILINE | re.DOTALL)
    select_data = re.findall(find_select_pattern, simply_homepage_text)
    select_data = select_data[0]
    find_options_regex = re.compile("<option value=\"[A-Za-z0-9 \\-()]+\" >[A-Za-z0-9)( ]+</option>|<option value=\"[A-Za-z0-9 \\-()]+\" selected>[A-Za-z0-9)( ]+</option>")
    options_found = re.findall(find_options_regex, select_data)
    for item in options_found:
        lang_dict[get_friendly_lang_name_from_options(item)] = get_lang_code_from_options(item)
    return lang_dict


def simply_get_source_language_list():
    global simply_homepage_text
    return {'Detect language': 'auto', 'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bambara': 'bm', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chichewa': 'ny', 'Chinese': 'zh-CN', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dhivehi': 'dv', 'Dogri': 'doi', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Filipino': 'tl', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Ilocano': 'ilo', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Konkani': 'gom', 'Korean': 'ko', 'Krio': 'kri', 'Kurdish (Kurmanji)': 'ku', 'Kurdish (Sorani)': 'ckb', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luganda': 'lg', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Maithili': 'mai', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Meiteilon (Manipuri)': 'mni-Mtei', 'Mizo': 'lus', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Odia (Oriya)': 'or', 'Oromo': 'om', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Quechua': 'qu', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Sanskrit': 'sa', 'Scots Gaelic': 'gd', 'Sepedi': 'nso', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Tsonga': 'ts', 'Turkish': 'tr', 'Turkmen': 'tk', 'Twi': 'ak', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}
    def get_friendly_lang_name_from_options(line):
        return re.sub("<.*?>", "", line)
    def get_lang_code_from_options(line):
        get_value_pattern = re.compile('value="[\\w\\-()]*"')
        lang_code_value = get_value_pattern.findall(line)
        if len(lang_code_value) > 0:
            lang_code_value = lang_code_value[0]
            lang_code_value = lang_code_value.replace('value="', "")
            lang_code_value = lang_code_value.replace('"', "")
            return lang_code_value
        else:
            return ""

    lang_dict = {}
    if simply_homepage_text is None:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        params = {
            'engine': 'google',
        }
        response = requests.get('https://simplytranslate.org/', params=params, headers=headers)
        simply_homepage_text = response.text
    find_select_pattern = re.compile("<select name=\"from\" aria-label=\"Source language\">.*?</select>", re.MULTILINE | re.DOTALL)
    select_data = re.findall(find_select_pattern, simply_homepage_text)
    select_data = select_data[0]
    find_options_regex = re.compile("<option value=\"[A-Za-z0-9 \\-()]+\" >[A-Za-z0-9)( ]+</option>|<option value=\"[A-Za-z0-9 \\-()]+\" selected>[A-Za-z0-9)( ]+</option>")
    options_found = re.findall(find_options_regex, select_data)
    for item in options_found:
        lang_dict[get_friendly_lang_name_from_options(item)] = get_lang_code_from_options(item)
    return lang_dict


def simply_translate_data(source_lang, target_lang, text):
    return simply_translate_data_nocache(source_lang, target_lang, text)


def simply_translate_data_nocache(source_lang, target_lang, text):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'null',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'engine': 'google',
    }

    data = {
        'from': source_lang,
        'to': target_lang,
        'text': text,
    }
    response = requests.post('https://simplytranslate.org/', params=params, headers=headers, data=data)
    return simply_extract_result(response)
