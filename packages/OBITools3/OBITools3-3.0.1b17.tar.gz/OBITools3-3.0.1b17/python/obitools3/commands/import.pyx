#cython: language_level=3

import sys
import os
import re

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms.view.view cimport View
from obitools3.dms.view import RollbackException
from obitools3.dms.view.typed_view.view_NUC_SEQS cimport View_NUC_SEQS
from obitools3.dms.column.column cimport Column
from obitools3.dms.obiseq cimport Nuc_Seq
from obitools3.dms import DMS
from obitools3.dms.taxo.taxo cimport Taxonomy
from obitools3.files.uncompress cimport CompressedFile


from obitools3.utils cimport tobytes, \
                             tostr, \
                             get_obitype, \
                             update_obitype

from obitools3.dms.capi.obiview cimport VIEW_TYPE_NUC_SEQS, \
                                        NUC_SEQUENCE_COLUMN, \
                                        ID_COLUMN, \
                                        DEFINITION_COLUMN, \
                                        QUALITY_COLUMN, \
                                        COUNT_COLUMN, \
                                        TAXID_COLUMN, \
                                        MERGED_PREFIX, \
                                        SCIENTIFIC_NAME_COLUMN
                                        
from obitools3.dms.capi.obidms cimport obi_import_view

from obitools3.dms.capi.obitypes cimport obitype_t, \
                                         OBI_VOID, \
                                         OBI_QUAL, \
                                         OBI_STR, \
                                         OBI_INT

from obitools3.dms.capi.obierrno cimport obi_errno

from obitools3.apps.optiongroups import addImportInputOption, \
                                        addTabularInputOption, \
                                        addTaxdumpInputOption, \
                                        addMinimalOutputOption, \
                                        addNoProgressBarOption, \
                                        addTaxonomyOption

from obitools3.uri.decode import open_uri

from obitools3.apps.config import logger

from cpython.exc cimport PyErr_CheckSignals

from io import BufferedWriter
import ast


__title__="Import sequences from different formats into a DMS"
 
 
default_config = {   'destview'     : None,
                     'skip'         : 0,
                     'only'         : None,
                     'skiperror'    : False,
                     'seqinformat'  : None,
                     'moltype'      : 'nuc',
                     'source'     : None
                 }

def addOptions(parser):
    
    addImportInputOption(parser)
    addTabularInputOption(parser)
    addTaxdumpInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)
    addNoProgressBarOption(parser)

    group = parser.add_argument_group('obi import specific options')

    group.add_argument('--preread',
                     action="store_true", dest="import:preread",
                     default=False,
                     help="Do a first readthrough of the dataset if it contains huge dictionaries (more than 100 keys) for "
                          "a much faster import. This option is not recommended and will slow down the import in any other case.")

    group.add_argument('--space-priority',
                     action="store_true", dest="import:space_priority",
                     default=False,
                     help="If importing a view into another DMS, do it by importing each line, saving disk space if the original view "
                          "has a line selection associated.")

#    group.add_argument('--only-id',
#                     action="store", dest="import:onlyid",
#                     help="only id")

