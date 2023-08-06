#cython: language_level=3

from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.dms.taxo.taxo cimport Taxonomy
from obitools3.apps.optiongroups import addMinimalInputOption
from obitools3.utils cimport tostr, bytes2str_object

 
__title__="Print a preview of a DMS, view, column...."


def addOptions(parser):    
    addMinimalInputOption(parser)
    group = parser.add_argument_group('obi ls specific options')

    group.add_argument('-l',
                     action="store_true", dest="ls:longformat",
                     default=False,
                     help="Detailed list in long format with all metadata.")


def run(config):

    DMS.obi_atexit()
    
    logger("info", "obi ls")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input")
    
    # Print representation
    if config['ls']['longformat']:
        print(input[1].repr_longformat())
    else:
        print(repr(input[1]))
    
    input[0].close(force=True)
