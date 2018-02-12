import xlsxwriter
import random

workbook = xlsxwriter.Workbook('Schedule.xlsx')
worksheet = workbook.add_worksheet('Techs')

# Set up schedule template
worksheet.set_column('B:G', 12)
worksheet.set_column('H:H', 5.5)
border = workbook.add_format({'border': 1})
fill = workbook.add_format({'bg_color': 'silver', 'border': 1})
worksheet.write('B1', 'Thursday', border)
worksheet.write('C1', 'Friday', border)
worksheet.write('D1', 'Saturday', border)
worksheet.write('E1', 'Monday', border)
worksheet.write('F1', 'Tuesday', border)
worksheet.write('G1', 'Wednesday', border)
worksheet.write('H1', 'Hours', border)

# Shifts for each work day
mon_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']
tue_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 LM', '8-5:30 SP']
wed_shifts = ['7:30-5 SX', '8-5:30 JM', '8-5:30 SP']
thu_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM']
fri_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']
sat_shifts = ['7:30-12', '8-12']

# Read employee names from techs.txt
file = open("techs.txt","r")
employee1 = file.readline()
employee2 = file.readline()
employee3 = file.readline()
employee4 = file.readline()
file.close()

# Prompt user for first date of new schedule and total weeks to generate
start_date = input("Enter the first date of the new schedule (mm/dd): ")
month_str = start_date[:2]
day_str = start_date[3:]

if month_str == '02':
    month_end = 28
elif month_str == '04' or month_str == '06' or month_str == '09' or month_str == '11':
    month_end = 30
else:
    month_end = 31

total_weeks = int(input("Enter total number of weeks to generate (enter as digit): "))

# Thursday
def thu(first_row, sat_worker, sat_worker2, rand_num):
    random.shuffle(thu_shifts)
    i = 0
    if (sat_worker != '1' and sat_worker2 != '1') or (sat_worker == '1' and rand_num >= 0.5) or (sat_worker2 == '1' and rand_num < 0.5):
        worksheet.write(first_row, 1, thu_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row, 1, 'OFF', border)

    if (sat_worker != '2' and sat_worker2 != '2') or (sat_worker == '2' and rand_num >= 0.5) or (sat_worker2 == '2' and rand_num < 0.5):
        worksheet.write(first_row + 1, 1, thu_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row + 1, 1, 'OFF', border)

    if (sat_worker != '3' and sat_worker2 != '3') or (sat_worker == '3' and rand_num >= 0.5) or (sat_worker2 == '3' and rand_num < 0.5):
        worksheet.write(first_row + 2, 1, thu_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row + 2, 1, 'OFF', border)

    if (sat_worker != '4' and sat_worker2 != '4') or (sat_worker == '4' and rand_num >= 0.5) or (sat_worker2 == '4' and rand_num < 0.5):
        worksheet.write(first_row + 3, 1, thu_shifts[i], border)
    else:
        worksheet.write(first_row + 3, 1, 'OFF', border)

# Friday
def fri(first_row):
    random.shuffle(fri_shifts)
    worksheet.write(first_row, 2, fri_shifts[0], border)
    worksheet.write(first_row + 1, 2, fri_shifts[1], border)
    worksheet.write(first_row + 2, 2, fri_shifts[2], border)
    worksheet.write(first_row + 3, 2, fri_shifts[3], border)

