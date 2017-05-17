from os.path import isdir
from sys import argv
from subprocess import call

distro_family = argv[1]
distro_efi_folder_name = argv[2]
if argv[3] == "grub":
    grub_mkconfig = "grub-mkconfig"
    grub = "grub"
else:
    grub_mkconfig = "grub2-mkconfig"
    grub = "grub2"
pkexec = argv[4]

if distro_family == "fedora":
    if isdir("/boot/efi/EFI/{}".format(distro_efi_folder_name)):
        call("{} {} -o /boot/efi/EFI/{}/grub.cfg".format(pkexec,grub_mkconfig,distro_efi_folder_name),shell=True)
    else:
        call("{} {} -o /boot/{}/grub.cfg".format(pkexec,grub_mkconfig,grub),shell=True)
else:
    call("{} {} -o /boot/{}/grub.cfg".format(pkexec,grub_mkconfig,grub),shell=True)

