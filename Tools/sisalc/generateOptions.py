#**************************************************************************#
#* FILE   **************     generateOptions.py    ************************#
#**************************************************************************#
#* Author: Patrick Miller December 28 2000                                *#
#**************************************************************************#
#*  *#
#**************************************************************************#
from string import split,strip,join
from sys import stdin,argv
from time import asctime,localtime,time

class option:
    def __init__(self,name,alt,func,doc,param0,param1,param2,queue):
	self.name	= name
        if alt:
            self.alt	= '"%s"'%alt
        else:
            self.alt    = 0
	self.func	= func
	self.doc	= doc
        if param0:
            self.param0	= '&%s'%param0
        else:
            self.param0 = 0
        if param1:
            self.param1	= '&%s'%param1
        else:
            self.param1 = 0
        if param2:
            self.param2	= '&%s'%param2
        else:
            self.param2 = 0
        if queue:
            self.queue	= '&%s'%queue
        else:
            self.queue = 0
	return

    def __str__(self):
        return '    {"%(name)s",%(alt)s,%(func)s,"%(doc)s",\n     "%(doc)s",\n     %(param0)s,%(param1)s,%(param2)s,%(queue)s},\n'%self.__dict__
        

# Read file information
#text = open('sisalc.c').read()
text = stdin.read()

# Grab the definition section
sections = split(text,'/* OPTIONS */')
definitions = sections[1]

# Each line turns into an option command
newOptions = '\n    /* Autogenerated using %s on %s */\n'%(argv[0],asctime(localtime(time())))
for line in split(definitions,'\n'):
    if not strip(line): continue
    # We need to find a type, a c location, and the def.
    [definePart,commentPart] = split(line,';')

    # Remove the static specifier if present
    cPart = split(definePart)
    if cPart[0] == 'static': del cPart[0]

    # First word is the type, second is id
    type = cPart[0]; del cPart[0]
    cname = cPart[0]; del cPart[0]

    # If there is anything left, it is the defaulted value for some
    # forms
    if cPart:
        initialValue = cPart[1]
    else:
        initialValue = ''

    # In the comment, we split into flags, default indicator, and doc
    defn = split(commentPart)
    del defn[0] # Remove /*

    # Must have at least one option flag
    name = defn[0]; del defn[0]
    if '=' in name:
        [name,argument] = split(name,'=')
    else:
        argument = None
    
    # Second one is optional
    if defn[0][0] == '(':
        alt = None
    else:
        alt = defn[0]; del defn[0]
        if '=' in alt:
            [alt,argument] = split(alt,'=')
        else:
            argument = None

    # We should have a default value specifier
    if defn[0][0] == '(':
        identifier = defn[0]; del defn[0]
    else:
        identifier = '()'

    # The rest (up to the */) is a doc string
    doc = join(defn[:-1])
    
    if type == 'int':
        if identifier == '(true)':
            newOptions = newOptions + str( option(name,alt,'defaultTrue',doc,cname,None,None,None) )
        elif identifier == '(false)':
            newOptions = newOptions + str( option(name,alt,'defaultFalse',doc,cname,None,None,None) )
        else:
            newOptions = newOptions + str( option(name,alt,'defaultInitialized',doc+' '+str(initialValue),cname,None,None,None) )
    elif type == 'char*':
        if argument:
            newOptions = newOptions + str( option(name,alt,'fetchStringEqual',doc,None,None,cname,None) )
        else:
            newOptions = newOptions + str( option(name,alt,'fetchStringNext',doc,None,None,cname,None) )
    elif type == 'charStarQueue*':
        newOptions = newOptions + str( option(name,alt,'appendQueue',doc,None,None,None,cname) )
    else:
        raise RuntimeError
sections[3] = newOptions
print join(sections,'/* OPTIONS */')

    

