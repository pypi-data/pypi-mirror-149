from datetime import datetime

import dunlin.utils                          as ut
import dunlin.standardfile.dun.readprimitive as rpr
import dunlin.standardfile.dun.builtin       as bi

###############################################################################
#Key-Value Reader for Substituted dun Strings
###############################################################################
def read_string(string, enforce_dict=True):
    '''
    The front-end algorithm for reading dun strings.

    Parameters
    ----------
    string : str
        The string to be parsed.
    
    Returns
    -------
    result : dict
        A dictionary.
    
    Notes
    -----
    Calls _read_dun. Convert the result to a dict if it was originally a list.
    '''
    result = _read_string(string, read_flat)
        
    if type(result) == list and enforce_dict:
        return dict(enumerate(result))
    else:
        return result
    
def _read_string(string, _flat_reader=lambda x: x):
    '''
    The back-end algorithm for reading dun strings. Should not be directly 
    called outside of testing purposes.

    Parameters
    ----------
    string : str
        The string to be parsed.
    _flat_reader : callable, optional
        The function that parses flattened containers. The default is lambda x: x.

    Returns
    -------
    result : dict, list
        The parsed value. The front-end version will carry out post-processing.
    
    Notes
    -----
    The _flat_reader argument is changed to read_flat in the front-end. Use of 
    the value lambda x: x is for development purposes in which the developer 
    does not need the individual items in the string to be evaluated.
    
    '''
    string  = preprocess_string(string)
    i0      = 0
    nested  = []
    curr    = []
    quote   = []
    bracket  = 0
    
    for i, char in enumerate(string):
        if char == '(' and not quote:
            bracket += 1
            
        elif char == ')' and not quote:
            bracket -= 1
            
        elif char == ',' and not quote and not bracket:
            append_chunk(string, i0, i, char, curr)
            
            #Update position
            i0 = i + 1
        
        elif char == '[' and not quote and not bracket:
            append_chunk(string, i0, i, char, curr)
            
            #Increase depth
            nested.append(curr)
            curr = []
            
            #Update position
            i0 = i + 1
            
        elif char == ']' and not quote and not bracket:
            if not nested:
                raise DunBracketError('open', string[max(0, i0-10): min(i+10, len(string))])
            append_chunk(string, i0, i, char, curr)
            
            #Decrease depth
            parsed = _flat_reader(curr)
            curr   = nested.pop()
            curr.append(parsed)
            i0 = i + 1
        
        elif char in ['"', "'"]:
            if not quote:
                quote.append(char)
            elif quote[-1] == char:
                quote.pop()
            else:
                quote.append(char)
            
        else:
            continue
    
    append_chunk(string, i0, len(string), None, curr)
    
    result = _flat_reader(curr)
    
    if len(nested) or bracket or quote:
        raise DunBracketError('close', string[max(0, i0-10): min(i+10, len(string))])
    
    return result

def preprocess_string(string):
    '''Strips the string and removes trailing commas that would complicate the 
    parsing process.
    '''
    new_string = string.strip()
    new_string = new_string[:-1] if new_string[-1] == ',' else new_string
    
    if not new_string:
        raise ValueError(new_string)
    
    elif new_string.strip()[-1] == ',':
        raise DunDelimiterError()
        
    return new_string

def append_chunk(string, i0, i, char, curr):
    '''Updates the current container when a "]" or "," is encountered. Checks 
    the sequence of last_char...chunk...char and raises an Exception if values 
    are detected before or after brackets not in accordance with syntax.
    
    :meta private:
    '''
    chunk      = string[i0: i].strip()
    last_char = string[i0-1] if i0 > 0 else None
    
    #Prevent values ,..., and [..., and start ...,
    if not chunk:
        if char == ',':
            if last_char in [',', '['] or i == 0:
                raise DunDelimiterError()
        return
    #Prevent values between start...[ without a = sign
    elif char == '[' and chunk[-1] != '=':
        raise DunOutsideError('bef', string[max(0, i0-10): min(i+10, len(string))])
    #Prevent creation of dict with list as key
    elif last_char == ']' and chunk[0] == '=':
        raise TypeError('Deteced a dict using a list as a key. Use a tuple instead.')
    #Prevent values between ]..., or ]...end that are not a multiplier
    elif last_char == ']' and chunk[0] != '*' and char in [',', None]:
        raise DunOutsideError('aft', string[max(0, i0-10): min(i+10, len(string))])
    
    curr.append(chunk)
    return chunk

