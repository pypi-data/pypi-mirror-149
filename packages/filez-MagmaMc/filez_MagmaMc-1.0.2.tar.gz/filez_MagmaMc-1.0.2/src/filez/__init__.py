import requests as request
from tkinter import messagebox
import json
ID = "notset"
DEVELOPER = False

baseurl = 'http://magma-mc.net/Modules/filez/filez.php/?ID='+ID
 # ID = the folder name of where the files will be stored please make sure -
 # you have created the project at http://magma-mc.net/projects.php
def _colorit(rgb, text):
    r, g, b = rgb
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)
def _check():
    global baseurl
    if ID == "notset":
        errortext = """
               filez.ID, not set,
               please set and make sure that the project exists,
               http://magma-mc.net/projects.php
              """

        _senderror(errortext)
        return False
    else:
        baseurl = 'http://magma-mc.net/Modules/filez/filez.php/?ID='+ID
        return True
def _senderror(text):
    print(_colorit((255, 0, 0), text))
    messagebox.showerror("Error", text)

def fread(file):
    if _check():
        Rfile = json.loads(str(request.get(baseurl+"&filez=read&filename="+file).text))
        if Rfile == "notexist":
            _senderror("""
                     Please Make Sure That The Project/Folder Your Trying To Read From Exists,
                     http://magma-mc.net/projects.php
                    """)
            return False
        return Rfile
    else:
        raise
def scan(folder="/", ReadFile=False):
    if _check():
        Rfolder = str(request.get(str(baseurl)+"&filez=scan&filename="+str(folder)).text)
        
        if Rfolder == "notexist":
            _senderror("""
                        Please Make Sure That The Project/Folder Your Trying To Read From Exists,
                        http://magma-mc.net/projects.php
                       """)
            return False
        elif ReadFile:
            if DEVELOPER == True:
                eval('print(Rfolder, "BEFORE SNIP", "\\n")')
            Rfolder = list([i.strip() for i in Rfolder.split('"') if len(i.strip().strip(',').strip(']').strip('['))>0])
            if DEVELOPER == True:
                eval('print(Rfolder, "AFTER SNIP", "\\n")')

            files = {}
            for filename in Rfolder:
                if DEVELOPER == True:
                    eval('print(str(fread(folder+filename)), "STR.FREAD.FOLDER+FILENAME", "\\n")')
                file = json.loads(str(fread(folder+filename)))
                files.update({filename: (json.dumps(file))})
            return files
        return json.loads(Rfolder)
    else:
        raise
def fwrite(file, data, type="c"):
    if _check():
        try:
            # check if data is json
            temp = json.loads(data)
        except:
            _senderror("""Please Make Sure That The data your Trying To Save Is Json""")
            raise
        Wfile = str(request.post(baseurl+"&filez=write&content="+data+"&filename="+file+"&type="+type).text)
        if Wfile == "notexist":
            _senderror("""
                        Please Make Sure That The Project Your Trying To Write To Exists,
                        http://magma-mc.net/projects.php
                       """)
            return False
        return True
    else:
        raise
def send(file, data, key="null", type="="):
    if _check():
        try:
            File = fread(file)
            if key == "null":
                File = data
            else:
                if type == "=":
                    File[key] = data
                elif type == "+":
                    File[key] = int(File[key]) + int(data)
                elif type == "-":
                    File[key] = int(File[key]) - int(data)
            fwrite(file, json.dumps(File))
        except:
            pass
def delete(file):
    if _check():
        try:
            request.post(baseurl+"&filez=delete&filename="+file)
        except:
            pass

print("\nFilez Successfully Started.\n")