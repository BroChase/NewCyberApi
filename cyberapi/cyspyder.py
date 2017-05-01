from tkinter import *
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox, Progressbar, Style
from tkinter import filedialog, messagebox
import json
import webbrowser
import unicodedata
import datetime
from time import strftime
import makemenu
import analysis
import requests
from dateutil import parser
from PIL import ImageTk, Image
import os
import textwrap
import time
import threading
import queue
import calltipwindow



class cyberapi(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Article Searcher")       #Title of window
        #set the frame dimentions and pack the parent window
        container = Frame(self)
        menu = makemenu.MainMenu(self).createMenu()

        self.updateque = queue.Queue()
        self.analyzer = analysis.Analyzer(self.updateque)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.resizable(width=False, height=False)

        #get screen dimensions and center window
        xoffset = int(self.winfo_screenwidth()/2-700/2)
        yoffset = int(self.winfo_screenheight()/2-550/2)
        self.geometry("%dx%d+%d+%d" % (700, 450, xoffset, yoffset))    #set geometry of window
        self.frames = {}
        for F in (SearchFrame, StartFrame):       #The two windows used in program sets the page
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame('StartFrame')
    def get_file(self):
        return SearchFrame.content
    def set_file(self, obj):
        SearchFrame.content = obj
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()                     #raise that window frame
        self.title(frame.title)             #rename the window title to the title in def Welcome

    def changeTitle(self, newTitle):
        self.title(newTitle)

class SearchFrame(Frame):
    content = None
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #self.analyzer = analysis.Analyzer(self.updateque)
        self.analysisthread = None
        self.controller = controller  # set the controller
        self.title = "Article Search"  # ttile of the window

        #title
        path = os.getcwd() + '\\resources\cyspider.jpg'
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.panel = Label(self, image=self.img)
        self.panel.pack()
        self.searchwindow()

        # widgets for results page
        # sunken box that topics print out into
        self.style = Style()
        self.style.configure('My.TFrame', background='#383838')

        # frame for individual analysis
        # self.sf = Frame(self, width=550, height=150, style='My.TFrame')
        # self.sf['relief'] = 'sunken'

        # frame for results analysis
        self.sf2 = Frame(self, width=550, height=150, style='My.TFrame')
        self.sf2['relief'] = 'sunken'

        # labels for article topics
        self.topicsHead = Label(self, text='Key Article Subjects', font="times 16 underline", background='#282828',
                                foreground='#5DE0DC')
        self.topics = Label(self, text='Click on an article to see more info', wraplength=500, font='times 14',
                            background='#383838', foreground='#5DE0DC', anchor=W, justify=LEFT)
        calltipwindow.createToolTip(self.topicsHead, "These are a few subjects that were mentioned in the article")

        # labels for results analysis
        self.resultTopicHead = Label(self, text='Most Mentioned Phrases in Results', font="times 16 underline",
                                     background='#282828', foreground='#5DE0DC')
        self.resultTopics = Label(self, text='Processing Data (0%)', wraplength=500, font='times 14',
                                  background='#383838', foreground='#5DE0DC', anchor=W, justify=LEFT)
        calltipwindow.createToolTip(self.resultTopicHead,
                                    "These are the most mentioned phrases in the resulting articles.")


    #search window populates the window with widgets for searching
    def searchwindow(self):
        #keyword entry
        self.largefont = ('Veranda', 24)
        self.ent_keyword = Entry(self, width=40, relief='raised', font=self.largefont, bd=1)
        #todo <Return> and entry is not empty call search()

        calltipwindow.createToolTip(self.ent_keyword, "Enter a word or phrase here to search by.")
        self.ent_keyword.bind('<Escape>', self.clear_text)
        self.ent_keyword.bind('<Key>', lambda event: self.callEnable(event, 'DefaultSearch'))

        self.var = IntVar()
        self.var.set(0)
        self.check_filter = Checkbutton(self, text="Advanced Filter", onvalue=1, offvalue=0, variable=self.var, command=self.filter_op, font="Veranda 16")
        calltipwindow.createToolTip(self.check_filter, "Click here for options to narrow your search")

        if not self.var.get():
            self.but_search = Button(self, text='Search', width=15, state='disable', font="Veranda 16", command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitlebody&title='
                + self.ent_keyword.get() + '&body=' + self.ent_keyword.get()))
            self.but_search.place(relx=.505, rely=.6, anchor=W)
        else:
            self.searchButton()

        #window placements
        #ENTRY BOX for keyword
        self.ent_keyword.place(relx=.5, rely=.5, anchor=CENTER)

        #check button
        self.check_filter.place(relx=.495, rely=.6, relheight=.059, anchor=E)
    #todo if the user selects to load a search it will simply jump to results

    def searchButton(self,event):
        if self.box.current() is 0:
            self.but_search.config(command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitlebody&title='
                + self.ent_keyword.get() + '&body=' + self.ent_keyword.get()))
        elif self.box.current() is 1:
            self.but_search.config(command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title=' + self.ent_keyword.get()))
        elif self.box.current() is 2:
            self.but_search.config(command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=bodyonly&body=' + self.ent_keyword.get()))
        elif self.box.current() is 3:
            self.but_search.config(command=lambda: self.search(
                'http://cbrown686-test.apigee.net/cyberapi/articles?q=uri&uripath='+ self.ent_keyword.get()))

        self.enableSearch2()

    #Hitting escape when editing the ENTRY box will clear it and disable the search button from being able to be used.
    def clear_text(self, event):
        self.ent_keyword.delete(0, 'end')
        self.but_search.configure(state='disable')
    #filter options populate uppon check box of Advanced search option
    def filter_op(self):
        if self.var.get() is 1:
            #appearing
            self.appearing_label = Label(self, text='Appearing In:', background='#282828', font=15, foreground='#5DE0DC')
            self.box_value = StringVar()
            self.box = Combobox(self, textvariable=self.box_value)
            calltipwindow.createToolTip(self.appearing_label, "Select where you want us to search "
                                                              "for your provided search phrase.")
            calltipwindow.createToolTip(self.box, "Select where you want us to search "
                                                              "for your provided search phrase.")
            self.box['values'] = ('Default', 'Title', 'Body', 'URL')
            self.box.current(0)
            self.box.bind('<<ComboboxSelected>>', self.searchButton)
            #author
            self.author_label = Label(self, text='Author:',background='#282828', font=15, foreground='#5DE0DC')
            self.author_entry = Entry(self, width=22, bd=2, background='#9A9A9A')
            calltipwindow.createToolTip(self.author_label,
                                        "Enter an author's first and/or last name (not case-sensitive).")
            calltipwindow.createToolTip(self.author_entry,
                                        "Enter an author's first and/or last name (not case-sensitive).")
            #subjectivity
            self.fsub_label = Label(self, text='Subjectivity:',background='#282828', font=15, foreground='#5DE0DC')
            calltipwindow.createToolTip(self.fsub_label, "Choose an option here if you only want to see articles"
                                                              " that are more objectively or subjectively written")
            self.var2 = IntVar()
            self.var2.set(1)
            self.fsub_nv = Radiobutton(self, text="Don't Care", variable=self.var2, value=1, background='#282828', foreground='#5DE0DC')
            calltipwindow.createToolTip(self.fsub_nv, "Select this if you want all articles returned regarless of how they are written.")
            self.fsub_gt = Radiobutton(self, text='More Subjective', variable=self.var2, value=2, background='#282828', foreground='#5DE0DC')
            calltipwindow.createToolTip(self.fsub_gt, "Select this if you only want articles that are more subjectively written.")
            self.fsub_lt = Radiobutton(self, text='More Objective', variable=self.var2, value=3, background='#282828', foreground='#5DE0DC')

            calltipwindow.createToolTip(self.fsub_lt, "Select this if you only want articles that are more objectively written.")
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

            calltipwindow.createToolTip(self.fD_label, "Narrow your results to articles published in the dates here.")
            calltipwindow.createToolTip(self.fD_format, "Narrow your results to articles published in the dates here.")
            calltipwindow.createToolTip(self.fD_beinlab, "Narrow your results to articles published in the dates here.")
            calltipwindow.createToolTip(self.fD_endlab, "Narrow your results to articles published in the dates here.")
            calltipwindow.createToolTip(self.fD_ent, "Enter Start Date here.")
            calltipwindow.createToolTip(self.fD_ent2, "Enter End Date here.")



        # window placements
            #appearing labael
            offset=100
            self.appearing_label.place(x=400, y=380+offset)
            #appearing pick
            self.box.place(x=510, y=380+offset)
            #author label
            self.author_label.place(x=400, y=405+offset)
            #author entry
            self.author_entry.place(x=510, y=405+offset)
            #subjectivity
            self.fsub_label.place(x=400, y=430+offset)
            self.fsub_nv.place(x=510, y=430+offset)
            self.fsub_gt.place(x=510, y=455+offset)
            self.fsub_lt.place(x=510, y=480+offset)

            #date
            self.fD_label.place(x=400, y=505+offset)
            self.fD_format.place(x=440, y=507+offset)
            self.fD_beinlab.place(x=510, y=505+offset)
            self.fD_ent.place(x=555, y=505+offset)
            self.fD_endlab.place(x=590, y=505+offset)
            self.fD_ent2.place(x=625, y=505+offset)

            # if the button gets unchecked it will destroy the labels and entry widgets.
        elif self.var.get() is 0:
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
    # does just that clears some
    def clearstuff(self):
        # check to see if the lables and entry boxes exist from a previous search options
        # if they do then destroy them then create the new search label and entry box
        self.ent_keyword.destroy()
        self.check_filter.destroy()
        self.but_search.destroy()
        if hasattr(self, 'appearing_label'):
            # self.ent_keyword.destroy()
            # self.check_filter.destroy()
            # self.but_search.destroy()
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
        self.ent_keyword.place(relx=.5, rely=.5, anchor=CENTER)
        self.check_filter.place(relx=.495, rely=.6, relheight=.059, anchor=E)
        self.but_search.place(relx=.505, rely=.6, anchor=W)
        if self.var.get() == 1:
            # window placements
            # appearing labael
            offset = 100
            self.appearing_label.place(x=400, y=380+offset)
            # appearing pick
            self.box.place(x=510, y=380+offset)
            # author label
            self.author_label.place(x=400, y=405+offset)
            # author entry
            self.author_entry.place(x=510, y=405+offset)
            # subjectivity
            self.fsub_label.place(x=400, y=430+offset)
            self.fsub_nv.place(x=510, y=430+offset)
            self.fsub_gt.place(x=510, y=455+offset)
            self.fsub_lt.place(x=510, y=480+offset)

            # date
            self.fD_label.place(x=400, y=505+offset)
            self.fD_format.place(x=440, y=507+offset)
            self.fD_beinlab.place(x=510, y=505+offset)
            self.fD_ent.place(x=555, y=505+offset)
            self.fD_endlab.place(x=590, y=505+offset)
            self.fD_ent2.place(x=625, y=505+offset)

    #hides the widgets to display the search results
    def hidestuff(self):
        self.ent_keyword.place_forget()
        self.check_filter.place_forget()
        self.but_search.place_forget()
        if self.var.get() == 1:
            # self.ent_keyword.place(x=(-100), y=(-100))
            # self.check_filter.place(x=(-100), y=(-100))
            # self.but_search.place(x=(-100), y=(-100))
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
    # adding comment
    #search for that almighty data mine.
    def oldsearch(self):
        self.searchprogress = Progressbar(self, orient="horizontal", style='mongo.Horizontal.TProgressbar', length=700,
                                          mode="indeterminate")
        self.searchprogress.place(relx=.5, rely=.8, anchor=CENTER)
        self.searchprogress.start()
        self.proglabel = Label(self, text="Fetching Results...", font="Times 14", bg="#282828", fg="#FFFFFF")
        self.proglabel.place(relx=.5, rely=.765, anchor=CENTER)
        # queue to share between gui and threads
        q = queue.Queue()
        self.data = SearchFrame.content
        # make sure search didn't time out
        if self.data != "ReadTimeout":
            # change label info to next task
            self.proglabel.config(text="Analyzing Data...")
            self.update()

            self.sf2 = Frame(self, width=550, height=150, style='My.TFrame')
            self.sf2['relief'] = 'sunken'

            self.master.master.updateque.queue.clear()

            # start thread to analyze data and repeat process
            analysisthread = ResultsAnalysisThread(self.data, self.master.master.analyzer, q, self.resultTopics)
            analysisthread.start()
            self.processingloop('percent')
            self.processingloop('dots')

            # stop the progress bar
            self.searchprogress.stop()

            self.hidestuff()
            style = Style(self)
            style.configure("Treeview", rowheight=30)
            self.tree = Treeview(self)
            self.tree.heading('#0', text='Results by Title')
            self.tree.column('#0', stretch=True)
            self.tree.place(relx=.3, relheight=1, relwidth=.7)

            # sunken box that topics print out into
            self.style = Style()
            self.style.configure('My.TFrame', background='#383838')

            # frame for individual analysis
            self.sf = Frame(self, width=550, height=150, style='My.TFrame')
            self.sf['relief'] = 'sunken'
            self.sf.place(relx=0, rely=.055, relwidth=.3, relheight=.4)

            # labels for article topics
            self.topicsHead = Label(self, text='Key Article Subjects', font="times 16 underline", background='#282828',
                                    foreground='#5DE0DC')
            calltipwindow.createToolTip(self.topicsHead, "These are a few subjects that were mentioned in the article")
            self.topics = Label(self, text='Click on an article to see more info', wraplength=500, font='times 14',
                                background='#383838', foreground='#5DE0DC', anchor=W, justify=LEFT)

            self.topicsHead.place(relx=.01, rely=.01, relwidth=.28)
            self.topics.place(relx=.01, rely=.065, relwidth=.28)

            # frame for results analysis
            self.sf2.place(relx=0, rely=.51, relwidth=.3, relheight=.4)

            self.resultTopicHead = Label(self, text='Most Mentioned Phrases in Results', font="times 16 underline",
                                         background='#282828', foreground='#5DE0DC')
            calltipwindow.createToolTip(self.resultTopicHead,
                                        "These are the most mentioned phrases in the resulting articles.")

            self.resultTopicHead.place(relx=.01, rely=.465, relwidth=.28)
            self.resultTopics.place(relx=.01, rely=.52, relwidth=.28)

            # New Search Edit Search Save Search
            self.new_search = Button(self, text='New Search', background='#383838', foreground='#5DE0DC',
                                     font=("Veranda 14"), command=self.NewSearch)


            for item in self.data:
                # remove BOM images first from body >uffff
                item['body'] = ''.join(c for c in unicodedata.normalize('NFC', item['body']) if c <= '\uFFFF')
                self.tree.insert('', 'end', text=item['title'], values=(item['uri'], item['body'], item['title'],
                                                                        item['author'],
                                                                        parser.parse(item['date']).strftime(
                                                                            '%B, %d, %Y')), tag='data')
            self.tree.tag_configure('data', font='Verdana 14')
            self.tree.bind('<Double-1>', self.on_click)
            self.tree.bind('<<TreeviewSelect>>', self.on_single_click)
            self.new_search.place(relx=0, rely=.95, relwidth=.1, relheight=.05, anchor=NW)
        self.searchprogress.destroy()
        self.proglabel.destroy()


    def search(self, url):
        self.searchprogress = Progressbar(self, orient="horizontal", style='mongo.Horizontal.TProgressbar', length=700, mode="indeterminate")
        self.searchprogress.place(relx=.5, rely=.8, anchor=CENTER)
        self.searchprogress.start()

        self.proglabel = Label(self, text="Fetching Results...", font="Times 14", bg="#282828", fg="#FFFFFF")
        self.proglabel.place(relx=.5, rely=.765, anchor=CENTER)

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

        # queue to share between gui and threads
        q = queue.Queue()

        #if SearchFrame.content == None:
        # start thread to get data from url
        thread = GetDataThread(url, q)
        thread.start()

        # wait until thread is done, then get data from queue
        self.updateuntildata(q, self.searchprogress)
        self.data = q.get(0)
        SearchFrame.content = self.data


        # make sure search didn't time out
        if self.data != "ReadTimeout":
            # change label info to next task
            self.proglabel.config(text="Analyzing Data...")
            self.update()

            self.master.master.updateque.queue.clear()

            # start thread to analyze data and repeat process
            self.analysisthread = ResultsAnalysisThread(self.data, self.master.master.analyzer, q, self.resultTopics)
            self.analysisthread.start()

            self.processingloop('percent')
            self.processingloop('dots')

            # stop the progress bar
            self.searchprogress.stop()

            self.hidestuff()
            style = Style(self)
            style.configure("Treeview", rowheight=30)
            self.tree = Treeview(self)
            self.tree.heading('#0', text='Results by Title')
            self.tree.column('#0', stretch=True)
            self.tree.place(relx=.3, relheight=1, relwidth=.7)

            self.sf.place(relx=0, rely=.055, relwidth=.3, relheight=.4)

            self.topicsHead.place(relx=.01, rely=.01, relwidth=.28)
            self.topics.place(relx=.01, rely=.065, relwidth=.28)


            # frame for results analysis
            self.sf2.place(relx=0, rely=.51, relwidth=.3, relheight=.4)


            self.resultTopicHead.place(relx=.01, rely=.465, relwidth=.28)
            self.resultTopics.place(relx=.01, rely=.52, relwidth=.28)


            # New Search Edit Search Save Search
            self.new_search = Button(self, text='New Search', background='#383838', foreground='#5DE0DC',
                                     font=("Veranda 14"), command=self.NewSearch)
            self.edit_search = Button(self, text='Edit Search', background='#383838', foreground='#5DE0DC',
                                      font=("Veranda 14"), command=self.EditSearch)
            self.save_search = Button(self, text='Save Search', background='#383838', foreground='#5DE0DC',
                                      font=("Veranda 14"), command=self.saveMenu)

            if self.data:
                for item in self.data:
                    # remove BOM images first from body >uffff
                    item['body'] = ''.join(c for c in unicodedata.normalize('NFC', item['body']) if c <= '\uFFFF')
                    self.tree.insert('', 'end', text=item['title'], values=(item['uri'], item['body'], item['title'],
                                                                            item['author'],
                                                                            parser.parse(item['date']).strftime(
                                                                                '%B, %d, %Y')), tag='data')

                self.tree.tag_configure('data', font='Verdana 14')
                self.tree.bind('<Double-1>', self.on_click)
                self.tree.bind('<<TreeviewSelect>>', self.on_single_click)


                self.new_search.place(relx=0, rely=.95, relwidth=.1, relheight=.05, anchor=NW)
                self.edit_search.place(relx=.1, rely=.95, relwidth=.1, relheight=.05, anchor=NW)
                self.save_search.place(relx=.2, rely=.95, relwidth=.1, relheight=.05, anchor=NW)

            else:
                self.edit_search = Button(self, text='Edit Search', background='#383838', foreground='#5DE0DC',
                                          command=self.EditSearch)
                self.edit_search.place(x=1, y=675)
                self.topics.config(text='No Articles Matching Search')
                self.resultTopics.config(text='')

        else:
            messagebox.showerror("Too Broad", "Search is too broad. Try refining with filters.")
            self.ent_keyword.focus_set()

        self.searchprogress.destroy()
        self.proglabel.destroy()

    def NewSearch(self):
        self.analysisthread.stopthread()
        self.deletesearch()
        self.searchwindow()


    def EditSearch(self):
        self.analysisthread.stopthread()
        self.deletesearch()
        self.undohide()

    def saveMenu(self):
        # create main directory and subdir(current date) if not made already
        path = os.getcwd() + "/Sessions/" + str(datetime.date.today())
        if not os.path.exists(path):
            os.makedirs(path)
        # get a filename from the user or default to current time
        currentTime = datetime.datetime.now().strftime("%H_%M_%S")

        filename = filedialog.asksaveasfilename(defaultextension="txt", initialdir=path, initialfile=currentTime)
        if filename:
            self.saveFilename = filename
            with open(filename, 'w') as outfile:
                json.dump(self.data, outfile)
            # with open(filename, 'w') as f:
            #     f.write("Testing Save As/No Current Save")


    #defind clear search
    def deletesearch(self):
        self.tree.destroy()
        self.sf.place_forget()
        self.topicsHead.place_forget()
        self.topics.place_forget()
        self.sf2.place_forget()
        self.resultTopicHead.place_forget()
        self.resultTopics.place_forget()
        self.new_search.destroy()
        try:
            self.edit_search.destroy()
            self.save_search.destroy()
        except AttributeError:
            return

    #on click gets the articles information and displays it in the Key Article Subjects window
    def on_single_click(self, event):
        self.topicsHead.config(text="Key Article Subjects")
        item = self.tree.item(self.tree.selection()[0], 'values')
        topicStr = '\n\n'.join(['\n'.join(textwrap.wrap('*' + phrase[0], width=33)) for phrase in
                                self.master.master.analyzer.getMostCommonNounPhrases(5, [item[1]], threading.Event())])
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

        makemenu.ArticleMenu(tw, tb, self.n)

        tb.insert('end', self.n[1])
        tb.config(state=DISABLED)
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

    def updateuntildata(self, q, progress):
        while q.empty():
            time.sleep(.01)
            progress.step(1)
            progress.master.update()

    def processingloop(self, updatetype):
        string = self.resultTopics.cget('text')
        if len(string) and string[0] == 'P':
            if updatetype == 'percent':
                if not self.master.master.updateque.empty():
                    string = "{}({}%)".format(re.search('Processing Data(\.|\s)*', string).group(0), str(self.master.master.updateque.get(0)))
                    self.after(300, lambda: self.processingloop('percent'))
                else:
                    self.after(100, lambda: self.processingloop('percent'))
            elif updatetype == 'dots':
                numdots = len(string.split('.')) % 4
                string = "Processing Data" + numdots * '.' + (3 - numdots) * ' ' + re.search('\(.+\)', string).group(0)
                self.after(300, lambda: self.processingloop('dots'))

        self.resultTopics.config(text=string)

class StartFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #container = Frame(self)
        self.controller = controller  # set the controller
        self.title = "CySpyder"              #ttile of the window
        path = os.getcwd() + '\\resources\spiderweb2.jpg'
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
        self.wl= Label(self, text='WELCOME', width=15, font='bold')
        self.wl.configure(background='#434343', foreground='#06c8e6')
        self.ns = Label(self, text='-New Session-', width=24, height=1)
        self.ns.configure(height=2, background='#828282', foreground='#06c8e6')
        self.ns.bind('<1>', self.start)
        self.rs = Label(self, text='Restore Search', width=28,height=2)
        self.rs.configure(background='#434343', foreground='#06c8e6')
        #window placements
        self.sf.place(x=298, y=162)
        self.wl.place(x=310,y=165)
        self.ns.place(x=300, y= 200)
        self.rs.place(x=0, relwidth=.25)
        self.menutree.place(x=0,y=10, relwidth=.25, relheight=.96)
        self.progress.place(y=440)

        self.bytes = 0
        self.maxbytes = 0
        self.openMenu()

    def openMenu(self):
        # set initial directory to savedScans folder
        path = os.path.join(os.getcwd(), "Sessions")
        filenames = os.listdir(path)

        for file in filenames:
            filetoprint = file.replace('2017-', '')
            self.menutree.insert('', 'end', text=filetoprint, tags='date')
            self.menutree.tag_configure('date', background='grey', foreground='yellow', font='bold, 10')
            path= os.path.join(os.getcwd(), 'Sessions'+'\\'+file)
            psr = os.listdir(path)
            for f in psr:
                filetoprint = f.replace('.txt', '')
                filetosend = f#.replace(' ', '')
                self.menutree.insert('', 'end', text='  -'+filetoprint, values=(file,filetosend), tags='article')
                self.menutree.tag_configure('article', background='#434343', foreground='#06c8e6')
            self.menutree.bind('<<TreeviewSelect>>', self.onmenuclick)

        #fill tree with greay past files
        for i in range(1,20):
            self.menutree.insert('', 'end', text='', tags='clean')
            self.menutree.tag_configure('clean', background='#434343')

    def onmenuclick(self, event):
        item = self.menutree.item(self.menutree.selection()[0], 'values')
        path = 'Sessions'+'\\'+item[0]+'\\'+item[1]
        with open(path, "r") as fin:
            SearchFrame.content = json.load(fin)
        #print(SearchFrame.content)
        xoffset = int(self.winfo_screenwidth() / 2 - 1280 / 2)
        yoffset = int(self.winfo_screenheight() / 2 - 800 / 2)
        self.controller.geometry("%dx%d+%d+%d" % (1100, 700, xoffset, yoffset))  # set geometry of window
        self.controller.show_frame('SearchFrame')
        self.master.master.analyzer.loadSpacy()
        self.master.master.frames['SearchFrame'].hidestuff()
        self.master.master.frames['SearchFrame'].oldsearch()

    def start(self, event):
        if analysis.Analyzer.nlp == None:
            self.progress["value"] = 0
            self.maxbytes = 50000
            self.progress["maximum"] = 50000
            #analysis.Analyzer.nlp
            self.master.master.analyzer.loadSpacy()
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

class GetDataThread(threading.Thread):
    def __init__(self, url, q):
        threading.Thread.__init__(self)
        self.queue = q
        self.url = url
    def run(self):
        try:
            data = requests.get(self.url, timeout=10).json()
            self.queue.put(data)
        except requests.exceptions.ReadTimeout:
            self.queue.put(requests.exceptions.ReadTimeout.__name__)

class ResultsAnalysisThread(threading.Thread):
    def __init__(self, data, analyzer, q, widget):
        threading.Thread.__init__(self)
        self.queue = q
        self.data = data
        self.analyzer = analyzer
        self.widget = widget
        self.stop = threading.Event()
    def run(self):
        results = '\n\n'.join(
            ['\n'.join(textwrap.wrap('*({}): '.format(phrase[1]) + str(phrase[0]), width=33)) for phrase in
             self.analyzer.getMostCommonNounPhrases(5, [item['body'] for item in self.data], self.stop)])
        try:
            self.widget.config(text=results)
        except TclError:
            pass
    def stopthread(self):
        self.stop.set()

if __name__ == "__main__":
    app = cyberapi()
    app.mainloop()