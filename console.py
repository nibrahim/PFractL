# Copyright (C) 2002 Noufal Ibrahim <noufal@cisco.com>
#
# This program is part of PfractL
#
# PfractL is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from Tkinter import *
from graphics import *

console=0

ERROR="error"
MESG="mesg"
SPL="special"

class messageconsole(viewbox):
    def __init__(self,parser,logger,oldone):
        self.parent=parser
        self.createwindowq()
        self.logger=logger
        self.oldone=oldone

    def createwindowq(self):
        "Console window"
        print "*** Initialising console window ***"

        self.consolewindow=Toplevel(self.parent.root)
        self.consolewindow.title("Message console")

        self.text=Text(self.consolewindow,bg="wheat",state=DISABLED)
        self.text.pack(side=TOP,expand=1,fill="x")
        
        closeb=Button(self.consolewindow,text="Close",command=self.closecallback,\
                     relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")
        closeb.pack(side=BOTTOM,expand=1,fill="x")

    def closecallback(self):
        self.consolewindow.destroy()

    def cprint(self,message,type):
        self.text.configure(state=NORMAL)
        if (type==MESG):
            self.text.tag_config(MESG,foreground="blue")
            self.text.insert(END,"*** " + message + " ***\n",MESG)
        elif (type==ERROR):
            self.text.tag_config(ERROR,foreground="red")
            self.text.insert(END,">>> " + message + " <<<\n",ERROR)
        elif (type==SPL):
            self.text.tag_config(SPL,foreground="black")
            self.text.insert(END,"---------- "+ message +" ----------\n",SPL)
            self.logger=self.oldone
        self.text.configure(state=DISABLED)
