import os
import sys

from . import config
from . import docsearch


def is_verbose():
    return os.environ['PAPERWORK_VERBOSE'] != ""

def is_interactive():
    return os.environ['PAPERWORK_INTERACTIVE'] != ""


def search(*args):
    """
    Arguments: <keyword1> [<keyword2> [<keyword3> [...]]]
    List the documents containing the keywords. Syntax is the same
    than with the search field in Paperwork-gui.
    Example: 'label:contrat AND paperwork'
    """
    if len(args) <= 0:
        sys.stderr.write("paperwork-shell: Need keywords.\n")
        return

    pconfig = config.PaperworkConfig()
    pconfig.read()

    if is_verbose():
        print ("Searching in {}".format(pconfig.settings['workdir'].value))

    dsearch = docsearch.DocSearch(pconfig.settings['workdir'].value)
    dsearch.reload_index()

    if is_verbose():
        print ("Search: {}".format(" ".join(args)))

    docs = dsearch.find_documents(" ".join(args))
    for doc in docs:
        if not is_verbose():
            print (doc.docid)
        else:
            sys.stdout.write(doc.docid)
            lines = doc.pages[0].boxes
            for line in lines:
                if len(line.content.strip()) == 0:
                    continue
                for word in line.word_boxes:
                    sys.stdout.write(" " + word.content)
                break
            sys.stdout.write("\n")


COMMANDS = {
    'search': search,
}