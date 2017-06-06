import subprocess
import os
import sys

home = os.environ["HOME"]

b = sys.argv[1]
web = "http://download.netbeans.org/netbeans/8.2/final/bundles/netbeans-8.2-linux.sh"
name = "/tmp/netbeans-8.2-linux.sh"
location = "{}/netbeans-8.2".format(home)

def install_():
    if not os.path.isfile(name):
        check = subprocess.call("curl -o {}  {}".format(name,web),shell=True)
        if check != 0 :
            exit(1)

    check = subprocess.call("chmod 755 {}".format(name),shell=True)
    if check != 0 :
        exit(1)

    check = subprocess.call("{} --silent \"-J-Dnb-base.installation.location={}\" \"-J-Dnb-base.jdk.location=/usr/lib/jvm/java-openjdk\" ".format(name,location),shell=True)
    if check != 0 :
        exit(1)
    exit(0)


def remove_():
    check = subprocess.call("chmod 755 {}/uninstall.sh".format(location),shell=True)
    if check != 0 :
        exit(1)

    check = subprocess.call("{}/uninstall.sh --silent".format(location),shell=True)
    if check != 0 :
        exit(1)
    exit(0)

def check_():
    if os.path.isdir("{}/bin".format(location)):
        exit(0)
    else:
        exit(1)



if b=="check":
    check_()

elif b== "install":
    install_()

elif b== "remove":
    remove_()