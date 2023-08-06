#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms.dms cimport DMS
from obitools3.dms.view import RollbackException
from obitools3.dms.capi.build_reference_db cimport build_reference_db
from obitools3.apps.optiongroups import addMinimalInputOption, addTaxonomyOption, addMinimalOutputOption, addNoProgressBarOption
from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.utils cimport tobytes, str2bytes
from obitools3.dms.view.view cimport View
from obitools3.dms.view.typed_view.view_NUC_SEQS cimport View_NUC_SEQS

from io import BufferedWriter
import sys
from cpython.exc cimport PyErr_CheckSignals


__title__="Build a reference database for ecotag"


def addOptions(parser):

    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)
    addNoProgressBarOption(parser)
 
    group = parser.add_argument_group('obi build_ref_db specific options')

    group.add_argument('--threshold','-t',
                      action="store", dest="build_ref_db:threshold",
                      metavar='<THRESHOLD>',
                      default=0.99,
                      type=float,
                      help="Score threshold as a normalized identity, e.g. 0.95 for an identity of 95%%. Default: 0.99.")


def run(config):
        
    DMS.obi_atexit()
    
    logger("info", "obi build_ref_db")

    # Open the input: only the DMS
    input = open_uri(config['obi']['inputURI'],
                     dms_only=True)
    if input is None:
        raise Exception("Could not read input")
    i_dms = input[0]
    i_dms_name = input[0].name
    i_view_name = input[1]

    # Open the output: only the DMS
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      dms_only=True)
    if output is None:
        raise Exception("Could not create output")
    o_dms = output[0]
    output_0 = output[0]
    final_o_view_name = output[1]
    
    # If stdout output or the input and output DMS are not the same, build the database creating a temporary view that will be exported to 
    # the right DMS and deleted in the other afterwards.
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

    # Read taxonomy name
    taxonomy_name = config['obi']['taxoURI'].split("/")[-1]   # Robust in theory

    # Save command config in View comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[i_dms_name]
    input_view_name= [i_view_name]
    input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
    input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    comments = View.print_config(config, "build_ref_db", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    
    if build_reference_db(i_dms.name_with_full_path, tobytes(i_view_name), tobytes(taxonomy_name), tobytes(o_view_name), comments, config['build_ref_db']['threshold']) < 0:
        raise Exception("Error building a reference database")
    
    # If the input and output DMS are not the same, export result view to output DMS
    if i_dms != o_dms:
        View.import_view(i_dms.full_path[:-7], o_dms.full_path[:-7], o_view_name, final_o_view_name)

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view = o_dms[o_view_name]
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    # Save command config in DMS comments
    o_dms.record_command_line(command_line)

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(o_dms[final_o_view_name]), file=sys.stderr)

    # If the input and the output DMS are different or if stdout output, delete the temporary imported view used to create the final view
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        View.delete_view(i_dms, o_view_name)
        o_dms.close(force=True)
    
    i_dms.close(force=True)

    logger("info", "Done.")
    
