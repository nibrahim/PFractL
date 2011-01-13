#!/usr/bin/python
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



from graphics import *
from editor import *
from FileDialog import *
from console import *

import math
import sys
import re
import stack
import pickle

logger=None

class parser(viewbox):
    "Draws a string specified in our little language"

    def autocomplete(self):
        "Completes fractal components that are unspecified"
        logger ("Checking for incomplete entries",MESG)
        if (self.fractal.has_key('Rgen') and (not self.fractal.has_key('Lgen'))):
            logger ("Autogenerating Lgen from Rgen:"+self.fractal['Rgen'],MESG)
            temp=self.fractal['Rgen']
##          All plusses with minuses
            temp=re.sub("\+",".",temp)
            temp=re.sub("-","+",temp)
            temp=re.sub("\.","-",temp)
        
##          All Rs with Ls and vice versa
            temp=re.sub("R",".",temp)
            temp=re.sub("L","R",temp)
            temp=re.sub("\.","L",temp)
        
            logger ("Lgen:"+temp,MESG)
            self.fractal['Lgen']=temp

        if (self.fractal.has_key('Lgen') and (not self.fractal.has_key('Rgen'))):
            logger ("Autogenerating Rgen from Lgen:"+self.fractal['Lgen'],MESG)
            temp=self.fractal['Lgen']
##          All plusses with minuses and vice versa
            temp=re.sub("\+",".",temp)
            temp=re.sub("-","+",temp)
            temp=re.sub("\.","-",temp)
        
##          All Rs with Ls and vice versa
            temp=re.sub("R",".",temp)
            temp=re.sub("L","R",temp)
            temp=re.sub("\.","L",temp)
        
            logger("Rgen:"+temp,MESG)
            self.fractal['Rgen']=temp
            
            
        if(self.fractal.has_key('name')):
            self.title(self.fractal['name'])
        else:
            logger("Fractal name string not found",MESG)
            self.title("Unspecified")


        if(self.fractal.has_key('xpos') and self.fractal.has_key('ypos')):
            self.x,self.y=self.fractal['xpos'],self.fractal['ypos']
        else:
            logger ("Fractal starting point unspecified",MESG)
            logger ("Using (132,"+str(HEIGHT-369)+")",MESG)
            self.fractal['xpos'],self.fractal['ypos']=132,HEIGHT-369
            self.x=132
            self.y=HEIGHT-369
        
        if (not self.fractal.has_key('maxlevel')):
            logger("Fractal maximum level depth unspecified",MESG)
            logger("Using default 6",MESG)
            self.fractal["maxlevel"]=6

        if (not self.fractal.has_key('sangle')):
            logger("Fractal starting angle unspecified",MESG)
            logger("Using default 0",MESG)
            self.fractal['sangle']=0
            
        self.level=1
        self.reset()
            
#Functions that handle all the artwork. 
    def renderstring(self,string,level):
        "The actual parser that recognises the language"
        for i in string:
#            print "angle :: " ,self.cangle
#            raw_input()
            if i=='D':                             #Basic line
                if (level == 1):
                    self.drawline(i)
#                    print i,
                else:
#                  print "Before: " + str(self.fractal['length'])
                    self.fractal['length']=self.fractal['length']/self.fractal['divisor']
#                    print "expanding D into",self.fractal['Dgen'],level
                    self.renderstring(self.fractal['Dgen'],level-1)
                    self.fractal['length']=self.fractal['length']*self.fractal['divisor']
#                    print "After: " + str(self.fractal['length'])
            elif i=='T':                             
                if (level == 1):
                    self.drawline(i)
#                    print i,
                else:
                    self.fractal['length']=self.fractal['length']/self.fractal['divisor']
#                    print "expanding T into",self.fractal['Tgen'],level
                    self.renderstring(self.fractal['Tgen'],level-1)
                    self.fractal['length']=self.fractal['length']*self.fractal['divisor']

            elif i=='d':
                if (level == 1):
                    self.movepointer()
                else:
                    self.fractal['length']=self.fractal['length']/self.fractal['divisor']
                    self.renderstring(self.fractal['dgen'],level-1)
                    self.fractal['length']=self.fractal['length']*self.fractal['divisor']
            elif i=='R':
                if (level == 1):
                    self.drawline(i)
