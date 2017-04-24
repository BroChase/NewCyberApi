from tkinter import *
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter import messagebox
from pprint import pprint
import urllib.request
import json
import webbrowser
import unicodedata

class cyberapi(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Python Port Scanner")       #Title of window
        #set the frame dimentions and pack the parent window
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.resizable(width=False, height=False)

        #get screen dimensions and center window
        xoffset = int(self.winfo_screenwidth()/2-1280/2)
        yoffset = int(self.winfo_screenheight()/2-800/2)
        self.geometry("%dx%d+%d+%d" % (1280, 800, xoffset, yoffset))    #set geometry of window

        self.frames = {}
        for F in (Welcome, searchtitlekeyword):       #The two windows used in program sets the page
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Welcome")          #call show_frame to display the welcome window

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
        #self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(5, weight=1)
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
        self.grid_rowconfigure(11, weight=20)


    def filter_op(self):
        if self.var.get():
            self.fauthor_label = Label(self, text='Author: ')
            self.fauthor_entry = Entry(self, width=22, bd=2)
            self.fsub_label = Label(self, text='Subjectivity: ')
            self.var2 = IntVar()
            self.var2.set(1)
            self.fsub_nv = Radiobutton(self, text ='Null', variable=self.var2, value=1, command=self.rbselection)
            self.fsub_gt = Radiobutton(self, text='GreaterThan', variable=self.var2, value=2, command=self.rbselection)
            self.fsub_lt = Radiobutton(self, text='LessThan', variable=self.var2, value=3, command=self.rbselection)
            #window formatting

            self.fauthor_label.grid(column=1, row=6, sticky='w')
            self.fauthor_entry.grid(column=2, row=6, sticky='W')
            self.fsub_label.grid(column=1, row=7, sticky='W')
            self.fsub_nv.grid(column=2, row=7, sticky='W')
            self.fsub_gt.grid(column=2, row=8, sticky='W')
            self.fsub_lt.grid(column=2, row=9, sticky='W')

#if the button gets unchecked it will destroy the labels and entry widgets.
        else:
            self.fauthor_label.destroy()
            self.fauthor_entry.destroy()
            self.fsub_label.destroy()
            self.fsub_nv.destroy()
            self.fsub_gt.destroy()
            self.fsub_lt.destroy()

        #formatting for the window
#search by title
    def rbselection(self):
        print('hi')


    def tkwsearch(self):
        self.ent_title = Entry(self, width=30, bd=2)
        self.titlelabel = Label(self, text='Title')
        if hasattr(self, 'bodylabel'):
            self.bodylabel.destroy()
            self.ent_body.destroy()

        self.but_search = Button(self, text='Search', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title='
                                                                                  + self.ent_title.get()))
        #window placement
        self.titlelabel.grid(column=2, row=1)
        self.ent_title.grid(column=3, row=1)
        self.but_search.grid(column=4, row=1)

#search by title&body todo write url path for getting keyword from body and title
    def tbssearch(self):
        self.ent_title = Entry(self, width=30, bd=2)
        self.titlelabel = Label(self, text='Title')
        self.bodylabel = Label(self, text='Body')
        self.ent_body = Entry(self, width=30, bd=2)

        self.but_search = Button(self, text='Search')

        #window placment
        self.titlelabel.grid(column=2, row=1)
        self.bodylabel.grid(column=2, row =2)
        self.ent_title.grid(column=3, row=1)
        self.ent_body.grid(column=3, row=2)
        self.but_search.grid(column=4, row=1)

#todo search by Date
    def sbdsearch(self):
        print('hi')
#todo search by uri
    def urisearch(self):
        self.ent_uri = Entry(self, width=30, bd=2)
        self.urilabel = Label(self, text="URI")
        self.but_ksearch = Button(self, text='Search', command=lambda: self.search('http://cbrown686-test.apigee.net/cyberapi/articles?q=uri&uripath='
                                                                                   + self.ent_uri.get()))

        self.ent_uri.grid(column=3, row=1)
        self.urilabel.grid(column=2, row=1)
        self.but_ksearch.grid(column=4, row=1)


    def search(self,url):
        r = urllib.request.urlopen(url)
        data = json.load(r)
        self.tree = Treeview(self)
        self.tree.heading('#0', text='Title')
        self.tree.column('#0', stretch=True)
        self.tree.grid(column=5, row=1,rowspan=10, sticky='nsew')

        if data:
            for item in (data):
                #remove BOM images first from body >uffff
                item['body'] = ''.join(c for c in unicodedata.normalize('NFC', item['body']) if c <= '\uFFFF')
                #populate the tree window
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



    def about(self):
        messagebox.showinfo("About", "Chase Brown")  # messagebox when File<About.? is selected

    def start(self):
        self.controller.show_frame("MainMenu")  # opens up the next window mainmenu

#todo -------------------------------------------
class searchtitlekeyword(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller        #set the controller
        self.title = "Results"              #ttile of the window



if __name__ == "__main__":
    app = cyberapi()
    app.mainloop()