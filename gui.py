import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
# from tkcalendar import Calendar, DateEntry
from techs import *
from acts import *
from receptionists import *
import linecache


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
        tech_pages = [TechMain, TechSettings, TechMon, TechWed, TechThu, TechSat]
        other_pages = [StartPage, ActMain, RecepMain, ActSettings, RecepSettings]
        pages = tech_pages + other_pages
        #for F in (StartPage, ActMain, RecepMain, TechMain, ActSettings, RecepSettings, TechSettings):
        for F in pages:
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
        p1.pack(side="top", fill="x", pady=(30, 0))

        self.controller = controller
        label = tk.Label(self, text="Schedule Builder", font=controller.title_font)
        label['font'] = tkfont.Font(family='Calibri', size=22, weight='bold')
        label.pack(side="top", fill="x", pady=(30, 25))

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
        tk.Label(self, text="ACTs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)
        tk.Button(self, text='Settings', command=lambda: controller.show_frame("ActSettings")).place(x=460, y=10)

        tk.Label(self, text="Enter the beginning date of the new schedule").pack(pady=(10, 0))
        sdate = Entry(self, width=12, justify='center')
        sdate.pack(pady=(0, 20))
        sdate.delete(0, END)
        sdate.insert(0, "MM/DD")

        wks = StringVar(self)
        wks.set("4")
        tk.Label(self, text="Total number of weeks to generate:").pack(pady=(10, 0))
        OptionMenu(self, wks, "1", "2", "3", "4", "5").pack(pady=(0, 20))

        sat_acts = [[] for _ in range(5)]
        sun_acts = [[] for _ in range(5)]
        tk.Label(self, text="Select which ACTS to work on the following days:").pack(pady=20)
        tk.Label(self, text="Sunday").place(x=150, y=392)
        tk.Label(self, text="Saturday").place(x=376, y=392)

        for i in range(5):
            tk.Label(self, text='Week {}'.format(i+1)).place(x=25, y=247 + (30*i))

            for j in range(2):
                sun_acts[i].append(StringVar(self))
                OptionMenu(self, sun_acts[i][j], *acts).place(width=85, x=85+(85*j), y=242+(30*i))
            for k in range(3):
                sat_acts[i].append(StringVar(self))
                OptionMenu(self, sat_acts[i][k], *acts).place(width=85, x=275+(85*k), y=242+(30*i))

        tk.Label(self, text="Append message to schedule?").pack(pady=(180, 0))
        msg = Entry(self, width=30, justify='center')
        msg.pack()
        msg.delete(0, END)
        msg.insert(0, '')

        f = tkfont.Font(family='Calibri', size=14, weight='bold')
        #tk.Button(self, text='Generate', font=f, background='CadetBlue3',
        #          command=lambda: generate_acts()).pack(pady=(35, 0))
        tk.Button(self, text='Generate', font=f, background='CadetBlue3',
                  command=lambda: generate_acts()).pack(pady=(35, 0))

        def generate_acts():
            # Check that input for beginning schedule date is valid
            if len(sdate.get()) != 5 or sdate.get()[2] != '/':
                messagebox.showerror("Error", "Invalid date input. Please use MM/DD")
                return
            month_str = sdate.get()[:2]
            day_str = sdate.get()[3:]
            try:
                int(month_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date input. Please use MM/DD")
                return
            try:
                int(day_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date input. Please use MM/DD")
                return

            for x in range(int(wks.get())):
                # Check that an employee is selected for every shift
                for i in range(2):
                    if sun_acts[x][i].get() == '':
                        messagebox.showerror("Error", "Week {}: Not enough selections made".format(x+1))
                        return
                for j in range(3):
                    if sat_acts[x][j].get() == '':
                        print("Saturday Error!")
                        messagebox.showerror("Error", "Week {}: Not enough selections made".format(x+1))
                        return
                # Check that an employee isn't selected more than once for the same day
                if sun_acts[x][0].get() == sun_acts[x][1].get():
                    messagebox.showerror("Error", "Week {} Sunday: An ACT was selected more than once.".format(x+1))
                    return
                elif sat_acts[x][0].get() == sat_acts[x][1].get() or \
                    sat_acts[x][0].get() == sat_acts[x][2].get() or \
                        sat_acts[x][1].get() == sat_acts[x][2].get():
                            messagebox.showerror("Error", ("Week {} Saturday: An ACT was selected "
                                                           "more than once").format(x+1))
                            return

            # Check that no employees are selected for the weeks that will not be generated
            # NOT WORKING
            """"""
            if int(wks.get()) < 5:
                for x in range(int(wks.get()), 5):
                    for i in range(2):
                        if sun_acts[x][i].get() != '':
                            messagebox.showerror("Error", ("Week {}: Selection(s) made past number of "
                                                           "weeks set to be generated").format(x + 1))
                            return
                    for j in range(3):
                        if sat_acts[x][j].get() != '':
                            messagebox.showerror("Error", ("Week {}: Selection(s) made past number of "
                                                           "weeks set to be generated").format(x + 1))
                            return

            # No Errors found
            for x in range(int(wks.get())):
                act_week(x + 1, sun_acts[x][0].get(), sun_acts[x][1].get(),
                         sat_acts[x][0].get(), sat_acts[x][1].get(), sat_acts[x][2].get())
            act_template(month_str, day_str, int(wks.get()), msg.get())
            messagebox.showinfo("Success", "ACT schedule created!")


class RecepMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # f = tkfont.Font(family='Calibri', size=14, weight='bold')
        tk.Label(self, text="Receptionists", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)
        tk.Button(self, text='Settings', command=lambda: controller.show_frame("RecepSettings")).place(x=460, y=10)

        tk.Label(self, text="Enter the beginning date of the new schedule").pack(pady=(10, 0))
        sdate = Entry(self, width=12, justify='center')
        sdate.pack(pady=(0, 20))
        sdate.delete(0, END)
        sdate.insert(0, "MM/DD")

        wks = StringVar(self)
        wks.set("4")
        tk.Label(self, text="Total number of weeks to generate:").pack(pady=(10, 0))
        OptionMenu(self, wks, "1", "2", "3", "4", "5").pack(pady=(0, 20))

        sat_receps = [[] for _ in range(5)]
        tk.Label(self, text="Select which receptionists to work on the following Saturdays:").pack(pady=20)
        for i in range(5):
            tk.Label(self, text="Week {}".format(i + 1)).place(x=75, y=247+(30*i))
            for j in range(4):
                sat_receps[i].append(StringVar(self))
                OptionMenu(self, sat_receps[i][j], *receps).place(width=85, x=135+(85*j), y=242+(30*i))

        tk.Label(self, text="Append message to schedule?").pack(pady=(180, 0))
        msg = Entry(self, width=30, justify='center')
        msg.pack()
        msg.delete(0, END)
        msg.insert(0, '')

        f = tkfont.Font(family='Calibri', size=14, weight='bold')
        tk.Button(self, text='Generate', font=f, background='CadetBlue3',
                  command=lambda: generate_receps()).pack(pady=(35, 0))

        def generate_receps():
            month_str = sdate.get()[:2]
            day_str = sdate.get()[3:]

            for x in range(int(wks.get())):
                if (sat_receps[x][0].get() == sat_receps[x][1].get() or
                    sat_receps[x][0].get() == sat_receps[x][2].get() or
                    sat_receps[x][0].get() == sat_receps[x][3].get() or
                    sat_receps[x][1].get() == sat_receps[x][2].get() or
                    sat_receps[x][1].get() == sat_receps[x][3].get() or
                        sat_receps[x][2].get() == sat_receps[x][3].get()):
                        messagebox.showerror("Error",
                                             "Week {}: A receptionist was selected more than once.".format(x+1))
                        return
                else:
                    recep_week(x+1, sat_receps[x][0].get(), sat_receps[x][1].get(),
                               sat_receps[x][2].get(), sat_receps[x][3].get())
            recep_template(month_str, day_str, int(wks.get()), msg.get())
            messagebox.showinfo("Success", "Receptionist schedule created!")


class TechMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("StartPage")).place(x=10, y=10)
        tk.Button(self, text='Settings', command=lambda: controller.show_frame("TechSettings")).place(x=460, y=10)

        tk.Label(self, text="Enter the beginning date of the new schedule").pack(pady=(10, 0))
        sdate = Entry(self, width=12, justify='center')
        sdate.pack(pady=(0, 20))
        sdate.delete(0, END)
        sdate.insert(0, "MM/DD")

        wks = StringVar(self)
        wks.set("4")
        tk.Label(self, text="Total number of weeks to generate:").pack(pady=(10, 0))
        OptionMenu(self, wks, "1", "2", "3", "4", "5").pack(pady=(0, 20))

        sat_techs = [[] for _ in range(5)]
        tk.Label(self, text="Select which techs to work on the following Saturdays:").pack(pady=20)
        for i in range(5):
            tk.Label(self, text="Week {}".format(i+1)).place(x=160, y=247 + (30*i))
            for j in range(2):
                sat_techs[i].append(StringVar(self))
                OptionMenu(self, sat_techs[i][j], *techs).place(width=85, x=210+(85*j), y=242+(30*i))

        tk.Label(self, text="Append message to schedule?").pack(pady=(180, 0))
        msg = Entry(self, width=30, justify='center')
        msg.pack()
        msg.delete(0, END)
        msg.insert(0, '')

        f = tkfont.Font(family='Calibri', size=14, weight='bold')
        tk.Button(self, text='Generate', font=f, background='CadetBlue3',
                  command=lambda: generate_techs()).pack(pady=(35, 0))

        def generate_techs():
            month_str = sdate.get()[:2]
            day_str = sdate.get()[3:]
            for x in range(int(wks.get())):
                if sat_techs[x][0].get() == sat_techs[x][1].get():
                    messagebox.showerror("Error", "Week {}: Same vet tech selected twice.".format(x+1))
                    return
                else:
                    tech_week(x+1, sat_techs[x][0].get(), sat_techs[x][1].get())
            tech_template(month_str, day_str, int(wks.get()), msg.get())
            messagebox.showinfo("Success", "Vet tech schedule created!")


class ActSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="ACTs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("ActMain")).place(x=10, y=10)
        tk.Label(self, text="Hello!!!").pack(pady=(10, 0))


class RecepSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Receptionists", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("RecepMain")).place(x=10, y=10)
        tk.Label(self, text="Hello!!!").pack(pady=(10, 0))


class TechSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("TechMain")).place(x=10, y=10)
        tk.Label(self, text="Settings").pack(pady=(10, 0))

        tk.Label(self, text='Edit shifts:').place(x=50, y=120)
        tk.Button(self, text='Monday', width=12, command=lambda: controller.show_frame('TechMon')).place(x=50, y=150)
        tk.Button(self, text='Tuesday', width=12, command=lambda: controller.show_frame('TechMon')).place(x=50, y=180)
        tk.Button(self, text='Wednesday', width=12, command=lambda: controller.show_frame('TechWed')).place(x=50, y=210)
        tk.Button(self, text='Thursday', width=12, command=lambda: controller.show_frame('TechThu')).place(x=50, y=240)
        tk.Button(self, text='Friday', width=12, command=lambda: controller.show_frame('TechMon')).place(x=50, y=270)
        tk.Button(self, text='Saturday', width=12, command=lambda: controller.show_frame('TechSat')).place(x=50, y=300)

        tk.Label(self, text='Employees:').place(x=340, y=120)


class TechMon(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("TechSettings")).place(x=10, y=10)
        tk.Label(self, text="Monday shifts").pack(pady=(10, 0))

        # Read shifts from file
        shifts = linecache.getline('config/techs/mon_shifts.txt', 1)
        mon_tech_shifts = [x.strip() for x in shifts.split(',')]
        hours = linecache.getline('config/techs/mon_shifts.txt', 2)
        mon_tech_hours = [x.strip() for x in hours.split(',')]
        mon_tech_shifts_e = ['blah', 'blah2', 'blah3', 'blah4', 'blah5', 'blah6']
        mon_tech_hours_e = [0, 0, 0, 0, 0, 0]
        tk.Label(self, text="Shifts").place(x=160, y=100)
        tk.Label(self, text="Hours").place(x=330, y=100)
        for i in range(len(mon_tech_shifts)):
            mon_tech_shifts_e[i] = Entry(self, width=17)
            mon_tech_shifts_e[i].place(x=160, y=120+(30*i))
            mon_tech_shifts_e[i].delete(0, END)
            mon_tech_shifts_e[i].insert(0, mon_tech_shifts[i])

            mon_tech_hours_e[i] = Entry(self, width=4)
            mon_tech_hours_e[i].place(x=330, y=120+(30*i))
            mon_tech_hours_e[i].delete(0, END)
            mon_tech_hours_e[i].insert(0, mon_tech_hours[i])

        tk.Button(self, text="Save changes", command=lambda: save_tech_mon()).place(x=200, y=350)

        def save_tech_mon():
            f = open("config/techs/mon_shifts.txt", "w+")
            for i in range(4):
                if i < 3:
                    f.write(mon_tech_shifts_e[i].get() + ", ")
                else:
                    f.write(mon_tech_shifts_e[i].get() + "\n")

            for i in range(4):
                if i < 3:
                    f.write(mon_tech_hours_e[i].get() + ", ")
                else:
                    f.write(mon_tech_hours_e[i].get())
            f.close()
            messagebox.showinfo("Success", "Changes have been saved!")
            controller.show_frame("TechSettings")

class TechWed(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("TechSettings")).place(x=10, y=10)
        tk.Label(self, text="Wednesday shifts").pack(pady=(10, 0))

        # Read shifts from file
        shifts = linecache.getline('config/techs/wed_shifts.txt', 1)
        wed_tech_shifts = [x.strip() for x in shifts.split(',')]
        hours = linecache.getline('config/techs/wed_shifts.txt', 2)
        wed_tech_hours = [x.strip() for x in hours.split(',')]
        wed_tech_shifts_e = ['blah', 'blah2', 'blah3', 'blah4', 'blah5', 'blah6']
        wed_tech_hours_e = [0, 0, 0, 0, 0, 0]
        tk.Label(self, text="Shifts").place(x=160, y=100)
        tk.Label(self, text="Hours").place(x=330, y=100)
        for i in range(len(wed_tech_shifts)):
            wed_tech_shifts_e[i] = Entry(self, width=17)
            wed_tech_shifts_e[i].place(x=160, y=120 + (30 * i))
            wed_tech_shifts_e[i].delete(0, END)
            wed_tech_shifts_e[i].insert(0, wed_tech_shifts[i])

            wed_tech_hours_e[i] = Entry(self, width=4)
            wed_tech_hours_e[i].place(x=330, y=120 + (30 * i))
            wed_tech_hours_e[i].delete(0, END)
            wed_tech_hours_e[i].insert(0, wed_tech_hours[i])

        tk.Button(self, text="Save changes", command=lambda: save_tech_wed()).place(x=200, y=350)

        def save_tech_wed():
            f = open("config/techs/wed_shifts.txt", "w+")
            for i in range(4):
                if i < 3:
                    f.write(wed_tech_shifts_e[i].get() + ", ")
                else:
                    f.write(wed_tech_shifts_e[i].get() + "\n")

            for i in range(4):
                if i < 3:
                    f.write(wed_tech_hours_e[i].get() + ", ")
                else:
                    f.write(wed_tech_hours_e[i].get())
            f.close()
            messagebox.showinfo("Success", "Changes have been saved!")
            controller.show_frame("TechSettings")


class TechThu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("TechSettings")).place(x=10, y=10)
        tk.Label(self, text="Thursday shifts").pack(pady=(10, 0))

        # Read shifts from file
        shifts = linecache.getline('config/techs/thu_shifts.txt', 1)
        thu_tech_shifts = [x.strip() for x in shifts.split(',')]
        hours = linecache.getline('config/techs/thu_shifts.txt', 2)
        thu_tech_hours = [x.strip() for x in hours.split(',')]
        thu_tech_shifts_e = ['blah', 'blah2', 'blah3', 'blah4', 'blah5', 'blah6']
        thu_tech_hours_e = [0, 0, 0, 0, 0, 0]
        tk.Label(self, text="Shifts").place(x=160, y=100)
        tk.Label(self, text="Hours").place(x=330, y=100)
        for i in range(len(thu_tech_shifts)):
            thu_tech_shifts_e[i] = Entry(self, width=17)
            thu_tech_shifts_e[i].place(x=160, y=120 + (30 * i))
            thu_tech_shifts_e[i].delete(0, END)
            thu_tech_shifts_e[i].insert(0, thu_tech_shifts[i])

            thu_tech_hours_e[i] = Entry(self, width=4)
            thu_tech_hours_e[i].place(x=330, y=120 + (30 * i))
            thu_tech_hours_e[i].delete(0, END)
            thu_tech_hours_e[i].insert(0, thu_tech_hours[i])

        tk.Button(self, text="Save changes", command=lambda: save_tech_thu()).place(x=200, y=350)

        def save_tech_thu():
            f = open("config/techs/thu_shifts.txt", "w+")
            for i in range(4):
                if i < 3:
                    f.write(thu_tech_shifts_e[i].get() + ", ")
                else:
                    f.write(thu_tech_shifts_e[i].get() + "\n")

            for i in range(4):
                if i < 3:
                    f.write(thu_tech_hours_e[i].get() + ", ")
                else:
                    f.write(thu_tech_hours_e[i].get())
            f.close()
            messagebox.showinfo("Success", "Changes have been saved!")
            controller.show_frame("TechSettings")


