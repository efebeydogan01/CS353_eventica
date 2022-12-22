from django import forms
import datetime
from django.forms import ModelForm
from django.db import connection

def to_dict(cursor):
    column_names = [c[0] for c in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class SignupForm(forms.Form):
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(format=('%Y-%m-%d') ,
        attrs={'class': 'form-control',
              'placeholder': 'Select the date',
              'type': 'date'
              }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
          self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class EventForm(forms.Form):
    EVENT_CHOICES = (
        ('Concert', 'Concert'), ('Sports','Sports'), ('Gathering','Gathering'), ('Art','Art'), ('Other', 'Other'))
    name = forms.CharField(label='Name', max_length=200)
    description = forms.CharField(label='Description')
    event_type = forms.ChoiceField(choices=EVENT_CHOICES)
    date = forms.CharField(label='Date and Time (ex. 2022-11-18 12:12:00)')
    age_limit = forms.CharField(label='Age Limit')
    total_quota = forms.CharField(label='Total Quota')
    price = forms.CharField(label='Price')
    
    sql = """SELECT VENUE_ID, NAME FROM VENUE"""
    cursor = connection.cursor()
    cursor.execute(sql)
    result = to_dict(cursor)
    venues = []
    for venue in result:
        venues.append((venue["VENUE_ID"], venue["NAME"]))

    VENUE_CHOICES = tuple(venues)
    venue = forms.ChoiceField(choices=VENUE_CHOICES, label='Venue')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
          self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class DateForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='From:')

