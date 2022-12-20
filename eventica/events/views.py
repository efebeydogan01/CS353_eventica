from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.db import connection

"""
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
"""


def home(request):
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT event_id, E.name name, date, event_type, V.name venue
                    FROM event E JOIN venue V USING (venue_id) 
                    WHERE E.name LIKE '%%' AND event_type="Concert" AND 
                    city="Ankara";
                    """)  # Todo: get input name, event_type, and user's city
    # fetchall() method returns every row as a tuple: https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
    column_names = [c[0] for c in cursor.description]
    events = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return render(request, "events/events.html", {
        "city": "ANKARA",  # todo: update city
        "events": events,
    })


def my_upcoming_events(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM my_upcoming_events""") # todo: add my_upcoming_events view (user_id necessary)
    column_names = [c[0] for c in cursor.description]
    events = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return render(request, "events/my_upcoming_events.html", {
        "events": my_upcoming_events,
    })


def login(request):
    return render(request, "login.html", )
