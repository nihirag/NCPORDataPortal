from django.db import models

# Create your models here.


class Data(models.Model):
    obstime = models.DateTimeField(primary_key=True)
    tempr = models.FloatField()
    ap = models.FloatField()
    ws = models.FloatField()
    wd = models.FloatField()
    rh = models.FloatField()
    blizzard = models.FloatField(null=True)
