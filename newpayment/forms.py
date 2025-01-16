from django import forms
from .models import NewShippingAddress

class NewShippingForm(forms.ModelForm):
    new_full_name=forms.CharField(label='',max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کامل خود را وارد کنید'}),required=True)
    new_email=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'}),required=True)
    new_address1=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس اول'}),required=True)
    new_address2=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس دوم'}),required=False)
    new_city=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شهر'}),required=True)
    new_state=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'منطقه'}),required=False)
    new_zipcode=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کدپستی'}),required=False)
    new_country=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کشور'}),required=True)

    class Meta:
        model=NewShippingAddress
        fields=['new_full_name','new_email','new_address1','new_address2','new_city','new_state','new_zipcode','new_country']
        exclude=['user',]