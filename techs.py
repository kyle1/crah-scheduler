import xlsxwriter
import random
import linecache
from acts import *
from receptionists import *

# Shifts for each work day
mon_shifts = [' 7:30-5 SX', ' 8-5:30 CH', ' 8-5:30 JM', ' 8-5:30 SP']
tue_shifts = [' 7:30-5 SX', ' 8-5:30 CH', ' 8-5:30 LM', ' 8-5:30 SP']
wed_shifts = [' 8-5:30 JM', ' 8-5:30 LM', ' 8-5:30 SP']  # 7:30-11:30 SX
thu_shifts = [' 7:30-5 SX', ' 8-5:30 CH', ' 8-5:30 JM']  # 8-11:30 LM
fri_shifts = [' 7:30-5 SX', ' 8-5:30 CH', ' 8-5:30 JM', ' 8-5:30 SP']

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
    for x in range(4):
        if sat_worker == techs[x]:
            sat_worker = x
        if sat_worker2 == techs[x]:
            sat_worker2 = x

    random.shuffle(mon_shifts)
    random.shuffle(tue_shifts)
    random.shuffle(wed_shifts)
    random.shuffle(thu_shifts)
    random.shuffle(fri_shifts)

    sat_list = [sat_worker, sat_worker2]
    random.shuffle(sat_list)
    wed_half = sat_list[0]
    thu_half = sat_list[1]

    i, j = 0, 0
    first_row = (num * (len(techs)+2)) - (len(techs))
    for x in range(4):
        # Vet tech names
        worksheet.write(first_row + x, 0, ' ' + techs[x], border)

        # Monday
        worksheet.write(first_row + x, 1, mon_shifts[x], border)

        # Tuesday
        worksheet.write(first_row + x, 2, tue_shifts[x], border)

        # Wednesday
        if x != wed_half:
            worksheet.write(first_row + x, 3, wed_shifts[i], border)
            i += 1
        else:
            worksheet.write(first_row + x, 3, ' 7:30-11:30 SX', border)

        # Thursday
        if x != thu_half:
            worksheet.write(first_row + x, 4, thu_shifts[j], border)
            j += 1
        else:
            worksheet.write(first_row + x, 4, ' 8-11:30 LM', border)

        # Friday
        worksheet.write(first_row + x, 5, fri_shifts[x], border)

        # Saturday
        if x == wed_half:
            worksheet.write(first_row + x, 6, ' 8-12', border)
        elif x == thu_half:
            worksheet.write(first_row + x, 6, ' 7:30-12', border)
        else:
            worksheet.write(first_row + x, 6, ' OFF', border)

        # Hours
        worksheet.write(first_row + x, 7, ' 40', border)

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
