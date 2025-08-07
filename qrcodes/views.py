import base64
from io import BytesIO


from django.shortcuts import render, redirect
import uuid
import qrcode

from integration_utils.bitrix24.exceptions import BitrixApiError
from qrcodes.models import QRcode as QRCODE

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from qrcodes.forms import QRCodeCreateForm

# Create your views here.


@main_auth(on_cookies=True)
def create_qrcode(request):
    user = request.bitrix_user_token
    form = QRCodeCreateForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            data_form = form.cleaned_data
            try:
                creation = user.call_api_method('catalog.product.get',params={'id':data_form['product_id']})['result']['product']
                print(creation)
                key = uuid.uuid4()

                QRCODE.objects.update_or_create(product_id=data_form['product_id'],defaults={'qr_code_uuid':key,'product_name':creation['name']})


            except BitrixApiError:

                return render(request,'error.html')


            return  redirect('get_qrcode',f'{creation['id']}')
    return render(request,'create_qrcode.html',locals())


@main_auth(on_cookies=True)
def get_qrcode(request,product_id):

    qrcode_model = QRCODE.objects.filter(product_id=product_id).latest('qr_code_uuid')
    data = f'http://localhost:8000/get_product/{qrcode_model.qr_code_uuid}/'

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=8,
                       border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_collor='black', back_color='white')
    print()
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request,'get_qrcode.html',locals())


