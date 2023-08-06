import re

import dunlin.utils as ut

s='''
#a : i, 0, 1, 2
#b : ii, 1, 2, 3

`a
b_{i} : {i}*{ii}
    $i, 0, 1, 2
    $ii, 1, 2, 3
  
`c
d_{i} : {{ii}}
    $#a
    %#b
    
'''

class Element:
    def __init__(self, template, interpolators=None, **fields):
        
        self.template       = template
        self._fields        = {}
        self._interpolators = {}
        
        self.fields = fields
        self.interpolators = interpolators
    
    @property
    def fields(self):
        return self._fields
    
    @fields.setter
    def fields(self, fields):
        self._fields.clear()
        if fields is None:
            return
        
        for field, values in fields.items():
            self.add_field(field, values)
            
    def add_field(self, field, values):
        if type(field) != str:
            raise TypeError()
            
        for v in values:
            if type(v) != str and not ut.isnum(v):
                raise TypeError()

        self._fields[field] = values
    
    def pop_field(self, field):
        return self._field.pop(field)
    
    @property
    def interpolators(self):
        return self._interpolators
    
    @interpolators.setter
    def interpolators(self, fields):
        self._interpolators.clear()
        
        if fields is None:
            return 
        
        for field, values in fields.items():
            self.add_interpolator(field, values)
        
    def add_interpolator(self, field, values):
        if type(field) != str:
            raise TypeError()
        
        if type(values) == str:
            if '\n' in values or '\r' in values:
                raise ValueError()
                
            self._interpolators[field] = values
        else:
            temp = []
            for v in values:
                if type(v) != str and not ut.isnum(v):
                    raise TypeError()
                else:
                    temp.append(str(v))
            string = ', '.join(temp)

            return self.add_interpolator(field, string)
        
    def interpolate(self, template):
        interpolators = self._interpolators
        
        def repl(match):
            field = match[0]
            field = field[1]
            
            if field in interpolators:
                return interpolators[field]
            else:
                raise SyntaxError(f'Encountered an unexpected interpolation: {field}') 
        
        interpolated = re.sub('#\w*(\W|$)', repl, template)
        
        return interpolated
    
    def sub_h(self, template):
        stored_fields = self._fields
        
        def repl(m):
            print(m[1])
            split = m[1].split(',')
                
            if len(split) == 1:
                field, delimiter = split[0], ','
            elif len(split) == 2:
                field, delimiter = split
            else:
                raise SyntaxError()
            
            field     = field.strip()
            delimiter = delimiter.strip()
            
            if field in stored_fields:
                to_sub = stored_fields[field]
            else:
                raise ValueError()
            
            to_sub = [str(i) for i in to_sub]
            
            if delimiter == ',':
                result = ', '.join(to_sub)
            elif delimiter in '+-':
                temp   = f' {delimiter}'
                result = temp.join(to_sub)
            elif delimiter in ':*/':
                temp   = f' {delimiter} ' 
                result = temp.join(to_sub)
            else:
                result = delimiter.join(to_sub)
            
            return result
        
        substituted = re.sub('{{([^{}}]*)}}', repl, template, flags=re.S)
        
        return substituted
    
    def sub_v(self, template):
        pass
    
    def to_data(self):
        template    = self.template
        template    = self.interpolate(template)
        template    = self.sub_h(template)
        dun_strings = self.sub_v(template)
        
        result = dun_strings
        return result
        
e0 = Element('a: {{i, +}} * {{ii}}', **{'i': [0, 1, 2, '{}'], 'ii': ['x', 'y']})
r=e0.sub_h(e0.template)
print(r)   


