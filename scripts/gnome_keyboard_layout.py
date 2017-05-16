import subprocess
import sys

b = sys.argv[1]
layout1 = sys.argv[2]
layout2 = sys.argv[3]




def check_():
    out = subprocess.Popen("gsettings get org.gnome.desktop.input-sources sources",\
    shell=True,stdout=subprocess.PIPE).communicate()[0]
    out = out.decode("utf-8").strip()
    if layout1 in out and layout2 in out:
        out= eval(out)
        if out[0][1]==layout1 and out[1][1]==layout2:
            exit(0)
        else:
            exit(1)
        
    else:
        exit(1)
        

if b=="check":
    check_()
elif b== "add":
    subprocess.call("gsettings set org.gnome.desktop.input-sources sources \"[('xkb', '{}'), ('xkb', '{}')]\"".format(layout1,layout2),shell=True)

