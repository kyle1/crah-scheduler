import xlsxwriter
import random
import linecache

# Read employee names from file
line = linecache.getline('employees.txt', 5)
receps = [x.strip() for x in line.split(',')]

workbook = xlsxwriter.Workbook('recep_schedule.xlsx')
worksheet = workbook.add_worksheet('Receptionists')
worksheet.set_landscape()
worksheet.set_default_row(11)

# Bold Times New Roman formatting
border = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'border': 1})
border.set_align('vcenter')
fill = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman', 'bold': 1, 'bg_color': 'gray', 'border': 1})
fill.set_align('vcenter')
'''
msg_format = workbook.add_format({'font_size': 16, 'font_name': 'Times New Roman', 'bold': 1, 'align': 'center'})
blue_bg = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman',
                              'bold': 1, 'bg_color': '#3399FF', 'border': 1})
'''
msg_format = workbook.add_format({'font_size': 16, 'font_name': 'Times New Roman', 'bold': 1, 'align': 'center'})
blue_bg = workbook.add_format({'font_size': 8, 'font_name': 'Times New Roman',
                              'bold': 1, 'bg_color': '#3399FF', 'border': 1})

blue_bg.set_align('vcenter')

'''
Calibri
border = workbook.add_format({'font_size': 8, 'border': 1})
border.set_align('vcenter')
fill = workbook.add_format({'font_size': 8, 'bg_color': 'gray', 'border': 1})
msg_format = workbook.add_format({'font_size': 16, 'bold': 1, 'align': 'center'})
blue_bg = workbook.add_format({'font_size': 8, 'bg_color': 'silver'})
blue_bg.set_align('vcenter')
'''

mon_helpers = [-1] * 5
tue_helpers = [-1] * 5
wed_helpers = [-1] * 5
thu_helpers = [-1] * 5
fri_helpers = [-1] * 5


