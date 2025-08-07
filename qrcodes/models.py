from django.db import models

# Create your models here.
class QRcode(models.Model):
    qr_code_uuid = models.UUIDField(primary_key=True)
    product_id = models.IntegerField(null=False)
    product_name = models.CharField()

    class Meta:
        get_latest_by = 'qr_code_uuid'