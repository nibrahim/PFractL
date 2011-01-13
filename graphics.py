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
HEIGHT=500
WIDTH=500

class viewbox:
    "Implements graphics stuff"
    def initialise(self,fg,bg):
        self.root=Tk(className="PFract-L")
        self.eachsegflag=0
        self.grammarflag=0
        self.markerflag=0
        
        main=Frame(self.root,bg="#b5b5b5")
        buttonf=Frame(main,borderwidth="2",bg="#b5b5b5")
        buttonf.pack(side=RIGHT,expand=1,fill="y")
        main.pack(side=TOP)
        self.canvas=Canvas(main,height=HEIGHT,width=WIDTH,bg=bg,borderwidth=2,\
                           relief=SUNKEN)
        self.canvas.pack(side=RIGHT)
        self.fg=fg
        self.root.bind('q',sys.exit)

        #First a title kind of box
        self.titlebox=Label(self.root,relief=SUNKEN,borderwidth=2)
        self.titlebox.config(text="P-FractL")
        self.titlebox.pack(side=TOP,expand=1,fill="x")
        #Now the status box
        self.mesgbox=Label(self.root,relief=SUNKEN,borderwidth=2)
        self.mesgbox.config(text="")
        self.mesgbox.pack(side=BOTTOM,expand=1,fill="x")


        # Now we create the control panel. I'm not sure if this is the
        # right place though

        f=Frame(self.root,borderwidth="2",bg="#b5b5b5")  #f is a frame to house the buttons
        self.bp=Button(f,bitmap="@./images/plus.xbm",relief=GROOVE,\
                       bg="#cdc0b0",activebackground="#eedfcc")
        self.bm=Button(f,bitmap="@./images/minus.xbm",relief=GROOVE,\
                       bg="#cdc0b0",activebackground="#eedfcc")
#         self.bq=Button(f,text="Q",command=sys.exit,relief=GROOVE,\
#                   bg="#cdc0b0",activebackground="#eedfcc")
        self.bs=Button(f,bitmap="@./images/left_ptr.xbm",\
                  relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")

        self.bi=Button(f,bitmap="@./images/info.xbm",\
                  relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")

        self.bc=Button(f,bitmap="@./images/console.xbm",\
                       relief=GROOVE,bg="#cdc0b0",activebackground="#eedfcc")
        
                
        updateb=Checkbutton(buttonf,text="Each segment",relief=GROOVE,\
                            bg="#cdc0b0",activebackground="#eedfcc",\
                            onvalue=1,offvalue=0,\
                            command=self.segcallback)

        markerb=Checkbutton(buttonf,text="Segment markers",relief=GROOVE,\
                            bg="#cdc0b0",activebackground="#eedfcc",\
                            onvalue=1,offvalue=0,command=self.markercallback)

        grammarb=Checkbutton(buttonf,text="Grammar symbols",relief=GROOVE,\
                            bg="#cdc0b0",activebackground="#eedfcc",\
                            onvalue=1,offvalue=0,command=self.grammarcallback)

        
        self.blist=[self.bp,self.bm,self.bs,self.bi]

#        f.pack(side=LEFT,expand=1,fill="y")
        f.pack(side=BOTTOM,expand=1,fill="x")


        #Now that that's done, lets get to work on the menus
        m=Menu(self.root) #The main menubar.
        self.root.config(menu=m)


        self.fm=Menu(m) #The file menu? :)
        m.add_cascade(label="File",menu=self.fm)
        self.fm.add_command(label="Load")
        self.fm.add_command(label="Save")
        self.fm.add_separator()
        self.fm.add_command(label="Exit PFractL",command=sys.exit)
#         self.bp.pack(side=TOP,expand=1,fill="x")
#         self.bm.pack(side=TOP,expand=1,fill="x")
#         self.bs.pack(side=TOP,expand=1,fill="x")
#         self.bi.pack(side=TOP,expand=1,fill="x")
#         self.bq.pack(side=TOP,expand=1,fill="x")        

        self.mlist=[(self.fm,1)]

        self.bp.pack(side=LEFT,expand=1,fill="both")
        self.bm.pack(side=LEFT,expand=1,fill="both")
        self.bs.pack(side=LEFT,expand=1,fill="both")
        self.bi.pack(side=LEFT,expand=1,fill="both")
        self.bc.pack(side=LEFT,expand=1,fill="both")
        updateb.pack(side=TOP,expand=1,fill="x")
        markerb.pack(side=TOP,expand=1,fill="x")
        grammarb.pack(side=TOP,expand=1,fill="x")
#        self.bq.pack(side=LEFT,expand=1,fill="both")        


    def segcallback(self):
        if (self.eachsegflag == 1):
            self.eachsegflag = 0
        else:
            self.eachsegflag = 1

    def segentrycallback(self,event):
        x=self.canvas.find_closest(event.x,event.y)
        self.canvas.itemconfig(x,fill="purple")

    def segleavecallback(self,event):
        x=self.canvas.find_closest(event.x,event.y)
        self.canvas.itemconfig(x,fill=self.fg)
    

    def markercallback(self):
        if (self.markerflag == 1):
            self.markerflag=0
            self.canvas.tag_unbind("segment","<Enter>")
            self.canvas.tag_unbind("segment","<Leave>")
        else:
            self.markerflag=1

    def marksegments(self):
        self.canvas.tag_bind("segment","<Enter>",self.segentrycallback)
        self.canvas.tag_bind("segment","<Leave>",self.segleavecallback)




    def grammarcallback(self):
        if (self.grammarflag == 1):
            self.grammarflag = 0
        else:
            self.grammarflag = 1
        
    def title(self,title):
        self.titlebox.configure(text=title)
        
    def mesg(self,message):
        self.mesgbox.configure(text=message)
        self.canvas.update()
        
    def line(self,x1,y1,x2,y2,symbol):
        self.canvas.create_line(self.convert(x1,y1),self.convert(x2,y2),\
                                fill=self.fg,tag="segment")

        if(self.markerflag == 1):
            self.canvas.create_arc(self.convert(x2,y2),self.convert(x2+3,y2+3),\
                                   start=0,extent=359,fill="blue")

        if(self.grammarflag == 1):
            nx=(x1+x2)/2.0
            ny=(y1+y2)/2.0
            self.canvas.create_text(self.convert(nx,ny),text=symbol,\
                                    font="fixed",fill="blue")
        if (self.eachsegflag == 1):
            self.canvas.update()

    def printmarker(self,x1,y1,symbol,color):
        self.canvas.create_text(self.convert(x1+2,y1+2),text=symbol,\
                                font="fixed",fill=color)
    

    def convert(self,tx,ty,h=HEIGHT,w=WIDTH):
        return tx,HEIGHT-ty

    def map(self):
        self.root.mainloop()


    def clear(self):
        for i in self.canvas.find_all():
            self.canvas.delete(i)

    def refresh(self):
        self.canvas.update()
        
    def setcallbacks(self,plus,minus,select,query,console,loadfile,savefile):
        "Ugly kluge to keep this separate"
        self.bp.configure(command=plus)
        self.bm.configure(command=minus)
        self.bs.configure(command=select)
        self.bi.configure(command=query)
        self.bc.configure(command=console)
        #NNOOOOOOO more and more shit is being dropped in here.
        self.fm.entryconfig(1,command=loadfile)
        self.fm.entryconfig(2,command=savefile)
