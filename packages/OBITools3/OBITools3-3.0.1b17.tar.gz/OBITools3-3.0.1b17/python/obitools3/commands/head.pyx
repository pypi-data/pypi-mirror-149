#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms import DMS
from obitools3.dms.view.view cimport View, Line_selection
from obitools3.uri.decode import open_uri
from obitools3.apps.optiongroups import addMinimalInputOption, addMinimalOutputOption, addNoProgressBarOption
from obitools3.dms.view import RollbackException
from obitools3.apps.config import logger
from obitools3.utils cimport str2bytes

import time
import sys
from io import BufferedWriter

from cpython.exc cimport PyErr_CheckSignals


__title__="Keep the N first lines of a view"

 
def addOptions(parser):
    
    addMinimalInputOption(parser)
    addMinimalOutputOption(parser)
    addNoProgressBarOption(parser)

    group=parser.add_argument_group('obi head specific options')

    group.add_argument('-n', '--sequence-count',
                       action="store", dest="head:count",
                       metavar='<N>',
                       default=10,
                       type=int,
                       help="Number of first records to keep.")

     
def run(config):
     
    DMS.obi_atexit()
    
    logger("info", "obi head")

    # Open the input
    input = open_uri(config["obi"]["inputURI"])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]

    # Open the output: only the DMS
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      dms_only=True)
    if output is None:
        raise Exception("Could not create output view")
    o_dms = output[0]
    output_0 = output[0]
    final_o_view_name = output[1]
    
    # If stdout output or the input and output DMS are not the same, create a temporary view that will be exported and deleted.
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        temporary_view_name = b"temp"
        i=0
        while temporary_view_name in i_dms:  # Making sure view name is unique in input DMS
            temporary_view_name = temporary_view_name+b"_"+str2bytes(str(i))
            i+=1
        o_view_name = temporary_view_name
        if type(output_0)==BufferedWriter:
            o_dms = i_dms
    else:
        o_view_name = final_o_view_name
    
    n = min(config['head']['count'], len(i_view))

    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(n, config)
    else:
        pb = None
        
    selection = Line_selection(i_view)
    
    for i in range(n):
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
        selection.append(i)

    if pb is not None:
        pb(i, force=True)
        print("", file=sys.stderr)

    # Create output view with the line selection
    try:
        o_view = selection.materialize(o_view_name)
    except Exception, e:
        raise RollbackException("obi head error, rollbacking view: "+str(e), o_view)
    
    # Save command config in DMS comments
    command_line = " ".join(sys.argv[1:])
    o_view.write_config(config, "head", command_line, input_dms_name=[i_dms.name], input_view_name=[i_view.name])
    o_dms.record_command_line(command_line)

    # If input and output DMS are not the same, export the temporary view to the output DMS
    # and delete the temporary view in the input DMS
    if i_dms != o_dms:
        o_view.close()
        View.import_view(i_dms.full_path[:-7], o_dms.full_path[:-7], o_view_name, final_o_view_name)
        o_view = o_dms[final_o_view_name]

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(view), file=sys.stderr)

    # If the input and the output DMS are different or if stdout output, delete the temporary imported view used to create the final view
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        View.delete_view(i_dms, o_view_name)
        o_dms.close(force=True)
    i_dms.close(force=True)
    
    logger("info", "Done.")
