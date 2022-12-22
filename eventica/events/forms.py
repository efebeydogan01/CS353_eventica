from django import forms
from django.forms import ModelForm

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
    print(event_type)
    date = forms.CharField(label='Date and Time (ex. 2022-11-18 12:12:00)')
    age_limit = forms.CharField(label='Age Limit')
    total_quota = forms.CharField(label='Total Quota')
    location = forms.CharField(label='Location')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
          self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})