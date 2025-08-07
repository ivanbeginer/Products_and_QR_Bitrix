from django import forms

from integration_utils.bitrix24.models import BitrixUserToken
from products.bitrix_user import user, ids


class QRCodeCreateForm(forms.Form):
    product_id = forms.ChoiceField(required=False, label='ID товара', choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получаем актуальный список товаров при каждом создании формы
        user = BitrixUserToken.objects.filter(user__is_admin=True).first()
        res = user.call_api_method('catalog.product.list', params={
            'select': ['id', 'iblockId'],
            'filter': {'iblockId': 15}
        })['result']['products']
        self.fields['product_id'].choices = ((product['id'], product['id']) for product in res)

