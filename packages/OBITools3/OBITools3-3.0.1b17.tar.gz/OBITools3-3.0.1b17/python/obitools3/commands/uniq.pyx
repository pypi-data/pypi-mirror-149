#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.dms import DMS
from obitools3.dms.view.view cimport View
from obitools3.dms.obiseq cimport Nuc_Seq_Stored
from obitools3.dms.view import RollbackException
from obitools3.dms.view.typed_view.view_NUC_SEQS cimport View_NUC_SEQS
from obitools3.dms.column.column cimport Column, Column_line
from obitools3.dms.capi.obiview cimport QUALITY_COLUMN, COUNT_COLUMN, NUC_SEQUENCE_COLUMN, ID_COLUMN, TAXID_COLUMN, \
                                        TAXID_DIST_COLUMN, MERGED_TAXID_COLUMN, MERGED_COLUMN, MERGED_PREFIX, \
                                        REVERSE_QUALITY_COLUMN
from obitools3.dms.capi.obitypes cimport OBI_INT, OBI_STR, index_t
from obitools3.apps.optiongroups import addMinimalInputOption, \
                                        addMinimalOutputOption, \
                                        addTaxonomyOption, \
                                        addEltLimitOption, \
                                        addNoProgressBarOption
from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.utils cimport tobytes, tostr, str2bytes

import sys
from cpython.exc cimport PyErr_CheckSignals
from io import BufferedWriter


__title__="Group sequence records together"

 
def addOptions(parser):
 
    addMinimalInputOption(parser)
    addTaxonomyOption(parser)
    addMinimalOutputOption(parser)
    addEltLimitOption(parser)
    addNoProgressBarOption(parser)
 
    group = parser.add_argument_group('obi uniq specific options')
 
    group.add_argument('--merge', '-m',
                       action="append", dest="uniq:merge",
                       metavar="<TAG NAME>",
                       default=[],
                       type=str,
                       help="Attributes to merge.") # note: must be a 1 elt/line column, but columns containing already merged information (name MERGED_*) are automatically remerged

    group.add_argument('--merge-ids', '-e',
                       action="store_true", dest="uniq:mergeids",
                       default=False,
                       help="Add the merged key with all ids of merged sequences.")
   
    group.add_argument('--category-attribute', '-c',
                        action="append", dest="uniq:categories",
                        metavar="<Attribute Name>",
                        default=[],
                        help="Add one attribute to the list of attributes "
                             "used to group sequences before dereplication "
                             "(option can be used several times).")


