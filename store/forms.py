from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    
    class Meta:
        model = User
        fields = ('username','email','password1', 'password2')
        
   
        
    # def save(self, commit=False):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user
    
    # def clean_email(self):
    #     if User.objects.filter(email=self.cleaned_data['email']).exists():
    #         raise forms.ValidationError(self.fields['email'].error_message['exists'])
    #     return self.cleaned_data['email']    
    
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('first_name','last_name', 'phone','address','distric','city','zipcode')