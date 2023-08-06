###################################################################################
#
# Pandora FMS Plugin functions library for Python
#
#  (c)  A. Kevin Rojas <kevin.rojas@pandorafms.com>
#       Rafael Ameijeiras <rafael.ameijeiras@pandorafms.com>
# 
###################################################################################
# -*- coding: utf-8 -*-
## IMPORTS

import json 
import sys
import os
from datetime import datetime
from subprocess import *
from requests_ntlm import HttpNtlmAuth
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests.sessions import Session

#########################################################################################
# Agent class
#########################################################################################

class Agent:
    """Basic agent class. Requires agent parameters (config {dictionary})
    and module definition (modules_def [list of dictionaries]) """
    def __init__(self, config, modules_def):
        self.config = config
        self.modules_def = modules_def


#########################################################################################
# OS check
#########################################################################################

POSIX = os.name == "posix"
WINDOWS = os.name == "nt"
LINUX = sys.platform.startswith("linux")
MACOS = sys.platform.startswith("darwin")
OSX = MACOS  # deprecated alias
FREEBSD = sys.platform.startswith("freebsd")
OPENBSD = sys.platform.startswith("openbsd")
NETBSD = sys.platform.startswith("netbsd")
BSD = FREEBSD or OPENBSD or NETBSD
SUNOS = sys.platform.startswith(("sunos", "solaris"))
AIX = sys.platform.startswith("aix")

#########################################################################################
# Timedate class
#########################################################################################

#class Timedate:
def now(print_flag=None, utimestamp=None):
    """Returns time in yyyy/mm/dd HH:MM:SS format by default. Use 1 as an argument
    to get epoch time (utimestamp)"""
    if utimestamp:
        time = datetime.timestamp(datetime.today())
    else:
        time = datetime.today().strftime('%Y/%m/%d %H:%M:%S')
    if print_flag:
        print (time)
    else:
        return (time)


#########################################################################################
# Debug_dict: prints dictionary in formatted json string.
#########################################################################################

class debug_dict:
    def __init__ (self, jsontxt):
        self.debug_json = json.dumps (jsontxt, indent=4)
        print (self.debug_json)


#########################################################################################
# version: Defines actual version of Pandora Server
#########################################################################################




#########################################################################################
# Returns current library version
#########################################################################################




#########################################################################################
# Check version compatibility
#########################################################################################



#########################################################################################
# Convert CSV string to hash
#########################################################################################



#########################################################################################
# Get current time (milis)
#########################################################################################

#########################################################################################
# print_agent
#########################################################################################
def print_agent(agent, modules, data_dir="/var/spool/pandora/data_in/", log_modules= None, print_flag = None):
    """Prints agent XML. Requires agent conf (dict) and modules (list) as arguments.
    - Use print_flag to show modules' XML in STDOUT.
    - Returns a tuple (xml, data_file).
    """
    data_file=None

    header = "<?xml version='1.0' encoding='UTF-8'?>\n"
    header += "<agent_data"
    for dato in agent:
        header += " " + str(dato) + "='" + str(agent[dato]) + "'"
    header += ">\n"
    xml = header
    if modules :
        for module in modules:
            modules_xml = print_module(module)
            xml += str(modules_xml)
    if log_modules :
        for log_module in log_modules:
            modules_xml = print_log_module(log_module)
            xml += str(modules_xml)
    xml += "</agent_data>"
    if not print_flag:
        data_file = write_xml(xml, agent["agent_name"], data_dir)
    else:
        print(xml)
    
    return (xml,data_file)