#                    print i,
                else:
                    self.fractal['length']=self.fractal['length']/self.fractal['divisor']
#                    print "expanding R into",self.fractal['Rgen'],level
                    self.renderstring(self.fractal['Rgen'],level-1)
                    self.fractal['length']=self.fractal['length']*self.fractal['divisor']
            elif i=='L':
                if (level == 1):
                    self.drawline(i)
#                    print i,
                else:
                    self.fractal['length']=self.fractal['length']/self.fractal['divisor']
#                    print "expanding L into",self.fractal['Lgen'],level
                    self.renderstring(self.fractal['Lgen'],level-1)
                    self.fractal['length']=self.fractal['length']*self.fractal['divisor']
            elif i=='X':
                if (level == 1):
                    self.drawline(i)
#                    print i,
            elif i=='B':
                    self.drawline(i)
#                    print i,
            elif i=='[':
                self.bstack.push((self.x,self.y,self.cangle))
            elif i==']':
                (self.x,self.y,self.cangle)=self.bstack.pop()
            elif i=='+':
##                 if (level == 1):
##                     print "+",
##                 if (level == 2):
##                     print ".+."
                 self.incrementangle()


            elif i=="-":
##                 if (level == 1):
##                     print "-",
##                 if (level == 2):
##                     print ".-."
                 self.decrementangle()
            else:
                print "Invalid command character :",i
                
                sys.exit(-1)
                

    def drawline(self,symbol):
        "Draws a line of the current length in the current direction"
        x=self.x
        y=self.y
        a=self.fractal['length']
        theta=self.cangle
        tx=x + a*math.cos(self.factor*theta)
        ty=y + a*math.sin(self.factor*theta)
        self.line(x,y,tx,ty,symbol)
        self.x=tx
        self.y=ty
        

    def movepointer(self):
        "Simply moves the pointer in the current direction"
        x=self.x
        y=self.y
        a=self.fractal['length']
        theta=self.cangle
        tx=x + a*math.cos(self.factor*theta)
        ty=y + a*math.sin(self.factor*theta)
        self.x=tx
        self.y=ty

    def incrementangle(self):
        if (self.grammarflag == 1):
            self.printmarker(self.x,self.y,'+',"blue")
        self.cangle=self.cangle+self.fractal['angle']
            
    def decrementangle(self): 
        if (self.grammarflag == 1):
            self.printmarker(self.x,self.y,'-',"blue")
        self.cangle=self.cangle-self.fractal['angle']

    def redraw(self):
        """Redraws the fractal but I'm not sure of the details yet."""
        self.clear()
        self.renderstring(self.fractal['axiom'],self.level)
        self.reset()

###################### #Callbacks for the buttons and stuff. ##################

    def deactivatebuttons(self):
        "Disables all the buttons"
        for i in self.blist:
            i.configure(state="disabled")

    def deactivatemenus(self):
        "Disables menu entries"
        for i in self.mlist:
            i[0].entryconfig(i[1],state="disabled")
        

    def activatebuttons(self):
        "Enables buttons"
        for i in self.blist:
            i.configure(state="normal")

    def activatemenus(self):
        "Enables menu items"
        for i in self.mlist:
            i[0].entryconfig(i[1],state="normal")

        
    def pluscallback(self):
        "What happens when the plus button is pressed"
        self.deactivatebuttons()     #Disable everything
        self.deactivatemenus()

        level=self.level             #Increment, clear the canvas and redraw
        if level != self.fractal['maxlevel']:
            level=level+1
            fractl.clear()
            fractl.generatefractal(level)
        else:
            self.mesg ("Max level reached")
        
        self.activatebuttons()       #Reactivate everything
        self.activatemenus()
        
        
    def minuscallback(self):
        "What happens when the minus button is pressed"
        self.deactivatebuttons()  #Disable everything
        self.deactivatemenus()

        level=self.level          #Decrement and draw after clearing
        if level != 1:
            level=level-1
            fractl.clear()
            fractl.generatefractal(level)
        else:
            self.mesg ("Can't go less than 1")
        
        self.activatebuttons()   #Reactivate everything
        self.activatemenus()


    def poscallback(self,event):
        """Temporary binding for canvas.
        Changes canvas behaviour to enable starting point selection.
        Restores left mouse key after this is done and """
        self.x,self.y=self.convert(event.x,event.y)
        self.fractal['xpos'],self.fractal['ypos']=self.x,self.y
        logger(str(event.x)+str(event.y),MESG)
        self.canvas.unbind("<Button-1>")
        self.canvas.configure(cursor="left_ptr")
        self.mesg("")


    def selectcallback(self):
        """Point selection callback. The callback for the button that
        handles the starting point selection"""
        self.mesg("Select starting point")
        self.canvas.configure(cursor="crosshair")
        self.canvas.bind("<Button-1>",self.poscallback)

    def infocallback(self):
        "Callback for the editor"
        editor=fractaleditor(self)

    def fileloadcallback(self):
        "The dialog box etc. for the load menu item"
        fd=FileDialog(self.root)
        file=fd.go(".","*.pf")
