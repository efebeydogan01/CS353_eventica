from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    # Convert month name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calender
    cal = HTMLCalendar().formatmonth(year, month_number)
    # get current year
    now = datetime.now()
    current_year = now.year

    return render(request, "events/home.html", {
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
    })

def login(request):
    return render(request, "events/login.html",)
