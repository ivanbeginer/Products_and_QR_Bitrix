from django import forms

class QRCodeCreateForm(forms.Form):
    product_id = forms.IntegerField()

