import sys,subprocess,os

f = os.path.expanduser(sys.argv[1])
b = sys.argv[2]
if len(sys.argv)>=4:
    pkexec = sys.argv[3]
    print (pkexec)


def check_():
    with open("/etc/dnf/dnf.conf","r") as myfile:
        for line in myfile.readlines():
            if line.strip().startswith("keepcache"):
                l = line.split("=")
                ll = l[1].strip()
                if ll=="1" or ll=="True" or ll == "true":
                    exit (0)
                else:
                    exit (1)
    exit(1)

            

def add_keepcache():
    result= ""
    with open("/etc/dnf/dnf.conf","r") as myfile:
        for line in myfile.readlines():
            line = line.strip()
            if line.startswith("keepcache"):
                continue
            result+=line+"\n"
    result+="keepcache = 1\n"
    with open(f,"w") as myfile:
        myfile.write(result)
    subprocess.call("{} cp {} /etc/dnf/dnf.conf".format(pkexec,f),shell=True)

def remove_keepcache():
    result= ""
    with open("/etc/dnf/dnf.conf","r") as myfile:
        for line in myfile.readlines():
            line = line.strip()
            if line.startswith("keepcache"):
                continue
            result+=line+"\n"
    result+="keepcache = 0\n"
    with open(f,"w") as myfile:
        myfile.write(result)
    subprocess.call("{} cp {} /etc/dnf/dnf.conf".format(pkexec,f),shell=True)


if b== "check":
    check_()
elif b == "add":
    add_keepcache()
elif b == "remove":
    remove_keepcache()