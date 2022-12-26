from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.urls import reverse


# Create your views here.
def my_upcoming_events(request):
    user_id = request.session['user_id']
    city = request.session['city'].lower()
    cursor = connection.cursor()
    cursor.execute(f"""
                    SELECT event_id
                    from ticket T
                    where user_id = {user_id}
                    """)
    paid_events_temp = to_dict(cursor)
    paid_events = []
    for event in paid_events_temp:
        paid_events.append(event["event_id"])

    if request.method == "POST":
        if request.POST["action"] == 'Cancel':
            event_id = int(request.POST["event"])
            price = int(request.POST["event_price"])
            cursor.execute(f"""
                            DELETE FROM joins
                            where user_id = {user_id} and event_id = {event_id}
                            """)
            if event_id in paid_events and price != 0:
                cursor.execute(f"""
                                UPDATE user
                                SET balance = balance + {price}
                                WHERE user_id = {user_id}
                                """)
                messages.success(request, 'You have successfully canceled your participation and the event fee has been refunded!', extra_tags='bg-success')
            else:
                messages.success(request, 'You have successfully canceled your participation!', extra_tags='bg-success')
            return redirect(reverse("my_upcoming_events"))
        
        elif request.POST["action"] == 'Pay':
            cursor.execute(f"""
                            SELECT balance
                            FROM user
                            WHERE user_id = {user_id}
                            """)
            balance = int(cursor.fetchall()[0][0])
            if balance <= 0:
                messages.success(request, 'You have insufficient funds to pay for this ticket, please add enough balance to your account!', extra_tags='bg-danger')
                return redirect(reverse("my_upcoming_events"))
            price = request.POST["event"]
            event_id = request.POST["event_id"]
            cursor.execute(f"""
                            UPDATE user
                            SET balance = balance - {price}
                            WHERE user_id = {user_id}
                            """)
            cursor.execute(f"""
                            INSERT INTO ticket values(NULL, {event_id}, {user_id})
                            """)
            messages.success(request, 'You have successfully paid for your ticket and the event fee has been deducted from your balance!', extra_tags='bg-success')
            return redirect(reverse("my_upcoming_events"))
        elif request.POST["action"] == 'AddFunds':
            amount = request.POST["amount"]
            cursor.execute(f"""
                            UPDATE user
                            SET balance = balance + {amount}
                            WHERE user_id = {user_id}
                            """)
            messages.success(request, 'You have successfully added funds to your balance!', extra_tags='bg-success')
            return redirect(reverse("my_upcoming_events"))
    cursor.execute(f"""
                            SELECT balance
                            FROM user
                            WHERE user_id = {user_id}
                            """)
    balance = int(cursor.fetchall()[0][0])
    search_title = request.GET["title"] if "title" in request.GET and request.GET["title"] else ''
    event_type = request.GET["event_type"] if "event_type" in request.GET and request.GET["event_type"] else ''
    q_search_title = "%" + search_title + "%"
    q_event_type = "%" + event_type + "%"
    cursor.execute(f"""
                    SELECT event_id, E.name name, date, event_type, remaining_quota, total_quota, age_limit, E.description, V.name venue, V.city city, price
                    FROM joins J natural join event E JOIN venue V USING (venue_id) 
                    WHERE J.user_id = {user_id} AND E.name LIKE %s AND event_type LIKE %s AND DATE(date) >= CURDATE();
                    """, [q_search_title, q_event_type])
    events = to_dict(cursor)
    return render(request, "my_upcoming_events.html", {
        "city": city.upper(),
        "filter_event_type": event_type.lower(),
        "filter_title": search_title,
        "events": events,
        "paid_events": paid_events,
        "balance": balance
    })

def to_dict(cursor):
    column_names = [c[0] for c in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data