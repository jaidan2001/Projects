from django import forms
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'
        labels ={
            'username':False,
            'password':False,
            'email':False,
            'role':False
        }
        widgets = {
            'username' : forms.TextInput(attrs = {'class' : 'admin-add-user-input', 'placeholder':'Username' }),
            'email' : forms.TextInput(attrs = {'class' : 'admin-add-user-input', 'placeholder':'Email'}),
            'password' : forms.TextInput(attrs = {'class' : 'admin-add-user-input', 'placeholder':'Password'}),
            
        }
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)

    #     for field_name in self.fields:
    #         self.fields[field_name].label = ''
        

class MovieForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = '__all__'
           
class TheaterForm(forms.ModelForm):
    class Meta:
        model = models.Theater
        fields = '__all__'


class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = models.Showtime
        fields = '__all__'

class BookedForm(forms.ModelForm):
    class Meta:
        model = models.Booked
        fields = '__all__'