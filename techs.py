import xlsxwriter
import random

# Shifts for each work day
mon_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']
tue_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 LM', '8-5:30 SP']
wed_shifts = ['7:30-5 SX', '8-5:30 JM', '8-5:30 SP']
thu_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM']
fri_shifts = ['7:30-5 SX', '8-5:30 CH', '8-5:30 JM', '8-5:30 SP']
sat_shifts = ['7:30-12', '8-12']

# Read employee names from techs.txt
with open("techs.txt") as f:
    techs = f.readlines()
techs = [x.strip() for x in techs]

workbook = xlsxwriter.Workbook('tech_schedule.xlsx')
worksheet = workbook.add_worksheet('Techs')
border = workbook.add_format({'border': 1})
fill = workbook.add_format({'bg_color': 'silver', 'border': 1})


# Generate full week
def week(num, sat_worker, sat_worker2):
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
    random.shuffle(sat_shifts)

    wed_off = random.choice([sat_worker, sat_worker2])
    if wed_off == sat_worker:
        thu_off = sat_worker2
    else:
        thu_off = sat_worker

    i = 0
    j = 0
    k = 0
    first_row = (num * 5) - 3
    for x in range(4):
        worksheet.write(first_row+x, 0, techs[x], border)
        worksheet.write(first_row+x, 1, mon_shifts[x], border)
        worksheet.write(first_row+x, 2, tue_shifts[x], border)

        if x+1 != wed_off:
            worksheet.write(first_row+x, 3, wed_shifts[i], border)
            i += 1
        else:
            worksheet.write(first_row+x, 3, 'OFF', border)

        if x+1 != thu_off:
            worksheet.write(first_row+x, 4, thu_shifts[j], border)
            j += 1
        else:
            worksheet.write(first_row+x, 4, 'OFF', border)

        worksheet.write(first_row+x, 5, fri_shifts[x], border)

        if (x+1 == sat_worker) or (x+1 == sat_worker2):
            worksheet.write(first_row+x, 6, sat_shifts[k], border)
            if sat_shifts[k] == '8-12':
                worksheet.write_number(first_row+x, 7, 36, border)
            else:
                worksheet.write_number(first_row+x, 7, 36.5, border)
            k += 1
        else:
            worksheet.write(first_row + x, 6, 'OFF', border)
            worksheet.write(first_row + x, 7, 40, border)


# Set up schedule template
def template(month_str, day_str, total_weeks):
    worksheet.set_column('B:G', 12)
    worksheet.set_column('H:H', 5.5)
    border = workbook.add_format({'border': 1})
    fill = workbook.add_format({'bg_color': 'silver', 'border': 1})
    column_headers = ['Monday', 'Tuesday', 'Wednesday', 'Thursdays', 'Friday', 'Saturday', 'Hours']
    for x in range(7):
        worksheet.write(0, x + 1, column_headers[x], border)

    for i in range(total_weeks):
        # Write calendar dates to appropriate cells
        if month_str == '02':
            month_end = 28
        elif month_str == '04' or month_str == '06' or month_str == '09' or month_str == '11':
            month_end = 30
        else:
            month_end = 31

        for j in range(6):
            worksheet.write_blank(5*i+1, 0, None, fill)
            worksheet.write_blank(5*i+1, 7, None, fill)
            worksheet.write(5*i+1, j + 1, month_str + '/' + day_str, fill)
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
    workbook.close()