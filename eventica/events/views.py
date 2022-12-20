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
    # Todo: get city and events from db

    cursor = connection.cursor()
    cursor.execute("""
                    SELECT event_id, E.name, date, event_type, V.name
                    FROM event E JOIN venue V USING (venue_id) 
                    WHERE E.name LIKE '%@title%' AND event_type=@type AND 
                    city=@my_city;
                    """)
    # fetchall() method returns every row as a tuple: https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
    events = cursor.fetchall()
    print(events)
    venues = []
    for event in events:
        cursor.execute(f"select name from venue where venue_id={event[2]}")
        venues.append(cursor.fetchall()[0][0])
    print(events)
    return render(request, "events/events.html", {
        "city": "ANKARA",
        "events": zip(events, venues),
    })


def login(request):
    return render(request, "login.html", )
