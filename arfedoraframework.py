# -*- coding: utf-8 -*-
#
#  arfedoraframework.py
#  
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  http://www.arfedora.blogspot.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GLib,GdkPixbuf,Gdk
import os
import time
import subprocess
import threading
import multiprocessing



class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent):
        Gtk.MessageDialog.__init__(self,parent=parent,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL,message_format=msg)
        
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            return True
        else:
            self.destroy()
            return False


class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message)
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()
                    


class TF(threading.Thread):
    def __init__(self,fun,check_if_sucess,data=None):
        threading.Thread.__init__(self)
        self.fun = fun
        self.check_if_sucess = check_if_sucess
        self.data = data
    
    def run(self):
        if self.data == None:
            try :
                check = self.fun()
            except:
                self.check_if_sucess.value = 4
                return
        else:
            try:
                check = self.fun(*self.data)
            except:
                self.check_if_sucess.value = 4
                return

        if check or check==None:
            self.check_if_sucess.value = 3
        else:
            self.check_if_sucess.value = 4



class TC(threading.Thread):
    def __init__(self,command,check_if_sucess,run_from_file,file_to_run,exec__,time_out=0.5):
        threading.Thread.__init__(self)
        self.command = command
        self.check_if_sucess = check_if_sucess
        self.time_out = time_out
        self.run_from_file= run_from_file
        self.file_to_run = file_to_run
        self.exec__ = exec__

    def run(self):
        command=[]
        if not self.run_from_file:
            for i in self.command:
                try:
                    check = subprocess.call(i,shell=True)
                    time.sleep(self.time_out)
                except:
                    self.check_if_sucess.value = 4
                    return
            if check == 0:
                self.check_if_sucess.value = 3
            else:
                self.check_if_sucess.value = 4
        else:
            try:
                to_run = "set -e\n"
                for c in self.command:
                    if isinstance(c,list) and c[0]=="norepr" :
                        to_run+=r"""{}""".format(c[1])+"\n"
                    else:
                        to_run+=repr(r"""{}""".format(c))[1:-1]+"\n"
                        
                with open(self.file_to_run,"w") as myfile:
                    myfile.write(to_run)
            except:
                self.check_if_sucess.value = 4
                return


            try:
                if os.getuid() != 0:
                    check = subprocess.call(self.exec__+" bash "+self.file_to_run,shell=True)
                else:
                    check = subprocess.call("bash "+self.file_to_run,shell=True)
            except:
                self.check_if_sucess.value = 4
                return

            if check == 0:
                self.check_if_sucess.value = 3
            else:
                self.check_if_sucess.value = 4



class WWait(threading.Thread):
    def __init__(self,check_if_sucess,msg="",speed=100,box=None):
        threading.Thread.__init__(self)
        self.msg=msg
        self.check_if_sucess = check_if_sucess
        self.speed = speed
        self.box=box
        self.p=Gtk.ProgressBar()
        if len(self.msg)!=0 :
            self.p.set_text(self.msg)
            self.p.set_show_text(self.msg)
        self.box.pack_start(self.p,False,False,0)
		
    def __pulse(self):
        if self.check_if_sucess.value !=2:
            self.p.set_fraction(0.0)
            self.p.hide()
            self.box.remove(self.p)
            return False
        else:
            self.p.pulse()
            return True

    def __loading_progressbar(self):
        self.source_id = GLib.timeout_add(self.speed, self.__pulse)

    def run(self):
        self.p.show()
        self.__loading_progressbar()




