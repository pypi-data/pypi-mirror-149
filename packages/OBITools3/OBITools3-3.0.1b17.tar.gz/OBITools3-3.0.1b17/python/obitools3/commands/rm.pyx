#cython: language_level=3

from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.apps.optiongroups import addMinimalInputOption
from obitools3.dms.view.view cimport View
import os
 
__title__="Delete a view"


def addOptions(parser):    
    addMinimalInputOption(parser)

def run(config):

    DMS.obi_atexit()
    
    logger("info", "obi rm")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input")
    
    # Check that it's a view
    if isinstance(input[1], View) :
        view = input[1]
    else: 
        raise NotImplementedError()
    
    # Get the path to the view file to remove
    path = input[0].full_path  # dms path
    path+=b"/VIEWS/"
    path+=view.name
    path+=b".obiview"
    
    # Close the view and the DMS
    view.close()
    input[0].close(force=True)
    
    # Rm
    os.remove(path)