class DunOutsideError(Exception):
    def __init__(self, pos='bef', excerpt=''):
        details = 'Values before bracket.' if pos == 'bef' else 'Values after bracket.'
        
        if excerpt:
            details += '\n"...' + excerpt + '..."' 
            
        super().__init__(details)

class DunDelimiterError(Exception):
    def __init__(self):
        super().__init__('Unexpected delimiter.')

class DunBracketError(Exception):
    def __init__(self, miss='open', excerpt=''):
        if miss == 'open':
            details = 'Detected an unexpected closing/missing opening bracket or quotation mark.'
        else:
            details = 'Detected an unexpected opening/missing closing bracket or quotation mark.'
        
        if excerpt:
            details +=  '\n"...' + excerpt + '..."' 
            
        super().__init__(details)
        
###############################################################################
#Reading Flat Containers
###############################################################################
def read_flat(flat):
    '''
    Reads a flat container and evaluates each item if it has not already been 
    evaluated.

    Parameters
    ----------
    flat : list
        A list of chunks to be parsed.

    Returns
    -------
    dict, list
        A dict or list of parsed items.
        
    '''
    
    flat_type = 'list'
    quote     = []
    
    for i in flat[0]:
        if i == '=' and not quote:
            flat_type = 'dict'
            break
        elif i in ['"', "'"]:
            if not quote:
                quote.append(i)
            elif quote[-1] == i:
                quote.pop()
            else:
                quote.append(i)

    if flat_type == 'dict':
        return read_dict(flat)
    else:
        return read_list(flat)

def read_dict(flat):
    result   = {}
    curr_key = None
    key_view = result.keys()

    for i, item in enumerate(flat):
        if type(item) == str:
            item = item.strip()
            
            if curr_key is not None:
                raise DunInconsistentError()
            
            if item[0] == '*':
                #Item is a list multiplier
                last_key = list(key_view)[-1]
                if type(result[last_key]) == list:
                    repeat           = read_repeat(item)
                    result[last_key] = result[last_key]*repeat
                else:
                    raise DunRepeatTypeError()
            
            else:
                #Item is a key-value pair
                key, value = split_first(item)
                key        = read_key(key)
    
                if value:
                    result[key] = read_value(value)
                else:
                    curr_key = key

        else:
            #Item has already been parsed
            if curr_key is None:
                raise DunInconsistentError()
            
            result[curr_key] = item
            curr_key = None
    
    if curr_key is not None:
        raise DunMissingError()
    return result

def split_first(string, delimiter='=', expect_present=True):
    quote = []
    for i, char in enumerate(string):
        if char == delimiter and not quote:
            return string[:i].strip(), string[i+1:].strip()
        
        elif char in ['"', "'"]:
            if not quote:
                quote.append(char)
            elif quote[-1] == char:
                quote.pop()
            else:
                quote.append(char)
    
    if expect_present:
        raise DunMissingError(string)
    elif quote:
        DunBracketError('close', string)
    else:
        return None

def read_list(flat):
    result       = [] 
    
    for i, item in enumerate(flat):
        if type(item) == str:
            item = item.strip()
            
            split = split_first(flat, expect_present=False)
            if split is not None:
                raise DunInconsistentError(f'Expected a list but detected: {item}')
            
            if item[0] == '*':
                repeat = read_repeat(item)
                if type(result[-1]) == list:
                    result[-1] = result[-1]*repeat
                else:
                    raise DunRepeatTypeError()
            else:
                value = read_value(item)
                result.append(value)
        else:
            result.append(item)
    
    return result

