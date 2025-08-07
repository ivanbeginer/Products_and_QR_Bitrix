from django import forms


class ProductCreateForm(forms.Form):

    title = forms.CharField(required=False)
    image = forms.ImageField()
    description = forms.CharField(required=False)
    price = forms.FloatField(min_value=0.00)
