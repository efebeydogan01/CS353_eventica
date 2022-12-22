from django.shortcuts import render, redirect
from django.db import connection


# Create your views here.
def my_upcoming_events(request):
    cursor = connection.cursor()
    #cursor.execute("""SELECT * FROM my_upcoming_events""")  # todo: add my_upcoming_events view (user_id necessary)
    my_upcoming_events = []#to_dict(cursor)
    return render(request, "my_upcoming_events.html", {
        "events": my_upcoming_events,
    })

def to_dict(cursor):
    column_names = [c[0] for c in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data