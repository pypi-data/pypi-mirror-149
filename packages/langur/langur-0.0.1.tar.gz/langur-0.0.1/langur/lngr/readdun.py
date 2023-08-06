import re

import dunlin.standardfile.dun.readstring    as rst
import dunlin.standardfile.dun.readelement   as rel
import dunlin.standardfile.dun.parsepath     as pp 

###############################################################################
#Main Algorithm
###############################################################################
def read_file(filename, _element=rel.read_element):
    with open(filename, 'r') as file:
        dct = read_lines(file, True, _element=_element)
    return dct

def read_string(string, _element=rel.read_element):
    lines = string.split('\n')
    return read_lines(lines, _element=_element)
    
###############################################################################
#Supporting Functions
###############################################################################
def read_lines(lines, includes_newline=False, _element=rel.read_element):
    '''Reads an iterable of lines.
    

    Parameters
    ----------
    lines : iterable
        An iterable of strings.
    includes_newline : bool, optional
        True if the lines contain the new line character at the end and False 
        otherwise. The default is False.
    _element : callable
        The function for parsing elements.
    
    Returns
    -------
    dct : dict
        The parsed data.

    '''
    dct           = {}
    curr_lst      = []
    curr_dct      = None
    interpolators = {}
    chunk_lst     = []
    join          = '' if includes_newline else '\n'
    
    for line in lines:
        split = rst.split_first(line, delimiter='#', expect_present=False)
        if split:
            line = split[0]
        
        if not line:
            chunk_lst.append(line)
        elif line[0].isspace():
            chunk_lst.append(line)
        else:
            if chunk_lst:
                chunk    = join.join(chunk_lst)
                curr_dct = read_chunk(dct, curr_lst, curr_dct, interpolators, chunk, rel.read_element)
            
            chunk_lst.clear()
            chunk_lst.append(line)
    
    if chunk_lst:
        chunk    = join.join(chunk_lst)
        curr_dct = read_chunk(dct, curr_lst, curr_dct, interpolators, chunk, rel.read_element)
    
    return dct
    
def read_chunk(dct, curr_lst, curr_dct, interpolators, chunk, _element):
    chunk  = chunk
    chunk_ = chunk.strip()
    
    if not chunk_:
        pass
    
    
    elif chunk[0] == '`':
        split = rst.split_first(chunk, expect_present=False)
        
        if len(split) != 2:
            raise SyntaxError('Invalid interpolators.')
        
        key, value = split
        key        = key[1:-1].strip()
        value      = value.strip()
        
        interpolators[key] = value
    
    elif chunk[0] == ';':
        split = rst.split_first(chunk, expect_present=False)
        
        if split is not None:
            msg = f'Could not determine if this chunk is a directory or an element.\n{chunk}'
            raise SyntaxError(msg)

        curr_dct, curr_lst = pp.go_to(dct, chunk, curr_lst)
        
    else:
        if curr_dct is None:
            msg = f'The section for this element has not been set yet\n{chunk}'
            raise SyntaxError(msg)
            
        parsed_element = _element(chunk, interpolators=interpolators)
        curr_dct.update(parsed_element)
    
    return curr_dct#dct, curr_lst, curr_dct, interpolators

# def string2chunks(string):
#     pattern = '(\S.+((\n\s*)*\n[^\n\S].+)*)'
#     return re.findall(pattern, string)


# s = '''

# `r` = linspace(0, 20, 11)

# . 'a.2'.0

# a = [ 0= x,
#       1= y
#      ]

# b = `r`
# c = '`c`'
# '''
s='''
!a
b{{n}}= [{i}]
    #i    = {ii} = {{val}}
    #i.ii = 0, 1, 2 
    $val  = 4, 5
    $n    = 7, 8
'''
s='''
;"b=5"
a = 4
#4
'''
if __name__ == '__main__':

    _element = rel.read_element
    r = read_string(s, 
                    _element=_element
                    )
    print(r)
    
    r = read_file('example_data.dun')
    print(r)