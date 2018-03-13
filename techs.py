import xlsxwriter
import random

# Shifts for each work day
mon_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']
tue_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 LM', '8-5:30 SP']
wed_shifts = ['8-5:30 JM', '8-5:30 LM', '8-5:30 SP']  # 7:30-11:30 SX
thu_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM']  # 8-11:30 LM
fri_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']

# Read employee names from techs.txt
# with open("techs.txt") as f:
#     techs = f.readlines()
# techs = [x.strip() for x in techs]
techs = ['Bobby', 'Suzy', 'Jenna', 'Amy']

workbook = xlsxwriter.Workbook('tech_schedule.xlsx')
worksheet = workbook.add_worksheet('Techs')
worksheet.set_landscape()
worksheet.set_default_row(12)
border = workbook.add_format({'font_size': 8, 'border': 1})
fill = workbook.add_format({'font_size': 8, 'bg_color': 'gray', 'border': 1})
merge_format = workbook.add_format({'font_size': 16, 'bold': 1, 'align': 'center'})


# Generate full week
def tech_week(num, sat_worker, sat_worker2):
    for x in range(4):
        if sat_worker == techs[x]:
            sat_worker = x+1
        if sat_worker2 == techs[x]:
            sat_worker2 = x+1

    random.shuffle(mon_shifts)
    random.shuffle(tue_shifts)
    random.shuffle(wed_shifts)
    random.shuffle(thu_shifts)
    random.shuffle(fri_shifts)

    sat_list = [sat_worker, sat_worker2]
    random.shuffle(sat_list)
    wed_half = sat_list[0]
    thu_half = sat_list[1]

    '''
    wed_half = random.choice([sat_worker, sat_worker2])
    if wed_half == sat_worker:
        thu_half = sat_worker2
    else:
        thu_half = sat_worker
    '''

    i, j = 0, 0
    first_row = (num * (len(techs)+1)) - (len(techs)-1)
    for x in range(4):
        # Vet tech names
        worksheet.write(first_row+x, 0, techs[x], border)

        # Monday
        worksheet.write(first_row+x, 1, mon_shifts[x], border)

        # Tuesday
        worksheet.write(first_row+x, 2, tue_shifts[x], border)

        # Wednesday
        if x+1 != wed_half:
            worksheet.write(first_row+x, 3, wed_shifts[i], border)
            i += 1
        else:
            worksheet.write(first_row+x, 3, '7:30-11:30 SX', border)

        # Thursday
        if x+1 != thu_half:
            worksheet.write(first_row+x, 4, thu_shifts[j], border)
            j += 1
        else:
            worksheet.write(first_row+x, 4, '8-11:30 LM', border)

        # Friday
        worksheet.write(first_row+x, 5, fri_shifts[x], border)

        # Saturday
        if x+1 == wed_half:
            worksheet.write(first_row+x, 6, '8-12', border)
        elif x+1 == thu_half:
            worksheet.write(first_row+x, 6, '7:30-12', border)
        else:
            worksheet.write(first_row+x, 6, 'OFF', border)

        # Hours
        worksheet.write(first_row+x, 7, 40, border)


# Set up schedule template
def tech_template(month_str, day_str, total_weeks, msg):
    worksheet.set_column('B:G', 12)
    worksheet.set_column('H:H', 5.5)
    column_headers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Hours']
    for x in range(7):
        worksheet.write(0, x + 1, column_headers[x], border)

    # Remove leading zeros for month & day
    month_str = int(month_str)
    month_str = str(month_str)
    day_str = int(day_str)
    day_str = str(day_str)

    # Write calendar dates to appropriate cells
    for i in range(total_weeks):
        if month_str == '02':
            month_end = 28
        elif month_str == '04' or month_str == '06' or month_str == '09' or month_str == '11':
            month_end = 30
        else:
            month_end = 31

        for j in range(6):
            worksheet.write_blank(5*i+1, 0, None, fill)
            worksheet.write_blank(5*i+1, 7, None, fill)
            worksheet.write(5*i+1, j+1, month_str + '/' + day_str, fill)
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

    worksheet.merge_range('A28:H28', msg, merge_format)
    workbook.close()
