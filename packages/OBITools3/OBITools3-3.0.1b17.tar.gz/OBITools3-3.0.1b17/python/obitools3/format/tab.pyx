#cython: language_level=3

cimport cython
from obitools3.dms.view.view cimport Line
from obitools3.utils cimport bytes2str_object, str2bytes, tobytes
from obitools3.dms.column.column cimport Column_line, Column_multi_elts
from obitools3.dms.column.typed_column.int cimport Column_int, Column_multi_elts_int

import sys

cdef class TabFormat:
    
    def __init__(self, list tags=[], header=True, bytes NAString=b"NA", bytes sep=b"\t", bint NAIntTo0=True, metabaR=False, ngsfilter=False):
        self.tags = set(tags)
        self.header = header
        self.first_line = True
        self.NAString = NAString
        self.sep = sep
        self.NAIntTo0 = NAIntTo0
        self.metabaR = metabaR
        self.ngsfilter = ngsfilter
        
    @cython.boundscheck(False)    
    def __call__(self, object data):
        
        cdef set ktags
        cdef list tags = [key for key in data]
        
        line = []
        
        if self.tags is not None and self.tags:
            ktags = self.tags
        else:
            ktags = set(tags)            
                
        if self.header and self.first_line:
            for k in ktags:
                if k in tags:
                    if self.metabaR:
                        if k == b'NUC_SEQ':
                            ktoprint = b'sequence'
                        else:
                            ktoprint = k.lower()
                        ktoprint = ktoprint.replace(b'merged_', b'')
                    else:
                        ktoprint = k
                    if isinstance(data.view[k], Column_multi_elts):
                        keys = data.view[k].keys()
                        keys.sort()
                        for k2 in keys:
                            line.append(tobytes(ktoprint)+b':'+tobytes(k2))
                    else:
                        line.append(tobytes(ktoprint))
            r = self.sep.join(value for value in line)
            r += b'\n'
            line = []
                    
        for k in ktags:
            if k in tags:
                value = data[k]
                if isinstance(data.view[k], Column_multi_elts):
                    keys = data.view[k].keys()
                    keys.sort()
                    if value is None:  # all keys at None
                        for k2 in keys: # TODO could be much more efficient
                            line.append(self.NAString)
                    else:
                        for k2 in keys: # TODO could be much more efficient
                            if value[k2] is not None:
                                line.append(str2bytes(str(bytes2str_object(value[k2]))))  # genius programming
                            else:
                                if self.NAIntTo0 and isinstance(data.view[k], Column_multi_elts_int):
                                    line.append(b"0")
                                else:
                                    line.append(self.NAString)
                else:
                    if value is not None or (self.NAIntTo0 and isinstance(data.view[k], Column_int)):
                        line.append(str2bytes(str(bytes2str_object(value))))
                    else:
                        line.append(self.NAString)
                  	      	
        if self.header and self.first_line:
            r += self.sep.join(value for value in line)
        else:
            r = self.sep.join(value for value in line)

        if self.first_line:
            self.first_line = False

        return r
