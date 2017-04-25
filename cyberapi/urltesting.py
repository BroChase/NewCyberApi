from tkinter import *
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox, Progressbar, Style
from tkinter import messagebox
from pprint import pprint
import urllib.request
import json
import webbrowser
import unicodedata
import re
import datetime
from time import strftime
import makemenu
from PIL import ImageTk, Image

class cyberapi(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Article Searcher")       #Title of window
        #set the frame dimentions and pack the parent window
        container = Frame(self)
        menu = makemenu.MenuMaker2000(self).createMenu()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.resizable(width=False, height=False)
        #self.resizable(width=False, height=False)

        #get screen dimensions and center window
        xoffset = int(self.winfo_screenwidth()/2-1280/2)
        yoffset = int(self.winfo_screenheight()/2-800/2)
        self.geometry("%dx%d+%d+%d" % (500, 300, xoffset, yoffset))    #set geometry of window
        self.frames = {}
        for F in (Welcome, searchtitlekeyword):       #The two windows used in program sets the page
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("Welcome")          #call show_frame to display the welcome window
        self.show_frame('searchtitlekeyword')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()                     #raise that window frame
        self.title(frame.title)             #rename the window title to the title in def Welcome

    def changeTitle(self, newTitle):
        self.title(newTitle)
class Welcome(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller        #set the controller
        self.title = "Article Search"              #ttile of the window
        self.grid_rowconfigure(15, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=5)
        self.grid_columnconfigure(8, weight=1)

        #Window Buttons
        self.but_titlesearch = Button(self, text='Search Title', width=35, command=self.tkwsearch,
                                      relief=RAISED, bd=4)
        self.but_titlebodysearch = Button(self, text='Search Title & Body', width=35, command=self.tbssearch,
                                         relief=RAISED, bd=4)
        self.but_datesearch = Button(self, text='Search By Date', width=35, command=self.sbdsearch,
                                     relief=RAISED, bd=4)
        self.but_urisearch = Button(self, text='Search By URI', width=35, command=self.urisearch,
                                    relief=RAISED, bd=4)
        self.var = IntVar()
        self.check_filter = Checkbutton(self, text="Advanced Filter", variable=self.var, command= self.filter_op)

        #Formatting of the window
        self.but_titlesearch.grid(column=1, row =1,columnspan=2)
        self.but_titlebodysearch.grid(column=1, row=2, columnspan=2)
        self.but_datesearch.grid(column=1, row=3, columnspan=2)
        self.but_urisearch.grid(column=1, row=4, columnspan=2)
        self.check_filter.grid(column=1, row=5, sticky='W')
        #todo row adustment
        self.grid_rowconfigure(13, weight=20)

    def filter_op(self):
        if self.var.get():
            self.fauthor_label = Label(self, text='Author: ')
            self.fauthor_entry = Entry(self, width=22, bd=2)
            self.fsub_label = Label(self, text='Subjectivity: ')
            self.var2 = IntVar()
            self.var2.set(1)
            self.fsub_nv = Radiobutton(self, text ='Null', variable=self.var2, value=1)
            self.fsub_gt = Radiobutton(self, text='GreaterThan', variable=self.var2, value=2)
            self.fsub_lt = Radiobutton(self, text='LessThan', variable=self.var2, value=3)
            self.fD_label = Label(self, text='Date: ')
            self.fD_format = Label(self, text='00/00/0000')
            self.fD_format.configure(foreground='grey')
            self.fD_beinlab = Label(self, text='Begin: ')
            self.fD_endlab = Label(self, text='End: ')
            self.fD_ent = Entry(self, width=10, bd=2)
            self.fD_ent.insert('end', '01/01/0001')
            self.fD_ent2 = Entry(self, width=10, bd=2)
            self.fD_ent2.insert('end', strftime('%m/%d/%Y'))
            #print(strftime('%m-%d-%Y'))


            #window placements
            self.fauthor_label.grid(column=1, row=6, sticky='w')
            self.fauthor_entry.grid(column=2, row=6, sticky='W')
            self.fsub_label.grid(column=1, row=7, sticky='W')
            self.fsub_nv.grid(column=2, row=7, sticky='W')
            self.fsub_gt.grid(column=2, row=8, sticky='W')
            self.fsub_lt.grid(column=2, row=9, sticky='W')
            self.fD_label.grid(column=1, row=10, sticky='W')
            self.fD_format.grid(column=2, row=10, sticky='W')
            self.fD_beinlab.grid(column=1, row=11, sticky='E')
            self.fD_ent.grid(column=2, row=11, sticky='W')
            self.fD_endlab.grid(column=1, row=12, sticky='E')
            self.fD_ent2.grid(column=2, row=12, sticky='W')

            #if the button gets unchecked it will destroy the labels and entry widgets.
        else:
            self.fauthor_label.destroy()
            self.fauthor_entry.destroy()
            self.fsub_label.destroy()
            self.fsub_nv.destroy()
            self.fsub_gt.destroy()
            self.fsub_lt.destroy()
            self.fD_label.destroy()
            self.fD_format.destroy()
            self.fD_ent.destroy()
            self.fD_beinlab.destroy()
            self.fD_endlab.destroy()
            self.fD_ent2.destroy()

    #search by title
    def tkwsearch(self):
        if self.var.get():
            self.var.set(0)
            self.filter_op()
        #check to see if the lables and entry boxes exist from a previous search options
        #if they do then destroy them then create the new search label and entry box
        if hasattr(self, 'titlelabel'):
            self.ent_title.destroy()
            self.titlelabel.destroy()
            self.but_search.destroy()
        if hasattr(self, 'bodylabel'):
            self.bodylabel.destroy()
            self.ent_body.destroy()
            self.but_search.destroy()
        if hasattr(self, 'urilabel'):
            self.urilabel.destroy()
            self.ent_uri.destroy()
            self.but_search.destroy()
        if hasattr(self, 'datelabel'):
            self.datelabel.destroy()
            self.sdatelabel.destroy()
            self.edatelabel.destroy()
            self.datelabelex.destroy()
            self.ent_date.destroy()
            self.ent_edate.destroy()
            self.but_search.destroy()

        self.ent_title = Entry(self, width=30, bd=2)
        self.ent_title.bind('<Return>', self.enableSearch)
        self.titlelabel = Label(self, text='Title')
        self.but_search = Button(self, text='Search', width=20, state='disable', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title='
                                                                                  + self.ent_title.get()))

        #http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title='string'
        #+ &author='string'&+&sub=gt&sdate='00/00/0000&edate='00/00/0000'

        #window placements
        self.titlelabel.grid(column=3, row=1)
        self.ent_title.grid(column=4, row=1)
        self.but_search.grid(column=5, row=1)

    #search by title&body
    def tbssearch(self):
        if self.var.get():
            self.var.set(0)
            self.filter_op()
        #check to see if the lables and entry boxes exist from a previous search options
        #if they do then destroy them then create the new search label and entry box
        if hasattr(self, 'titlelabel'):
            self.ent_title.destroy()
            self.titlelabel.destroy()
            self.but_search.destroy()
        if hasattr(self, 'bodylabel'):
            self.bodylabel.destroy()
            self.ent_body.destroy()
            self.but_search.destroy()
        if hasattr(self, 'urilabel'):
            self.urilabel.destroy()
            self.ent_uri.destroy()
            self.but_search.destroy()
        if hasattr(self, 'datelabel'):
            self.datelabel.destroy()
            self.sdatelabel.destroy()
            self.edatelabel.destroy()
            self.datelabelex.destroy()
            self.ent_date.destroy()
            self.ent_edate.destroy()
            self.but_search.destroy()
        self.ent_title = Entry(self, width=30, bd=2)
        self.titlelabel = Label(self, text='Title')
        self.bodylabel = Label(self, text='Body')
        self.ent_body = Entry(self, width=30, bd=2)
        self.ent_body.bind('<Return>', self.enableSearch)
        self.but_search = Button(self, text='Search', width=20, state='disable', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordbody&title='
                                                                                  + self.ent_title.get()+'&body=' + self.ent_body.get()))
        #window placments
        self.titlelabel.grid(column=3, row=1)
        self.bodylabel.grid(column=3, row =2)
        self.ent_title.grid(column=4, row=1)
        self.ent_body.grid(column=4, row=2)
        self.but_search.grid(column=5, row=1)
    #search by uri
    def urisearch(self):
        if self.var.get():
            self.var.set(0)
            self.filter_op()
        #check to see if the lables and entry boxes exist from a previous search options
        #if they do then destroy them then create the new search label and entry box
        if hasattr(self, 'titlelabel'):
            self.ent_title.destroy()
            self.titlelabel.destroy()
            self.but_search.destroy()
        if hasattr(self, 'bodylabel'):
            self.bodylabel.destroy()
            self.ent_body.destroy()
            self.but_search.destroy()
        if hasattr(self, 'urilabel'):
            self.urilabel.destroy()
            self.ent_uri.destroy()
            self.but_search.destroy()
        if hasattr(self, 'datelabel'):
            self.datelabel.destroy()
            self.sdatelabel.destroy()
            self.edatelabel.destroy()
            self.datelabelex.destroy()
            self.ent_date.destroy()
            self.ent_edate.destroy()
            self.but_search.destroy()
        self.ent_uri = Entry(self, width=30, bd=2)
        self.ent_uri.bind('<Return>', self.enableSearch)
        self.urilabel = Label(self, text="URI")
        self.but_search = Button(self, text='Search', width=20, state='disable', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=uri&uripath='
                                                                                   + self.ent_uri.get()))
        #http://cbrown686-test.apigee.net/cyberapi/articles?q=uri&uripath='string'
        #+ &author='string'&+&sub=gt&sdate='00/00/0000&edate='00/00/0000'

        #window placements
        self.urilabel.grid(column=3, row=1)
        self.ent_uri.grid(column=4, row=1)
        self.but_search.grid(column=5, row=1)

    #search by Date
    def sbdsearch(self):
        if self.var.get():
            self.var.set(0)
            self.filter_op()
        #check to see if the lables and entry boxes exist from a previous search options
        #if they do then destroy them then create the new search label and entry box
        if hasattr(self, 'titlelabel'):
            self.ent_title.destroy()
            self.titlelabel.destroy()
            self.but_search.destroy()
        if hasattr(self, 'bodylabel'):
            self.bodylabel.destroy()
            self.ent_body.destroy()
            self.but_search.destroy()
        if hasattr(self, 'urilabel'):
            self.urilabel.destroy()
            self.ent_uri.destroy()
            self.but_search.destroy()
        if hasattr(self, 'datelabel'):
            self.datelabel.destroy()
            self.sdatelabel.destroy()
            self.edatelabel.destroy()
            self.datelabelex.destroy()
            self.ent_date.destroy()
            self.ent_edate.destroy()
            self.but_search.destroy()

        self.datelabel = Label(self, text='Date: ')
        self.sdatelabel = Label(self, text='Begin: ')
        self.edatelabel = Label(self, text='End: ')
        self.datelabelex = Label(self, text='00/00/0000')
        self.datelabelex.configure(foreground='grey')
        self.ent_date = Entry(self, width=10, bd=2)
        self.ent_edate = Entry(self, width=10, bd=2)
        self.ent_date.insert('end', '01/01/2016')
        self.ent_edate.insert('end', strftime('%m/%d/%Y'))
        self.ent_edate.bind('<Return>', self.enableSearch)
        self.but_search = Button(self, text='Search', width=20, state='disable', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=date&adate='
                                                                                  + self.ent_date.get()+'&zdate='+self.ent_edate.get()))
        #http://cbrown686-test.apigee.net/cyberapi/articles?q=date&adate='00/00/0000'&zdate='00/00/0000
        #+ &author='string'&+&sub=gt&sdate='00/00/0000&edate='00/00/0000'

        #window plecements
        self.but_search.grid(column=5, row=1)
        self.datelabel.grid(column=3, row=1)
        self.sdatelabel.grid(column=3, row=2)
        self.edatelabel.grid(column=3, row=3)
        self.datelabelex.grid(column=4, row=1, sticky='W')
        self.ent_date.grid(column=4, row=2, sticky='W')
        self.ent_edate.grid(column=4, row=3, sticky='W')

    def search(self,url):
        if self.var.get():
            print(self.var.get())
        #if hasattr(self, 'fauthor_entry'):
            au = self.fauthor_entry.get()
            au = au.replace(' ', '+')
            #var2 is the state of the radio check button
            if self.var2.get() == 2:
                url = url+'&author='+au+'&sub=gt&sdate='+self.fD_ent.get()+'&edate='+self.fD_ent2.get()
                print(url)
            elif self.var2.get() == 3:
                url = url+'&author='+au+'&sub=gt&sdate='+self.fD_ent.get()+'&edate='+self.fD_ent2.get()
            else:
                url = url + '&author=' + au + '&sub=&sdate=' + self.fD_ent.get()+'&edate='+self.fD_ent2.get()
        else:
            url = url+'&author=&sub=&sdate=01/01/0001&edate='+strftime('%m/%d/%Y')
            print(url)
        r = urllib.request.urlopen(url)
        data = json.load(r)
        self.tree = Treeview(self)
        self.tree.heading('#0', text='Results by Title')
        self.tree.column('#0', stretch=True)
        #todo edit rowspan to change size of the tree window with title return
        self.tree.grid(column=7, row=2, rowspan=12, sticky='nsew')

        if data:
            for item in (data):
                #remove BOM images first from body >uffff
                item['body'] = ''.join(c for c in unicodedata.normalize('NFC', item['body']) if c <= '\uFFFF')
                self.tree.insert('', 'end', text=item['title'], values=(item['uri'], item['body'], item['title'],
                                                                        item['author'], item['date']))

            self.tree.bind('<Double-1>', self.on_click)
