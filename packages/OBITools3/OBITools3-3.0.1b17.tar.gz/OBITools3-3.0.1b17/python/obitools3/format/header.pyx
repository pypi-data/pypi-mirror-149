#cython: language_level=3

from obitools3.dms.capi.obiview cimport NUC_SEQUENCE_COLUMN, \
                                        ID_COLUMN, \
                                        DEFINITION_COLUMN, \
                                        QUALITY_COLUMN, \
                                        COUNT_COLUMN

from obitools3.utils cimport str2bytes, bytes2str_object
from obitools3.dms.column.column cimport Column_line
from obitools3.dms.column.typed_column.int cimport Column_int, Column_multi_elts_int


cdef class HeaderFormat:
    
    SPECIAL_KEYS = [NUC_SEQUENCE_COLUMN, ID_COLUMN, DEFINITION_COLUMN, QUALITY_COLUMN]
    
    def __init__(self, str format="fasta", list tags=[], bint printNAKeys=False, bytes NAString=b"NA", bint NAIntTo0=False):
        '''
            @param format: 
            @type  format: `str`
            
            @param tags:
            @type  tags: `list` of `bytes`
            
            @param printNAKeys: 
            @type  printNAKeys: `bool` 
            
            @param NAString:
            @type NAString: `bytes`
        '''
        
        self.tags           = set(tags)
        self.printNAKeys    = printNAKeys
        self.NAString       = NAString
        self.NAIntTo0       = NAIntTo0
        
        if format=="fasta":
            self.start=b">"
        elif format=="fastq":
            self.start=b"@"
        
        self.headerBufferLength = 1000

        
    def __call__(self, object data):
        cdef bytes header
        cdef list tags = [key for key in data if key not in self.SPECIAL_KEYS]
        cdef set  ktags
        cdef list lines = [b""]
        cdef bytes tagline
        
        if self.tags is not None and self.tags:
            ktags = self.tags
        else:
            ktags = set(tags)
            
        for k in ktags:
            if k in tags:
                value = data[k]
                if value is None or (isinstance(value, Column_line) and value.is_NA()):
                    if isinstance(data.view[k], Column_int) and self.NAIntTo0: # people want missing int values to be 0
                        value = b'0'
                    elif self.printNAKeys:
                        value = self.NAString
                    else:
                        value = None
                else:
                    if type(value) == Column_line:
                        if isinstance(data.view[k], Column_multi_elts_int) and self.NAIntTo0:
                            value = dict(value)
                            for key in data.view[k].keys():
                                if key not in value or value[key]:
                                    value[key] = 0
                        else:
                            value = value.bytes()
                    else:
                        if type(value) == tuple:
                            value=list(value)
                    value = str2bytes(str(bytes2str_object(value))) # genius programming
                if value is not None:
                    lines.append(k + b"=" + value + b";")   
                
        if len(lines) > 1:
            tagline=b" ".join(lines)
        else:
            tagline=b""
            
        if data[DEFINITION_COLUMN] is not None:
            header = self.start + data[ID_COLUMN] + tagline + b" " + data[DEFINITION_COLUMN]
        else:
            header = self.start + data[ID_COLUMN] + tagline
             
        return header
        