#########################################################################################
# print_module
#########################################################################################
def print_module(module, print_flag=None):
    """Returns module in XML format. Accepts only {dict}.\n
    - Only works with one module at a time: otherwise iteration is needed.
    - Module "value" field accepts str type or [list] for datalists.
    - Use print_flag to show modules' XML in STDOUT.
    """
    data = dict(module)
    module_xml = ("<module>\n"
                  "\t<name><![CDATA[" + str(data["name"]) + "]]></name>\n"
                  "\t<type>" + str(data["type"]) + "</type>\n"
                  )
    
    if type(data["type"]) is not str and "string" not in data["type"]: #### Strip spaces if module not generic_data_string
        data["value"] = data["value"].strip()
    if isinstance(data["value"], list): # Checks if value is a list
        module_xml += "\t<datalist>\n"
        for value in data["value"]:
            if type(value) is dict and "value" in value:
                module_xml += "\t<data>\n"
                module_xml += "\t\t<value><![CDATA[" + str(value["value"]) + "]]></value>\n"
                if "timestamp" in value:
                    module_xml += "\t\t<timestamp><![CDATA[" + str(value["timestamp"]) + "]]></timestamp>\n"
            module_xml += "\t</data>\n"
        module_xml += "\t</datalist>\n"
    else:
        module_xml += "\t<data><![CDATA[" + str(data["value"]) + "]]></data>\n"
    if "desc" in data:
        module_xml += "\t<description><![CDATA[" + str(data["desc"]) + "]]></description>\n"
    if "unit" in data:
        module_xml += "\t<unit><![CDATA[" + str(data["unit"]) + "]]></unit>\n"
    if "interval" in data:
        module_xml += "\t<module_interval><![CDATA[" + str(data["interval"]) + "]]></module_interval>\n"
    if "tags" in data:
        module_xml += "\t<tags>" + str(data["tags"]) + "</tags>\n"
    if "module_group" in data:
        module_xml += "\t<module_group>" + str(data["module_group"]) + "</module_group>\n"
    if "module_parent" in data:
        module_xml += "\t<module_parent>" + str(data["module_parent"]) + "</module_parent>\n"
    if "min_warning" in data:
        module_xml += "\t<min_warning><![CDATA[" + str(data["min_warning"]) + "]]></min_warning>\n"
    if "min_warning_forced" in data:
        module_xml += "\t<min_warning_forced><![CDATA[" + str(data["min_warning_forced"]) + "]]></min_warning_forced>\n"
    if "max_warning" in data:
        module_xml += "\t<max_warning><![CDATA[" + str(data["max_warning"]) + "]]></max_warning>\n"
    if "max_warning_forced" in data:
        module_xml += "\t<max_warning_forced><![CDATA[" + str(data["max_warning_forced"]) + "]]></max_warning_forced>\n"
    if "min_critical" in data:
        module_xml += "\t<min_critical><![CDATA[" + str(data["min_critical"]) + "]]></min_critical>\n"
    if "min_critical_forced" in data:
        module_xml += "\t<min_critical_forced><![CDATA[" + str(data["min_critical_forced"]) + "]]></min_critical_forced>\n"
    if "max_critical" in data:
        module_xml += "\t<max_critical><![CDATA[" + str(data["max_critical"]) + "]]></max_critical>\n"
    if "max_critical_forced" in data:
        module_xml += "\t<max_critical_forced><![CDATA[" + str(data["max_critical_forced"]) + "]]></max_critical_forced>\n"
    if "str_warning" in data:
        module_xml += "\t<str_warning><![CDATA[" + str(data["str_warning"]) + "]]></str_warning>\n"
    if "str_warning_forced" in data:
        module_xml += "\t<str_warning_forced><![CDATA[" + str(data["str_warning_forced"]) + "]]></str_warning_forced>\n"
    if "str_critical" in data:
        module_xml += "\t<str_critical><![CDATA[" + str(data["str_critical"]) + "]]></str_critical>\n"
    if "str_critical_forced" in data:
        module_xml += "\t<str_critical_forced><![CDATA[" + str(data["str_critical_forced"]) + "]]></str_critical_forced>\n"
    if "critical_inverse" in data:
        module_xml += "\t<critical_inverse><![CDATA[" + str(data["critical_inverse"]) + "]]></critical_inverse>\n"
    if "warning_inverse" in data:
        module_xml += "\t<warning_inverse><![CDATA[" + str(data["warning_inverse"]) + "]]></warning_inverse>\n"
    if "max" in data:
        module_xml += "\t<max><![CDATA[" + str(data["max"]) + "]]></max>\n"
    if "min" in data:
        module_xml += "\t<min><![CDATA[" + str(data["min"]) + "]]></min>\n"
    if "post_process" in data:
        module_xml += "\t<post_process><![CDATA[" + str(data["post_process"]) + "]]></post_process>\n"
    if "disabled" in data:
        module_xml += "\t<disabled><![CDATA[" + str(data["disabled"]) + "]]></disabled>\n"
    if "min_ff_event" in data:
        module_xml += "\t<min_ff_event><![CDATA[" + str(data["min_ff_event"]) + "]]></min_ff_event>\n"
    if "status" in data:
        module_xml += "\t<status><![CDATA[" + str(data["status"]) + "]]></status>\n"
    if "timestamp" in data:
        module_xml += "\t<timestamp><![CDATA[" + str(data["timestamp"]) + "]]></timestamp>\n"
    if "custom_id" in data:
        module_xml += "\t<custom_id><![CDATA[" + str(data["custom_id"]) + "]]></custom_id>\n"
    if "critical_instructions" in data:
        module_xml += "\t<critical_instructions><![CDATA[" + str(data["critical_instructions"]) + "]]></critical_instructions>\n"
    if "warning_instructions" in data:
        module_xml += "\t<warning_instructions><![CDATA[" + str(data["warning_instructions"]) + "]]></warning_instructions>\n"
    if "unknown_instructions" in data:
        module_xml += "\t<unknown_instructions><![CDATA[" + str(data["unknown_instructions"]) + "]]></unknown_instructions>\n"
    if "quiet" in data:
        module_xml += "\t<quiet><![CDATA[" + str(data["quiet"]) + "]]></quiet>\n"
    if "module_ff_interval" in data:
        module_xml += "\t<module_ff_interval><![CDATA[" + str(data["module_ff_interval"]) + "]]></module_ff_interval>\n"
    if "crontab" in data:
        module_xml += "\t<crontab><![CDATA[" + str(data["crontab"]) + "]]></crontab>\n"
    if "min_ff_event_normal" in data:
        module_xml += "\t<min_ff_event_normal><![CDATA[" + str(data["min_ff_event_normal"]) + "]]></min_ff_event_normal>\n"
    if "min_ff_event_warning" in data:
        module_xml += "\t<min_ff_event_warning><![CDATA[" + str(data["min_ff_event_warning"]) + "]]></min_ff_event_warning>\n"
    if "min_ff_event_critical" in data:
        module_xml += "\t<min_ff_event_critical><![CDATA[" + str(data["min_ff_event_critical"]) + "]]></min_ff_event_critical>\n"
    if "ff_type" in data:
        module_xml += "\t<ff_type><![CDATA[" + str(data["ff_type"]) + "]]></ff_type>\n"
    if "ff_timeout" in data:
        module_xml += "\t<ff_timeout><![CDATA[" + str(data["ff_timeout"]) + "]]></ff_timeout>\n"
    if "each_ff" in data:
        module_xml += "\t<each_ff><![CDATA[" + str(data["each_ff"]) + "]]></each_ff>\n"
    if "module_parent_unlink" in data:
        module_xml += "\t<module_parent_unlink><![CDATA[" + str(data["parent_unlink"]) + "]]></module_parent_unlink>\n"
    if "global_alerts" in data:
        for alert in data["alert"]:
            module_xml += "\t<alert_template><![CDATA[" + alert + "]]></alert_template>\n"
    module_xml += "</module>\n"

    if print_flag:
        print (module_xml)

    return (module_xml)
