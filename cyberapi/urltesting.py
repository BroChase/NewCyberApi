from tkinter import *
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter import messagebox
from pprint import pprint
import urllib.request
import json
import webbrowser


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
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        #Window Buttons
        self.but_titlesearch = Button(self, text='Search Title', width=30, command=self.tkwsearch,
                                      relief=RAISED, bd=4)
        self.but_titlebodysearch = Button(self, text='Search Title & Body', width=30, command=self.tbssearch,
                                         relief=RAISED, bd=4)

        #Formatting of the window
        self.but_titlesearch.grid(column=1, row =1)
        self.but_titlebodysearch.grid(column=1, row=2)
        self.grid_rowconfigure(3, weight=20)

#search by title
    def tkwsearch(self):
        self.ent_title = Entry(self, text='Title', width=30,bd=2)
        self.but_search = Button(self, text='Search', command=lambda: self.search(self.ent_title.get()))

        #window placement
        self.ent_title.grid(column=2, row=1)
        self.but_search.grid(column=3, row=1, sticky='N')
#todo search by title&body
    def tbssearch(self):
        print('hi')
#todo search by Date

#todo search by uri

    def search(self, title):
        url = 'http://cbrown686-test.apigee.net/cyberapi/articles?q=keywordtitle&title=' + title
        r = urllib.request.urlopen(url)
        data = json.load(r)
        self.tree = Treeview(self)
        self.tree.heading('#0', text='Title')
        self.tree.column('#0', stretch=True)
        self.tree.grid(column=4, row=1,rowspan=3, sticky='nsew')
        if data:
            for item in (data):
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

