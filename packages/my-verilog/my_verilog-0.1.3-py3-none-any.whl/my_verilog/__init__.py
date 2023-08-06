import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator


class port:
    def __init__(self, name:str, IO:str, lenth:int):
        self.name = name
        self.__not__ = "~" + name
        self.lenth = lenth
        if IO == 'out' and lenth == 1:
            self.item = vast.Ioport(vast.Output(self.name)) 
            
        elif IO == 'in' and lenth == 1:
            self.item = vast.Ioport(vast.Input(self.name))
            
        elif IO == 'out' and lenth != 1:
            width = vast.Width(vast.IntConst(str(lenth-1)),vast.IntConst('0'))
            self.item = vast.Ioport(vast.Output(self.name,width=width)) 

        elif IO == 'in' and lenth != 1:
            width = vast.Width(vast.IntConst(str(lenth-1)),vast.IntConst('0'))
            self.item = vast.Ioport(vast.Input(self.name,width=width))  
            
    def __add__(self, other):
        try:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)

    def __sub__(self, other):
        try:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
    def __and__(self, other):
        try:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
    def __invert__(self):
        return port('~' + self.name, 'out', self.lenth)
        
    def __or__(self, other):
        try:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
            
    def __mul__(self, other):
        try:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
 
    def __getitem__(self, key):
        try:
            dat_1,dat_2 = str(key)[6:-7].split(',')
            dat_2 = dat_2.replace(' ','')
            return port(self.name + '[' + dat_1 + ':' + dat_2 + ']', 'out', 1)
        except:
            return port(self.name + '[' + str(key) + ']', 'out', 1)
      
class reg:
    def __init__(self, name:str, lenth:int):
        self.name = name
        self.__not__ = "~" + name
        self.lenth = lenth
        if lenth == 1:
            self.item = vast.Reg(self.name) 

        else:
            width = vast.Width(vast.IntConst(str(lenth-1)),vast.IntConst('0'))
            self.item = vast.Reg(self.name,width=width) 
            
    def __add__(self, other):
        try:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)

    def __sub__(self, other):
        try:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
    def __and__(self, other):
        try:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
    def __invert__(self):
        return '~' + self.name
        
    def __or__(self, other):
        try:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
            
    def __mul__(self, other):
        try:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
 
    def __getitem__(self, key):
        try:
            dat_1,dat_2 = str(key)[6:-7].split(',')
            dat_2 = dat_2.replace(' ','')
            return port(self.name + '[' + dat_1 + ':' + dat_2 + ']', 'out', 1)
        except:
            return port(self.name + '[' + str(key) + ']', 'out', 1)

class wire:
    def __init__(self, name:str, lenth:int):
        self.name = name
        self.lenth = lenth
        if lenth == 1:
            self.item = vast.Wire(self.name) 

        else:
            width = vast.Width(vast.IntConst(str(lenth-1)),vast.IntConst('0'))
            self.item = vast.Wire(self.name,width=width)  
            
    def __add__(self, other):
        try:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' + ' + other.name, 'out', self.lenth)

    def __sub__(self, other):
        try:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' - ' + other.name, 'out', self.lenth)
    def __and__(self, other):
        try:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' & ' + other.name + ')', 'out', self.lenth)
    def __invert__(self):
        return '~' + self.name
        
    def __or__(self, other):
        try:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
        except:
            return port('(' + self.name + ' | ' + other.name + ')', 'out', self.lenth)
            
    def __mul__(self, other):
        try:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
        except:
            return port(self.name + ' * ' + other.name, 'out', self.lenth)
 
    def __getitem__(self, key):
        try:
            dat_1,dat_2 = str(key)[6:-7].split(',')
            dat_2 = dat_2.replace(' ','')
            return port(self.name + '[' + dat_1 + ':' + dat_2 + ']', 'out', 1)
        except:
            return port(self.name + '[' + str(key) + ']', 'out', 1)

        
class module:
    def  __init__(self, name, params, items, *ports):
        self.params = vast.Paramlist((params))                
        self.items = items  
        self.name = name
        items_ = []
        ports_ = []
        self.extern_count = 0
        self.extern_ = []
        try:
            for item in items:
                try:
                    if 'extern' in item:
                        extern = reg('extern'+str(self.extern_count), 1)
                        items_.append(extern.item)
                        self.extern_count = self.extern_count + 1
                        self.extern_.append(item.replace('extern_',''))
                except:
                    items_.append(item)
            for port in ports: 
                ports_.append(port.item)
        except:
            pass
        ports = vast.Portlist(ports_)
        self.ports = ports               
        self.ast = vast.ModuleDef(name,params,ports,items_)
    
    def visit(self):
        codegen = ASTCodeGenerator()
        code = codegen.visit(self.ast) 
        for i in range(self.extern_count):
            code = code.replace('reg extern'+str(i),self.extern_[i])
        return code

class always:
    def __init__(self, *sens):
        self.sens_1 = []
        self.sens_2 = []
        self.block = []
        for var in sens:
            self.sens_1.append(var)
            self.sens_2.append(vast.Sens(vast.Identifier(var.name), type='posedge'))
        self.senslist = vast.SensList(self.sens_2)

        self.item = vast.Always(self.senslist, None)
    
    def append(self, item):
        self.block.append(item)
        self.item = vast.Always(self.senslist, vast.Block(self.block))



def IF(stat, block_1, block_2):
        return vast.IfStatement(vast.Identifier(stat), vast.Block(block_1), vast.Block(block_2))

def assign(port, dat):
    try:
        return vast.Assign(vast.Identifier(port.name),vast.Identifier(dat.name))  
    except:
        try:
            return vast.Assign(vast.Identifier(str(port)),vast.Identifier(dat.name))  
        except:
            return vast.Assign(vast.Identifier(port.name),vast.IntConst(str(dat))) 


def extern_module(module,name,*ports):
    code = 'extern_' + module.name + ' ' + name + '('
    for port in ports:
        try:
            code = code + port.name
        except:
            code = code + str(port)
        code = code + ','
    code = code[0:-1] + ')'
    return code

def nonblock_assign(var, other):
    try:
        name = other.name
        block = vast.NonblockingSubstitution(
            vast.Lvalue(vast.Identifier(var.name)),
            vast.Rvalue(vast.Identifier(other.name)))
    
    except:
        try:
            block = vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier(var.name)),
                vast.Rvalue(vast.Identifier(str(other))))
        except:
            block = vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier(var.name)),
                vast.Rvalue(other))

    return block
        
def block_assign(var, other):
    try:
        name = other.name
        block = vast.BlockingSubstitution(
            vast.Lvalue(vast.Identifier(var.name)),
            vast.Rvalue(vast.Identifier(other.name)))
        
    except:
        try:
            block = vast.BlockingSubstitution(
                vast.Lvalue(vast.Identifier(var.name)),
                vast.Rvalue(vast.Identifier(str(other))))
        except:
            block = vast.BlockingSubstitution(
                vast.Lvalue(vast.Identifier(var.name)),
                vast.Rvalue(other))

    return block

def items_set(*items):
    items_ = []
    for item in items:
        try:
            item_ = item.item
            items_.append(item_)
        except:
            items_.append(item)
    return items_
    
def bus(*ports):
    name = ''
    name = name + '{'
    for port in ports:
        name = name + port.name + ','
    name = name.strip(',')
    name = name + '}'
    return name











    
    