# Saturday
def sat(first_row, sat_worker, sat_worker2):
    random.shuffle(sat_shifts)
    i = 0
    if sat_worker == '1' or sat_worker2 == '1':
        worksheet.write(first_row, 3, sat_shifts[i], border)
        if sat_shifts[i] == '8-12':
            worksheet.write_number(first_row, 7, 36, border)
        else: worksheet.write_number(first_row, 7, 36.5, border)
        i += 1
    else:
        worksheet.write(first_row, 3, 'OFF', border)
        worksheet.write_number(first_row, 7, 40, border)             # Hours

    if sat_worker == '2' or sat_worker2 == '2':
        worksheet.write(first_row + 1, 3, sat_shifts[i], border)
        if sat_shifts[i] == '8-12':
            worksheet.write_number(first_row + 1, 7, 36, border)
        else: worksheet.write_number(first_row + 1, 7, 36.5, border)
        i += 1
    else:
        worksheet.write(first_row + 1, 3, 'OFF', border)
        worksheet.write_number(first_row + 1, 7, 40, border)         # Hours

    if sat_worker == '3' or sat_worker2 == '3':
        worksheet.write(first_row + 2, 3, sat_shifts[i], border)
        if sat_shifts[i] == '8-12':
            worksheet.write_number(first_row + 2, 7, 36, border)
        else: worksheet.write_number(first_row + 2, 7, 36.5, border)
        i += 1
    else:
        worksheet.write(first_row + 2, 3, 'OFF', border)
        worksheet.write_number(first_row + 2, 7, 40, border)         # Hours

    if sat_worker == '4' or sat_worker2 == '4':
        worksheet.write(first_row + 3, 3, sat_shifts[i], border)
        if sat_shifts[i] == '8-12':
            worksheet.write_number(first_row + 3, 7, 36, border)
        else: worksheet.write_number(first_row + 3, 7, 36.5, border)
        i += 1
    else:
        worksheet.write(first_row + 3, 3, 'OFF', border)
        worksheet.write_number(first_row + 3, 7, 40, border)          # Hours

# Monday
def mon(first_row):
    random.shuffle(mon_shifts)
    worksheet.write(first_row, 4, mon_shifts[0], border)
    worksheet.write(first_row + 1, 4, mon_shifts[1], border)
    worksheet.write(first_row + 2, 4, mon_shifts[2], border)
    worksheet.write(first_row + 3, 4, mon_shifts[3], border)

# Tuesday
def tue(first_row):
    random.shuffle(tue_shifts)
    worksheet.write(first_row, 5, tue_shifts[0], border)
    worksheet.write(first_row + 1, 5, tue_shifts[1], border)
    worksheet.write(first_row + 2, 5, tue_shifts[2], border)
    worksheet.write(first_row + 3, 5, tue_shifts[3], border)

# Wednesday
def wed(first_row, sat_worker, sat_worker2, rand_num):
    random.shuffle(wed_shifts)
    i = 0
    if (sat_worker != '1' and sat_worker2 != '1') or (sat_worker == '1' and rand_num < 0.5) or (sat_worker2 == '1' and rand_num >= 0.5):
        worksheet.write(first_row, 6, wed_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row, 6, 'OFF', border)

    if (sat_worker != '2' and sat_worker2 != '2') or (sat_worker == '2' and rand_num < 0.5) or (sat_worker2 == '2' and rand_num >= 0.5):
        worksheet.write(first_row + 1, 6, wed_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row + 1, 6, 'OFF', border)

    if (sat_worker != '3' and sat_worker2 != '3') or (sat_worker == '3' and rand_num < 0.5) or (sat_worker2 == '3' and rand_num >= 0.5):
        worksheet.write(first_row + 2, 6, wed_shifts[i], border)
        i += 1
    else:
        worksheet.write(first_row + 2, 6, 'OFF', border)

    if (sat_worker != '4' and sat_worker2 != '4') or (sat_worker == '4' and rand_num < 0.5) or (sat_worker2 == '4' and rand_num >= 0.5):
        worksheet.write(first_row + 3, 6, wed_shifts[i], border)
    else:
        worksheet.write(first_row + 3, 6, 'OFF', border)