cdef merge_taxonomy_classification(View_NUC_SEQS o_view, Taxonomy taxonomy, dict config) :
    
    cdef int             taxid
    cdef Nuc_Seq_Stored  seq
    cdef list            m_taxids
    cdef bytes           k
    cdef object          tsp
    cdef object          tgn
    cdef object          tfa
    cdef object          sp_sn
    cdef object          gn_sn
    cdef object          fa_sn

    # Create columns and save them for efficiency
    if b"species" in o_view and o_view[b"species"].data_type_int != OBI_INT :
        o_view.delete_column(b"species")
    if b"species" not in o_view:
        Column.new_column(o_view, 
                          b"species", 
                          OBI_INT
                         )
    species_column = o_view[b"species"]

    if b"genus" in o_view and o_view[b"genus"].data_type_int != OBI_INT :
        o_view.delete_column(b"genus")
    if b"genus" not in o_view:
        Column.new_column(o_view, 
                          b"genus", 
                          OBI_INT
                         )
    genus_column = o_view[b"genus"]

    if b"family" in o_view and o_view[b"family"].data_type_int != OBI_INT :
        o_view.delete_column(b"family")
    if b"family" not in o_view:
        Column.new_column(o_view, 
                          b"family", 
                          OBI_INT
                         )
    family_column = o_view[b"family"]

    if b"species_name" in o_view and o_view[b"species_name"].data_type_int != OBI_STR :
        o_view.delete_column(b"species_name")
    if b"species_name" not in o_view:
        Column.new_column(o_view, 
                          b"species_name", 
                          OBI_STR
                         )
    species_name_column = o_view[b"species_name"]

    if b"genus_name" in o_view and o_view[b"genus_name"].data_type_int != OBI_STR :
        o_view.delete_column(b"genus_name")
    if b"genus_name" not in o_view:
        Column.new_column(o_view, 
                          b"genus_name", 
                          OBI_STR
                         )
    genus_name_column = o_view[b"genus_name"]

    if b"family_name" in o_view and o_view[b"family_name"].data_type_int != OBI_STR :
        o_view.delete_column(b"family_name")
    if b"family_name" not in o_view:
        Column.new_column(o_view, 
                          b"family_name", 
                          OBI_STR
                         )
    family_name_column = o_view[b"family_name"]

    if b"rank" in o_view and o_view[b"rank"].data_type_int != OBI_STR :
        o_view.delete_column(b"rank")
    if b"rank" not in o_view:
        Column.new_column(o_view, 
                          b"rank", 
                          OBI_STR
                         )
    rank_column = o_view[b"rank"]

    if b"scientific_name" in o_view and o_view[b"scientific_name"].data_type_int != OBI_STR :
        o_view.delete_column(b"scientific_name")
    if b"scientific_name" not in o_view:
        Column.new_column(o_view, 
                          b"scientific_name", 
                          OBI_STR
                         )
    scientific_name_column = o_view[b"scientific_name"]  
    
    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(len(o_view), config)
    else:
        pb = None
    
    i=0
    for seq in o_view:
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
        if MERGED_TAXID_COLUMN in seq :
            m_taxids = []            
            m_taxids_dict = seq[MERGED_TAXID_COLUMN]
            for k in m_taxids_dict.keys() :
                if m_taxids_dict[k] is not None:
                    m_taxids.append(int(k))
            taxid = taxonomy.last_common_taxon(*m_taxids)
            seq[TAXID_COLUMN] = taxid
            tsp = taxonomy.get_species(taxid)
            tgn = taxonomy.get_genus(taxid)
            tfa = taxonomy.get_family(taxid)
            
            if tsp is not None:
                sp_sn = taxonomy.get_scientific_name(tsp)
            else:
                sp_sn = None   # TODO was '###', discuss
                tsp = None     # TODO was '-1', discuss
                
            if tgn is not None:
                gn_sn = taxonomy.get_scientific_name(tgn)
            else:
                gn_sn = None
                tgn = None
                
            if tfa is not None:
                fa_sn = taxonomy.get_scientific_name(tfa)
            else:
                fa_sn = None
                tfa = None
            
            species_column[i] = tsp
            genus_column[i] = tgn
            family_column[i] = tfa
                
            species_name_column[i] = sp_sn
            genus_name_column[i] = gn_sn
            family_name_column[i] = fa_sn
            
            rank_column[i] = taxonomy.get_rank(taxid)
            scientific_name_column[i] = taxonomy.get_scientific_name(taxid)
        i+=1
    
    if pb is not None:
        pb(len(o_view), force=True)
    

