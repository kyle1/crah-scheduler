import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
from PIL import ImageTk
# from tkcalendar import Calendar, DateEntry
from techs import *


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
            background='CadetBlue3', width=20).pack()
        tk.Button(self, text="Receptionists", font=f, command=lambda: controller.show_frame("RecepMain"),
            background='CadetBlue3', width=20).pack()
        tk.Button(self, text="Vet Techs", font=f, command=lambda: controller.show_frame("TechMain"),
            background='CadetBlue3', width=20).pack()


class ActMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="ACTs", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)


class RecepMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Receptionists", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)


class TechMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        f = tkfont.Font(family='Calibri', size=14, weight='bold')
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))

        tk.Label(self, text="Enter the beginning date of the new schedule").pack(pady=(10, 0))
        sdate = Entry(self, width=12, justify='center')
        sdate.pack(pady=(0, 20))
        sdate.delete(0, END)
        sdate.insert(0, "MM/DD")


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
        s5t1 = StringVar(self)
        s5t2 = StringVar(self)
        techs = ['Bobby', 'Suzy', 'Jenna', 'Amy']
        tk.Label(self, text="Select which techs to work on the following Saturdays:").pack(pady=20)
        for x in range(5):
            tk.Label(self, text=x+1).place(x=85, y=213+(30*x))
        OptionMenu(self, s1t1, *techs).place(width=100, x=105, y=208)
        OptionMenu(self, s1t2, *techs).place(width=100, x=205, y=208)
        OptionMenu(self, s2t1, *techs).place(width=100, x=105, y=238)
        OptionMenu(self, s2t2, *techs).place(width=100, x=205, y=238)
        OptionMenu(self, s3t1, *techs).place(width=100, x=105, y=268)
        OptionMenu(self, s3t2, *techs).place(width=100, x=205, y=268)
        OptionMenu(self, s4t1, *techs).place(width=100, x=105, y=298)
        OptionMenu(self, s4t2, *techs).place(width=100, x=205, y=298)
        OptionMenu(self, s5t1, *techs).place(width=100, x=105, y=328)
        OptionMenu(self, s5t2, *techs).place(width=100, x=205, y=328)

        tk.Label(self, text="Append message to schedule?").pack(pady=(145, 0))
        msg = Entry(self, width=30, justify='center')
        msg.pack()
        msg.delete(0, END)
        msg.insert(0, '')

        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)

        # Really need to figure out a better way to pass the selected menu options...
        tk.Button(self, text='Generate', font=f, background='CadetBlue3',
                command=lambda: test(sdate.get(), s1t1.get(), s1t2.get(), s2t1.get(), s2t2.get(), s3t1.get(), s3t2.get(), s4t1.get(), s4t2.get(), wks.get(), msg.get())).place(x=159, y=435)

        def test(sdate, s1t1, s1t2, s2t1, s2t2, s3t1, s3t2, s4t1, s4t2, wks, msg):
            #print(msg)
            month_str = sdate[:2]
            day_str = sdate[3:]
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
            template(month_str, day_str, int(wks), msg)

# if __name__ == "__main__":
sat1tech1 = ''
app = ScheduleBuilder()
app.title("CRAH Schedule Builder")
app.geometry("420x500")
ttk.Style(app).theme_use('clam')
app.mainloop()