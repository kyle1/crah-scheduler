import xlsxwriter
import random

# Shifts for each work day
mon_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130', '9-CL 130-230 TECH']
tue_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130', '9-CL 130-230 TECH']
wed_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130', '9-CL 130-230 TECH']
thu_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130', '9-CL 130-230 TECH']
fri_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130', '9-CL 130-230 TECH']
sat_shifts = ['730-430 12-1 PR', '730-430 12-1', '8-5 12-2']
sun_shifts = ['8-5 12-1 PR', '8-5 12-1']


# Read employee names from acts.txt
# with open("acts.txt") as f:
#     acts = f.readlines()
# acts = [x.strip() for x in acts]
acts = ['Shawnn', 'Sanora', 'Lucy', 'Emily', 'Alexis', 'Courtney']

workbook = xlsxwriter.Workbook('act_schedule.xlsx')
worksheet = workbook.add_worksheet('ACTs')
worksheet.set_landscape()
worksheet.set_default_row(12)
border = workbook.add_format({'border': 1})
fill = workbook.add_format({'font_size': 8, 'bg_color': 'silver', 'border': 1})
small_text = workbook.add_format({'font_size': 8, 'border': 1})


# Generate full week
def act_week(num):
    # 1 ACT off/off
    # 3 ACTs work/off
    # 2 ACTS off/work

    weekend_off = 0
    mon_off = 1
    tue_off = 2
    wed_off = 3
    thu_off = 4
    fri_off = 5

    random.shuffle(mon_shifts)
    random.shuffle(tue_shifts)
    random.shuffle(wed_shifts)
    random.shuffle(thu_shifts)
    random.shuffle(fri_shifts)
    random.shuffle(sat_shifts)
    random.shuffle(sun_shifts)

    mon_ctr = 0
    tue_ctr = 0
    wed_ctr = 0
    thu_ctr = 0
    fri_ctr = 0

    first_row = (num * (len(acts)+1)) - (len(acts)-1)
    for x in range(len(acts)):
        # ACT names
        worksheet.write(first_row+x, 0, acts[x], small_text)

        # Sunday
        if x == weekend_off:
            worksheet.write(first_row + x, 1, 'OFF', small_text)
            worksheet.write(first_row + x, 7, 'OFF', small_text)

        # Monday
        if x != mon_off:
            worksheet.write(first_row + x, 2, mon_shifts[mon_ctr], small_text)
            mon_ctr += 1
        else:
            worksheet.write(first_row + x, 2, 'OFF', small_text)

        # Tuesday
        if x != tue_off:
            worksheet.write(first_row + x, 3, tue_shifts[tue_ctr], small_text)
            tue_ctr += 1
        else:
            worksheet.write(first_row + x, 3, 'OFF', small_text)

        # Wednesday
        if x != wed_off:
            worksheet.write(first_row + x, 4, wed_shifts[wed_ctr], small_text)
            wed_ctr += 1
        else:
            worksheet.write(first_row + x, 4, 'OFF', small_text)

        # Thursday
        if x != thu_off:
            worksheet.write(first_row + x, 5, thu_shifts[thu_ctr], small_text)
            thu_ctr += 1
        else:
            worksheet.write(first_row + x, 5, 'OFF', small_text)

        # Friday
        if x != fri_off:
            worksheet.write(first_row + x, 6, fri_shifts[fri_ctr], small_text)
            fri_ctr += 1
        else:
            worksheet.write(first_row + x, 6, 'OFF', small_text)

        # Hours
        if x == weekend_off:
            worksheet.write(first_row + x, 8, '40', small_text)


# Set up schedule template
def act_template(month_str, day_str, total_weeks, msg):
    worksheet.set_column('A:A', 6.5)
    worksheet.set_column('B:B', 12)
    worksheet.set_column('C:G', 14)
    worksheet.set_column('H:H', 12)
    worksheet.set_column('I:I', 5)
    column_headers = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                      'Friday', 'Saturday', 'Hours']
    for x in range(8):
        worksheet.write(0, x+1, column_headers[x], small_text)

    # Get rid of leading zeros
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

        for j in range(7):
            worksheet.write_blank((len(acts)+1)*i+1, 0, None, fill)
            worksheet.write_blank((len(acts)+1)*i+1, 8, None, fill)
            worksheet.write((len(acts)+1)*i+1, j + 1, month_str + '/' + day_str, fill)
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
            month_str = str(month)
            day_str = str(day)

    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 16})
    worksheet.merge_range('A31:H31', msg, merge_format)
    workbook.close()
