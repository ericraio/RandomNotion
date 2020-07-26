import os
import random
import jedi
import webbrowser
from notion.client import NotionClient

def main(num_rand_rows):
    '''
    inputs: a dictionary mapping a collection page to its URL
    outputs: a random row from each collection, plus its URL
    '''
    client = NotionClient('<replace me>')

    # replace these urls with any of the collection pages you seek to get a random note from
    # this only works on collection pages (e.g. table, board, calendar, list, gallery)
    urls = [
        # 'https://www.notion.so/../Projects-',  # Projects
        # 'https://www.notion.so/../Areas-',     # Areas
        # 'https://www.notion.so/../Resources-', # Resources
    ]

    rand = random.randint(0, len(urls) - 1)
    url = urls[rand]
    note = get_note(None, client, url)
    webbrowser.open(f"notion://www.notion.so/{note.id}".replace("-", ""))

def get_note(note, client, url):
    if not note:
        note = get_note(client.get_block(url), client, url)
    else:
        if hasattr(note.__class__, 'collection'):
            note = get_note_for_collection(note)
        elif hasattr(note.__class__, 'children'):
            note = get_note_for_children(note.children)

    if hasattr(note.__class__, 'collection'):
        note = get_note_for_collection(note)

    if not note or not note.title or any(ele in note.title for ele in skip_title_list):
        note = get_note(client.get_block(url), client, url)

    return note

def get_note_for_children(children):
    if len(children) == 0:
        return children
    else:
        note = get_random_note(children)

        if len(note.children) > 0:
            if not contains_element(note, "CollectionViewPageBlock") and (contains_element(note, "TextBlock") or contains_element(note, "VideoBlock")):
                if contains_element(note, "PageBlock"):
                    roll = random.randint(1,100)
                    if roll <= 50:
                        return note
                    else:
                        return get_note_for_children(note.children)
                else:
                    return note
            elif contains_element(note, "CollectionViewPageBlock") and not contains_element(note, "PageBlock"):
                return get_random_note(note.children)
            else:
                if contains_element(note, "PageBlock"):
                    if contains_element(note, "CollectionViewPageBlock"):
                        note = get_random_note(note.children)
                        if contains_element(note, "PageBlock"):
                            return get_note_for_children(note.children)
                        else:
                            return note
                    else:
                        if contains_element(note, "TextBlock") or contains_element(note, "VideoBlock"):
                            return note
                        else:
                            return None
        else:
            return None


def contains_element(note, el):
    arr = []
    for child in note.children:
        arr.append(get_class(child))
    if note.title == "Power":
        print(arr)
        print(note)
    return any(ele in el for ele in arr)

def get_random_note(children):
    rand = random.randint(0, len(children) - 1)
    note = children[rand]
    if len(note.children) == 0: # Working with a collection
        rand = random.randint(0, len(children) - 1)
        return children[rand]

    return note

def get_class(node):
    return type(node).__name__

def get_note_for_collection(page):
    rows = page.collection.get_rows()
    if not rows:
        page.collection.refresh()
        rows = page.collection.get_rows()

    if not rows:
        return

    n = len(rows)
    for _ in range(num_rand_rows):
        rand_idx = random.randint(0, n-1)
        return rows[rand_idx]

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    # either take in user arg for number of rows
    # default to five since the API call is kinda slow XD
    num_rand_rows = 5

    skip_title_list = [
            # Add titles or partial match to title's to skip in random generator
    ]

    main(num_rand_rows)
