import xlsxwriter
import random
import linecache
from acts import *
from receptionists import *

# Read employee names from file
line = linecache.getline('employees.txt', 8)
techs = [x.strip() for x in line.split(',')]

workbook = xlsxwriter.Workbook('tech_schedule.xlsx')
worksheet = workbook.add_worksheet('Techs')
worksheet.set_landscape()
worksheet.set_default_row(12)

'''
Bold Times New Roman formatting
border = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'border': 1})
border.set_align('vcenter')
fill = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'bg_color': 'gray', 'border': 1})
fill.set_align('vcenter')
msg_format = workbook.add_format({'font_size': 16, 'font_name': 'Times New Roman', 'bold': 1, 'align': 'center'})
'''

border = workbook.add_format({'font_size': 8, 'border': 1})
border.set_align('vcenter')
fill = workbook.add_format({'font_size': 8, 'bg_color': 'gray', 'border': 1})
fill.set_align('vcenter')
msg_format = workbook.add_format({'font_size': 16, 'bold': 1, 'align': 'center'})

# Generate full week
def tech_week(num, sat_worker, sat_worker2):
    # Set hours to zero before starting running total
    tech_hours = [0] * len(techs)

    # Read in shifts to be assigned
    f = open("config/techs/mon_shifts.txt", "r")
    shifts = f.readline()
    mon_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    mon_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()

    f = open("config/techs/tue_shifts.txt", "r")
    shifts = f.readline()
    tue_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    tue_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()

    f = open("config/techs/wed_shifts.txt", "r")
    shifts = f.readline()
    wed_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    wed_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()

    adjust = 0
    for i in range(len(wed_shifts)):
        if wed_hours[i-adjust] <= 5.0:
            wed_half = wed_shifts[i]
            wed_half_hours = wed_hours[i]
            wed_shifts.remove(wed_shifts[i])
            wed_hours.remove(wed_hours[i])
            adjust += 1

    f = open("config/techs/thu_shifts.txt", "r")
    shifts = f.readline()
    thu_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    thu_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()
    for i in range(len(thu_shifts)):
        if thu_hours[i] <= 5:
            thu_half = thu_shifts[i]
            thu_half_hours = thu_hours[i]
            thu_shifts.remove(thu_shifts[i])
            thu_hours.remove(thu_hours[i])

    f = open("config/techs/fri_shifts.txt", "r")
    shifts = f.readline()
    fri_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    fri_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()

    f = open("config/techs/sat_shifts.txt", "r")
    shifts = f.readline()
    sat_shifts = [x.strip() for x in shifts.split(',')]
    hours = f.readline()
    sat_hours = [float(x.strip()) for x in hours.split(',')]
    f.close()

    for x in range(4):
        if sat_worker == techs[x]:
            sat_worker = x
        if sat_worker2 == techs[x]:
            sat_worker2 = x

    # Shuffle shifts for random assignments
    combo = list(zip(mon_shifts, mon_hours))
    random.shuffle(combo)
    mon_shifts, mon_hours = zip(*combo)

    combo = list(zip(tue_shifts, tue_hours))
    random.shuffle(combo)
    tue_shifts, tue_hours = zip(*combo)

    combo = list(zip(wed_shifts, wed_hours))
    random.shuffle(combo)
    wed_shifts, wed_hours = zip(*combo)

    combo = list(zip(thu_shifts, thu_hours))
    random.shuffle(combo)
    thu_shifts, thu_hours = zip(*combo)

    combo = list(zip(fri_shifts, fri_hours))
    random.shuffle(combo)
    fri_shifts, fri_hours = zip(*combo)

    # combo = list(zip(sat_shifts, sat_hours))
    # random.shuffle(combo)
    # sat_shifts, sat_hours = zip(*combo)

    sat_list = [sat_worker, sat_worker2]
    random.shuffle(sat_list)
    wed_half_tech = sat_list[0]
    thu_half_tech = sat_list[1]

    i, j, k = 0, 0, 0
    first_row = (num * (len(techs)+2)) - (len(techs))
    for x in range(4):
        # Vet tech names
        worksheet.write(first_row + x, 0, ' ' + techs[x], border)

        # Monday
        worksheet.write(first_row + x, 1, mon_shifts[x], border)
        tech_hours[x] += mon_hours[x]

        # Tuesday
        worksheet.write(first_row + x, 2, tue_shifts[x], border)
        tech_hours[x] += tue_hours[x]

        # Wednesday
        if x != wed_half_tech:
            worksheet.write(first_row + x, 3, wed_shifts[i], border)
            tech_hours[x] += wed_hours[i]
            i += 1
        else:
            worksheet.write(first_row + x, 3, wed_half, border)
            tech_hours[x] += wed_half_hours

        # Thursday
        if x != thu_half_tech:
            worksheet.write(first_row + x, 4, thu_shifts[j], border)
            tech_hours[x] += thu_hours[j]
            j += 1
        else:
            worksheet.write(first_row + x, 4, thu_half, border)
            tech_hours[x] += thu_half_hours

        # Friday
        worksheet.write(first_row + x, 5, fri_shifts[x], border)
        tech_hours[x] += fri_hours[x]

        # Saturday
        if x != wed_half_tech and x != thu_half_tech:
            worksheet.write(first_row + x, 6, 'OFF', border)

    # Saturday continued
    if tech_hours[wed_half_tech] < tech_hours[thu_half_tech]:
        worksheet.write(first_row + wed_half_tech, 6, sat_shifts[0], border)
        tech_hours[wed_half_tech] += sat_hours[0]
        worksheet.write(first_row + thu_half_tech, 6, sat_shifts[1], border)
        tech_hours[thu_half_tech] += sat_hours[1]
    else:
        worksheet.write(first_row + wed_half_tech, 6, sat_shifts[1], border)
        tech_hours[wed_half_tech] += sat_hours[1]
        worksheet.write(first_row + thu_half_tech, 6, sat_shifts[0], border)
        tech_hours[thu_half_tech] += sat_hours[0]


    # Hours
    for x in range(4):
        worksheet.write(first_row + x, 7, tech_hours[x], border)


    worksheet.write(first_row + 4, 0, ' Floater', border)

    # Write ACT/receptionist floaters to tech schedule if ACT/receptionist schedule(s) have been generated
    if mon_assistants[num-1] != -1 and mon_helpers[num-1] != -1:
        worksheet.write(first_row + 4, 1, ' ' + mon_assistants[num - 1] + '/' + mon_helpers[num - 1], border)
    elif mon_assistants[num-1] != -1 and mon_helpers[num-1] == -1:
        worksheet.write(first_row + 4, 1, ' ' + mon_assistants[num - 1], border)
    elif mon_assistants[num-1] == -1 and mon_helpers[num-1] != -1:
        worksheet.write(first_row + 4, 1, ' ' + mon_helpers[num - 1], border)
    else:
        worksheet.write(first_row + 4, 1, None, border)

    if tue_assistants[num - 1] != -1 and tue_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 2, ' ' + tue_assistants[num - 1] + '/' + tue_helpers[num - 1], border)
    elif tue_assistants[num - 1] != -1 and tue_helpers[num - 1] == -1:
        worksheet.write(first_row + 4, 2, ' ' + tue_assistants[num - 1], border)
    elif tue_assistants[num - 1] == -1 and tue_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 2, ' ' + tue_helpers[num - 1], border)
    else:
        worksheet.write(first_row + 4, 2, None, border)

    if wed_assistants[num - 1] != -1 and wed_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 3, ' ' + wed_assistants[num - 1] + '/' + wed_helpers[num - 1], border)
    elif wed_assistants[num - 1] != -1 and wed_helpers[num - 1] == -1:
        worksheet.write(first_row + 4, 3, ' ' + wed_assistants[num - 1], border)
    elif wed_assistants[num - 1] == -1 and wed_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 3, ' ' + wed_helpers[num - 1], border)
    else:
        worksheet.write(first_row + 4, 3, None, border)

    if thu_assistants[num - 1] != -1 and thu_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 4, ' ' + thu_assistants[num - 1] + '/' + thu_helpers[num - 1], border)
    elif thu_assistants[num - 1] != -1 and thu_helpers[num - 1] == -1:
        worksheet.write(first_row + 4, 4, ' ' + thu_assistants[num - 1], border)
    elif thu_assistants[num - 1] == -1 and thu_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 4, ' ' + thu_helpers[num - 1], border)
    else:
        worksheet.write(first_row + 4, 4, None, border)

    if fri_assistants[num - 1] != -1 and fri_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 5, ' ' + fri_assistants[num - 1] + '/' + fri_helpers[num - 1], border)
    elif fri_assistants[num - 1] != -1 and fri_helpers[num - 1] == -1:
        worksheet.write(first_row + 4, 5, ' ' + fri_assistants[num - 1], border)
    elif fri_assistants[num - 1] == -1 and fri_helpers[num - 1] != -1:
        worksheet.write(first_row + 4, 5, ' ' + fri_helpers[num - 1], border)
    else:
        worksheet.write(first_row + 4, 5, None, border)

    worksheet.write(first_row + 4, 6, None, border)
    worksheet.write(first_row + 4, 7, None, border)


