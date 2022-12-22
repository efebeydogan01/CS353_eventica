from django.shortcuts import render, redirect
from django.db import connection


# Create your views here.
def my_upcoming_events(request):
    user_id = request.session['user_id']
    city = request.session['city'].lower()
    cursor = connection.cursor()

    if request.method == "POST":
        event_id = request.POST["event"]
        cursor.execute(f"""
                        DELETE FROM joins
                        where user_id = {user_id} and event_id = {event_id}
                        """)
        return redirect(request.META['HTTP_REFERER'])

    search_title = request.GET["title"] if "title" in request.GET and request.GET["title"] else ''
    event_type = request.GET["event_type"] if "event_type" in request.GET and request.GET["event_type"] else ''
    q_search_title = "%" + search_title + "%"
    q_event_type = "%" + event_type + "%"
    cursor.execute(f"""
                    SELECT event_id, E.name name, date, event_type, remaining_quota, total_quota, age_limit, E.description, V.name venue, V.city city, price
                    FROM joins J natural join event E JOIN venue V USING (venue_id) 
                    WHERE J.user_id = {user_id} AND E.name LIKE %s AND event_type LIKE %s;
                    """, [q_search_title, q_event_type])
    events = to_dict(cursor)
    cursor.execute(f"""
                    SELECT event_id
                    from ticket T
                    where user_id = {user_id}
                    """)
    paid_events_temp = to_dict(cursor)
    paid_events = []
    for event in paid_events_temp:
        paid_events.append(event["event_id"])
    return render(request, "my_upcoming_events.html", {
        "city": city.upper(),
        "filter_event_type": event_type.lower(),
        "filter_title": search_title,
        "events": events,
        "paid_events": paid_events,
    })

def to_dict(cursor):
    column_names = [c[0] for c in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data