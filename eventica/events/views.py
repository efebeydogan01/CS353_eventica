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
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT event_id, E.name name, date, event_type, remaining_quota, total_quota, age_limit, V.name venue
                    FROM event E JOIN venue V USING (venue_id) 
                    WHERE E.name LIKE '%%' AND event_type="Concert" AND 
                    city="Ankara";
                    """)  # Todo: get input name, event_type, and user's city
    # fetchall() method returns every row as a tuple: https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
    column_names = [c[0] for c in cursor.description]
    events = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    if request.method == "POST":
        event_id = request.POST["event"]
        user_id = request.session['user_id']
        cursor.execute(f"""
                        SELECT age_limit, remaining_quota
                        FROM event E
                        where E.event_id = {event_id}
                        """)
        event_info = cursor.fetchall()
        age_limit = event_info[0][0]
        remaining_quota = event_info[0][1]
        birthdate = datetime. strptime(request.session['date_of_birth'], "%Y-%m-%d")
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if remaining_quota <= 0:
            messages.error(request, 'There is not enough quota left in the event!', extra_tags="bg-danger")
        elif age < age_limit:
            messages.error(request, 'You are not old enough to attend this event!', extra_tags="bg-danger")
        else:
            try:
                cursor.execute(f"""
                                INSERT INTO joins values({event_id}, {user_id})
                                """)
                messages.success(request, 'Successfully joined the event!', extra_tags='bg-success')
            except:
                messages.error(request, 'You have already joined the event', extra_tags="bg-danger")

    return render(request, "events/events.html", {
        "city": request.session['city'].upper(),
        "name": request.session['name'],
        "date_of_birth": request.session['date_of_birth'],
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

