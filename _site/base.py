from django.utils import translation
import json

std_title_clause = " - Davide Wiest"
lang_independant_files = ("credentials", "data")
allowed_languages = ("en", "de")


def openfile(filename, subfield=None):
    with open(f"_site/static/_content/{filename}", "r", encoding="utf-8") as f:
        file = json.load(f)
        if subfield:
            file = file.get(subfield, file)

    return file

def build_params(title, storage_ptrs, params, language):
    
    c_files = {}
    for storage_ptr in storage_ptrs + ["base"]:
        if storage_ptr != "":
            if "/" in storage_ptr:
                filename, subfield = storage_ptr.split("/")
            else:
                filename, subfield = (storage_ptr, "")
            
            c_files[filename + "_" + subfield.capitalize() if subfield != "" else filename] = openfile(language + "_" + filename + ".json" if filename not in lang_independant_files else filename + ".json", subfield=subfield if subfield != "" else None)
        else:
            c_files[filename] = {}

    bparams = {
        "title": title + std_title_clause,
        "base_url": "https://davidewiest.com",
        "c": c_files,
        "l": language
    }

    return {**bparams, **params}

def choose_lang(request):
    language = translation.get_language_from_request(request)

    # first priority
    if request.method == "GET":
        if request.GET.get("language") in allowed_languages:
            # change request.session["language"]
            # change db user settings.language
            return request.GET.get("language")
    
    # second priority
    if "user_id" in request.session:
        # change request.session["language"] with db
        pass
    
    # third priority
    if request.session.get("language") in allowed_languages:
        return request.session["language"]
    
    # allow only de or en
    if language in ("ch", "au"):
        language = "de"
    if language != "de":
        language = "en"

    # language = "en"

    return language

def handle_requestdata(request, l):
    if request.GET.get("language") in allowed_languages:
        request.session["language"] = l
        return request.GET.get("language")
        
    if request.session.get("language") not in allowed_languages:
        request.session["language"] = l

    