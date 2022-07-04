from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Question, Response, Profile
from django import forms
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryFileField  

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        #  fields = '__all__' agr ese likte toh sare feilds aa jate , abi username, email, pwd etc dikege form me bs
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {  # this will keep the focus first on email feild rather than username, kuki phle likha h widget me
            'email': forms.EmailInput(attrs={  # just a way of accessing n modifying feild attributes
                'required': True,
                'placeholder': 'lisa@example.com',
                'autofocus': True
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'lisamora',
            }),       
        }


    def __init__(self, *args, **kwargs):
#   https://stackoverflow.com/questions/49413185/django-password-fields-placeholder        
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'placeholder': 'password'}
        self.fields['password2'].widget.attrs = {'placeholder': 'confirm password'}

class LoginForm(AuthenticationForm):
    class Meta:
        fields = '__all__'

class NewQuestionForm(forms.ModelForm):
    image =  CloudinaryFileField(
    options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 800, 'height': 500,
      'eager': [{ 'crop': 'fill', 'width': 800, 'height': 500 }]
    })
    class Meta:
        model = Question
        fields = ['title', 'body', 'image', 'url', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
                'placeholder': 'Be specific'
            })          

        }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'autofocus': True,
                'rows': 2,
                'placeholder': 'What are your thoughts?',
            })
        }        

class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'What are your thoughts?'
            })
        }


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar =  CloudinaryFileField(
    options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 100, 'height': 100,
      'eager': [{ 'crop': 'fill', 'width': 100, 'height': 100 }]
    })
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']