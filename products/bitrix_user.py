from integration_utils.bitrix24.models import BitrixUserToken

user = BitrixUserToken.objects.filter(user__is_admin=True).first()
res = user.call_api_method('catalog.product.list',params={'select':['id','iblockId'],'filter':{'iblockId':15}})['result']['products']
ids = ((product['id'],product['id']) for product in res)