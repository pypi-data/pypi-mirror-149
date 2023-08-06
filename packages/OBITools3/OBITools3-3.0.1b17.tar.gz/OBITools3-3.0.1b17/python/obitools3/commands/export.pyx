#cython: language_level=3

from obitools3.apps.progress cimport ProgressBar  # @UnresolvedImport
from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.dms.obiseq import Nuc_Seq
from obitools3.dms.capi.obiview cimport QUALITY_COLUMN
from obitools3.writers.tab import TabWriter
from obitools3.format.tab import TabFormat
from obitools3.utils cimport tobytes, tostr

from obitools3.apps.optiongroups import addMinimalInputOption, \
                                        addExportOutputOption, \
                                        addNoProgressBarOption

import sys
import io

from cpython.exc cimport PyErr_CheckSignals

__title__="Export a view to a different file format"


def addOptions(parser):
    
    addMinimalInputOption(parser)
    addExportOutputOption(parser)
    addNoProgressBarOption(parser)


def run(config):
        
    DMS.obi_atexit()
    
    logger("info", "obi export : exports a view to a different file format")
    
    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input")
    iview = input[1]
    
    if 'outputformat' not in config['obi']:
        if iview.type == b"NUC_SEQS_VIEW":
            if QUALITY_COLUMN in iview:
                config['obi']['outputformat'] = b'fastq'
            else:
                config['obi']['outputformat'] = b'fasta'
        else:
            config['obi']['outputformat'] = b'tabular'
    
    # Open the output
    output = open_uri(config['obi']['outputURI'],
                      input=False)
    if output is None:
        raise Exception("Could not open output URI")

    output_object = output[0]
    writer = output[1]
        
     # Check that the input view has the type NUC_SEQS if needed    # TODO discuss, maybe bool property
    if (output[2] == Nuc_Seq) and (iview.type != b"NUC_SEQS_VIEW") :  # Nuc_Seq_Stored? TODO
        raise Exception("Error: the view to export in fasta or fastq format is not a NUC_SEQS view")
    
    if config['obi']['only'] is not None:
        withoutskip = min(input[4], config['obi']['only'])
    else:
        withoutskip = input[4]
     
    if config['obi']['skip'] is not None:
        skip = min(input[4], config['obi']['skip'])
    else:
        skip = 0
    
    # Initialize the progress bar
    if config['obi']['noprogressbar']:
        pb = None
    else:
        pb = ProgressBar(withoutskip - skip, config)

    if config['obi']['outputformat'] == b'metabaR':
        # Check prefix
        if "metabarprefix" not in config["obi"]:
            raise Exception("Prefix needed when exporting for metabaR (--metabaR-prefix option)")
        else:
            metabaRprefix = config["obi"]["metabarprefix"]
        
    i=0
    for seq in iview :
        PyErr_CheckSignals()
        if pb is not None:
            pb(i)
        try:
            writer(seq)
        except (StopIteration, BrokenPipeError, IOError):
            break
        i+=1

    if pb is not None:
        pb(i, force=True)
        print("", file=sys.stderr)

    if config['obi']['outputformat'] == b'metabaR':
        
        # Export ngsfilter file if view provided
        if 'metabarngsfilter' in config['obi']:
            ngsfilter_input = open_uri(config['obi']['metabarngsfilter'])
            if ngsfilter_input is None:
                raise Exception("Could not read ngsfilter view for metabaR output")
            ngsfilter_view = ngsfilter_input[1]
    
            ngsfilter_output = open(config['obi']['metabarprefix']+'.ngsfilter', 'w')
            
            for line in ngsfilter_view:

                line_to_print = b""                
                line_to_print += line[b'experiment']
                line_to_print += b"\t"
                line_to_print += line[b'sample']
                line_to_print += b"\t"
                line_to_print += line[b'forward_tag']
                line_to_print += b":"
                line_to_print += line[b'reverse_tag']
                line_to_print += b"\t"
                line_to_print += line[b'forward_primer']
                line_to_print += b"\t"
                line_to_print += line[b'reverse_primer']
                line_to_print += b"\t"
                line_to_print += line[b'additional_info']
                
                print(tostr(line_to_print), file=ngsfilter_output)
            
            if ngsfilter_input[0] != input[0]:
                ngsfilter_input[0].close()
            ngsfilter_output.close()
            
        # Export sample metadata
        samples_output = open(config['obi']['metabarprefix']+'_samples.csv', 'w')

        # Export sample metadata file if view provided
        if 'metabarsamples' in config['obi']:
            samples_input = open_uri(config['obi']['metabarsamples'])
            if samples_input is None:
                raise Exception("Could not read sample view for metabaR output")
            samples_view = samples_input[1]
        
            # Export with tab formatter
            TabWriter(TabFormat(header=True, sep='\t',), 
                      samples_output,
                      header=True)
            
            if samples_input[0] != input[0]:
                samples_input[0].close()
        
        # Else export just sample names from main view
        else:
            
            sample_list = []
            if 'MERGED_sample' in iview:
                sample_list = iview['MERGED_sample'].keys()
            elif 'sample' not in iview:
                for seq in iview:
                    sample = seq['sample']
                    if sample not in sample_list:
                        sample_list.append(sample)
            else:
                logger("warning", "Can not read sample list from main view for metabaR sample list export")            
            
            print("sample_id", file=samples_output)
            for sample in sample_list:
                line_to_print = b""                
                line_to_print += sample
                line_to_print += b"\t"
                print(tostr(line_to_print), file=samples_output)
        
        samples_output.close()

    # TODO save command in input dms?
    
    if not BrokenPipeError and not IOError:
        output_object.close()
    iview.close()
    input[0].close(force=True)

    logger("info", "Done.")

    if BrokenPipeError or IOError:
        sys.stderr.close()
