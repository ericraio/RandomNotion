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
        for _ in range(num_rand_rows):
            if hasattr(note.__class__, 'collection'):
                note = get_note_for_collection(note)
            elif hasattr(note.__class__, 'children'):
                note = get_notes_for_children(note.children)

    if not note:
        note = get_note(client.get_block(url), client, url)

    return note

def get_notes_for_children(children):
    if len(children) == 0:
        return children
    else:
        rand = random.randint(0, len(children) - 1)
        return children[rand]


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
    main(num_rand_rows)