class TechSat(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Vet Techs", font=controller.title_font).pack(side="top", fill="x", pady=(10, 0))
        tk.Button(self, text="<<", command=lambda: controller.show_frame("TechSettings")).place(x=10, y=10)
        tk.Label(self, text="Saturday shifts").pack(pady=(10, 0))

        # Read shifts from file
        shifts = linecache.getline('config/techs/sat_shifts.txt', 1)
        sat_tech_shifts = [x.strip() for x in shifts.split(',')]
        hours = linecache.getline('config/techs/sat_shifts.txt', 2)
        sat_tech_hours = [x.strip() for x in hours.split(',')]
        sat_tech_shifts_e = ['blah', 'blah2', 'blah3', 'blah4', 'blah5', 'blah6']
        sat_tech_hours_e = [0, 0, 0, 0, 0, 0]
        tk.Label(self, text="Shifts").place(x=160, y=100)
        tk.Label(self, text="Hours").place(x=330, y=100)
        for i in range(len(sat_tech_shifts)):
            sat_tech_shifts_e[i] = Entry(self, width=17)
            sat_tech_shifts_e[i].place(x=160, y=120 + (30 * i))
            sat_tech_shifts_e[i].delete(0, END)
            sat_tech_shifts_e[i].insert(0, sat_tech_shifts[i])

            sat_tech_hours_e[i] = Entry(self, width=4)
            sat_tech_hours_e[i].place(x=330, y=120 + (30 * i))
            sat_tech_hours_e[i].delete(0, END)
            sat_tech_hours_e[i].insert(0, sat_tech_hours[i])

        tk.Button(self, text="Save changes", command=lambda: save_tech_sat()).place(x=200, y=350)

        def save_tech_sat():
            f = open("config/techs/thu_shifts.txt", "w+")
            for i in range(4):
                if i < 3:
                    f.write(sat_tech_shifts_e[i].get() + ", ")
                else:
                    f.write(sat_tech_shifts_e[i].get() + "\n")

            for i in range(4):
                if i < 3:
                    f.write(sat_tech_hours_e[i].get() + ", ")
                else:
                    f.write(sat_tech_hours_e[i].get())
            f.close()
            messagebox.showinfo("Success", "Changes have been saved!")
            controller.show_frame("TechSettings")


# if __name__ == "__main__":
app = ScheduleBuilder()
app.title("CRAH Schedule Builder")
app.geometry("560x580")
ttk.Style(app).theme_use('clam')
app.resizable(width=False, height=False)
app.mainloop()
