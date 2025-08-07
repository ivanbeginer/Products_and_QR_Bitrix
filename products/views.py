import base64

from django.http import HttpResponse
from django.shortcuts import render, redirect

from integration_utils.bitrix24.models import BitrixUserToken
from qrcodes.models import QRcode

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from products.forms import ProductCreateForm

# Create your views here.








def handle_upload_file(file):
    with open(f'media/{file}','wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
@main_auth(on_cookies=True)
def create_product(request):
    user = request.bitrix_user_token
    form = ProductCreateForm(request.POST, request.FILES)
    print(request.FILES)
    if request.method=='POST':
        if form.is_valid():
            data = form.cleaned_data
            print(data['image'])
            handle_upload_file(data['image'])
            with open(str(f'media/{data['image']}'),'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            print(data)
            product = user.call_api_method('catalog.product.add',params={'fields':{

                'iblockId':15,
                'name':data['title'],
                'detailPicture':{'fileData':[data['image'],encoded_string]},
                'detailText':data['description'],
                'purchasingPrice':data['price'],
                'purchasingCurrency':'RUB'
            }})['result']

            return render(request,'success.html')
        else:
            form = ProductCreateForm()
    return render(request,'base.html',locals())


def get_product(request,qr_uuid):
    user = BitrixUserToken.objects.filter(user__is_admin=True).first()
    qr = QRcode.objects.filter(qr_code_uuid=qr_uuid).first()
    res = user.call_api_method('catalog.product.get',params={'id':qr.product_id})['result']['product']
    image = user.call_api_method('catalog.productImage.get',params={'productId':qr.product_id,'id':res['detailPicture']['id']})['result']['productImage']['detailUrl']
    print(res)
    return render(request,'get_product.html',locals())