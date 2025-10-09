import calendar          # loads Python’s calendar module

yy = 2025                # sets the year
mm = 12                  # sets the month (December)

calendar.setfirstweekday(calendar.SUNDAY)
print(calendar.month(2025, 12))    # prints that month’s calendar in text form, customizable to start the week on Sunday
