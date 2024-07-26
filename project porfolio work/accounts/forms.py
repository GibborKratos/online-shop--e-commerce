from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm, LoginForm
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        # Add the class to the password1 and password2 fields
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        
    first_name = forms.CharField(max_length=25, label='First Name', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control'}), required=True)
    last_name = forms.CharField(max_length=25, label='Last Name', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}), required=True)
    email = forms.CharField(max_length=25, label='Email', widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control'}), required=True)
    phone = forms.CharField(max_length=25, label='Phone', widget=forms.TextInput(attrs={'placeholder':'Phone', 'class':'form-control', 'minlength':'10', 'pattern':r'^(0)\d{9}$', 'title':'10 digit phone number'}), required=True)
    password1 = forms.CharField(max_length=25, label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}), required=True)
    password2 = forms.CharField(max_length=25, label='Password Confirmation', widget=forms.PasswordInput(attrs={'placeholder':'Password(again)', 'class':'form-control'}), required=True)
    address = forms.CharField(max_length=500, label='Address', widget=forms.TextInput(attrs={'placeholder':'Address', 'class':'form-control'}),  required=True)
    referrer = forms.CharField(max_length=100, label='Referrer', widget=forms.TextInput(attrs={'placeholder':'Referrer', 'class':'form-control'}), required=False)



    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.referrer = self.cleaned_data['referrer']
        if user.referrer:
            try:
                # Retrieve the referrer from the CustomUser model
                referrer_user = CustomUser.objects.get(username=user.referrer)
                # Add coins to the referrer (let's say you add 10 coins)
                referrer_user.wallet += 1000
                # Save the referrer's new coin total back to the database
                referrer_user.save()
            except CustomUser.DoesNotExist:
                # Handle the case where the referrer username doesn't exist
                print(f"No user found for username: {user.referrer}")
        else:
            user.referrer = ""
                
                
        user.save()
        return user
    
    field_order = ['first_name', 'last_name', 'username','email', 'phone', 'address' ,'password1', 'password2']

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        
    

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)