def read_repeat(x):
    try:
        return int(x[1:])
    except:
        raise DunRepeatInvalidError()

class DunInconsistentError(Exception):
    def __init__(self, msg=''):
        if msg:
            'Inconsistent data type.\n' + msg
        else:
            msg = 'Inconsistent data type.'
        super().__init__(msg)

class DunRepeatTypeError(Exception):
    def __init__(self,):
        super().__init__('Repeat can only come after a list.')

class DunRepeatInvalidError(Exception):
    def __init__(self, msg=''):
        if msg:
            msg = 'Repeat must be an integer.\n' + msg
        else:
            msg = 'Repeat must be an integer.'
        super().__init__(msg)

class DunMissingError(Exception):
    def __init__(self, msg=''):
        if msg:
            msg = 'Unexpected comma/equal sign or missing key/value.\n' + msg
        else:
            msg = 'Unexpected comma/equal sign or missing key/value.'
        super().__init__(msg)

###############################################################################
#Reading Keys/Values
###############################################################################
def read_key(key):
    '''Parses keys.
    '''
    allowed =  [int, float, str, bool, tuple, datetime]
    parsed  = read_value(key) 
    
    if type(key) in allowed:
        return parsed
    else:
        temp = [str(i.__name__) for i in allowed]
        msg  = f'{key} cannot be used as a key. Allowed types are {temp}'
        raise TypeError(msg)

def read_value(x):
    if not x:
        raise ValueError(x)
    
    if x[0] == '!':
        try:
            func_name, args = ut.split_functionlike(x[1:])
        except:
            raise InvalidFunction(x)
        
        args            = split_top_delimiter(args)
        args            = [rpr.read_primitive(i) for i in args]
        
        if func_name in bi.builtin_functions:
            try:
                return bi.builtin_functions[func_name](*args)
            except:
                raise FailedFunction(x)
        else:
            raise NoFunction(func_name)
            
    elif x[0] == '(' and x[-1] == ')' and not rpr.ismath(x):
        values = split_top_delimiter(x[1:-1])
        values = [rpr.read_primitive(v) for v in values]
        return tuple(values)
    
    else:
        return rpr.read_primitive(x)

def split_top_delimiter(string, delimiter=','):
    string = string.strip()
    i0     = 0
    inside_quotes = False
    chunks = []
    for i, char in enumerate(string):
        if char == delimiter and not inside_quotes:
            
            chunk = string[i0: i].strip()
            
            if chunk:
                if len(chunk) > 1 and chunk[0] == chunk[-1] and chunk[0] in ["'","'"]:
                    chunk = chunk[1:-1]
                chunks.append(chunk)
            else:
                raise ValueError(f'Encountered blank value or extra delimiters: {string}')
                
            i0    = i + 1
        
        elif char in ["'","'"]:
            inside_quotes = not inside_quotes

    if i0 < len(string):
        chunk = string[i0: ].strip()
        
        if chunk:
            if len(chunk) > 1 and chunk[0] == chunk[-1] and chunk[0] in ["'","'"]:
                chunk = chunk[1:-1]
            chunks.append(chunk)
        else:
            raise ValueError(f'Encountered blank value or extra delimiters: {string}')
            
    return chunks

class InvalidFunction(Exception):
    def __init__(self, x):
        msg = f'Invalid function call {x}'
        super().__init__(msg)

class NoFunction(Exception):
    def __init__(self, f):
        msg = f'No function "{f}"'
        super().__init__(msg)

class FailedFunction(Exception):
    def __init__(self, x):
        msg = f'Could not execute "{x}". Some arguments may be wrong.'
        super().__init__(msg)