# Set up schedule template
def tech_template(month_str, day_str, total_weeks, msg):
    worksheet.set_column('B:G', 13)
    worksheet.set_column('H:H', 5.5)
    column_headers = [' Monday', ' Tuesday', ' Wednesday', ' Thursday', ' Friday', ' Saturday', ' Hours']
    worksheet.set_row(0, 15)
    for x in range(7):
        worksheet.write(0, x + 1, column_headers[x], border)

    # Remove leading zeros for month & day
    month_str = int(month_str)
    month_str = str(month_str)
    day_str = int(day_str)
    day_str = str(day_str)

    # Write calendar dates to appropriate cells
    for i in range(total_weeks):
        if month_str == '2':
            month_end = 28
        elif month_str == '4' or month_str == '6' or month_str == '9' or month_str == '11':
            month_end = 30
        else:
            month_end = 31

        for j in range(6):
            worksheet.write_blank(6*i+1, 0, None, fill)
            worksheet.write_blank(6*i+1, 7, None, fill)
            worksheet.write(6*i+1, j+1, ' ' + month_str + '/' + day_str, fill)
            month = int(month_str)
            day = int(day_str)
            if day == month_end:
                if month == 12:
                    month = 1
                else:
                    month += 1
                day = 1
            else:
                day += 1
            # Increment date an additional time for Sat -> Mon
            if j == 5:
                if day == month_end:
                    if month == 12:
                        month = 1
                    else:
                        month += 1
                    day = 1
                else:
                    day += 1
            month_str = str(month)
            day_str = str(day)

    if total_weeks > 4:
        worksheet.merge_range('A34:H35', msg, msg_format)
    else:
        worksheet.merge_range('A28:H29', msg, msg_format)
    workbook.close()
