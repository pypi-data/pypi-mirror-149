r"""A python module for administration tools
    """
  
import subprocess 
import sys
import os

def multipleReplace(text, wordDict):
    """
    take a text and replace words that match the key in a dictionary
    with the associated value, return the changed text
    """
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

def runprocess(cmd,returnstdout=True):
    print("Running %s" % cmd)
    if (returnstdout):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = process.communicate()[0]
        output = output.split('\n')
        return output
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        while 1:
            output = process.stdout.readline()[:-1]
            print(output)
            if output == '': return None



def docx_replace(old_file, wordDict, new_file):
    import zipfile
    import shutil
    # This allows the old and new file to be identical
    temporary_file = "tmp.docx"
    shutil.copyfile(old_file,temporary_file)    
    zin  = zipfile.ZipFile (temporary_file, 'r')
    zout = zipfile.ZipFile (new_file,       'w')

    for item in zin.infolist():
        buffer = zin.read(item.filename)

        if (item.filename == 'word/document.xml'):
            res = buffer.decode("utf-8")
            for keyword in wordDict:
                res = res.replace(keyword,wordDict[keyword])
            buffer = res.encode("utf-8")

        if (item.filename == 'word/header1.xml'):
            res = buffer.decode("utf-8")
            for keyword in wordDict:
                res = res.replace(keyword,wordDict[keyword])
            buffer = res.encode("utf-8")

        zout.writestr(item, buffer)

    zout.close()
    zin.close()



def sed(infile, wordDict, outfile, delimiter=';'):
    """
    Replace text in infile and replace words that match the 
    key in a dictionary with the associated value.
    Output new text to outfile. 
    Operation similar to 'seds' basic string operation
    """
    text = delimiter.join(open(infile,'r').readlines())
    for key in wordDict:
        text = text.replace(key, str(wordDict[key]))
    open(outfile,'w').writelines(text.split(delimiter))

def ssh_connect(host,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh.connect('%s.marintek.sintef.no' % host,
                username='tken', password=password)
    return ssh


def find_occurrences(string, lines, specificOccurrenceWanted = False):
    try:
        occurrences = \
            [loc for loc, line in enumerate(lines)  \
                 if string in line]
        if specificOccurrenceWanted:
            return occurrences[specificOccurrenceWanted-1]
        else: return occurrences

    except Exception:
        print("Can't find %d occurrence %s in file lines" % \
            (specificOccurrenceWanted, string))
        sys.exit(-1)


def timer(func):
    """
        This function shows the execution time of 
        the function object passed
    """
    from time import time
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def getpassword():
    """ Script requires a password """
    text = "Enter password to run script"
    try:
        return getpass.unix_getpass(prompt=text)
    except:
        try:
            return getpass.win_getpass(prompt=text)
        except:
            sys.stderr.write('Error in getting password')
            sys.stderr.flush()
            sys.exit(-1)


def formatwrite(f, L,width=11,usef=True):  
    #print L
    f.write('%-1s' % L[0])
    for listitem in L[1:]:
        if isinstance(listitem,str):   format ="%"+ "-%ds" % width
        if isinstance(listitem,int):   format ="%"+ "-%dd" % width
        if isinstance(listitem,float): 
            if (usef): format ="%"+ "-%d.3f" % width
            else:      format ="%"+ "-%d.3e" % width
        f.write(format % listitem)
    f.write('\n')

   
def ntasks(process):
    """ -1 is required as to remove the empty line"""
    output = runprocess('tasklist /v | findstr %s' % process)
    return len(output)-1
    

def winhold(process,limit):
    """ -1 is required as to remove the empty line"""
    from time import sleep
    print(ntasks(process))
    while ntasks(process) > limit: sleep(6)


def ntasks_linux():
    """ -1 is required as to remove the empty line"""
    output = runprocess('qstat -r -u tike')
    return max(0,len(output)-1 -5)


def linuxhold(limit):
    """
    """
    from time import sleep
    import os
    while ntasks_linux() > limit: sleep(6)


def mkdir(folder):
    try: os.mkdir(folder)
    except: pass

    
    