cdef uniq_sequences(View_NUC_SEQS view, View_NUC_SEQS o_view, ProgressBar pb, dict config, list mergedKeys_list=None, Taxonomy taxonomy=None, bint mergeIds=False, list categories=None, int max_elts=1000000) :
     
    cdef int            i
    cdef int            k
    cdef int            k_count
    cdef int            o_idx
    cdef int            u_idx
    cdef int            i_idx
    cdef int            i_count
    cdef int            o_count
    cdef str            key_str
    cdef bytes          key
    cdef bytes          mkey
    cdef bytes          merged_col_name
    cdef bytes          o_id
    cdef bytes          i_id
    cdef set            mergedKeys_set
    cdef tuple          unique_id
    cdef list           catl
    cdef list           mergedKeys
    cdef list           mergedKeys_list_b
    cdef list           mergedKeys_m
    cdef list           str_merged_cols
    cdef list           merged_sequences
    cdef dict           uniques
    cdef dict           merged_infos
    cdef dict           mkey_infos
    cdef dict           merged_dict
    cdef dict           mkey_cols
    cdef Nuc_Seq_Stored i_seq
    cdef Nuc_Seq_Stored o_seq
    cdef Nuc_Seq_Stored u_seq
    cdef Column         i_seq_col
    cdef Column         i_id_col
    cdef Column         i_taxid_col
    cdef Column         i_taxid_dist_col
    cdef Column         o_id_col
    cdef Column         o_taxid_dist_col
    cdef Column         o_merged_col
    cdef Column         o_count_col
    cdef Column         i_count_col
    cdef Column_line    i_mcol  
    cdef object         taxid_dist_dict
    cdef object         iter_view
    cdef object         mcol
    cdef object         to_merge
    cdef list           merged_list

    uniques = {}
    
    for column_name in view.keys():
        if column_name[:7] == b"MERGED_":
            info_to_merge = column_name[7:]
            if mergedKeys_list is not None:
                mergedKeys_list.append(tostr(info_to_merge))
            else:
                mergedKeys_list = [tostr(info_to_merge)]
    
    mergedKeys_list_b = []
    if mergedKeys_list is not None:
        for key_str in mergedKeys_list:
            mergedKeys_list_b.append(tobytes(key_str))
        mergedKeys_set=set(mergedKeys_list_b)
    else:
        mergedKeys_set=set() 
 
    if taxonomy is not None:
        mergedKeys_set.add(TAXID_COLUMN)
         
    mergedKeys = list(mergedKeys_set)
        
    k_count = len(mergedKeys)
     
    mergedKeys_m = []
    for k in range(k_count):
        mergedKeys_m.append(MERGED_PREFIX + mergedKeys[k])
    
    # Check that not trying to remerge without total count information
    for key in mergedKeys_m:
        if key in view and COUNT_COLUMN not in view:
            raise Exception("\n>>>>\nError: trying to re-merge tags without total count tag. Run obi annotate to add the count tag from the relevant merged tag, i.e.: \nobi annotate --set-tag COUNT:'sum([value for key,value in sequence['MERGED_sample'].items()])' dms/input dms/output\n")
    
    if categories is None:
        categories = []
 
    # Keep columns that are going to be used a lot in variables 
    i_seq_col = view[NUC_SEQUENCE_COLUMN]
    i_id_col = view[ID_COLUMN]
    if TAXID_COLUMN in view:
        i_taxid_col = view[TAXID_COLUMN]
    if TAXID_DIST_COLUMN in view:
        i_taxid_dist_col = view[TAXID_DIST_COLUMN]

 
    # First browsing
    i = 0
    o_idx = 0
    
    logger("info", "First browsing through the input")
    merged_infos = {}
    iter_view = iter(view)
    for i_seq in iter_view :
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
         
        # This can't be done in the same line as the unique_id tuple creation because it generates a bug
        # where Cython (version 0.25.2) does not detect the reference to the categs_list variable and deallocates 
        # it at the beginning of the function.
        # (Only happens if categs_list is an optional parameter, which it is).
        catl = []
        for x in categories :
            catl.append(i_seq[x])    
          
        #unique_id = tuple(catl) + (i_seq_col[i],)
        unique_id = tuple(catl) + (i_seq_col.get_line_idx(i),)
        #unique_id = tuple(i_seq[x] for x in categories) + (seq_col.get_line_idx(i),)  # The line that cython can't read properly
         
        if unique_id in uniques:
            uniques[unique_id].append(i)
        else:
            uniques[unique_id] = [i]

        for k in range(k_count):
            key = mergedKeys[k]
            mkey = mergedKeys_m[k]
            if mkey in i_seq:
                if mkey not in merged_infos:
                    merged_infos[mkey] = {}
                    mkey_infos = merged_infos[mkey]
                    mkey_infos['nb_elts'] = view[mkey].nb_elements_per_line
                    mkey_infos['elt_names'] = view[mkey].elements_names
            if key in i_seq:
                if mkey not in merged_infos:
                    merged_infos[mkey] = {}
                    mkey_infos = merged_infos[mkey]
                    mkey_infos['nb_elts'] = 1
                    mkey_infos['elt_names'] = [i_seq[key]]
                else:
                    mkey_infos = merged_infos[mkey]
                    if i_seq[key] not in mkey_infos['elt_names']:     # TODO make faster? but how?
                        mkey_infos['elt_names'].append(i_seq[key])
                        mkey_infos['nb_elts'] += 1
        i+=1

    # Create merged columns
    str_merged_cols = []
    mkey_cols = {}
    for k in range(k_count):
        key = mergedKeys[k]
        merged_col_name = mergedKeys_m[k]
        
