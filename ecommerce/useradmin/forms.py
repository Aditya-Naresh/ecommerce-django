from django import forms
from accounts.models import Account
from store.models import *
from category.models import Category
from multiupload.fields import MultiImageField
from store.models import ProductGallery

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']


    
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter Phone Number"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email Address"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    
    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does Not Match!"
            )
    





class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name','description','cat_image']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"





class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['brand_name', 'image']
    
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"






class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('product_name','description','price','image','stock','is_available','brand','category')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"





class VariationForm(forms.ModelForm):
    
    class Meta:
        model = Variation
        fields = ('product','variation_category','variation_value')


    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"



class ImageForm(forms.ModelForm):
    Images = MultiImageField(min_num=1, max_num=100, max_file_size=1024*1024*5)
    

    class Meta:
        model = ProductGallery
        exclude = ['image', 'product']