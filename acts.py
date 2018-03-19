import xlsxwriter
import random
import linecache

# Shifts for each work day
mon_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130']
tue_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130']
wed_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130']
thu_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130']
fri_shifts = ['7-4 1130-1230 PR', '7-4 1130-130', '830-530 12-130 PR', '830-530 12-130']
sat_shifts = ['730-430 12-1 PR', '730-430 12-1', '8-5 12-2']
sun_shifts = ['8-5 12-1 PR', '8-5 12-1']

# Read employee names from file
line = linecache.getline('employees.txt', 2)
acts = [x.strip() for x in line.split(',')]

workbook = xlsxwriter.Workbook('act_schedule.xlsx')
worksheet = workbook.add_worksheet('ACTs')
worksheet.set_landscape()
worksheet.set_default_row(12)

'''
Bold Times New Roman formatting
border = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'border': 1})
fill = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'bg_color': 'gray', 'border': 1})
merge_format = workbook.add_format({'font_size': 16, 'font_name': 'Times New Roman', 'bold': 1, 'align': 'center'})
silver_bg = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'bg_color': 'silver'})
'''

border = workbook.add_format({'border': 1})
fill = workbook.add_format({'font_size': 8, 'bg_color': 'gray', 'border': 1})
small_text = workbook.add_format({'font_size': 8, 'border': 1})
merge_format = workbook.add_format({'font_size': 16, 'bold': 1, 'align': 'center'})
silver_bg = workbook.add_format({'font_size': 8, 'bg_color': 'silver'})


# Generate full week
def act_week(num, sun_worker, sun_worker2, sat_worker, sat_worker2, sat_worker3):
    # 1 ACT off/off
    # 3 ACTs work/off
    # 2 ACTS off/work

    for x in range(6):
        if sun_worker == acts[x]:
            sun_worker = x
        if sun_worker2 == acts[x]:
            sun_worker2 = x
        if sat_worker == acts[x]:
            sat_worker = x
        if sat_worker2 == acts[x]:
            sat_worker2 = x
        if sat_worker3 == acts[x]:
            sat_worker3 = x

    jumble = [sun_worker, sun_worker2, sat_worker, sat_worker2, sat_worker3]
    jumble = random.sample(jumble, 5)
    mon_off = jumble[0]
    tue_off = jumble[1]
    wed_off = jumble[2]
    thu_off = jumble[3]
    fri_off = jumble[4]

    tech_asst = [0, 1, 2, 3, 4]
    jum = 0
    while jum == 0:
        tech_asst = random.sample(tech_asst, 5)
        if (tech_asst[0] != mon_off and tech_asst[1] != tue_off and tech_asst[2] != wed_off
           and tech_asst[3] != thu_off and tech_asst[4] != fri_off):
                mon_asst = tech_asst[0]
                tue_asst = tech_asst[1]
                wed_asst = tech_asst[2]
                thu_asst = tech_asst[3]
                fri_asst = tech_asst[4]
                jum = 1

    # Shuffle shifts before assigning to employees
    random.shuffle(mon_shifts)
    random.shuffle(tue_shifts)
    random.shuffle(wed_shifts)
    random.shuffle(thu_shifts)
    random.shuffle(fri_shifts)
    random.shuffle(sat_shifts)
    random.shuffle(sun_shifts)

    sun_ctr = 0
    mon_ctr = 0
    tue_ctr = 0
    wed_ctr = 0
    thu_ctr = 0
    fri_ctr = 0
    sat_ctr = 0

    first_row = (num * (len(acts)+1)) - (len(acts)-1)
    for x in range(len(acts)):
        hours = 0

        # ACT names
        worksheet.write(first_row+x, 0, acts[x], small_text)

        # Sunday
        if x != sun_worker and x != sun_worker2:
            worksheet.write(first_row + x, 1, 'OFF', small_text)
        else:
            worksheet.write(first_row + x, 1, sun_shifts[sun_ctr], small_text)
            sun_ctr += 1
            hours += 8

        # Monday
        if x != mon_off:
            if x == mon_asst:
                worksheet.write(first_row + x, 2, '9-CL 130-230 TECH', silver_bg)
                hours += 8
            else:
                worksheet.write(first_row + x, 2, mon_shifts[mon_ctr], small_text)
                if mon_shifts[mon_ctr] == '7-4 1130-130':
                    hours += 7
                else:
                    hours += 8
                mon_ctr += 1
        else:
            worksheet.write(first_row + x, 2, 'OFF', small_text)

        # Tuesday
        if x != tue_off:
            if x == tue_asst:
                worksheet.write(first_row + x, 3, '9-CL 130-230 TECH', silver_bg)
                hours += 8
            else:
                worksheet.write(first_row + x, 3, tue_shifts[tue_ctr], small_text)
                if tue_shifts[tue_ctr] == '7-4 1130-130':
                    hours += 7
                else:
                    hours += 8
                tue_ctr += 1
        else:
            worksheet.write(first_row + x, 3, 'OFF', small_text)

        # Wednesday
        if x != wed_off:
            if x == wed_asst:
                worksheet.write(first_row + x, 4, '9-CL 130-230 TECH', silver_bg)
                hours += 8
            else:
                worksheet.write(first_row + x, 4, wed_shifts[wed_ctr], small_text)
                if wed_shifts[wed_ctr] == '7-4 1130-130':
                    hours += 7
                else:
                    hours += 8
                wed_ctr += 1
        else:
            worksheet.write(first_row + x, 4, 'OFF', small_text)

        # Thursday
        if x != thu_off:
            if x == thu_asst:
                worksheet.write(first_row + x, 5, '9-CL 130-230 TECH', silver_bg)
                hours += 8
            else:
                worksheet.write(first_row + x, 5, thu_shifts[thu_ctr], small_text)
                if thu_shifts[thu_ctr] == '7-4 1130-130':
                    hours += 7
                else:
                    hours += 8
                thu_ctr += 1
        else:
            worksheet.write(first_row + x, 5, 'OFF', small_text)

        # Friday
        if x != fri_off:
            if x == fri_asst:
                worksheet.write(first_row + x, 6, '9-CL 130-230 TECH', silver_bg)
                hours += 8
            else:
                worksheet.write(first_row + x, 6, fri_shifts[fri_ctr], small_text)
                if fri_shifts[fri_ctr] == '7-4 1130-130':
                    hours += 7
                else:
                    hours += 8
                fri_ctr += 1
        else:
            worksheet.write(first_row + x, 6, 'OFF', small_text)

        # Saturday
        if x != sat_worker and x != sat_worker2 and x != sat_worker3:
            worksheet.write(first_row + x, 7, 'OFF', small_text)
        else:
            worksheet.write(first_row + x, 7, sat_shifts[sat_ctr], small_text)
            if sat_shifts[sat_ctr] == '8-5 12-2':
                hours += 7
            else:
                hours += 8
            sat_ctr += 1

        # Hours
        worksheet.write(first_row + x, 8, hours, small_text)


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

        for j in range(7):
            worksheet.write_blank((len(acts)+1)*i+1, 0, None, fill)
            worksheet.write_blank((len(acts)+1)*i+1, 8, None, fill)
            worksheet.write((len(acts)+1)*i+1, j+1, month_str + '/' + day_str, fill)
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

    if total_weeks > 4:
        worksheet.merge_range('A38:H39', msg, merge_format)
    else:
        worksheet.merge_range('A31:H32', msg, merge_format)

    workbook.close()