def run(config):
    
    cdef   tuple       input
    cdef   tuple       output 
    cdef   int         i
    cdef   type        value_type
    cdef   obitype_t   value_obitype
    cdef   obitype_t   old_type
    cdef   obitype_t   new_type
    cdef   bint        get_quality
    cdef   bint        NUC_SEQS_view
    cdef   bint        silva
    cdef   bint        rdp
    cdef   int         nb_elts
    cdef   object      d
    cdef   View        view
    cdef   object      entries
    cdef   object      entry
    cdef   Column      id_col
    cdef   Column      def_col
    cdef   Column      seq_col
    cdef   Column      qual_col
    cdef   Column      old_column
    cdef   Column      sci_name_col
    cdef   bytes       sci_name
    cdef   bint        rewrite
    cdef   dict        dcols
    cdef   int         skipping
    cdef   bytes       tag
    cdef   object      value
    cdef   list        elt_names
    cdef   int         old_nb_elements_per_line
    cdef   int         new_nb_elements_per_line
    cdef   list        old_elements_names
    cdef   list        new_elements_names
    cdef   ProgressBar pb
    global             obi_errno
        
    DMS.obi_atexit()
    
    logger("info", "obi import: imports an object (file(s), obiview, taxonomy...) into a DMS")
    
    entry_count = -1
    pb = None
    
    if not config['obi']['taxdump']:
        input = open_uri(config['obi']['inputURI'])
        if input is None:  # TODO check for bytes instead now?
            raise Exception("Could not open input URI")
        
        if config['obi']['only'] is not None:
            entry_count = min(input[4], config['obi']['only'])
        else:
            entry_count = input[4]
        
        if entry_count > 0:
            logger("info", "Importing %d entries", entry_count)
        else:
            logger("info", "Importing an unknown number of entries")
        
        # TODO a bit dirty?
        if input[2]==Nuc_Seq or input[2]==View_NUC_SEQS:
            v = View_NUC_SEQS
        else:
            v = View 
    else:
        v = None
    
    if config['obi']['taxdump'] or (isinstance(input[1], View) and not config['import']['space_priority']): 
        dms_only=True
    else:
        dms_only=False
    
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      newviewtype=v,
                      dms_only=dms_only)
    if output is None:
        raise Exception("Could not open output")
    
    o_dms = output[0]
    
    # Read taxdump
    if config['obi']['taxdump']:  # The input is a taxdump to import in a DMS
        # Check if taxonomy name isn't already taken
        taxo_name = output[1].split(b'/')[1]
        if Taxonomy.exists(o_dms, taxo_name):
            raise Exception("Taxonomy name already exists in this DMS")
        taxo = Taxonomy.open_taxdump(o_dms, config['obi']['inputURI'])
        taxo.write(taxo_name)
        taxo.close()
        o_dms.record_command_line(" ".join(sys.argv[1:]))
        o_dms.close(force=True)
        logger("info", "Done.")
        return

    # Open taxonomy if there is one
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        taxo_uri = open_uri(config['obi']['taxoURI'])
        if taxo_uri is None or taxo_uri[2] == bytes:
            raise Exception("Couldn't open taxonomy")
        taxo = taxo_uri[1]

    else :
        taxo = None

    # If importing a view between two DMS and not wanting to save space if line selection in original view, use C API
    if isinstance(input[1], View) and not config['import']['space_priority']:
        if obi_import_view(input[0].name_with_full_path, o_dms.name_with_full_path, input[1].name, tobytes((config['obi']['outputURI'].split('/'))[-1])) < 0 :
            input[0].close(force=True)
            output[0].close(force=True)
            raise Exception("Error importing a view in a DMS")
        o_dms.record_command_line(" ".join(sys.argv[1:]))
        input[0].close(force=True)
        output[0].close(force=True)
        logger("info", "Done.")
        return

    # Reinitialize the progress bar
    if entry_count >= 0 and config['obi']['noprogressbar'] == False:
        pb = ProgressBar(entry_count, config)
    else:
        pb = None
        
    NUC_SEQS_view = False
    if isinstance(output[1], View) :
        view = output[1]
        if output[2] == View_NUC_SEQS :
            NUC_SEQS_view = True
    else: 
        raise NotImplementedError()

    # Save basic columns in variables for optimization
    if NUC_SEQS_view :
        id_col = view[ID_COLUMN]
        def_col = view[DEFINITION_COLUMN]
        seq_col = view[NUC_SEQUENCE_COLUMN]

    # Prepare taxon scientific name and taxid refs if RDP or SILVA file
    silva = False
    rdp = False
    unite = False
    if 'inputformat' in config['obi'] and (config['obi']['inputformat'] == b"silva" or config['obi']['inputformat'] == b"rdp" or config['obi']['inputformat'] == b"unite"):
        #if taxo is None:
        #    raise Exception("A taxonomy (as built by 'obi import --taxdump') must be provided for SILVA and RDP files")
        if config['obi']['inputformat'] == b"silva":
            silva = True
        elif config['obi']['inputformat'] == b"rdp":
            rdp = True
        elif config['obi']['inputformat'] == b"unite":
            unite = True
        sci_name_col = Column.new_column(view, SCIENTIFIC_NAME_COLUMN, OBI_STR)
        if taxo is not None:
            taxid_col = Column.new_column(view, TAXID_COLUMN, OBI_INT)

    dcols = {}

    # First read through the entries to prepare columns with dictionaries as they are very time-expensive to rewrite
    if config['import']['preread']:
        logger("info", "First readthrough...")
        entries = input[1]
        i = 0
        dict_dict = {}
        for entry in entries:
            PyErr_CheckSignals()
        
            if entry is None:  # error or exception handled at lower level, not raised because Python generators can't resume after any exception is raised
                if config['obi']['skiperror']:
                    i-=1
                    continue
                else:
                    raise Exception("obi import error in first readthrough")
            
            if pb is not None:
                pb(i)
            elif not i%50000:
                logger("info", "Read %d entries", i)
    
            for tag in entry :
                newtag = tag
                if tag[:7] == b"merged_":
                    newtag = MERGED_PREFIX+tag[7:]
                if type(entry[tag]) == dict :
                    if tag in dict_dict:
                        dict_dict[newtag][0].update(entry[tag].keys())
                    else:
                        dict_dict[newtag] = [set(entry[tag].keys()), get_obitype(entry[tag])]
            i+=1
        
        if pb is not None:
            pb(i, force=True)
            print("", file=sys.stderr)
       
        for tag in dict_dict:
            dcols[tag] = (Column.new_column(view, tag, dict_dict[tag][1], \
                              nb_elements_per_line=len(dict_dict[tag][0]), \
                              elements_names=list(dict_dict[tag][0]), \
                              dict_column=True), \
                          dict_dict[tag][1])
    
        
        # Reinitialize the input
        if isinstance(input[0], CompressedFile):
            input_is_file = True
        
        # Reinitialize the progress bar
        if entry_count >= 0 and config['obi']['noprogressbar'] == False:
            pb = ProgressBar(entry_count, config)
        else:
            pb = None

        try:
            input[0].close()
        except AttributeError:
            pass
        input = open_uri(config['obi']['inputURI'], force_file=input_is_file)
        if input is None:
            raise Exception("Could not open input URI")
    