#on_click "double clicking on the article from the tree window opens up the article to be viewed"

    def on_click(self, event):
        item = self.tree.selection()[0]
        self.n = self.tree.item(item,'values')
        tw = Toplevel(self)
        tw.title(self.n[2])
        tb = Text(tw, width=100, height=40)
        tb.insert('end', self.n[1])
        link = Label(tw, text=self.n[0])
        link.configure(foreground='blue', cursor='hand2')
        link.bind('<1>', self.op_link)
        auth = Label(tw, text='Author: ' + self.n[3])
        articledate = Label(tw, text=self.n[4])
        topics = Label(tw, text='Topics:')

        #window formatting for tw
        link.grid(column=1, row=1, columnspan=4)
        tb.grid(column=1, row=3, columnspan=4)
        auth.grid(column=1, row=4, columnspan =2,sticky='W')
        articledate.grid(column=3, row=4, sticky='W')
        topics.grid(column=4, row=4)

    #op_link "double click on the link at the top of the page opens up the url link
    def op_link(self, event):
        webbrowser.open_new(self.n[0])

    #event bind when Return is entered after a title keyword is entered will enable the search button.
    def enableSearch(self, event):
        self.but_search.configure(state='normal')



#todo -------------------------------------------
class searchtitlekeyword(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        container = Frame(self)
        self.controller = controller  # set the controller
        #self.controller = controller        #set the controller
        self.title = "CreepyCrawler"              #ttile of the window
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)


        path = 'spiderweb2.jpg'
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.panel = Label(self, image=self.img)
        self.panel.grid(column=1, row=1,columnspan=20,rowspan=20)

        s = Style()
        s.configure("blue.Horizontal.TProgressbar", troughcolor='black', background='#00FFF1')
        self.progress = Progressbar(self, orient="horizontal", style='blue.Horizontal.TProgressbar', length=500, mode="determinate")
        #self.controller.attributes('-transparentcolor', 'black')
        self.style = Style()
        self.style.configure('My.TFrame', background='#434343')
        self.sf = Frame(self, width=186, height=120, style='My.TFrame')
        self.sf['relief']='sunken'

        self.wl= Label(self, text='WELCOME', width=18)
        self.wl.configure(background='#434343', foreground='#06c8e6', font='bold')
        self.ns = Label(self, text='New Session', width=25)
        self.ns.configure(height=2, background='#828282', foreground='#06c8e6')
        self.rs = Label(self, text='Restore Session', width=25)
        self.rs.configure(background='#434343', foreground='#06c8e6')
        #window placements
        self.progress.grid(column=1, row=1, sticky='N')
        self.sf.grid(column=1, row=2, rowspan=4)
        self.wl.grid(column=1, row=2, sticky='S')
        self.ns.grid(column=1, row=3)
        self.rs.grid(column=1, row=4, sticky='N')

        self.bytes = 0
        self.maxbytes = 0


    def start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 10000
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)
        else:
            self.welcomewindowing()


    def welcomewindowing(self):
        xoffset = int(self.winfo_screenwidth() / 2 - 1280 / 2)
        yoffset = int(self.winfo_screenheight() / 2 - 800 / 2)
        self.controller.geometry("%dx%d+%d+%d" % (1280, 800, xoffset, yoffset))  # set geometry of window
        self.controller.show_frame('Welcome')



if __name__ == "__main__":
    app = cyberapi()
    app.mainloop()