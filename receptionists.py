import xlsxwriter
import random

# Shifts for each work day
mon_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230'] # 130/2-CL, 715-245 10-1030
tue_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230'] # 130/2-CL, 715-245 10-1030
wed_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230'] # 130/2-CL, 715-245 10-1030
thu_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230'] # 130/2-CL, 715-245 10-1030
fri_shifts = ['B730-430 1130-1230', '730-430 1130-1230', '830-530 1-2', '9-CL 130-230'] # 130/2-CL, 715-245 10-1030
sat_shifts = ['B8-CL', '745-12', '8-12', '8-CL']

# Read employee names from techs.txt
# with open("techs.txt") as f:
#     techs = f.readlines()
# techs = [x.strip() for x in techs]
receps = ['Darcy', 'Haley', 'Carlos', 'Jenna G', 'Megan', 'Sydney', 'Gloria', 'Blanca']

workbook = xlsxwriter.Workbook('recep_schedule.xlsx')
worksheet = workbook.add_worksheet('Receptionists')
worksheet.set_landscape()
worksheet.set_default_row(10)
border = workbook.add_format({'font_size': 8, 'border': 1})
fill = workbook.add_format({'font_size': 8, 'bg_color': 'gray', 'border': 1})
merge_format = workbook.add_format({'font_size': 16, 'bold': 1, 'align': 'center'})


# Generate full week
def recep_week(num, sat_worker, sat_worker2, sat_worker3, sat_worker4):
    for x in range(8):
        if sat_worker == receps[x]:
            sat_worker = x+1
        if sat_worker2 == receps[x]:
            sat_worker2 = x+1
        if sat_worker3 == receps[x]:
            sat_worker3 = x+1
        if sat_worker4 == receps[x]:
            sat_worker4 = x+1

    sat_list = [sat_worker, sat_worker2, sat_worker3, sat_worker4]
    half_list = []
    pt_sats = 0

    if sat_worker == 7 or sat_worker == 8:
        pt_sats += 1
    else:
        half_list.append(sat_worker)

    if sat_worker2 == 7 or sat_worker2 == 8:
        pt_sats += 1
    else:
        half_list.append(sat_worker2)

    if sat_worker3 == 7 or sat_worker3 == 8:
        pt_sats += 1
    else:
        half_list.append(sat_worker3)

    if sat_worker4 == 7 or sat_worker4 == 8:
        pt_sats += 1
    else:
        half_list.append(sat_worker4)

    random.shuffle(half_list)

    # Ensure half days are given to Saturday workers first, then FT employees
    if len(half_list) == 2:
        mon_half = half_list[0]
        tue_half = half_list[1]
        maybe_half = []
        for x in range(2, 7):
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
        for x in range(2, 7):
            if mon_half != x and tue_half != x and wed_half != x:
                maybe_half2.append(x)

        random.shuffle(maybe_half2)
        thu_half = maybe_half2[0]

    else:
        mon_half = half_list[0]
        tue_half = half_list[1]
        wed_half = half_list[2]
        thu_half = half_list[3]

    for x in range(2, 7):
        if x != mon_half and x != tue_half and x != wed_half and x != thu_half:
            fri_half = x

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

    # Darcy's shifts
    worksheet.write(first_row, 1, '715-245 10-1030', border)
    worksheet.write(first_row, 2, '715-245 10-1030', border)
    worksheet.write(first_row, 3, '715-245 10-1030', border)
    worksheet.write(first_row, 4, '715-245 10-1030', border)
    worksheet.write(first_row, 5, '715-245 10-1030', border)
    worksheet.write(first_row, 6, 'OFF', border)
    worksheet.write(first_row, 7, '35', border)

    hours = [35, 0, 0, 0, 0, 0, 0, 0]
    for x in range(5):
        # Monday
        if x+2 != mon_half:
            worksheet.write(first_row+x+1, 1, mon_shifts[i], border)
            i += 1
            hours[x+1] = 8
        else:
            worksheet.write(first_row+x+1, 1, '2-CL', border)
            hours[x+1] = 4

        worksheet.write(first_row+x+2, 1, 'OFF', border)
        worksheet.write(first_row+x+3, 1, 'OFF', border)

        # Tuesday
        if x+2 != tue_half:
            worksheet.write(first_row+x+1, 2, tue_shifts[j], border)
            j += 1
            hours[x+1] += 8
        else:
            worksheet.write(first_row+x+1, 2, '2-CL', border)
            hours[x+1] += 4

        worksheet.write(first_row + x + 2, 2, 'OFF', border)
        worksheet.write(first_row + x + 3, 2, 'OFF', border)

        # Wednesday
        if x+2 != wed_half:
            worksheet.write(first_row+x+1, 3, wed_shifts[k], border)
            k += 1
            hours[x+1] += 8
        else:
            worksheet.write(first_row+x+1, 3, '2-CL', border)
            hours[x+1] += 4

        worksheet.write(first_row + x + 2, 3, 'OFF', border)
        worksheet.write(first_row + x + 3, 3, 'OFF', border)

        # Thursday
        if x+2 != thu_half:
            worksheet.write(first_row+x+1, 4, thu_shifts[m], border)
            m += 1
            hours[x+1] += 8
        else:
            worksheet.write(first_row+x+1, 4, '2-CL', border)
            hours[x+1] += 4

        worksheet.write(first_row + x + 2, 4, 'OFF', border)
        worksheet.write(first_row + x + 3, 4, 'OFF', border)

        # Friday
        if x+2 != fri_half:
            worksheet.write(first_row+x+1, 5, fri_shifts[n], border)
            n += 1
            hours[x+1] += 8
        else:
            worksheet.write(first_row+x+1, 5, '2-CL', border)
            hours[x+1] += 4

        worksheet.write(first_row + x + 2, 5, 'OFF', border)
        worksheet.write(first_row + x + 3, 5, 'OFF', border)

    for x in range(7):
        if x+2 == sat_worker or x+2 == sat_worker2 or x+2 == sat_worker3 or x+2 == sat_worker4:
            # Saturday
            worksheet.write(first_row+x+1, 6, sat_shifts[p], border)
            if sat_shifts[p] == '8-12':
                hours[x+1] += 4
            else:
                hours[x+1] += 4.3
            p += 1
        else:
            worksheet.write(first_row+x+1, 6, 'OFF', border)

    for x in range(8):
        # Hours
        worksheet.write(first_row+x, 7, hours[x], border)


# Set up schedule template
def recep_template(month_str, day_str, total_weeks, msg):
    worksheet.set_column('B:G', 14)
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
        worksheet.set_margins(left=0.5, right=0.3, top=0.3, bottom=0.5)
        worksheet.merge_range('A49:H49', msg, merge_format)
    else:
        worksheet.merge_range('A40:H40', msg, merge_format)

    workbook.close()