#    if 'onlyid' in config['import']:
#        onlyid = tobytes(config['import']['onlyid'])
#    else:
#        onlyid = None
    
    entries = input[1]
    i = 0
    for entry in entries :
        
        PyErr_CheckSignals()

        if entry is None:  # error or exception handled at lower level, not raised because Python generators can't resume after any exception is raised
            if config['obi']['skiperror']:
                continue
            else:
                raise RollbackException("obi import error, rollbacking view", view)
        
        if pb is not None:
            pb(i)
        elif not i%50000:
            logger("info", "Imported %d entries", i)
        
#        if onlyid is not None and entry.id != onlyid:
#            continue
        
        try:
             
            if NUC_SEQS_view: 
                id_col[i] = entry.id           
                def_col[i] = entry.definition
                seq_col[i] = entry.seq
                # Check if there is a sequencing quality associated by checking the first entry    # TODO haven't found a more robust solution yet
                if i == 0:
                    get_quality = QUALITY_COLUMN in entry
                    if get_quality:
                        Column.new_column(view, QUALITY_COLUMN, OBI_QUAL)
                        qual_col = view[QUALITY_COLUMN]
                if get_quality:
                    qual_col[i] = entry.quality
                    
                # Parse taxon scientific name if RDP or Silva or Unite file
                if (rdp or silva or unite):
                    if rdp or silva:
                        sci_names = entry.definition.split(b";")
                        sci_name_col[i] = sci_names[-1]
                    elif unite:
                        sci_names = entry.id.split(b'|')[-1].split(b';')
                        sci_name_col[i] = re.sub(b'[a-zA-Z]__', b'', sci_names[-1])
                    # Fond taxid if taxonomy provided
                    if taxo is not None :
                        for sci_name in reversed(sci_names):
                            if unite:
                                sci_name = re.sub(b'[a-zA-Z]__', b'', sci_name)
                            if sci_name.split()[0] != b'unidentified' and sci_name.split()[0] != b'uncultured' and sci_name.split()[0] != b'metagenome':
                                taxon = taxo.get_taxon_by_name(sci_name)
                                if taxon is not None:
                                    sci_name_col[i] = taxon.name
                                    taxid_col[i] = taxon.taxid
                                    #print(taxid_col[i], sci_name_col[i])
                                    break

            for tag in entry :
                
                if tag != ID_COLUMN and tag != DEFINITION_COLUMN and tag != NUC_SEQUENCE_COLUMN and tag != QUALITY_COLUMN :  # TODO dirty 
                                    
                    value = entry[tag]
                    if tag == b"taxid":
                        tag = TAXID_COLUMN
                    if tag == b"count":
                        tag = COUNT_COLUMN
                    if tag[:7] == b"merged_":
                        tag = MERGED_PREFIX+tag[7:]

                    if type(value) == bytes and value[:1]==b"[" :
                        try:
                            if type(eval(value)) == list:
                                value = eval(value)
                                #print(value)
                        except:
                            pass
                    
                    if tag not in dcols :
                                                
                        value_type = type(value)
                        nb_elts = 1
                        value_obitype = OBI_VOID
                        dict_col = False
                        
                        if value_type == dict :
                            nb_elts = len(value)
                            elt_names = list(value)
                            dict_col = True
                        else :
                            nb_elts = 1
                            elt_names = None
                        
                        if value_type == list :
                            tuples = True
                        else:
                            tuples = False
                        
                        value_obitype = get_obitype(value)
                                                
                        if value_obitype != OBI_VOID :
                            dcols[tag] = (Column.new_column(view, tag, value_obitype, nb_elements_per_line=nb_elts, elements_names=elt_names, dict_column=dict_col, tuples=tuples), value_obitype)
                                                     
                            # Fill value
                            dcols[tag][0][i] = value
                         
                        # TODO else log error?
     
                    else :
             
                        rewrite = False
     
                        # Check type adequation
                        old_type = dcols[tag][1]
                        new_type = OBI_VOID
                        new_type = update_obitype(old_type, value)
                        if old_type != new_type :
                            rewrite = True
     
                        try:
                            # Check that it's not the case where the first entry contained a dict of length 1 and now there is a new key                        
                            if type(value) == dict and \
                                dcols[tag][0].nb_elements_per_line == 1 \
                                and set(dcols[tag][0].elements_names) != set(value.keys()) :
                                raise IndexError  # trigger column rewrite
                            
                            # Fill value
                            dcols[tag][0][i] = value
                         
                        except (IndexError, OverflowError):
                                                                                 
                            value_type = type(value)
                            old_column = dcols[tag][0]
                            old_nb_elements_per_line = old_column.nb_elements_per_line
                            new_nb_elements_per_line = 0
                            old_elements_names = old_column.elements_names
                            new_elements_names = None
         
                            #####################################################################
                             
                            # Check the length and keys of column lines if needed
                            if value_type == dict :    # Check dictionary keys
                                for k in value :
                                    if k not in old_elements_names :
                                        new_elements_names = list(set(old_elements_names+[tobytes(k) for k in value]))
                                        rewrite = True
                                        break
                             
                            elif value_type == list or value_type == tuple :  # Check vector length
                                if old_nb_elements_per_line < len(value) :
                                    new_nb_elements_per_line = len(value)
                                    rewrite = True
                             
                            #####################################################################
                             
                            if rewrite :
                                if new_nb_elements_per_line == 0 and new_elements_names is not None :
                                    new_nb_elements_per_line = len(new_elements_names)
                                 
                                # Reset obierrno 
                                obi_errno = 0
     
                                dcols[tag] = (view.rewrite_column_with_diff_attributes(old_column.name, 
                                                                                       new_data_type=new_type, 
                                                                                       new_nb_elements_per_line=new_nb_elements_per_line,
                                                                                       new_elements_names=new_elements_names,
                                                                                       rewrite_last_line=False), 
                                              new_type)
                                 
                                # Update the dictionary:
                                for t in dcols :
                                    dcols[t] = (view[t], dcols[t][1])
                                 
                                # Fill value
                                dcols[tag][0][i] = value
        
        except Exception as e:
            print("\nCould not import sequence:", repr(entry), "(error raised:", e, ")")
            if 'skiperror' in config['obi'] and not config['obi']['skiperror']:
                raise e
            else:
                pass
                i-=1  # overwrite problematic entry
        
        i+=1
 
    if pb is not None:
        pb(i, force=True)
        print("", file=sys.stderr)
    logger("info", "Imported %d entries", len(view))
    
    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    view.write_config(config, "import", command_line, input_str=[os.path.abspath(config['obi']['inputURI'])])
    output[0].record_command_line(command_line)

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(view), file=sys.stderr)
    
    try:
        input[0].close()
    except AttributeError:
        pass
    try:
        output[0].close(force=True)
    except AttributeError:
        pass

    logger("info", "Done.")
