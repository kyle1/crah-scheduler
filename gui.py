import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
# from tkcalendar import Calendar, DateEntry
from techs import *


# only needed for mac?
from PIL import ImageTk


class ScheduleBuilder(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames on top of each other,
        # then the one we want visible will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ActMain, RecepMain, TechMain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location; the one on the
            # top of the stacking order will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        logo = ImageTk.PhotoImage(file="crah.png")
        p1 = Label(self, image=logo)
        p1.image = logo
        p1.pack(side="top", fill="x", pady=(15, 0))

        self.controller = controller
        label = tk.Label(self, text="Schedule Builder", font=controller.title_font)
        label['font'] = tkfont.Font(family='Calibri', size=22, weight='bold')
        label.pack(side="top", fill="x", pady=(0, 15))

        f = tkfont.Font(family='Calibri', size=10, weight='bold')
        tk.Button(self, text="ACTs", font=f, command=lambda: controller.show_frame("ActMain"),
            background='DodgerBlue2', width=20).pack()
        tk.Button(self, text="Receptionists", font=f, command=lambda: controller.show_frame("RecepMain"),
            background='DodgerBlue2', width=20).pack()
        tk.Button(self, text="Vet Techs", font=f, command=lambda: controller.show_frame("TechMain"),
            background='DodgerBlue2', width=20).pack()


class ActMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="ACTs", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("StartPage")).pack()


class RecepMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Receptionists", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("StartPage")).pack()


class TechMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        f = tkfont.Font(family='Calibri', size=14, weight='bold')
        tk.Label(self, text="Vet Techs", font=f).pack(side="top", fill="x", pady=(10, 0))

        tk.Label(self, text="Select the beginning date of the new schedule").pack(pady=(15, 70))

        def print_sel():
            start_date = cal.selection_get()
            print("Start date is {}".format(start_date))

        wks = StringVar(self)
        wks.set("4")  # initial value

        tk.Label(self, text="Total number of weeks to generate:").pack()
        OptionMenu(self, wks, "1", "2", "3", "4", "5").pack()

        s1t1 = StringVar(self)
        s1t2 = StringVar(self)
        s2t1 = StringVar(self)
        s2t2 = StringVar(self)
        s3t1 = StringVar(self)
        s3t2 = StringVar(self)
        s4t1 = StringVar(self)
        s4t2 = StringVar(self)
        techs = ['Bobby', 'Suzy', 'Jenna', 'Amy']
        tk.Label(self, text="Select which techs to work on the following Saturdays:").pack(pady=20)
        for x in range(4):
            tk.Label(self, text=x+1).place(x=75, y=243+(30*x))
        OptionMenu(self, s1t1, *techs).place(width=100, x=105, y=240)
        OptionMenu(self, s1t2, *techs).place(width=100, x=205, y=240)
        OptionMenu(self, s2t1, *techs).place(width=100, x=105, y=270)
        OptionMenu(self, s2t2, *techs).place(width=100, x=205, y=270)
        OptionMenu(self, s3t1, *techs).place(width=100, x=105, y=300)
        OptionMenu(self, s3t2, *techs).place(width=100, x=205, y=300)
        OptionMenu(self, s4t1, *techs).place(width=100, x=105, y=330)
        OptionMenu(self, s4t2, *techs).place(width=100, x=205, y=330)

        tk.Button(self, text='< Go Back', command=lambda: controller.show_frame('StartPage')).place(x=30, y=420)

        # Really need to figure out a better way to pass the selected menu options...
        tk.Button(self, text='Generate schedule',
                command=lambda: test(s1t1.get(), s1t2.get(), s2t1.get(), s2t2.get(), s3t1.get(), s3t2.get(), s4t1.get(), s4t2.get(), wks.get())).place(x=220, y=420)

        def test(s1t1, s1t2, s2t1, s2t2, s3t1, s3t2, s4t1, s4t2, wks):
            sat_techs = [[] for i in range(5)]
            sat_techs[0].append(s1t1)
            sat_techs[0].append(s1t2)
            sat_techs[1].append(s2t1)
            sat_techs[1].append(s2t2)
            sat_techs[2].append(s3t1)
            sat_techs[2].append(s3t2)
            sat_techs[3].append(s4t1)
            sat_techs[3].append(s4t2)

            for i in range(int(wks)):
                week(i+1, sat_techs[i][0], sat_techs[i][1])
            template('3', '3', int(wks))

# if __name__ == "__main__":
sat1tech1 = ''
app = ScheduleBuilder()
app.title("CRAH Schedule Builder")
app.geometry("420x500")
ttk.Style(app).theme_use('clam')
app.mainloop()