# Generate full week
def recep_week(num, sat_worker, sat_worker2, sat_worker3, sat_worker4):
    # Shifts for each work day
    mon_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    tue_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    wed_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    thu_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    fri_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    sat_shifts = ['B8-CL', '745-12', '8-12', '8-CL']

    # Choose random hospital shift to be the tech-helper shift
    # Remove the chosen shift from the list of shifts above and store it separately so it does not get assigned twice
    helper_shiftlist = ['730-430 1130-1230', '830-530 1-2', '9-CL 130-230']
    mon_helpershift = random.choice(helper_shiftlist)
    mon_shifts.remove(mon_helpershift)
    tue_helpershift = random.choice(helper_shiftlist)
    tue_shifts.remove(tue_helpershift)
    wed_helpershift = random.choice(helper_shiftlist)
    wed_shifts.remove(wed_helpershift)
    thu_helpershift = random.choice(helper_shiftlist)
    thu_shifts.remove(thu_helpershift)
    fri_helpershift = random.choice(helper_shiftlist)
    fri_shifts.remove(fri_helpershift)

    for x in range(8):
        if sat_worker == receps[x]:
            sat_worker = x
        if sat_worker2 == receps[x]:
            sat_worker2 = x
        if sat_worker3 == receps[x]:
            sat_worker3 = x
        if sat_worker4 == receps[x]:
            sat_worker4 = x

    # Set up to give Saturday workers a half day shift during the week
    half_list = []
    pt_sats = 0

    if sat_worker == 6 or sat_worker == 7:
        pt_sats += 1
    else:
        half_list.append(sat_worker)

    if sat_worker2 == 6 or sat_worker2 == 7:
        pt_sats += 1
    else:
        half_list.append(sat_worker2)

    if sat_worker3 == 6 or sat_worker3 == 7:
        pt_sats += 1
    else:
        half_list.append(sat_worker3)

    if sat_worker4 == 6 or sat_worker4 == 7:
        pt_sats += 1
    else:
        half_list.append(sat_worker4)

    random.shuffle(half_list)

    # Half day shifts are given to Saturday workers first, then to random full-time employees
    if len(half_list) == 2:
        mon_half = half_list[0]
        tue_half = half_list[1]
        maybe_half = []
        for x in range(1, 6):
            if mon_half != x and tue_half != x:
                maybe_half.append(x)

        random.shuffle(maybe_half)
        wed_half = maybe_half[0]
        thu_half = maybe_half[1]

    elif len(half_list) == 3:
        mon_half = half_list[0]
        tue_half = half_list[1]
        wed_half = half_list[2]

        maybe_half2 = []
        for x in range(1, 6):
            if mon_half != x and tue_half != x and wed_half != x:
                maybe_half2.append(x)

        random.shuffle(maybe_half2)
        thu_half = maybe_half2[0]

    else:
        mon_half = half_list[0]
        tue_half = half_list[1]
        wed_half = half_list[2]
        thu_half = half_list[3]

    for x in range(1, 6):
        if x != mon_half and x != tue_half and x != wed_half and x != thu_half:
            fri_half = x

    # Shuffle shifts before assigning to employees
    random.shuffle(mon_shifts)
    random.shuffle(tue_shifts)
    random.shuffle(wed_shifts)
    random.shuffle(thu_shifts)
    random.shuffle(fri_shifts)
    random.shuffle(sat_shifts)

    i, j, k, m, n, p = 0, 0, 0, 0, 0, 0

    first_row = (num * (len(receps)+1)) - (len(receps)-1)
    for x in range(8):
        # Receptionist names
        worksheet.write(first_row+x, 0, receps[x], border)

    # Darcy
    for x in range(1, 6):
        worksheet.write(first_row, x, '715-245 10-1030', border)

    worksheet.write(first_row, 6, 'OFF', border)
    worksheet.write(first_row, 7, '35', border)

    hours = [35, 0, 0, 0, 0, 0, 0, 0]

    # Haley, Carlos, Jenna G, Megan, Sydney
    tech_helpers = [2, 3, 4]
    tech_helpers2 = random.sample(tech_helpers, 2)
    tech_helpers = tech_helpers + tech_helpers2
    jum = 0
    while jum == 0:
        tech_helpers = random.sample(tech_helpers, 5)
        if (tech_helpers[0] != mon_half and tech_helpers[1] != tue_half
            and tech_helpers[2] != wed_half and tech_helpers[3] != thu_half
            and tech_helpers[4] != fri_half):
                mon_helper = tech_helpers[0]
                tue_helper = tech_helpers[1]
                wed_helper = tech_helpers[2]
                thu_helper = tech_helpers[3]
                fri_helper = tech_helpers[4]
                jum = 1

    for x in range(1, 6):
        # Monday
        if x != mon_half:
            if x == mon_helper:
                worksheet.write(first_row + x, 1, mon_helpershift, blue_bg)
            else:
                worksheet.write(first_row + x, 1, mon_shifts[i], border)
                i += 1
            hours[x] = 8
        else:
            worksheet.write(first_row + x, 1, '2-CL', border)
            hours[x] = 4

        # Tuesday
        if x != tue_half:
            if x == tue_helper:
                worksheet.write(first_row + x, 2, tue_helpershift, blue_bg)
            else:
                worksheet.write(first_row + x, 2, tue_shifts[j], border)
                j += 1
            hours[x] += 8
        else:
            worksheet.write(first_row + x, 2, '2-CL', border)
            hours[x] += 4

        # Wednesday
        if x != wed_half:
            if x == wed_helper:
                worksheet.write(first_row + x, 3, wed_helpershift, blue_bg)
            else:
                worksheet.write(first_row + x, 3, wed_shifts[k], border)
                k += 1
            hours[x] += 8
        else:
            worksheet.write(first_row + x, 3, '2-CL', border)
            hours[x] += 4

        # Thursday
        if x != thu_half:
            if x == thu_helper:
                worksheet.write(first_row + x, 4, thu_helpershift, blue_bg)
            else:
                worksheet.write(first_row + x, 4, thu_shifts[m], border)
                m += 1
            hours[x] += 8
        else:
            worksheet.write(first_row+x, 4, '2-CL', border)
            hours[x] += 4

        # Friday
        if x != fri_half:
            if x == fri_helper:
                worksheet.write(first_row + x, 5, fri_helpershift, blue_bg)
            else:
                worksheet.write(first_row + x, 5, fri_shifts[n], border)
                n += 1
            hours[x] += 8
        else:
            worksheet.write(first_row+x, 5, '2-CL', border)
            hours[x] += 4

    # Gloria and Blanca (OFF during week)
    for x in range(6, 8):
        for j in range(1, 6):
            worksheet.write(first_row+x, j, 'OFF', border)

    for x in range(1, 8):
        if x == sat_worker or x == sat_worker2 or x == sat_worker3 or x == sat_worker4:
            # Saturday
            worksheet.write(first_row+x, 6, sat_shifts[p], border)
            if sat_shifts[p] == '8-12':
                hours[x] += 4
            else:
                hours[x] += 4.3
            p += 1
        else:
            worksheet.write(first_row+x, 6, 'OFF', border)

    # Hours
    for x in range(8):
        str_hours = str(hours[x])
        worksheet.write(first_row + x, 7, ' ' + str_hours, border)

    # Set up list of tech helpers to use when generating tech schedule
    mon_helpers[num-1] = receps[mon_helper]
    tue_helpers[num-1] = receps[tue_helper]
    wed_helpers[num-1] = receps[wed_helper]
    thu_helpers[num-1] = receps[thu_helper]
    fri_helpers[num-1] = receps[fri_helper]


# Set up schedule template
def recep_template(month_str, day_str, total_weeks, msg):
    worksheet.set_column('B:G', 17)
    worksheet.set_column('H:H', 5)
    column_headers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Hours']
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
            worksheet.write_blank(9*i+1, 0, None, fill)
            worksheet.write_blank(9*i+1, 7, None, fill)
            worksheet.write(9*i+1, j+1, month_str + '/' + day_str, fill)
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
        worksheet.set_margins(left=0.75, right=0.5, top=0.25, bottom=0.4)
        worksheet.merge_range('A49:H50', msg, msg_format)
    else:
        worksheet.merge_range('A40:H41', msg, msg_format)

    workbook.close()
