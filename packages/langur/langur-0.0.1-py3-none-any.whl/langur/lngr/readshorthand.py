import re
from collections import UserDict

import dunlin.standardfile.dun.readstring as rst

###############################################################################
#Substitution of Shorthands
###############################################################################
def read_shorthand(element):
    temp = get_template_and_shorthands(element)
    return substitute(*temp)
    
def substitute(template, horizontal, vertical):
    parsed_horizontal = {}
    for key, dct in horizontal.items():
        join      = dct.join
        template_ = dct.template
        temp      = _substitute(template_, dct)
        
        parsed_horizontal[key] = join.join(temp)
    
    intermediate = template.format(**parsed_horizontal)
    result       = _substitute(intermediate, vertical)
    
    return result

def _substitute(template, dct):
    result = []
    
    if not dct:
        return [template]
    
    for row in zip(*dct.values()):
        local = dict(zip(dct.keys(), row))
        
        chunk = template.format(**local)
    
        result.append(chunk)
    
    return result

###############################################################################
#Splitting of Element
###############################################################################
def get_template_and_shorthands(element):
    # pattern = '^[^#$]*'
    # found    = re.findall(pattern, element)
    # template = found[0].strip()
    
    # pattern = '([#$])([^#$=]*)=([^#$]*)'
    # found   = re.findall(pattern, element)
    
    template, found = string2chunks(element)
    vertical   = {}
    horizontal = {}
    print(element)
    print(found)
    print('.....................')
    for shorthand_type, key, value  in found:
        key = key.strip()
        
        check_valid_shorthand_key(shorthand_type, key)
        
        if shorthand_type == '$$':
            values_ = rst.split_top_delimiter(value)
            if not values_:
                raise ValueError(f'Shorthand must have at least one value.\n{element}')
            
            vertical[key] = values_
            
        elif shorthand_type == '$':
            split = key.split('.')
            if len(split) == 1:
                horizontal.setdefault(key, Horizontal())
                horizontal[key].template = value.strip()
            else:
                key, attr = split
                key       = key.strip()
                attr      = attr.strip()
                horizontal.setdefault(key, Horizontal())
                
                if attr == 'join' or attr == '_j':
                    value = value.strip()
                    if value[0] == value[-1] and value[0] in ['"', "'"]:
                        join = value[1:-1]
                    else:
                        join = value    
                        
                    horizontal[key].join = join
                else:
                    values_ = rst.split_top_delimiter(value, ',')
                    # values_ = rst.split_top_delimiter(value, ',')
                    if not values_:
                        raise ValueError(f'Shorthand must have at least one value.\n{element}')
                    
                    horizontal[key][attr] = values_
        else:
            raise ValueError(f'No shorthand type "{shorthand_type}"\n{element}')
    return template, horizontal, vertical

def check_valid_shorthand_key(shorthand_type, key):
    pass


def string2chunks(string):
    template   = None
    i0         = 0
    quote      = []
    delimiter  = ''
    key        = None
    value      = None
    chunks     = []
    
    for i, char in enumerate(string):
        
        if char == '$' and not quote:
            if template is None:
                template = string[i0:i]
                
            if key is None and value is None:
                delimiter += char
                i0         = i + 1
                continue
            elif key is not None and value is not None:
                chunks.append([delimiter, key, value])
                delimiter = char
                key       = None
                value     = None
                i0        = i + 1
                continue
            else:
                raise ValueError('Missing or incomplete key-value pair.')
            
        elif char == '=' and not quote and template is not None and value is None:
            value = ''
            continue
        
        elif char in '\'\"':
            if not quote:
                quote.append(char)
            elif quote[-1] == char:
                quote.pop()
            else:
                quote.append(char)
        
        if template is not None:
            if key is None:
                key = char
            elif value is None:
                key += char
            else:
                value += char
    
    if template is None:
        return string, []
    
    elif delimiter:
        chunks.append([delimiter, key, value])
    
    return template, chunks
    
class Horizontal(UserDict):
    template = ''
    join     = ', '




