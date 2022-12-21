from django import forms

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

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ( )
        labels = {
            'name' : '',
            'description' : ''
            'date' : ''
            'event-type' : ''
            'status' : ''
            'age-limit' : ''
            'total-quota' : ''
        }
