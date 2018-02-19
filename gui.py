import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

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
        tk.Button(self, text="Receptionists", font=f,command=lambda: controller.show_frame("RecepMain"),
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

        f = tkfont.Font(family='Calibri', size=10)
        tk.Label(self, text="Select the beginning date of the new schedule", font=f).pack(pady=(15, 0))

        def print_sel():
            start_date = cal.selection_get()
            print("Start date is {}".format(start_date))

        #top = tk.Toplevel(app)
        #cal = Calendar(app, font="Arial 14").pack()
        #cal = DateEntry(self, width=8, background='darkblue', foreground='white', borderwidth=2).pack()
        #date_button = ttk.Button(self, text="ok", command=print_sel)
        #date_button.pack()

        wks = StringVar(self)
        wks.set("4")  # initial value

        tk.Label(self, text="Total number of weeks to generate?").pack()
        OptionMenu(self, wks, "1", "2", "3", "4", "5").pack()

        sat1tech1 = StringVar(self)
        sat1tech1.set("Bobby")
        sat1tech2 = StringVar(self)
        sat1tech2.set("Bobby")

        tk.Label(self, text="Which techs to work 1st Saturday?").pack()
        sat1 = OptionMenu(self, sat1tech1, "Bobby", "Suzy", "Jenna", "Amy")
        sat1.pack(padx=5, pady=10, side=LEFT)
        sat1 = OptionMenu(self, sat1tech2, "Bobby", "Suzy", "Jenna", "Amy")
        sat1.pack(padx=5, pady=10, side=LEFT)
        def ok():
            print("value is {}".format(wks.get()))
            self.quit()

        tk.Button(self, text="Get week count", command=ok).pack()

        tk.Button(self, text='Go Back', command=lambda: controller.show_frame('StartPage')).pack(pady=20)


# if __name__ == "__main__":

app = ScheduleBuilder()
app.title("CRAH Schedule Builder")
app.geometry("420x500")
ttk.Style(app).theme_use('clam')
app.mainloop()