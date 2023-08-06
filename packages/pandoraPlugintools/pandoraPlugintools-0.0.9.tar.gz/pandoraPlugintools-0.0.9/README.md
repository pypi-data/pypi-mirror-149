# Python: module plugintools for PandoraFMS Developers

## Example


``` python
import pandoraPlugintools as pt

# Agent example
agent_data = {
        "agent_name"  : "agentname",
        "agent_alias" : "alias",
        "parent_agent_name" : "parent agent",
        "description" : "agente de pruebas",
        "version"     : "v756",
        "os_name"     : "Windows",
        "os_version"  : "10",
        "timestamp"   : datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
        "address"     : "127.0.0.1",
        "group"       : "Servers",
        "interval"    : "300",
}
modules = [{
        "name"      :   "test1",
        "type"      :   "generic_data",
        "value"     :   12344
},{
        "name"      :   "test2",
        "type"      :   "generic_data_string",
        "value"     :   "test"
}]

# test example translate macros
macros = {
    '_test_': 'Prueba',
    '_agent_name_':'pandora_agent'
}

string = '_test_ macro translator to agent _agent_name_'
print (translate_macros(macros, string))

# Print Agent
test_agent = pt.print_agent(agent_data, modules,data_dir='/tmp/', print_flag=0)

# Define tentacle conf 
tentacle_conf = {
    'address' : 'server.pandora.com',
    'port' : '41121',
    #'password' : 'pass'
}

# Send datafile file 
if test_agent[1] is not None:
    pt.tentacle_xml(test_agent[1], tentacle_conf, debug=0)

```


## Dependencies

* [json](json.html)  
* [os](os.html)  
* [psutil](psutil.html)  
* [sys](sys.html)  

## Classes

* [builtins.object](builtins.html#object)
* [Agent](plugintools.html#Agent)

   
class **Agent**([builtins.object](builtins.html#object))

 

Basic agent class. Requires agent parameters (config {dictionary})  
and module definition (modules\_def \[list of dictionaries\]) 

 

Methods defined here:  

**\_\_init\_\_**(self, config, modules\_def)

Initialize self.  See help(type(self)) for accurate signature.

* * *

Data descriptors defined here:  

**\_\_dict\_\_**

dictionary for instance variables (if defined)

**\_\_weakref\_\_**

list of weak references to the object (if defined)

   
## Functions

 
**auth\_call**(session, authtype, user, passw)

Authentication for url request. Requires request.sessions.Session() [object](builtins.html#object).  
   
Args:  
- session ([object](builtins.html#object)): request Session() [object](builtins.html#object).  
- authtype (str): 'ntlm', 'basic' or 'digest'.  
- user (str): auth user.  
- passw (str): auth password.

* * *

**call\_url**(url, authtype, user, passw, time\_out)

Call URL. Uses request module to get url contents.  
   
Args:  
- url (str): URL  
- authtype (str): ntlm', 'basic', 'digest'. Optional.  
- user (str): auth user. Optional.  
- passw (str): auth password. Optional.  

Returns:  
- str: call output
    
* * *

**debug\_dict**(func)

debug\_dict \[Decorator\]. Prints an indented json.  
Write @debug\_dict above any function that returns a dictionary or a list of dictionaries.

* * *

**now**(print\_flag=None, utimestamp=None)

Returns time in yyyy/mm/dd HH:MM:SS format by default. Use 1 as an argument  
to get epoch time (utimestamp)

* * *

**parse\_configuration**(file='/etc/pandora/pandora\_server.conf', separator=' ')

Parse configuration. Reads configuration file and stores its data as dict.
 
Args:
- file (str): configuration file path. Defaults to "/etc/pandora/pandora\_server.conf". 
- separator (str, optional): Separator for option and value. Defaults to " ".
 
Returns:
- dict: containing all keys and values from file.

* * *

**print\_agent**(agent, modules, data\_dir='/var/spool/pandora/data\_in/', log\_modules=None, print\_flag=None)

Prints agent XML. Requires agent conf (dict) and modules (list) as arguments.  
- Use print\_flag to show modules' XML in STDOUT.  
- Returns a tuple (xml, data\_file).

* * *

**print\_log\_module**(module, print\_flag=None)

Returns log module in XML format. Accepts only {dict}.  
   
- Only works with one module at a time: otherwise iteration is needed.  
- Module "value" field accepts str type.  
- Use not\_print\_flag to avoid printing the XML (only populates variables).

* * *

**print\_module**(module, print\_flag=None)

Returns module in XML format. Accepts only {dict}.  
   
- Only works with one module at a time: otherwise iteration is needed.  
- Module "value" field accepts str type or \[list\] for datalists.  
- Use print\_flag to show modules' XML in STDOUT.

* * *

**tentacle\_xml**(file, tentacle\_ops, tentacle\_path='', debug=0)

Sends file using tentacle protocol  
   
- Only works with one file at time.  
- file variable needs full file path.  
- tentacle\_opts should be a dict with tentacle options (address \[password\] \[port\]).  
- tentacle\_path allows to define a custom path for tentacle client in case is not in sys path).  
- if debug is enabled, the data file will not be removed after being sent.  
   
Returns 0 for OK and 1 for errors.

* * *

**write\_xml**(xml, agent\_name, data\_dir='/var/spool/pandora/data\_in/')

Creates a agent .data file in the specified data_dir folder.

Args:
- xml (str): XML string to be written in the file.
- agent_name (str): agent name for the xml and file name.
- data_dir (str): folder in which the file will be created.

* * *

**translate\_macros**(macro\_dic: dict, data: str)

Expects a macro dictionary key:value (macro\_name:macro\_value) 
and a string to replace macro. \n
It will replace the macro_name for the macro_value in any string.

* * *

**parse\_csv_file**(file, separator=';', count\_parameters=None, debug=False) -> list:
    
Parse csv configuration. Reads configuration file and stores its data in an array.

Args:
- file (str): configuration csv file path. \n
- separator (str, optional): Separator for option and value. Defaults to ";".
- coun_parameters (int): min number of parameters each line shold have. Default None
- debug: print errors on lines

Returns:
- List: containing a list for each csv line.
* * *