#        if merged_infos[merged_col_name]['nb_elts'] == 1:
#            raise Exception("Can't merge information from a tag with only one element (e.g. one sample ; don't use -m option)")
        
        if merged_col_name in view:
            i_col = view[merged_col_name]
        else:
            i_col = view[key]
        
        if merged_infos[merged_col_name]['nb_elts'] > max_elts:
            str_merged_cols.append(merged_col_name)
            Column.new_column(o_view,
                              merged_col_name,
                              OBI_STR,
                              to_eval=True,
                              comments=i_col.comments,
                              alias=merged_col_name
                             )

        else:
            Column.new_column(o_view,
                              merged_col_name,
                              OBI_INT,
                              nb_elements_per_line=merged_infos[merged_col_name]['nb_elts'],
                              elements_names=list(merged_infos[merged_col_name]['elt_names']),
                              dict_column=True,
                              comments=i_col.comments,
                              alias=merged_col_name
                             )
        
        mkey_cols[merged_col_name] = o_view[merged_col_name]

    # taxid_dist column
    if mergeIds and TAXID_COLUMN in mergedKeys:
        if len(view) > max_elts: #The number of different IDs corresponds to the number of sequences in the view
            str_merged_cols.append(TAXID_DIST_COLUMN)
            Column.new_column(o_view, 
                              TAXID_DIST_COLUMN, 
                              OBI_STR,
                              to_eval=True,
                              alias=TAXID_DIST_COLUMN
                             )
        else:
            Column.new_column(o_view, 
                              TAXID_DIST_COLUMN, 
                              OBI_INT,
                              nb_elements_per_line=len(view),
                              elements_names=[id for id in i_id_col],
                              dict_column=True,
                              alias=TAXID_DIST_COLUMN
                             )

    del(merged_infos)
    
    # Merged ids column
    if mergeIds :
        Column.new_column(o_view,
                          MERGED_COLUMN,
                          OBI_STR,
                          tuples=True,
                          alias=MERGED_COLUMN
                         )

    # Keep columns in variables for efficiency
    o_id_col = o_view[ID_COLUMN]
    if TAXID_DIST_COLUMN in o_view:
        o_taxid_dist_col = o_view[TAXID_DIST_COLUMN]
    if MERGED_COLUMN in o_view:
        o_merged_col = o_view[MERGED_COLUMN]
    if COUNT_COLUMN not in o_view:
        Column.new_column(o_view,
                          COUNT_COLUMN,
                          OBI_INT)
    o_count_col = o_view[COUNT_COLUMN]
    if COUNT_COLUMN in view:
        i_count_col = view[COUNT_COLUMN]
    
    if pb is not None:
        pb(len(view), force=True)
        print("")
        
    logger("info", "Second browsing through the input")
    
    # Initialize the progress bar
    if pb is not None:
        pb = ProgressBar(len(view))
        
    o_idx = 0
    total_treated = 0
    
    for unique_id in uniques :
        PyErr_CheckSignals()
        
        merged_sequences = uniques[unique_id]
        
        u_idx = uniques[unique_id][0]
        u_seq = view[u_idx]
        o_view[o_idx] = u_seq
        o_seq = o_view[o_idx]
        o_id = o_seq.id
        
        if mergeIds:
            merged_list = [view[idx].id for idx in merged_sequences]
            if MERGED_COLUMN in view: # merge all ids if there's already some merged ids info
                merged_list.extend(view[MERGED_COLUMN][idx] for idx in merged_sequences)
            merged_list = list(set(merged_list)) # deduplicate the list
            o_merged_col[o_idx] = merged_list

        o_count = 0

        if TAXID_DIST_COLUMN in u_seq and i_taxid_dist_col[u_idx] is not None:
            taxid_dist_dict = i_taxid_dist_col[u_idx]
        else:
            taxid_dist_dict = {}           

        merged_dict = {}
        for mkey in mergedKeys_m:
            merged_dict[mkey] = {}

        for i_idx in merged_sequences:
            PyErr_CheckSignals()
            
            if pb is not None:
                pb(total_treated)
 
            i_id = i_id_col[i_idx]
            i_seq = view[i_idx]

            if COUNT_COLUMN not in i_seq or i_count_col[i_idx] is None:
                i_count = 1
            else:
                i_count = i_count_col[i_idx]
 
            o_count += i_count
        
            for k in range(k_count):
                                
                key = mergedKeys[k]
                mkey = mergedKeys_m[k]
                
                if key==TAXID_COLUMN and mergeIds:
                    if TAXID_DIST_COLUMN in i_seq:
                        taxid_dist_dict.update(i_taxid_dist_col[i_idx])
                    if TAXID_COLUMN in i_seq:
                        taxid_dist_dict[i_id] = i_taxid_col[i_idx]

                # merge relevant keys
                if key in i_seq:
                    to_merge = i_seq[key]
                    if to_merge is not None:
                        if type(to_merge) != bytes:
                            to_merge = tobytes(str(to_merge))
                        mcol = merged_dict[mkey]
                        if to_merge not in mcol or mcol[to_merge] is None:
                            mcol[to_merge] = i_count
                        else:
                            mcol[to_merge] = mcol[to_merge] + i_count
                        o_seq[key] = None
                # merged infos already in seq: merge the merged infos
                if mkey in i_seq:
                    mcol = merged_dict[mkey] # dict
                    i_mcol = i_seq[mkey] # column line
                    if i_mcol.is_NA() == False:
                        for key2 in i_mcol:
                            if key2 not in mcol:
                                mcol[key2] = i_mcol[key2]
                            else:
                                mcol[key2] = mcol[key2] + i_mcol[key2]
                                        
            for key in i_seq.keys():
                # Delete informations that differ between the merged sequences
                # TODO make special columns list? // could be more efficient
                if key != COUNT_COLUMN and key != ID_COLUMN and key != NUC_SEQUENCE_COLUMN and key in o_seq and o_seq[key] != i_seq[key] \
                    and key not in merged_dict :
                    o_seq[key] = None
            
            total_treated += 1
            
        # Write merged dicts
        for mkey in merged_dict: 
            if mkey in str_merged_cols:
                mkey_cols[mkey][o_idx] = str(merged_dict[mkey])
            else:
                mkey_cols[mkey][o_idx] = merged_dict[mkey]
                # Sets NA values to 0  # TODO discuss, for now keep as None and test for None instead of testing for 0 in tools
                #for key in mkey_cols[mkey][o_idx]:
                #    if mkey_cols[mkey][o_idx][key] is None:
                #        mkey_cols[mkey][o_idx][key] = 0

        # Write taxid_dist
        if mergeIds and TAXID_COLUMN in mergedKeys:
            if TAXID_DIST_COLUMN in str_merged_cols:
                o_taxid_dist_col[o_idx] = str(taxid_dist_dict)
            else:
                o_taxid_dist_col[o_idx] = taxid_dist_dict
                
        o_count_col[o_idx] = o_count
        o_idx += 1
    
    if pb is not None:
        pb(len(view), force=True)
    
    # Deletes quality columns if there is one because the matching between sequence and quality will be broken (quality set to NA when sequence not)
    if QUALITY_COLUMN in view:
        o_view.delete_column(QUALITY_COLUMN)
    if REVERSE_QUALITY_COLUMN in view:
        o_view.delete_column(REVERSE_QUALITY_COLUMN)
    
    # Delete old columns that are now merged
    for k in range(k_count):
        if mergedKeys[k] in o_view:
            o_view.delete_column(mergedKeys[k])
    
    if taxonomy is not None:
        print("")  # TODO because in the middle of progress bar. Better solution?
        logger("info", "Merging taxonomy classification")
        merge_taxonomy_classification(o_view, taxonomy, config)



