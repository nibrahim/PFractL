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

class fractaleditor(viewbox):
    def __init__(self,parser):
        self.parent=parser
        self.parent.mesg("Fractal parameters")
        self.createwindowq()
        

        
    def quitcallback(self):
        self.editwindow.destroy()
        self.parent.mesg("")
        self.parent.activatebuttons()
        self.parent.activatemenus()
#       self.parent.autocomplete()
#        self.parent.redraw()
        j=0
        listbox=self.listbox
        for i in self.parent.fractal.keys():
#             listbox.append([])
#             listbox[j].append(Frame(self.editwindow))
#             listbox[j].append(Label(listbox[j][0],text=i,bg="#cdb7b5"))
#             listbox[j].append(Entry(listbox[j][0],width=max))
            listbox[j][2].destroy()
            listbox[j][1].destroy()
            listbox[j][0].destroy()
            j=j+1

        

    def commitcallback(self):
        print "*** Updating fractal parameters ***"
        j=0
        listbox=self.listbox
        for i in self.parent.fractal.keys():
#            listbox[j][0].pack(side=TOP,expand=1,fill="x")    #The frame
#            listbox[j][1].pack(side=LEFT,expand=1,fill="x")   #The label
            field=listbox[j][1].config("text")[4]
            value=listbox[j][2].get()
            print field,value


            if ((len(value) > 0) and ( '0' <= value[0] <= '9')) :
                value=float(value)
            self.parent.fractal[field]=value                
            j=j+1

            
        
    
    def createwindowq(self):
        "Query callback"
        print "*** Complete fractal information ***"
        self.parent.deactivatebuttons()
        self.parent.deactivatemenus()
        max=0
        for i in self.parent.fractal.keys():
            if len(str(self.parent.fractal[i]))>max:
                max=len(str(self.parent.fractal[i]))
        self.editwindow=Toplevel(self.parent.root)
        self.editwindow.title(self.parent.fractal['name']+": Parameters")

        buttonframe=Frame(self.editwindow)
        buttonframe.pack(side=BOTTOM)

        doneb=Button(buttonframe,text="Dismiss",command=self.quitcallback,\
                     relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")
        
        commitb=Button(buttonframe,text="Commit",command=self.commitcallback,\
                     relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")
        
        commitb.pack(side=LEFT)
        doneb.pack(side=LEFT)
        j=0
##        listbox=range(0,len(self.data.keys()))
##        for i in range(0,len(self.data.keys())):
##            listbox[i]=[]
##        print "Here",listbox[0][0]
        self.listbox=[]
        listbox=self.listbox
        for i in self.parent.fractal.keys():
            listbox.append([])
            listbox[j].append(Frame(self.editwindow))
            listbox[j].append(Label(listbox[j][0],text=i,bg="#cdb7b5"))
            listbox[j].append(Entry(listbox[j][0],width=max))

            listbox[j][0].pack(side=TOP,expand=1,fill="x")    #The frame
            listbox[j][1].pack(side=LEFT,expand=1,fill="x")   #The label
            listbox[j][2].pack(side=LEFT)  #The entry box
            listbox[j][2].insert(END,str(self.parent.fractal[i]))
            j=j+1
#       self.elements=j
