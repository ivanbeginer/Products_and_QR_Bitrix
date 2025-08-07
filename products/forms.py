from django import forms


class ProductCreateForm(forms.Form):

    title = forms.CharField(required=False,label='Название товара')
    image = forms.ImageField(required=False,label='Изображение товара')
    description = forms.CharField(required=False,label='Описание товара')
    price = forms.FloatField(required=False,min_value=0.00,label='Стоимость товара')
