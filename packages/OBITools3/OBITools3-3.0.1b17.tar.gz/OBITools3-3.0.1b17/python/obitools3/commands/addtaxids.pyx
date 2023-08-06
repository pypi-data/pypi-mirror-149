#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms import DMS
from obitools3.dms.view.view cimport View, Line_selection
from obitools3.uri.decode import open_uri
from obitools3.apps.optiongroups import addMinimalInputOption, addTaxonomyOption, addMinimalOutputOption, addNoProgressBarOption
from obitools3.dms.view import RollbackException
from obitools3.dms.column.column cimport Column
from functools import reduce
from obitools3.apps.config import logger
from obitools3.utils cimport tobytes, str2bytes, tostr
from io import BufferedWriter
from obitools3.dms.capi.obiview cimport NUC_SEQUENCE_COLUMN, \
                                        ID_COLUMN, \
                                        DEFINITION_COLUMN, \
                                        QUALITY_COLUMN, \
                                        COUNT_COLUMN, \
                                        TAXID_COLUMN
from obitools3.dms.capi.obitypes cimport OBI_INT
from obitools3.dms.capi.obitaxonomy cimport MIN_LOCAL_TAXID
import time
import math 
import sys

from cpython.exc cimport PyErr_CheckSignals

 
__title__="Annotate sequences with their corresponding NCBI taxid found from the taxon scientific name"


 
def addOptions(parser):
    
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)
    addNoProgressBarOption(parser)

    group=parser.add_argument_group('obi addtaxids specific options')

    group.add_argument('-t', '--taxid-tag', 
                       action="store", 
                       dest="addtaxids:taxid_tag",
                       metavar="<TAXID_TAG>",
                       default=b"TAXID",
                       help="Name of the tag to store the found taxid "
                            "(default: 'TAXID').")

    group.add_argument('-n', '--taxon-name-tag', 
                       action="store", 
                       dest="addtaxids:taxon_name_tag",
                       metavar="<SCIENTIFIC_NAME_TAG>",
                       default=b"SCIENTIFIC_NAME",
                       help="Name of the tag giving the scientific name of the taxon "
                            "(default: 'SCIENTIFIC_NAME').")

    group.add_argument('-g', '--try-genus-match',
                     action="store_true", dest="addtaxids:try_genus_match",
                     default=False,
                     help="Try matching the first word of <SCIENTIFIC_NAME_TAG> when can't find corresponding taxid for a taxon. "
                          "If there is a match it is added in the 'parent_taxid' tag. (Can be used by 'obi taxonomy' to add the taxon under that taxid).")

    group.add_argument('-a', '--restricting-ancestor', 
                       action="store", 
                       dest="addtaxids:restricting_ancestor",
                       metavar="<RESTRICTING_ANCESTOR>",
                       default=None,
                       help="Enables to restrict the search of taxids under an ancestor specified by its taxid.")

    group.add_argument('-l', '--log-file', 
                       action="store", 
                       dest="addtaxids:log_file",
                       metavar="<LOG_FILE>",
                       default='',
                       help="Path to a log file to write informations about not found taxids.")


