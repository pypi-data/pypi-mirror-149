from datetime import datetime

import dunlin.standardfile.dun.readprimitive as rpr
import dunlin.standardfile.dun.readstring    as rst

def go_to(dct, path, curr_lst, assign=None):
    '''
    Recurses through a dictionary to reach a sub-dictionary, analagous to 
    traversing directories in paths in a system of folders.  

    Parameters
    ----------
    dct : dict
        The dictionary that will be accessed.
    path : str or list
        If `path` is a string, it consists of keys separated by delimiters. The 
        first character of the path must be the delimiter. For example `.a.b`. 
        Alternatively, `path` can be a list of keys. 
    curr_lst : list of keys
        A list of keys corresponding to the current directory. Allows the function 
        to parse relative paths such as `..b` which means b is a subdirectory 
        of the current directory.
    assign : TYPE, optional
        The value to assign to the directory. If not None, the directory is 
        replaced with the value of this argument. The default is None.

    Notes
    -----
    Dunlin's language does not make use of the assign argument. May be removed 
    in the future.
    
    Returns
    -------
    dst : dict
        Returns the subdirectory. It will be created if it does not already exist. 
        If the `assign` argument is used, it will be the value of `assign` instead 
        of a dictionary.
    curr_lst : list of str
        A list of keys corresponding to the current directory.

    '''
    #Preprocess
    path     = split_path(path) if type(path) == str else path
    path_lst = replace_relative_path(path, curr_lst)
    
    #Recurse and update curr_lst
    dst = recurse(dct, path_lst, assign)
    curr_lst.clear()
    curr_lst.extend(path_lst)
    
    return dst, curr_lst

def split_path(string):
    '''
    Splits a path-like string into keys. Each key must be a valid primitive in 
    dunlin's language. The delimiter is ignored if it occurs inside a pair of 
    quotes.
    
    Notes
    -----
    The delimiter is expected to occur at the start of the string.
    '''
    string = string.strip()
    if not string:
        raise ValueError('Blank path.')
        
    delimiter = string[0]
    string    = string[1:]
    i0        = 0
    quote     = []
    chunks    = []
    
    for i, char in enumerate(string):
        if char == delimiter and not quote:
            chunk = string[i0: i].strip()
            if chunk:
                chunk = read_key(chunk)
                
            chunks.append(chunk)
            
            i0 = i + 1
        
        elif char in ["'", '"']:
            if not quote:
                quote.append(char)
            elif quote[-1] == char:
                quote.pop()
            else:
                quote.append(char)
    
    if i0 < len(string):
        chunk = string[i0: ].strip()
        if chunk:
            chunk = read_key(chunk)
        chunks.append(chunk)
    
    return chunks

def read_key(chunk):
    '''Parses the chunk into a key and ensures that the key is a primitive or 
    tuple. 
    
    Notes
    -----
    Calls the `read_string` function and checks that the result is a list of 
    length 1. The key is then taken to be the first value. The type is then 
    checked before returning the key.
    
    See Also
    --------
    dunlin.standardfile.dun.readstring.read_string
    '''
    allowed =  [int, float, str, bool, tuple, datetime]
    parsed  = rst.read_string(chunk, enforce_dict=False)
    
    if type(parsed) == list and len(parsed) == 1:
        key = parsed[0]
        
        if type(key) in allowed:
            return key

    temp = [str(i.__name__) for i in allowed]
    msg  = f'{chunk} cannot be used as a key. Allowed types are {temp}'
    raise TypeError(msg)

def replace_relative_path(path, curr_lst):
    '''Converts path from a string into a list. Replaces the blanks in the path 
    with values from curr_lst.
    '''
    path_       = []
    allow_blank = True
    
    for i, p in enumerate(path):
        if type(p) == str and not p:
            if allow_blank:
                if i >= len(curr_lst):
                    raise ValueError(f'Directory missing {path}')
                    
                s = curr_lst[i]
                path_.append(s)
                
        else:
            path_.append(p)
            allow_blank = False

    return path_

def recurse(dct, path_lst, assign=None):
    '''The recursive function for accessing the subdirectory. Creates new 
    directories (dicts) if they do not already exist.
    '''
    #Get next level
    next_level = path_lst[0]
    dct_       = dct.setdefault(next_level, type(dct)())
    
    if len(path_lst) == 1:
        if assign:
            dct[next_level] = assign
            return assign
        else:
            return dct_
        
    else:
        path_lst_ = path_lst[1:]

        return recurse(dct_, path_lst_, assign)

if __name__ == '__main__':
    # r = split_path('.a.b.c.d')
    # print(r)
    # r = split_path('.a."b.c".d')
    # print(r)
    
    # r = replace_relative_path(['', '', '', 'd'], ['a', 'b', 'c'])
    # print(r)
    dct      = {}
    curr_lst = []
    path     = '.a.b'
    
    dst, curr_lst = go_to(dct, path, curr_lst)
    
    path = '..0.4'
    
    dst, curr_lst = go_to(dct, path, curr_lst)
    print(dct)