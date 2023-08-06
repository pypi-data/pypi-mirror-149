#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms import DMS
from obitools3.dms.view.view cimport View, Line_selection
from obitools3.uri.decode import open_uri
from obitools3.apps.optiongroups import addMinimalInputOption, addTaxonomyOption, addMinimalOutputOption, addNoProgressBarOption
from obitools3.dms.view import RollbackException
from obitools3.apps.config import logger
from obitools3.utils cimport tobytes

import sys
from cpython.exc cimport PyErr_CheckSignals

 
__title__="Split"

 
def addOptions(parser):
    
    addMinimalInputOption(parser)
    addNoProgressBarOption(parser)

    group=parser.add_argument_group("obi split specific options")
 
    group.add_argument('-p','--prefix',
                       action="store", dest="split:prefix",
                       metavar="<PREFIX>",
                       help="Prefix added to each subview name (included undefined)")

    group.add_argument('-t','--tag-name',
                       action="store", dest="split:tagname",
                       metavar="<TAG_NAME>",
                       help="Attribute/tag used to split the input")
      
    group.add_argument('-u','--undefined',
                       action="store", dest="split:undefined",
                       default=b'UNDEFINED',
                       metavar="<VIEW_NAME>",
                       help="Name of the view where undefined sequenced are stored (will be PREFIX_VIEW_NAME)")


def run(config):
     
    DMS.obi_atexit()
    
    logger("info", "obi split")

    # Open the input
    input = open_uri(config["obi"]["inputURI"])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]

    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(len(i_view), config)
    else:
        pb = None
    
    tag_to_split = config["split"]["tagname"]
    undefined = tobytes(config["split"]["undefined"])
    selections = {}
    
    # Go through input view and split
    for i in range(len(i_view)):
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
        line = i_view[i]
        if tag_to_split not in line or line[tag_to_split] is None or len(line[tag_to_split])==0:
            value = undefined
        else:
            value = line[tag_to_split]
        if value not in selections:
            selections[value] = Line_selection(i_view)
        selections[value].append(i)
        
    if pb is not None:
        pb(len(i_view), force=True)
        print("", file=sys.stderr)

    # Create output views with the line selection
    try:
        for cat in selections:
            o_view_name = config["split"]["prefix"].encode()+cat
            o_view = selections[cat].materialize(o_view_name)
            # Save command config in View and DMS comments
            command_line = " ".join(sys.argv[1:])
            input_dms_name=[input[0].name]
            input_view_name=[input[1].name]
            if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
                input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
                input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
            o_view.write_config(config, "split", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
            o_view.close()
    except Exception, e:
        raise RollbackException("obi split error, rollbacking view: "+str(e), o_view)

    i_dms.record_command_line(command_line)
    i_dms.close(force=True)

    logger("info", "Done.")