#       print " ***************** To load fractal file:", file,":" # DEBUG
        if(file != None):
            try:
                f=open(file,"r")
            except IOError:
                self.mesg("No such file")
                logger("No such file :"+file,ERROR)
                self.activatebuttons()
                return
            self.fractal=pickle.load(f)
            f.close()
            logger("Loaded fractal file "+file,SPL)
            self.autocomplete()
            self.cangle=self.fractal['sangle']
            fractl.redraw()
            self.activatebuttons()
        else:
            self.mesg("Invalid file")
            logger("Invalid file name :"+file,ERROR)

    def filesavecallback(self):
        "The dialog box etc. for the save menu item"
        fd=FileDialog(self.root)
        file=fd.go(".","*.pf")
        if (file != None):
            f=open(file,"w")
            pickle.dump(self.fractal,f)
            f.close()
            logger("File "+file+" saved",SPL)
            self.activatebuttons()
        else:
            self.mesg("Invalid file")
            logger("Invalid file name",ERROR)


    def consolecallback(self):
        global logger
        self.console=messageconsole(self,logger,self.loggerdummy)
        logger=self.console.cprint
            
#########################    Public interfaces  ################################
    def generatefractal(self,level):
        self.level=level
        self.mesg("Creating fractal - Level:"+str(self.level))
        self.renderstring(self.fractal['axiom'],self.level)
        self.mesg ("Level:"+str(self.level))
        if (self.markerflag == 1):
            self.marksegments()
        self.reset()

    def reset(self):
        "Resets dynamic parameters"
        self.x,self.y=self.fractal['xpos'],self.fractal['ypos']
        self.cangle=self.fractal['sangle']


    def loggerdummy(self,t1,t2):
        pass

 ##   def temp_stub(self):
##        self.fractal={"name":"Testing",\
##                      "ypos":454.0,\
##                      "maxlevel":12.0,\
##                      "sangle":0.0,\
##                      "xpos":74.0,\
##                      "Lgen":"+RDX-LDL-XDR+",\
##                      "Rgen":"-LDX+RDR+XDL-",\
##                      "Dgen":"DXX",\
##                      "divisor":2.33333,\
##                      "angle":90.0,\
##                      "length":200,\
##                      "axiom":"L"
##                      }
                      
        

    def __init__(self):
        "Initialises parser components"
        #Starting coordinates and angle

        #        self.temp_stub()

        global logger
        logger=self.loggerdummy
        self.bstack=stack.Stack()
        self.lstack=stack.Stack()
        
        self.factor=math.pi/180.0 #rad to degree
        self.level=1

        self.initialise(bg="#ffe4b5",fg="chocolate")   #Set up graphics routines

        self.setcallbacks(plus=self.pluscallback,\
                          minus=self.minuscallback,\
                          select=self.selectcallback,\
                          query=self.infocallback,\
                          console=self.consolecallback,\
                          loadfile=self.fileloadcallback,\
                          savefile=self.filesavecallback)

        
        try:
            if self.fractal:
                pass
        except AttributeError:
            self.deactivatebuttons()
       

fractl=parser()

def main():
    global fractl
    fractl.map()
    fractl.generatefractal(1)
    

    
        

main()