class BlockInstallRemoveButton(Gtk.HBox):
    def __init__(self,parent_,image,label_status,label,commands_install,commands_remove,run_from_file=False,tocheck=None, \
    exec__=["pkexec","pkexec"],program_name="arfedora",status=None,func_install=None,func_remove=False,argv_install=None, \
    argv_remove=None,choice=False,speed=200,signal="clicked", \
    if_true=None,if_false=None,if_e=None,if_not_e=None,nothing=None,\
    choice_install_message="",choice_remove_message="",install_button_tooltip="",remove_button_tooltip="",nothing_button_tooltip="",info=""):
        Gtk.HBox.__init__(self)
        self.set_homogeneous(True)
        self.parent_ = parent_
        self.func_install = func_install
        self.func_remove = func_remove
        self.argv_install = argv_install
        self.argv_remove = argv_remove
        self.label = label
        self.tocheck = tocheck
        self.check_if_sucess = multiprocessing.Value("i",2)
        self.commands_install = commands_install
        self.commands_remove = commands_remove
        self.status = status
        self.speed = speed
        self.signal = signal
        self.exec__ = exec__
        self.choice = choice
        self.run_from_file = run_from_file
        self.program_name = program_name
        self.image = image
        self.label_status = label_status
        self.button_box = Gtk.VBox()
        self.buttonb = Gtk.VBox()
        self.button_box.set_homogeneous(True)
        self.file_to_run = self.init_arfedora()
        self.c = self.check()
        self.if_true = if_true
        self.if_false = if_false
        self.if_e = if_e
        self.if_not_e = if_not_e
        self.nothing = nothing
        self.choice_install_message= choice_install_message
        self.choice_remove_message= choice_remove_message
        self.install_button_tooltip = install_button_tooltip
        self.remove_button_tooltip = remove_button_tooltip
        self.nothing_button_tooltip = nothing_button_tooltip
        self.info = info
        self.info_label = Gtk.Label(self.info[0:58])

        if self.c:
            self.button = Gtk.Button(label=self.label[1])
            self.button.get_style_context().add_class("destructive-action")
            self.button.set_tooltip_text(self.remove_button_tooltip)
            if self.func_install == None :
                self.button.connect(self.signal,self.install_remove_command)
            else:
                self.button.connect(self.signal,self.install_remove_func)
        else:
            self.button = Gtk.Button(label=self.label[0])
            self.button.get_style_context().add_class("suggested-action")
            self.button.set_tooltip_text(self.install_button_tooltip)
            if self.func_install == None:
                self.button.connect(self.signal,self.install_remove_command)
            else:
                self.button.connect(self.signal,self.install_remove_func)


        if len(self.if_true) != 0:
            if not self.if_true_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        if len(self.if_false) != 0:
            if not self.if_false_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        if len(self.if_e) != 0:
            if not self.if_e_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)
                
        if len(self.if_not_e) != 0:
            if not self.if_not_e_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        self.grid = Gtk.Grid(row_homogeneous=True)
        self.grid.attach(self.image,0,0,1,1)
        self.grid.attach_next_to(self.label_status,self.image,Gtk.PositionType.BOTTOM,1,1)
        self.buttonb.pack_start(self.button,False,False,0)
        self.button_box.pack_start(self.buttonb,False,False,0)
        self.pack_start(self.grid,False,False,0)
        self.pack_start(self.info_label,False,False,0)
        self.pack_start(self.button_box,False,False,0)



    def if_true_(self):
        for i in self.if_true:
            if subprocess.call(i,shell=True) != 0:
                return False
        return True

    def if_false_(self):
        for i in self.if_false:
            if subprocess.call(i,shell=True) != 0:
                return True
        return False

    def if_e_(self):
        for k,v in self.if_e.items():
            if subprocess.Popen(k,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("utf-8").strip() == v:
                return False
        return True

    def if_not_e_(self):
        for k,v in self.if_not_e.items():
            if subprocess.Popen(k,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("utf-8").strip() != v:
                return False
        return True

    def check(self):
        if isinstance(self.tocheck,list):
            for i in self.tocheck:
                if subprocess.call(i,shell=True) != 0:
                    return False
        else:
            if subprocess.call(self.tocheck,shell=True) != 0:
                return False
        return True
    
    
    def install_remove_command(self,button):
        if self.c:
            if self.choice:
                y = Yes_Or_No(self.choice_remove_message,self.parent_)
                if not y.check():
                    return
            self.check_if_sucess.value = 2
            self.parent_.set_sensitive(False)
            t1 = TC(self.commands_remove,self.check_if_sucess,self.run_from_file,file_to_run=self.file_to_run,exec__=self.exec__[1])
        else:
            if self.choice:
                y = Yes_Or_No(self.choice_install_message,self.parent_)
                if not y.check():
                    return
            self.check_if_sucess.value = 2
            self.parent_.set_sensitive(False)
            t1 = TC(self.commands_install,self.check_if_sucess,self.run_from_file,file_to_run=self.file_to_run,exec__=self.exec__[1])
        t2 = WWait(check_if_sucess=self.check_if_sucess,speed=self.speed,box=self.buttonb)
        t1.start()
        t2.start()
        if self.c:
            GLib.idle_add(self.install_remove_check_if_done,True)
        else:
            GLib.idle_add(self.install_remove_check_if_done)
        

    def install_remove_func(self,button):
        if self.c:
            if self.choice:
                y = Yes_Or_No(self.choice_remove_message,self.parent_)
                if not y.check():
                    return
            self.check_if_sucess.value = 2
            self.parent_.set_sensitive(False)
            t1 = TF(self.func_remove,self.check_if_sucess,self.argv_remove)
        else:
            if self.choice:
                y = Yes_Or_No(self.choice_install_message,self.parent_)
                if not y.check():
                    return
            self.check_if_sucess.value = 2
            self.parent_.set_sensitive(False)
            t1 = TF(self.func_install,self.check_if_sucess,self.argv_install)
        t2 = WWait(check_if_sucess=self.check_if_sucess,speed=self.speed,box=self.buttonb)
        t1.start()
        t2.start()
        if self.c:
            GLib.idle_add(self.install_remove_check_if_done,True)
        else:
            GLib.idle_add(self.install_remove_check_if_done)


    def install_remove_check_if_done(self,remove=False):
        if self.check_if_sucess.value == 3:
            if remove :
                if self.check()!=self.c:
                    self.button.set_label(self.label[0])
                    self.button.get_style_context().remove_class("destructive-action")
                    self.button.get_style_context().add_class("suggested-action")
                    self.button.set_tooltip_text(self.install_button_tooltip)
                    self.c = False
                    if self.status != None:
                        self.status[0](*self.status[1])
                else:
                    self.c = True
                    if self.status != None:
                        self.status[0](*self.status[2])


            else:
                if self.check()!=self.c:
                    self.button.set_label(self.label[1])
                    self.button.get_style_context().remove_class("suggested-action")
                    self.button.get_style_context().add_class("destructive-action")
                    self.button.set_tooltip_text(self.remove_button_tooltip)
                    if self.status != None:
                        self.status[0](*self.status[1])
                    self.c = True
                else:
                    if self.status != None:
                        self.status[0](*self.status[2])
                    self.c = False
                    

            if len(self.if_true) != 0:
                if not self.if_true_():
                    self.button.set_label(self.nothing)
                    self.button.set_sensitive(False)
                    self.button.set_tooltip_text(self.nothing_button_tooltip)

            if len(self.if_false) != 0:
                if not self.if_false_():
                    self.button.set_label(self.nothing)
                    self.button.set_sensitive(False)
                    self.button.set_tooltip_text(self.nothing_button_tooltip)

            if len(self.if_e) != 0:
                if not self.if_e_():
                    self.button.set_label(self.nothing)
                    self.button.set_sensitive(False)
                    self.button.set_tooltip_text(self.nothing_button_tooltip)
                
            if len(self.if_not_e) != 0:
                if not self.if_not_e_():
                    self.button.set_label(self.nothing)
                    self.button.set_sensitive(False)
                    self.button.set_tooltip_text(self.nothing_button_tooltip)


            self.parent_.set_sensitive(True)
            return False
        
        elif self.check_if_sucess.value == 4:
            if self.status != None:
                self.status[0](*self.status[2])

            self.parent_.set_sensitive(True)
            return False

        return True

    def init_arfedora(self):
        logname = os.getenv("LOGNAME")
        file_to_run = "{}".format(os.path.join("/home",logname,"."+self.program_name+"_to_run"))

        try:
            with open(file_to_run,"w") as myfile:
                pass
        except:
            exit("Error Try Create File {}.").format(file_to_run)

        if oct(os.stat(file_to_run).st_mode)[-3:]!="755":
            if os.getuid() != 0:
                check = subprocess.call("{} chmod 755 {}".format(self.exec__[1],file_to_run),shell=True)
            else:
                check = subprocess.call("chmod 755 {}".format(file_to_run),shell=True)
            if check != 0:
                exit()
        return file_to_run




















class BlockOneShotButton(Gtk.HBox):
    def __init__(self,parent_,image,label_status,label,commands_install,commands_remove,run_from_file=False,tocheck=None, \
    exec__=["pkexec","pkexec"],program_name="arfedora",status=None,func_install=None,func_remove=False,argv_install=None, \
    argv_remove=None,choice=False,speed=200,signal="clicked", \
    if_true=None,if_false=None,if_e=None,if_not_e=None,nothing=None,\
    choice_install_message="",choice_remove_message="",install_button_tooltip="",remove_button_tooltip="",nothing_button_tooltip="",info=""):
        Gtk.HBox.__init__(self)
        self.set_homogeneous(True)
        self.parent_ = parent_
        self.func_install = func_install
        self.argv_install = argv_install
        self.label = label
        self.check_if_sucess = multiprocessing.Value("i",2)
        self.commands_install = commands_install
        self.status = status
        self.speed = speed
        self.signal = signal
        self.exec__ = exec__
        self.choice = choice
        self.run_from_file = run_from_file
        self.program_name = program_name
        self.image = image
        self.label_status = label_status
        self.button_box = Gtk.VBox()
        self.buttonb = Gtk.VBox()
        self.button_box.set_homogeneous(True)
        self.file_to_run = self.init_arfedora()
        self.if_true = if_true
        self.if_false = if_false
        self.if_e = if_e
        self.if_not_e = if_not_e
        self.nothing = nothing
        self.choice_install_message= choice_install_message
        self.install_button_tooltip = install_button_tooltip
        self.nothing_button_tooltip = nothing_button_tooltip
        self.info = info
        self.info_label = Gtk.Label(self.info[0:58])

        self.button = Gtk.Button(label=self.label[0])
        self.button.get_style_context().add_class("suggested-action")
        self.button.set_tooltip_text(self.install_button_tooltip)
        if self.func_install == None:
            self.button.connect(self.signal,self.install_command)
        else:
            self.button.connect(self.signal,self.install_func)


        if len(self.if_true) != 0:
            if not self.if_true_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        if len(self.if_false) != 0:
            if not self.if_false_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        if len(self.if_e) != 0:
            if not self.if_e_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)
                
        if len(self.if_not_e) != 0:
            if not self.if_not_e_():
                self.button.set_label(self.nothing)
                self.button.set_sensitive(False)
                self.button.set_tooltip_text(self.nothing_button_tooltip)

        self.grid = Gtk.Grid(row_homogeneous=True)
        self.grid.attach(self.image,0,0,1,1)
        self.grid.attach_next_to(self.label_status,self.image,Gtk.PositionType.BOTTOM,1,1)
        self.buttonb.pack_start(self.button,False,False,0)
        self.button_box.pack_start(self.buttonb,False,False,0)
        self.pack_start(self.grid,False,False,0)
        self.pack_start(self.info_label,False,False,0)
        self.pack_start(self.button_box,False,False,0)



    def if_true_(self):
        for i in self.if_true:
            if subprocess.call(i,shell=True) != 0:
                return False
        return True

    def if_false_(self):
        for i in self.if_false:
            if subprocess.call(i,shell=True) != 0:
                return True
        return False

    def if_e_(self):
        for k,v in self.if_e.items():
            if subprocess.Popen(k,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("utf-8").strip() == v:
                return False
        return True

    def if_not_e_(self):
        for k,v in self.if_not_e.items():
            if subprocess.Popen(k,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("utf-8").strip() != v:
                return False
        return True

    
    
    def install_command(self,button):
        if self.choice:
            y = Yes_Or_No(self.choice_install_message,self.parent_)
            if not y.check():
                return
        
        self.check_if_sucess.value = 2
        self.parent_.set_sensitive(False)
        t1 = TC(self.commands_install,self.check_if_sucess,self.run_from_file,file_to_run=self.file_to_run,exec__=self.exec__[1])
        t2 = WWait(check_if_sucess=self.check_if_sucess,speed=self.speed,box=self.buttonb)
        t1.start()
        t2.start()
        GLib.idle_add(self.install_check_if_done)
        

    def install_func(self,button):
        if self.choice:
            y = Yes_Or_No(self.choice_install_message,self.parent_)
            if not y.check():
                return
        self.check_if_sucess.value = 2
        self.parent_.set_sensitive(False)
        t1 = TF(self.func_install,self.check_if_sucess,self.argv_install)
        t2 = WWait(check_if_sucess=self.check_if_sucess,speed=self.speed,box=self.buttonb)
        t1.start()
        t2.start()
        GLib.idle_add(self.install_check_if_done)


    def install_check_if_done(self):
        if self.check_if_sucess.value == 3:
            if self.status != None:
                self.status[0](*self.status[1])
                    
            self.parent_.set_sensitive(True)
            return False
        
        elif self.check_if_sucess.value == 4:
            if self.status != None:
                self.status[0](*self.status[2])

            self.parent_.set_sensitive(True)
            return False

        return True

    def init_arfedora(self):
        logname = os.getenv("LOGNAME")
        file_to_run = "{}".format(os.path.join("/home",logname,"."+self.program_name+"_to_run"))

        try:
            with open(file_to_run,"w") as myfile:
                pass
        except:
            exit("Error Try Create File {}.").format(file_to_run)

        if oct(os.stat(file_to_run).st_mode)[-3:]!="755":
            if os.getuid() != 0:
                check = subprocess.call("{} chmod 755 {}".format(self.exec__[1],file_to_run),shell=True)
            else:
                check = subprocess.call("chmod 755 {}".format(file_to_run),shell=True)
            if check != 0:
                exit()
        return file_to_run
