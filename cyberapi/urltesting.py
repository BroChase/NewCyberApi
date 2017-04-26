from tkinter import *
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox, Progressbar, Style
from tkinter import messagebox, filedialog
from pprint import pprint
import urllib.request
import json
import webbrowser
import unicodedata
import re
import datetime
from time import strftime
import makemenu
import analysis
import requests
from dateutil import parser
from PIL import ImageTk, Image
import os

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

        #get screen dimensions and center window
        xoffset = int(self.winfo_screenwidth()/2-1280/2)
        yoffset = int(self.winfo_screenheight()/2-800/2)
        self.geometry("%dx%d+%d+%d" % (700, 450, xoffset, yoffset))    #set geometry of window
        self.frames = {}
        for F in (SearchFrame, StartFrame):       #The two windows used in program sets the page
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("Welcome")          #call show_frame to display the welcome window
        self.show_frame('StartFrame')
        #self.show_frame('SearchFrame')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()                     #raise that window frame
        self.title(frame.title)             #rename the window title to the title in def Welcome

    def changeTitle(self, newTitle):
        self.title(newTitle)

class SearchFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.analyzer = analysis.Analyzer()

        self.controller = controller  # set the controller
        self.title = "Article Search"  # ttile of the window

        #title
        path = 'crawler.jpg'
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.panel = Label(self, image=self.img)
        self.panel.pack()
        self.searchwindow()

    #search window populates the window with widgets for searching
    def searchwindow(self):
        #keyword entry
        self.largefont = ('Veranda', 15)
        self.ent_keyword = Entry(self, width=40, relief='raised', font=self.largefont, bd=1)
        #todo <Return> and entry is not empty call search()


        self.ent_keyword.bind('<Escape>', self.clear_text)
        self.ent_keyword.bind('<Key>', lambda event: self.callEnable(event, 'DefaultSearch'))

        self.var = IntVar()
        self.check_filter = Checkbutton(self, text="Advanced Filter", variable=self.var, command=self.filter_op)

        if not self.var.get():
            self.but_search = Button(self, text='Search', width=15, state='disable', command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitlebody&title='
                + self.ent_keyword.get() + '&body=' + self.ent_keyword.get()))
            self.but_search.place(x=515, y=350)
        else:
            self.searchButton()

        #window placements
        #ENTRY BOX for keyword
        self.ent_keyword.place(x=300, y=310)

        #check button
        self.check_filter.place(x=400, y=350)
    #todo if the user selects to load a search it will simply jump to results

    def searchButton(self,event):
        if self.box.current() is 0:
            self.but_search = Button(self, text='Search', width=15, state='disable', command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitlebody&title='
                + self.ent_keyword.get() + '&body=' + self.ent_keyword.get()))
            self.but_search.place(x=515, y=350)
            self.enableSearch2()
        elif self.box.current() is 1:
            self.but_search = Button(self, text='Search', width=15, state='disable', command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title='
                + self.ent_keyword.get()))
            self.but_search.place(x=515, y=350)
            self.enableSearch2()
        elif self.box.current() is 2:
            self.but_search = Button(self, text='Search', width=15, state='disable', command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=bodyonly&body='
                + self.ent_keyword.get()))
            self.but_search.place(x=515, y=350)
            self.enableSearch2()
        elif self.box.current() is 3:
            self.but_search = Button(self, text='Search', width=15, state='disable', command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=uri&uripath='
                + self.ent_keyword.get()))
            self.but_search.place(x=515, y=350)
            self.enableSearch2()
    #Hitting escape when editing the ENTRY box will clear it and disable the search button from being able to be used.
    def clear_text(self, event):
        self.ent_keyword.delete(0, 'end')
        self.but_search.configure(state='disable')
    #filter options populate uppon check box of Advanced search option
    def filter_op(self):
        if self.var.get():
            #appearing
            self.appearing_label = Label(self, text='Appearing In:', background='#282828', font=15, foreground='#5DE0DC')
            self.box_value = StringVar()
            self.box = Combobox(self, textvariable=self.box_value)
            self.box['values'] = ('Default', 'Title', 'Body', 'URL')
            self.box.current(0)
            self.box.bind('<<ComboboxSelected>>', self.searchButton)
            #author
            self.author_label = Label(self, text='Author:',background='#282828', font=15, foreground='#5DE0DC')
            self.author_entry = Entry(self, width=22, bd=2, background='#9A9A9A')
            #subjectivity
            self.fsub_label = Label(self, text='Subjectivity:',background='#282828', font=15, foreground='#5DE0DC')
            self.var2 = IntVar()
            self.var2.set(1)
            self.fsub_nv = Radiobutton(self, text="Don't Care", variable=self.var2, value=1, background='#282828', foreground='#5DE0DC')
            self.fsub_gt = Radiobutton(self, text='More Subjective', variable=self.var2, value=2, background='#282828', foreground='#5DE0DC')
            self.fsub_lt = Radiobutton(self, text='More Objective', variable=self.var2, value=3, background='#282828', foreground='#5DE0DC')
            #date
            self.fD_label = Label(self, text='Date:',background='#282828', font=15, foreground='#5DE0DC')
            self.fD_format = Label(self, text='00/00/0000', background='#282828',foreground='#BBBBBB')
            self.fD_format.configure(foreground='grey')
            self.fD_beinlab = Label(self, text='From:',background='#282828', foreground='#BBBBBB')
            self.fD_endlab = Label(self, text='To:',background='#282828', foreground='#BBBBBB')
            self.fD_ent = Entry(self, width=10, bd=2, background='#9A9A9A')
            self.fD_ent.insert('end', '01/01/0001')
            self.fD_ent2 = Entry(self, width=10, bd=2, background='#9A9A9A')
            self.fD_ent2.insert('end', strftime('%m/%d/%Y'))


        # window placements
            #appearing labael
            self.appearing_label.place(x=400, y=380)
            #appearing pick
            self.box.place(x=510, y=380)
            #author label
            self.author_label.place(x=400, y=405)
            #author entry
            self.author_entry.place(x=510, y=405)
            #subjectivity
            self.fsub_label.place(x=400, y=430)
            self.fsub_nv.place(x=510, y=430)
            self.fsub_gt.place(x=510, y=455)
            self.fsub_lt.place(x=510, y=480)

            #date
            self.fD_label.place(x=400, y=505)
            self.fD_format.place(x=440, y=507)
            self.fD_beinlab.place(x=510, y=505)
            self.fD_ent.place(x=555, y=505)
            self.fD_endlab.place(x=590, y=505)
            self.fD_ent2.place(x=625, y=505)

            # if the button gets unchecked it will destroy the labels and entry widgets.
        else:
            self.appearing_label.destroy()
            self.box.destroy()
            self.author_label.destroy()
            self.author_entry.destroy()
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
    # does just that clears some shit bra
    def clearshit(self):
        # check to see if the lables and entry boxes exist from a previous search options
        # if they do then destroy them then create the new search label and entry box
        self.ent_keyword.destroy()
        self.check_filter.destroy()
        self.but_search.destroy()
        if hasattr(self, 'appearing_label'):
            self.ent_keyword.destroy()
            self.check_filter.destroy()
            self.but_search.destroy()
            self.appearing_label.destroy()
            self.box.destroy()
            self.author_label.destroy()
            self.author_entry.destroy()
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
    #undoes the hide of the seach buttons so that they can edit the search
    def undohide(self):
        self.ent_keyword.place(x=300, y=310)
        self.check_filter.place(x=400, y=350)
        self.but_search.place(x=515, y=350)
        if hasattr(self, 'appearing_label'):
            # window placements
            # appearing labael
            self.appearing_label.place(x=400, y=380)
            # appearing pick
            self.box.place(x=510, y=380)
            # author label
            self.author_label.place(x=400, y=405)
            # author entry
            self.author_entry.place(x=510, y=405)
            # subjectivity
            self.fsub_label.place(x=400, y=430)
            self.fsub_nv.place(x=510, y=430)
            self.fsub_gt.place(x=510, y=455)
            self.fsub_lt.place(x=510, y=480)

            # date
            self.fD_label.place(x=400, y=505)
            self.fD_format.place(x=440, y=507)
            self.fD_beinlab.place(x=510, y=505)
            self.fD_ent.place(x=555, y=505)
            self.fD_endlab.place(x=590, y=505)
            self.fD_ent2.place(x=625, y=505)

    #hides the widgets to display the search results
    def hideshit(self):
        self.ent_keyword.place(x=(-100), y=(-100))
        self.check_filter.place(x=(-100), y=(-100))
        self.but_search.place(x=(-100), y=(-100))
        if hasattr(self, 'appearing_label'):
            self.ent_keyword.place(x=(-100), y=(-100))
            self.check_filter.place(x=(-100), y=(-100))
            self.but_search.place(x=(-100), y=(-100))
            self.appearing_label.place(x=(-100), y=(-100))
            self.box.place(x=(-100), y=(-100))
            self.author_label.place(x=(-100), y=(-100))
            self.author_entry.place(x=(-100), y=(-100))
            self.fsub_label.place(x=(-100), y=(-100))
            self.fsub_nv.place(x=(-100), y=(-100))
            self.fsub_gt.place(x=(-100), y=(-100))
            self.fsub_lt.place(x=(-100), y=(-100))
            self.fD_label.place(x=(-100), y=(-100))
            self.fD_format.place(x=(-100), y=(-100))
            self.fD_ent.place(x=(-100), y=(-100))
            self.fD_beinlab.place(x=(-100), y=(-100))
            self.fD_endlab.place(x=(-100), y=(-100))
            self.fD_ent2.place(x=(-100), y=(-100))

    #search for that almighty data mine.
    def search(self, url):
        print(url)
        if self.var.get():
            au = self.author_entry.get()
            au = au.replace(' ', '+')
            # var2 is the state of the radio check button
            if self.var2.get() == 2:
                url = url + '&author=' + au + '&sub=gt&sdate=' + self.fD_ent.get() + '&edate=' + self.fD_ent2.get()
                # print(url)
            elif self.var2.get() == 3:
                url = url + '&author=' + au + '&sub=gt&sdate=' + self.fD_ent.get() + '&edate=' + self.fD_ent2.get()
            else:
                url = url + '&author=' + au + '&sub=&sdate=' + self.fD_ent.get() + '&edate=' + self.fD_ent2.get()
        else:
            url = url + '&author=&sub=&sdate=01/01/0001&edate=' + strftime('%m/%d/%Y')

        print(url)
        data = requests.get(url).json()
        print(data)

        self.hideshit()
        self.tree = Treeview(self)
        self.tree.heading('#0', text='Results by Title')
        self.tree.column('#0', stretch=True)
        self.tree.place(x=682, relheight=1, relwidth=.38)

        if data:
            for item in data:
                # remove BOM images first from body >uffff
                item['body'] = ''.join(c for c in unicodedata.normalize('NFC', item['body']) if c <= '\uFFFF')
                self.tree.insert('', 'end', text=item['title'], values=(item['uri'], item['body'], item['title'],
                                                                        item['author'],
                                                                        parser.parse(item['date']).strftime(
                                                                            '%B, %d, %Y')))

            self.tree.bind('<Double-1>', self.on_click)
            self.tree.bind('<<TreeviewSelect>>', self.on_single_click)

            #sunken box that topics print out into
            self.style = Style()
            self.style.configure('My.TFrame', background='#383838')
            self.sf = Frame(self, width=550, height=150, style='My.TFrame')
            self.sf['relief'] = 'sunken'
            self.sf.place(x=70, y=80)

            # labels for article topics
            self.topicsHead = Label(self, font="times 16 underline",background='#282828', foreground='#5DE0DC')
            self.topics = Label(self, wraplength=500, font='times 14',background='#383838', foreground='#5DE0DC')
            self.topics.place(x=100, y=95)
            self.topicsHead.place(x=250, y=50)

            #New Search Edit Search Save Search
            self.new_search = Button(self, text='New Search', background='#383838', foreground='#5DE0DC',
                                     command= self.NewSearch)
            self.edit_search = Button(self, text='Edit Search', background='#383838', foreground='#5DE0DC',
                                      command=self.EditSearch)
            self.save_search = Button(self, text='Save Search', background='#383838', foreground='#5DE0DC')

            self.new_search.place(x=1, y=675)
            self.edit_search.place(x=75, y=675)
            self.save_search.place(x=145, y=675)

        else:
            self.edit_search = Button(self, text='Edit Search', background='#383838', foreground='#5DE0DC',
                                      command=self.EditSearch)
            self.edit_search.place(x=1, y=675)
            self.topicsHead = Label(self, font="times 16 underline",background='#282828', foreground='#5DE0DC')
            self.topics = Label(self, wraplength=500, font='times 14',background='#383838', foreground='#5DE0DC')
            self.topics.place(x=100, y=95)
            self.topicsHead.place(x=250, y=50)
            self.topicsHead.config(text='No Articles Matching Search')
            self.topics.config(text='')



            # on_click "double clicking on the article from the tree window opens up the article to be viewed"
    def NewSearch(self):
        self.deletesearch()
        self.searchwindow()
    def EditSearch(self):
        self.deletesearch()
        self.undohide()

    #todo implement the save function
    def SaveSearch(self):
        print('hi')

    #defind clear search
    def deletesearch(self):
        self.tree.destroy()
        self.sf.destroy()
        self.topicsHead.destroy()
        self.topics.destroy()
        self.new_search.destroy()
        self.edit_search.destroy()
        self.save_search.destroy()

    #on click gets the articles information and displays it in the Key Article Subjects window
    def on_single_click(self, event):
        self.topicsHead.config(text="Key Article Subjects")
        item = self.tree.item(self.tree.selection()[0], 'values')
        topicStr = ', '.join(self.analyzer.getMostCommonNounPhrases(5, [item[1]])) + '\n'
        self.topics.config(text=topicStr)

    #on d click will open the article for display
    def on_click(self, event):
        item = self.tree.selection()[0]
        self.n = self.tree.item(item, 'values')
        tw = Toplevel(self)
        xoffset = int(self.winfo_screenwidth() / 2 - 1280 / 2)
        yoffset = int(self.winfo_screenheight() / 2 - 800 / 2)
        tw.geometry("%dx%d+%d+%d" % (800, 600, xoffset, yoffset))  # set geometry of window
        tw.title(self.n[2])
        tb = Text(tw, width=90, height=40, font="Times 14", wrap=WORD)
        tb.insert('end', self.n[1])
        link = Label(tw, text=self.n[0])
        link.configure(foreground='blue', cursor='hand2')
        link.bind('<1>', self.op_link)
        auth = Label(tw, text='Author: ' + self.n[3])
        articledate = Label(tw, text='Date Published: ' + self.n[4])

        # window formatting for tw
        link.place(x=0, y=0, relwidth=1)
        tb.place(y=20, relwidth=1, relheight=1)
        auth.pack(side=LEFT, anchor='sw')
        articledate.pack(side=RIGHT, anchor='se')
    # op_link "double click on the link at the top of the page opens up the url link
    def op_link(self, event):
        webbrowser.open_new(self.n[0])

    def callEnable(self, event, searchType):
        self.after(100, lambda: self.enableSearch(event, searchType))

    # event bind when Return is entered after a title keyword is entered will enable the search button.
    def enableSearch(self, event, searchType):
        string = ''
        if searchType == 'DefaultSearch':
            string = self.ent_keyword.get()
        if string.strip() != '':
            self.but_search.configure(state='normal')
        else:
            self.but_search.configure(state='disabled')
    # check for when no event bind is present to be used to pass in and no need for searchType
    def enableSearch2(self):
        string = self.ent_keyword.get()
        if string.strip() != '':
            self.but_search.configure(state='normal')
        else:
            self.but_search.configure(state='disabled')

class StartFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        container = Frame(self)
        self.controller = controller  # set the controller
        self.title = "CreepyCrawler"              #ttile of the window

        path = 'spiderweb2.jpg'
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.panel = Label(self, image=self.img)
        self.panel.pack()

        #Progress Bar
        self.s = Style()
        self.s.theme_use('clam')
        self.s.configure("mongo.Horizontal.TProgressbar", foreground='#38494C', background='#5AE9FF')
        self.progress = Progressbar(self, orient="horizontal", style='mongo.Horizontal.TProgressbar', length=700, mode="determinate")
        self.controller.attributes('-transparentcolor', '#38494C')

        #Menu Frame window
        self.style = Style()
        self.style.configure('My.TFrame', background='#434343')
        self.sf = Frame(self, width=179, height=76, style='My.TFrame')
        self.sf['relief']='sunken'

        #todo to be populated with old searches to be able to reopen.
        self.menutree = Treeview(self)
        self.menutree.column('#0', stretch=True)

        #Menu Labels
        self.wl= Label(self, text='WELCOME', width=24, height=2)
        self.wl.configure(background='#434343', foreground='#06c8e6')
        self.ns = Label(self, text='New Session', width=24, height=1)
        self.ns.configure(height=2, background='#828282', foreground='#06c8e6')
        self.ns.bind('<1>', self.start)
        self.rs = Label(self, text='Restore Session', width=28,height=2)
        self.rs.configure(background='#434343', foreground='#06c8e6')
        #window placements
        self.sf.place(x=298, y=162)
        self.wl.place(x=300,y=165)
        self.ns.place(x=300, y= 200)
        self.rs.place(x=0, relwidth=.25)
        self.menutree.place(x=0, relwidth=.25, relheight=.98)
        self.progress.place(y=440)

        self.bytes = 0
        self.maxbytes = 0

    #little display load bar for visual effect :P
    def start(self, event):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 1500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(25, self.read_bytes)
        else:
            self.welcomewindowing()

    def welcomewindowing(self):
        xoffset = int(self.winfo_screenwidth() / 2 - 1280 / 2)
        yoffset = int(self.winfo_screenheight() / 2 - 800 / 2)
        self.controller.geometry("%dx%d+%d+%d" % (1100, 700, xoffset, yoffset))  # set geometry of window
        self.controller.show_frame('SearchFrame')


if __name__ == "__main__":
    app = cyberapi()
    app.mainloop()