def run(config):
    
    cdef tuple         input
    cdef tuple         output 
    cdef tuple         taxo_uri
    cdef Taxonomy      taxo
    cdef View_NUC_SEQS entries
    cdef View_NUC_SEQS o_view
    cdef ProgressBar   pb
    
    DMS.obi_atexit()
    
    logger("info","obi uniq")
    
    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input view")    
    if input[2] != View_NUC_SEQS:
        raise NotImplementedError('obi uniq only works on NUC_SEQS views')
    
    # Open the output
    output = open_uri(config['obi']['outputURI'],
                      input=False,
                      newviewtype=View_NUC_SEQS)
    if output is None:
        raise Exception("Could not create output view")
    
    i_dms = input[0]
    entries = input[1]
    o_dms = output[0]
    output_0 = output[0]
    
    # If stdout output create a temporary view that will be exported and deleted.
    if type(output_0)==BufferedWriter:
        temporary_view_name = b"temp"
        i=0
        while temporary_view_name in i_dms:  # Making sure view name is unique in input DMS
            temporary_view_name = temporary_view_name+b"_"+str2bytes(str(i))
            i+=1
        o_view_name = temporary_view_name
        o_dms = i_dms
        o_view = View_NUC_SEQS.new(i_dms, o_view_name)
    else:
        o_view = output[1]
    
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        taxo_uri = open_uri(config['obi']['taxoURI'])
        if taxo_uri is None or taxo_uri[2] == bytes:
            raise RollbackException("Couldn't open taxonomy, rollbacking view", o_view)
        taxo = taxo_uri[1]
    else :
        taxo = None

    # Initialize the progress bar
    if config['obi']['noprogressbar'] == False:
        pb = ProgressBar(len(entries), config)
    else:
        pb = None
    
    if len(entries) > 0:
        try:
            uniq_sequences(entries, o_view, pb, config, mergedKeys_list=config['uniq']['merge'], taxonomy=taxo, mergeIds=config['uniq']['mergeids'], categories=config['uniq']['categories'], max_elts=config['obi']['maxelts'])       
        except Exception, e:
            raise RollbackException("obi uniq error, rollbacking view: "+str(e), o_view)
    
    if pb is not None:
        print("", file=sys.stderr)

    # Save command config in View and DMS comments
    command_line = " ".join(sys.argv[1:])
    input_dms_name=[input[0].name]
    input_view_name=[input[1].name]
    if 'taxoURI' in config['obi'] and config['obi']['taxoURI'] is not None:
        input_dms_name.append(config['obi']['taxoURI'].split("/")[-3])
        input_view_name.append("taxonomy/"+config['obi']['taxoURI'].split("/")[-1])
    o_view.write_config(config, "uniq", command_line, input_dms_name=input_dms_name, input_view_name=input_view_name)
    o_dms.record_command_line(command_line)

    # stdout output: write to buffer
    if type(output_0)==BufferedWriter:
        logger("info", "Printing to output...")
        o_view.print_to_output(output_0, noprogressbar=config['obi']['noprogressbar'])
        o_view.close()

    #print("\n\nOutput view:\n````````````", file=sys.stderr)
    #print(repr(o_view), file=sys.stderr)

    # If stdout output, delete the temporary result view in the input DMS
    if type(output_0)==BufferedWriter:
        View.delete_view(i_dms, o_view_name)

    i_dms.close(force=True)
    o_dms.close(force=True)

    logger("info", "Done.")

