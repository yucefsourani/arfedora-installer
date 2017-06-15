from os.path import isfile
from sys import argv
from subprocess import Popen,call,PIPE,check_output
import os

b = argv[1]
if b == "setup":
    pkexec = argv[2]

try:
    default_terminal_profile=eval(check_output("gsettings get org.gnome.Terminal.ProfilesList list",shell=True).decode("utf-8").strip())[0]
except:
    exit(1)

def setup_():
    if not isfile("/usr/bin/bicon"):
        check = call("{} dnf install bicon -y --best".format(pkexec),shell=True)
        if check!=0:
            exit(1)

    check = call("gsettings set   org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ use-custom-command true".format(default_terminal_profile),shell=True)
    print (check)
    if check!=0:
        exit(1)

    check = call("gsettings set   org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ custom-command 'bicon'".format(default_terminal_profile),shell=True)
    print (check)
    if check!=0:
        exit(1)
    exit(0)

def remove_():
    check = call("gsettings set   org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ use-custom-command false".format(default_terminal_profile),shell=True)
    if check!=0:
        exit(1)

    check = call("gsettings reset   org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ custom-command".format(default_terminal_profile),shell=True)
    print (check)
    if check!=0:
        exit(1)
    exit(0)

def check_():
    if not isfile("/usr/bin/bicon"):
        exit(1)
    

    check = call("gsettings get  org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ use-custom-command |grep true".format(default_terminal_profile),\
    shell=True)
    print ("check1 %s"%check)
    if check!=0:
        exit(1)

    check = call("gsettings get   org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:{}/ custom-command |grep bicon".format(default_terminal_profile),\
    shell=True)
    print ("check2 %s"%check)
    if check!=0:
        exit(1)
    print ("check sucess")
    exit(0)

if b== "check":
    check_()
elif b == "setup":
    setup_()
elif b == "remove":
    remove_()