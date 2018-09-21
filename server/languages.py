from __future__ import unicode_literals
import json
import os.path

TRANSLATIONS_ROOT_PATH = os.path.join(os.path.dirname(__file__), 'translations')


def load_translations_for_language(lang_code):
    """
    Takes one of the supported language codes and loads the corresponding
    translations dict from the file system.
    """
    lang_file_path = os.path.join(TRANSLATIONS_ROOT_PATH, '{}.json'.format(lang_code.lower()))
    with open(lang_file_path, 'r') as lang_file:
        return json.load(lang_file)
