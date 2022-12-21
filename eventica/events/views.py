from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.db import connection
from events.forms import *
from django.views import View

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
    user_info = request.session['user_info']
    return render(request, "events/events.html", {
        "city": request.session['city'],  # todo: update city
        "name": request.session['name'],  # todo: update city
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
            request.session['date_of_birth'] = date_of_birth
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