def run(config):
     
    DMS.obi_atexit()
    
    logger("info", "obi addtaxids")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input view")
    i_dms = input[0]
    i_view = input[1]
    i_view_name = input[1].name

    # Open the output: only the DMS, as the output view is going to be created by cloning the input view
    # (could eventually be done via an open_uri() argument)
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      dms_only=True)
    if output is None:
        raise Exception("Could not create output view")
    o_dms = output[0]
    output_0 = output[0]
    o_view_name = output[1]

    # stdout output: create temporary view
    if type(output_0)==BufferedWriter:
        o_dms = i_dms
        i=0
        o_view_name = b"temp"
        while o_view_name in i_dms: # Making sure view name is unique in output DMS
            o_view_name = o_view_name+b"_"+str2bytes(str(i))
            i+=1
        imported_view_name = o_view_name

    # If the input and output DMS are not the same, import the input view in the output DMS before cloning it to modify it
    # (could be the other way around: clone and modify in the input DMS then import the new view in the output DMS)
    if i_dms != o_dms:
        imported_view_name = i_view_name
        i=0
        while imported_view_name in o_dms:  # Making sure view name is unique in output DMS
            imported_view_name = i_view_name+b"_"+str2bytes(str(i))
            i+=1
        View.import_view(i_dms.full_path[:-7], o_dms.full_path[:-7], i_view_name, imported_view_name)
        i_view = o_dms[imported_view_name]

    # Clone output view from input view
    o_view = i_view.clone(o_view_name)
    if o_view is None:
        raise Exception("Couldn't create output view")
    i_view.close()

    # Open taxonomy
    taxo_uri = open_uri(config['obi']['taxoURI'])
    if taxo_uri is None or taxo_uri[2] == bytes:
        raise Exception("Couldn't open taxonomy")
    taxo = taxo_uri[1]

    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(len(o_view), config)
    else:
        pb = None
        
    try:
        if config['addtaxids']['log_file']:
            logfile = open(config['addtaxids']['log_file'], 'w')
        else:
            logfile = None
        if config['addtaxids']['try_genus_match']:
            try_genus = True
        else:
            try_genus = False
        if 'restricting_ancestor' in config['addtaxids']:
            res_anc = int(config['addtaxids']['restricting_ancestor'])
        else:
            res_anc = None
        taxid_column_name = config['addtaxids']['taxid_tag']
        parent_taxid_column_name = "PARENT_TAXID" # TODO macro
        taxon_name_column_name = config['addtaxids']['taxon_name_tag']
        taxid_column = Column.new_column(o_view, taxid_column_name, OBI_INT)
        parent_taxid_column = Column.new_column(o_view, parent_taxid_column_name, OBI_INT)
        taxon_name_column = o_view[taxon_name_column_name]
        
        found_count = 0
        not_found_count = 0
        parent_found_count = 0
        
        for i in range(len(o_view)):
            PyErr_CheckSignals()
            if pb is not None:
                pb(i)
            taxon_name = taxon_name_column[i]
            taxon = taxo.get_taxon_by_name(taxon_name, res_anc)
            if taxon is not None:
                taxid_column[i] = taxon.taxid
                found_count+=1
            elif try_genus: # try finding genus or other parent taxon from the first word
                #print(i, o_view[i].id)
                taxon_name_sp = taxon_name.split(b" ")
                taxon = taxo.get_taxon_by_name(taxon_name_sp[0], res_anc)
                if taxon is not None:
                    parent_taxid_column[i] = taxon.taxid
                    parent_found_count+=1
                    if logfile:
                        print("Found parent taxon for", tostr(taxon_name), file=logfile)
                else:
                    not_found_count+=1
                    if logfile:
                        print("No taxid found for", tostr(taxon_name), file=logfile)
            else:
                not_found_count+=1
                if logfile:
                    print("No taxid found for", tostr(taxon_name), file=logfile)

    except Exception, e:
        raise RollbackException("obi addtaxids error, rollbacking view: "+str(e), o_view)

    if pb is not None:
        pb(i, force=True)
        print("", file=sys.stderr)
    
    logger("info", "\nTaxids found: "+str(found_count)+"/"+str(len(o_view))+" ("+str(round(found_count*100.0/len(o_view), 2))+"%)")
    if config['addtaxids']['try_genus_match']:
        logger("info", "\nParent taxids found: "+str(parent_found_count)+"/"+str(len(o_view))+" ("+str(round(parent_found_count*100.0/len(o_view), 2))+"%)")
    logger("info", "\nTaxids not found: "+str(not_found_count)+"/"+str(len(o_view))+" ("+str(round(not_found_count*100.0/len(o_view), 2))+"%)") 
    
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[i_view_name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "addtaxids", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    o_dms.record_command_line(command_line)

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(o_view), file=sys.stderr)

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    # If the input and the output DMS are different or if stdout output, delete the temporary imported view used to create the final view
    if i_dms != o_dms or type(output_0)==BufferedWriter:
        View.delete_view(o_dms, imported_view_name)
        o_dms.close(force=True)
    i_dms.close(force=True)

    logger("info", "Done.")
