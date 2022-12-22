from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime, date
from django.db import connection
from events.forms import *
from django.views import View
from django.http import HttpResponseRedirect
from .forms import EventForm
from django.contrib import messages

def home(request):
    city = request.session['city'].lower()
    user_name = request.session['name']
    date_of_birth = request.session['date_of_birth']

    cursor = connection.cursor()

    if request.method == "POST":
        event_id = request.POST["event"]
        user_id = request.session['user_id']
        cursor.execute(f"""
                        SELECT age_limit, remaining_quota, date
                        FROM event E
                        WHERE E.event_id = {event_id}
                        """)
        event_info = cursor.fetchall()
        age_limit = event_info[0][0]
        remaining_quota = event_info[0][1]
        event_date = str(event_info[0][2])
        birthdate = datetime. strptime(date_of_birth, "%Y-%m-%d")
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        print(event_date)

        cursor.execute(f"""
                        SELECT *
                        FROM joins natural join event
                        where user_id = {user_id} AND date = STR_TO_DATE('{event_date}', '%Y-%m-%d %H:%i:%s') AND event_id <> {event_id} 
                        """)
        colliding = cursor.fetchall()
        if remaining_quota <= 0:
            messages.error(request, 'There is not enough quota left in the event!', extra_tags="bg-danger")
        elif age < age_limit:
            messages.error(request, 'You are not old enough to attend this event!', extra_tags="bg-danger")
        elif colliding:
            messages.error(request, 'This event collides with other event(s) that you are attending!', extra_tags="bg-danger")
        else:
            try:
                cursor.execute(f"""INSERT INTO joins values({event_id}, {user_id})""")
                messages.success(request, 'Successfully joined the event!', extra_tags='bg-success')
            except:
                messages.error(request, 'You have already joined the event', extra_tags="bg-danger")
        return redirect(request.META['HTTP_REFERER'])

    search_title = request.GET["title"] if "title" in request.GET and request.GET["title"] else ''
    event_type = request.GET["event_type"] if "event_type" in request.GET and request.GET["event_type"] else ''

    q_search_title = "%" + search_title + "%"
    q_event_type = "%" + event_type + "%"
    cursor.execute("""
                    SELECT event_id, E.name name, date, event_type, remaining_quota, total_quota, age_limit, E.description, V.name venue
                    FROM event E JOIN venue V USING (venue_id) 
                    WHERE city = %s AND E.name LIKE %s AND event_type LIKE %s;
                    """, [city, q_search_title, q_event_type])
    events = to_dict(cursor)

    return render(request, "events/events.html", {
        "city": city.upper(),
        "name": user_name,
        "date_of_birth": date_of_birth,
        "filter_event_type": event_type.lower(),
        "filter_title": search_title,
        "events": events,
    })


def my_upcoming_events(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM my_upcoming_events""") # todo: add my_upcoming_events view (user_id necessary)
    my_upcoming_events = to_dict(cursor)
    return render(request, "events/my_upcoming_events.html", {
        "events": my_upcoming_events,
    })

def create_event(request):
    context={}
    context['form'] = EventForm()
        
    '''submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            cursor.execute(''' ''')
            return HttpResponseRedirect('/create_event?submitted=True')
        else:
            form = EventForm
            if 'submitted' in request.GET:
                submitted = True'''
    return render(request, 'events/create_event.html', context)

class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # checking if user exists
            cursor = connection.cursor()
            cursor.execute(
                'select user_id from user where email=\'' + email + '\' and password=\'' + password + '\''
            )
            desc = cursor.fetchall()

            if len(desc) == 0:
                return redirect('login')
            # storing user_id in session
            desc = desc[0]
            user_id = desc[0]
            request.session['user_id'] = user_id
            cursor2 = connection.cursor()
            cursor2.execute('select name from user where user_id=\'' + str(user_id) + '\'')
            desc = cursor2.fetchall()
            desc = desc[0]
            name = desc[0]
            request.session['name'] = name
            cursor2.execute('select city from user where user_id=\'' + str(user_id) + '\'')
            desc = cursor2.fetchall()
            desc = desc[0]
            city = desc[0]
            request.session['city'] = city
            cursor2.execute('select phone_number from user where user_id=\'' + str(user_id) + '\'')
            desc = cursor2.fetchall()
            desc = desc[0]
            phone_number = desc[0]
            request.session['phone_number'] = phone_number
            cursor2.execute('select date_of_birth from user where user_id=\'' + str(user_id) + '\'')
            desc = cursor2.fetchall()
            desc = desc[0]
            date_of_birth = desc[0]
            request.session['date_of_birth'] = str(date_of_birth)
            return redirect('home')
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

class SignupView(View):
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            date_of_birth = form.cleaned_data['date_of_birth']
            cursor = connection.cursor()
            sql = """
                        INSERT INTO `user` 
                        (`name`, `email`, `password`, `phone_number`, `city`, `address`, `date_of_birth`) 
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');
                    """.format(name, email, password, phone_number, city, address, date_of_birth)
            cursor.execute(sql)
        # request.session['user_type'] = 'customer'
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)
    def get(self, request):
        form = SignupForm()
        context = {'form': form}
        return render(request, 'signup.html', context)


def to_dict(cursor):
    column_names = [c[0] for c in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data
