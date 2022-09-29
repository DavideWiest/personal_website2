import json
from django.utils import translation

class LangSetter(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        language = translation.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        translation.deactivate()
        return response


def openfile(filename, subfield=None):
    with open(f"_site/static/_content/{filename}", "r", encoding="utf-8") as f:
        file = json.load(f)
        if subfield:
            file = file.get(subfield, file)

    return file


std_title_clause = " - Davide Wiest"

def build_params(title, storage_ptrs, params):
    c_files = {}
    for storage_ptr in storage_ptrs:
        if storage_ptr != "":
            if "/" in storage_ptr:
                filename, subfield = storage_ptr.split("/")
            else:
                filename, subfield = (storage_ptr, "")
            
            c_files[filename + "_" + subfield.capitalize() if subfield != "" else filename] = openfile(filename + ".json", subfield=subfield if subfield != "" else None)
        else:
            c_files[filename] = {}

    bparams = {
        "title": title + std_title_clause,
        "base_url": "http://127.0.0.1:8000/", # "https://davidewiest.com"
        "c": c_files
    }

    return {**bparams, **params}
