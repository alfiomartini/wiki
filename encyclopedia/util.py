import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    It returns a 2-tuple: the first item being directories
    (in this case, none), and the second item being files
    """
    _, filenames = default_storage.listdir("entries")
    #  for each markdown file name, it replaces the .md extension
    # for the empty space, then sort the result iterable object and
    # transforms it into a list
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    # rewrites entry, if it exists
    if default_storage.exists(filename):
        default_storage.delete(filename)
    # The content argument must be an instance of django.core.files.File or a 
    # file-like object that can be wrapped in a file
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
