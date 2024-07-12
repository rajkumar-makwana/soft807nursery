from django import forms
from .models import *


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = [
            "image"
            ]
        exclude = ["product"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"