from aqt import mw
import re
import os
import SimplyTranslate
import aqt.qt

languages_const = None  # it's not exactly a "constant" but whatever


def set_default_source_language(lang):
    setConf("default_source_language", lang)

def set_default_target_language(lang):
    setConf("default_target_language", lang)

def get_default_target_language():
    return getConf("default_target_language")

def get_default_source_language():  ## FIXED: clean up horribly inconsistent object naming
    return getConf("default_source_language")

def set_default_reverso_source_language(lang):
    setConf("default_reverso_source_language", lang)

def set_default_reverso_target_language(lang):
    setConf("default_reverso_target_language", lang)

def get_default_reverso_target_language():
    return getConf("default_reverso_target_language")

def get_default_reverso_source_language():
    return getConf("default_reverso_source_language")

def return_reverso_languages():
    arr_default = [
        "English",
        "Arabic",
        "Chinese",
        "Dutch",
        "English",
        "French",
        "German",
        "Hebrew",
        "Italian",
        "Japanese",
        "Korean",
        "Polish",
        "Portuguese",
        "Romanian",
        "Russian",
        "Spanish",
        "Swedish",
        "Turkish",
        "Ukrainian"
    ]
    return arr_default

def reverso_return_source_langs():
    return_arr = []
    arr_default = return_reverso_languages()
    default = get_default_reverso_source_language()
    if not default is None:
        return_arr.append(default)
        return_arr.extend(arr_default)
    else:
        return arr_default
    return return_arr


def reverso_return_target_langs():
    return_arr = []
    arr_default = return_reverso_languages()
    default = get_default_reverso_target_language()
    if default is not None:
        return_arr.append(default)
        return_arr.extend(arr_default)
    else:
        return arr_default
    return return_arr

def get_index_from_combo(name: str, combo_obj: aqt.qt.QComboBox):
    for i in range(combo_obj.count()):
        if combo_obj.itemText(i) == name:
            return i
    return None

def languageToCode(lang):
    global languages_const
    init_languages_const()
    return languages_const[lang]
def getSourceLanguageList() -> list:
    init_languages_const()
    source_languages = []
    default_source_language = get_default_source_language()
    # FIXED: add the most recently selected language as the first in the values!
    if default_source_language is not None:
        source_languages.append(default_source_language)
    # source_languages.append("Detect Language") # no longer supporting this, caused too many problems!
    for language in languages_const:
        source_languages.append(language)
    return source_languages

def init_languages_const():
    global languages_const
    if languages_const is None:
        languages_const = SimplyTranslate.simply_get_source_language_list()
def getTargetLanguageList() -> list:
    global languages_const
    init_languages_const()
    target_languages = []
    default_target_language =get_default_target_language()
    if default_target_language is not None:
        target_languages.append(default_target_language)
    ## TODO: bring most recent to the top
    for language in languages_const:
        if language != "Detect language":
            target_languages.append(language)
    return target_languages

def sanitizeFilename(filename) -> str:
    sanitized = ""
    sanitized = re.sub("[^A-Za-z0-9_]", '', filename)
    return sanitized

def getConfFilepath(confOptName):
    indivFilename = sanitizeFilename(confOptName) + ".txt"
    filename = os.path.dirname(__file__) + "/user_files/conf-dir/" + indivFilename
    return filename.replace("\n", "").replace("\r", "")

def setConf(confOptName, confOptValue) -> None:
    myFilename = getConfFilepath(confOptName)
    if (os.path.isfile(myFilename)):
        mode="w"
    else:
        mode="w+"
    writeFile = open(myFilename, mode)
    writeFile.write(confOptValue)
    writeFile.close()


def getConf(confOptName):
    the_file_path = getConfFilepath(confOptName) # Naming variables ):
    confvalue = ""
    if not os.path.isfile(the_file_path):
        return None
    else:
        file = open(the_file_path, "r")
        for line in file.readlines():
            confvalue += line
        return confvalue