#########################################################################################
# print_module
#########################################################################################

def print_log_module(module, print_flag = None):
    """Returns log module in XML format. Accepts only {dict}.\n
    - Only works with one module at a time: otherwise iteration is needed.
    - Module "value" field accepts str type.
    - Use not_print_flag to avoid printing the XML (only populates variables).
    """
    data = dict(module)
    module_xml = ("<log_module>\n"
                  "\t<source><![CDATA[" + str(data["source"]) + "]]></source>\n"
                  "\t<data>\"" + str(data["value"]) + "\"</data>\n"
                  )
    
    module_xml += "</log_module>\n"

    if print_flag:
        print (module_xml)

    return (module_xml)


#########################################################################################
# write_xml
#########################################################################################

def write_xml(xml, agent_name, data_dir="/var/spool/pandora/data_in/"):
    """Creates a agent .data file in the specified data_dir folder\n
    Args:
    - xml (str): XML string to be written in the file.
    - agent_name (str): agent name for the xml and file name.
    - data_dir (str): folder in which the file will be created."""
    Utime = datetime.now().strftime('%s')
    data_file = "%s/%s.%s.data" %(str(data_dir),agent_name,str(Utime))
    try:
        with open(data_file, 'x') as data:
            data.write(xml)
    except OSError as o:
        sys.exit(f"ERROR - Could not write file: {o}, please check directory permissions")
    except Exception as e:
        sys.exit(f"{type(e).__name__}: {e}")
    return (data_file)