# Generate schedule for an entire pay week - MAKE LOOP?
def week(num, sat_worker, sat_worker2):
    if num == 1:
        start_row = 2
        worksheet.write('A3', employee1, border)
        worksheet.write('A4', employee2, border)
        worksheet.write('A5', employee3, border)
        worksheet.write('A6', employee4, border)
    elif num == 2:
        start_row = 7
        worksheet.write('A8', employee1, border)
        worksheet.write('A9', employee2, border)
        worksheet.write('A10', employee3, border)
        worksheet.write('A11', employee4, border)
    elif num == 3:
        start_row = 12
        worksheet.write('A13', employee1, border)
        worksheet.write('A14', employee2, border)
        worksheet.write('A15', employee3, border)
        worksheet.write('A16', employee4, border)
    elif num == 4:
        start_row = 17
        worksheet.write('A18', employee1, border)
        worksheet.write('A19', employee2, border)
        worksheet.write('A20', employee3, border)
        worksheet.write('A21', employee4, border)
    else:
        start_row = 22
        worksheet.write('A23', employee1, border)
        worksheet.write('A24', employee2, border)
        worksheet.write('A25', employee3, border)
        worksheet.write('A26', employee4, border)

    rando = random.random()
    thu(start_row, sat_worker, sat_worker2, rando)
    fri(start_row)
    sat(start_row, sat_worker, sat_worker2)
    mon(start_row)
    tue(start_row)
    wed(start_row, sat_worker, sat_worker2, rando)

for i in range(total_weeks):
    # Prompt user to enter Saturday workers for each pay week
    print("Which employees to work on Saturday of Week", i + 1, "?")
    sat_worker, sat_worker2 = input('1. {}2. {}3. {}4. {}\n'.format(employee1, employee2, employee3, employee4)).split()
    week(i + 1, sat_worker, sat_worker2)

    # Set up rows to contain the appropriate dates
    if i == 0:
        for j in range(6):
            worksheet.write_blank(1, 0, None, fill)
            worksheet.write_blank(1, 7, None, fill)
            worksheet.write(1, j + 1, month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                    day = 1
                else:
                    month += 1
                    day = 1
            else:
                day += 1

            # Increment an additional time for Sat -> Mon
            if j == 2:
                if day == month_end:
                    day = 1
                else:
                    day += 1

            month_str = str(month)
            day_str = str(day)

    if i == 1:
        for j in range(6):
            worksheet.write_blank(6, 0, None, fill)
            worksheet.write_blank(6, 7, None, fill)
            worksheet.write(6, j + 1, month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                    day = 1
                else:
                    month += 1
                    day = 1
            else:
                day += 1

            # Increment an additional time for Sat -> Mon
            if j == 2:
                if day == month_end:
                    day = 1
                else:
                    day += 1

            month_str = str(month)
            day_str = str(day)

    if i == 2:
        for j in range(6):
            worksheet.write_blank(11, 0, None, fill)
            worksheet.write_blank(11, 7, None, fill)
            worksheet.write(11, j + 1, month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                    day = 1
                else:
                    month += 1
                    day = 1
            else:
                day += 1

            # Increment an additional time for Sat -> Mon
            if j == 2:
                if day == month_end:
                    day = 1
                else:
                    day += 1

            month_str = str(month)
            day_str = str(day)

    if i == 3:
        for j in range(6):
            worksheet.write_blank(16, 0, None, fill)
            worksheet.write_blank(16, 7, None, fill)
            worksheet.write(16, j + 1, month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                    day = 1
                else:
                    month += 1
                    day = 1
            else:
                day += 1

            # Increment an additional time for Sat -> Mon
            if j == 2:
                if day == month_end:
                    day = 1
                else:
                    day += 1

            month_str = str(month)
            day_str = str(day)

    if i == 4:
        for j in range(6):
            worksheet.write_blank(21, 0, None, fill)
            worksheet.write_blank(21, 7, None, fill)
            worksheet.write(21, j + 1, month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                    day = 1
                else:
                    month += 1
                    day = 1
            else:
                day += 1

            # Increment an additional time for Sat -> Mon
            if j == 2:
                if day == month_end:
                    day = 1
                else:
                    day += 1

            month_str = str(month)
            day_str = str(day)

workbook.close()