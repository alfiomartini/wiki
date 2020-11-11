import re
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# see: https://www.tutorialspoint.com/How-to-run-Python-functions-from-command-line


def remove_file(filename):
    filename = f"entries/{filename}.md"
    if os.path.exists(filename):
        os.remove(filename)
        print(f'filename {filename} was removed.')
    else:
        print(f"File {filename} does not exist.")


def collapse_newlines(text):
    newlines = re.compile(r'\n\n+')
    text = newlines.sub('\n\n', text)
    return text


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    filenames = os.listdir("entries")
    # for each markdown file name, it replaces the .md extension
    # for the empty space, then sort the resulting list
    entries_list = [re.sub(r"\.md$", "", filename)
                    for filename in filenames if filename.endswith(".md")]
    entries_list.sort()
    return entries_list


def normalize(text):
    # remove white spaces => lower -> capitalize first char
    return text.replace(" ", "").lower().title()


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    # rewrites entry, if it exists
    file = open(filename, 'wt')
    file.write(content)
    file.close()

# this is a hack, because of problems with filenames in
# Heroku.


def get_filename(entry, entries):
    for filename in entries:
        if entry.lower() == filename.lower():
            return filename
    return entry


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    entries = list_entries()
    new_title = get_filename(title, entries)
    filename = f"entries/{new_title}.md"
    try:
        f = open(filename, 'rt', encoding='utf-8')
        content = f.read()
        f.close()
        return content
    except FileNotFoundError:
        return None