#########################################################################################
# tentacle_xml
#########################################################################################
def tentacle_xml(file, tentacle_ops,tentacle_path='', debug=0):
    """Sends file using tentacle protocol\n
    - Only works with one file at time.
    - file variable needs full file path.
    - tentacle_opts should be a dict with tentacle options (address [password] [port]).
    - tentacle_path allows to define a custom path for tentacle client in case is not in sys path).
    - if debug is enabled, the data file will not be removed after being sent.

    Returns 0 for OK and 1 for errors.
    """

    if file is None :
        sys.stderr.write("Tentacle error: file path is required.")
    else :
        data_file = file
    
    if tentacle_ops['address'] is None :
        sys.stderr.write("Tentacle error: No address defined")
        return 1
    
    try :
        with open(data_file, 'r') as data:
            data.read()
        data.close()
    except Exception as e :
        sys.stderr.write(f"Tentacle error: {type(e).__name__} {e}")
        return 1

    tentacle_cmd = f"{tentacle_path}tentacle_client -v -a {tentacle_ops['address']} "
    if "port" in tentacle_ops:
        tentacle_cmd += f"-p {tentacle_ops['port']} "
    if "password" in tentacle_ops:
        tentacle_cmd += f"-x {tentacle_ops['password']} "
    tentacle_cmd += f"{data_file} "

    tentacle_exe=Popen(tentacle_cmd, stdout=PIPE, shell=True)
    rc=tentacle_exe.wait()

    if rc != 0 :
        sys.stderr.write("Tentacle error")
        return 1
    elif debug == 0 : 
        os.remove(file)
 
    return 0

#########################################################################################
## Plugin devolution in case of error
#########################################################################################



#########################################################################################
# Arguments parser
#########################################################################################



#########################################################################################
# Configuration file parser
#########################################################################################

def parse_configuration(file="/etc/pandora/pandora_server.conf", separator=" "):
    """
    Parse configuration. Reads configuration file and stores its data as dict.

    Args:
    - file (str): configuration file path. Defaults to "/etc/pandora/pandora_server.conf". \n
    - separator (str, optional): Separator for option and value. Defaults to " ".

    Returns:
    - dict: containing all keys and values from file.
    """
    config = {}
    try:
        with open (file, "r") as conf:
            lines = conf.read().splitlines()
            for line in lines:
                if line.startswith("#") or len(line) < 1 :
                    pass
                else:
                    option, value = line.strip().split(separator)
                    config[option.strip()] = value.strip()

        return config
    except Exception as e:
        print (f"{type(e).__name__}: {e}")

