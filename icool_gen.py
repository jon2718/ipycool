import json
from pprint import pprint

title_def='Default ICOOL'
cont_def={'npart': '10000', 'bgen': '.true'}
bmt_def={}

def parse_icool_lang():
    with open('icool_commands.json') as data_file:
        data=json.load(data_file)
        #pprint(data)
        ic=get_ICOOL_COMMANDS(data)
        reg=get_REGION_COMMANDS(data)
        #pprint(ic)
        return ic
        
def get_ICOOL_COMMANDS(icool_dict):
    return icool_dict['ICOOL_COMMANDS']
    
def get_REGION_COMMANDS(icool_dict):
    return icool_dict['REGION_COMMANDS']

def get_NAMELIST(namelist):
    ic=get_icool_commands()
    return ic[namelist]

def get_CONT_COMMANDS():
    ic=get_icool_commands()
    return ic['CONT']

def CONT_COMMAND(command):
    cc=get_CONT_COMMANDS()
    return cc[command]

def help(command_spec):
    return command_spec[3]

def get_IC_command_spec(command):
    ic=parse_icool_lang()
    for key in ic:
        if command in ic[key]:
            return (key, ic[key][command])

def help(command):
    cs=get_IC_command_spec(command)
    if cs:
        print command,"is in namespec:", cs[0]
        print "Help for", command, ":", cs[1][0]

def list_all_commands():
    ic=parse_icool_lang()
    for key in ic:
        print key, ':\n'
        for command in ic[key]:
            print command
        print '\n'
        
def list_all_commands_verbose():
    ic=parse_icool_lang()
    for key in ic:
        print key, ':\n'
        for command in ic[key]:
            print command, ic[key][command]
        print '\n'

    

def for001_gen(path, title=title_def, cont_dict=cont_def, bmt_dict=bmt_def):
    file_and_directory=path+'/'+'for001.dat'
    f=open(file_and_directory, 'w')
    gen_title(f, title)
    cr(f)
    gen_cont(f, cont_dict)
    cr(f)
    gen_bmt(f, bmt_dict)
    f.close()
    
def gen_title(f, program_title):
    f.write(program_title)
    gen_cr(f)
    
def gen_cont(f, cont_dict):
    f.write('&cont')
    gen_sp(f)
    f.write('npart=')
    f.write(cont_dict['npart'])
    gen_sp(f)
    f.write('bgen=')
    f.write(cont_dict['bgen'])
    gen_cr(f)
    
def gen_bmt(f, bmt_dict):
    f.write('&bmt')
    gen_cr(f)
    
def gen_cr(f):
    f.write('\n')

def gen_sp(f):
    f.write(' ')
    
    


    