#########################################################################################
# csv file parser
#########################################################################################
def parse_csv_file(file, separator=';', count_parameters=None, debug=False) -> list:
    """
    Parse csv configuration. Reads configuration file and stores its data in an array.

    Args:
    - file (str): configuration csv file path. \n
    - separator (str, optional): Separator for option and value. Defaults to ";".
    - coun_parameters (int): min number of parameters each line shold have. Default None
    - debug: print errors on lines

    Returns:
    - List: containing a list for of values for each csv line.
    """
    csv_arr = []
    try:
        with open (file, "r") as conf:
            lines = conf.read().splitlines()
            for line in lines:
                if line.startswith("#") or len(line) < 1 :
                    continue
                else:
                    value = line.strip().split(separator)
                    if count_parameters is None or len(value) >= count_parameters:
                        csv_arr.append(value)
                    elif debug==True: 
                        print(f'Csv line: {line} doesnt match minimun parameter defined: {count_parameters}',file=sys.stderr)

        return csv_arr
    except Exception as e:
        print (f"{type(e).__name__}: {e}")
        return 1

#########################################################################################
# URL calls
#########################################################################################

def auth_call(session, authtype, user, passw):
    """Authentication for url request. Requires request.sessions.Session() object.

    Args:
    - session (object): request Session() object.
    - authtype (str): 'ntlm', 'basic' or 'digest'.
    - user (str): auth user.
    - passw (str): auth password.
    """
    if authtype == 'ntlm':
        session.auth = HttpNtlmAuth(user, passw)
    elif authtype == 'basic':
        session.auth = HTTPBasicAuth(user, passw)
    elif authtype == 'digest':
        session.auth = HTTPDigestAuth(user, passw)

def call_url(url, authtype, user, passw, time_out):
    """Call URL. Uses request module to get url contents.

    Args:
    - url (str): URL
    - authtype (str): ntlm', 'basic', 'digest'. Optional.
    - user (str): auth user. Optional.
    - passw (str): auth password. Optional.

    Returns:
    - str: call output
    """
    # using with so we make sure the session is closed even when exceptions are encountered
    with Session() as session:
        if authtype != None:
            auth_call(session, authtype, user, passw)
        try:
            output = session.get(url, timeout=time_out, verify=False)
        except ValueError:
            exit("Error: URL format not valid (example http://myserver/page.php)")
        except Exception as e:
            exit(f"{type(e).__name__}:\t{str(e)}")
        else:
            return output

#########################################################################################
# SNMP walk value (sacarlo del snmpwalk.py)
#########################################################################################



#########################################################################################
# SNMP get value (sacarlo del snmpwalk.py)
#########################################################################################



#########################################################################################
# Translate macro
#########################################################################################
def translate_macros(macro_dic: dict, data: str)  -> str:
    """Expects a macro dictionary key:value (macro_name:macro_value) 
    and a string to replace macro. \n
    It will replace the macro_name for the macro_value in any string.
    """
    for macro_name, macro_value in macro_dic.items():
        data = data.replace(macro_name, macro_value) 

    return data

#########################################################################################
# TEST
#########################################################################################

if __name__ == '__main__':
    # ejemplo agente
    agent_data = {
           "agent_name"  : "agentname",
           "agent_alias" : "alias",
           "parent_agent_name" : "parent agent",
           "description" : "agente de pruebas",
           "version"     : "v756",
           "os_name"     : "Windows",
           "os_version"  : "10",
           "timestamp"   : datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
           #"utimestamp"  : int(datetime.timestamp(datetime.today())),
           "address"     : "127.0.0.1",
           "group"       : "Servers",
           "interval"    : "300",
    }
    modulos = [{
            "name"      :   "test1",
            "type"      :   "generic_data",
            "value"     :   12344
    },{
            "name"      :   "test2",
            "type"      :   "generic_data_string",
            "value"     :   "test"
    }]
    
    # Print Agent
    test_agent = print_agent(agent_data, modulos,data_dir='/tmp/', print_flag=0)
    
    # Define tentacle conf 
    tentacle_conf = {
        'address' : 'server.pandora.com',
        'port' : '41121',
        #'password' : 'pass'
    }
    
    # Send datafile file 
    if test_agent[1] is not None:
        tentacle_xml(test_agent[1], tentacle_conf, debug=0)

    # test example translate macros
    macros = {
        '_test_': 'Prueba',
        '_agent_name_':'pandora_agent'
    }

    string = '_test_ macro translator to agente _agent_name_'
    print (translate_macros(macros, string))