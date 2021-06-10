from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.db.models.deletion import CASCADE
from users.models import User
# Create your models here.
class ESP8266(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,related_name='esp')
    chip_id = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=150)
    #... unnecessary board fields ....
    board_up_time = models.TimeField(blank=True,null=True)
    flash_free_space = models.IntegerField(blank=True,null=True)
    ram_free_space = models.IntegerField(blank=True,null=True)
    rest_number = models.IntegerField(blank=True,null=True)
    #... unnecessary ESP fields .... 
    mac_address = models.CharField(max_length=17,unique=True,blank=True,null=True)
    local_ip_address = models.GenericIPAddressField(blank=True,null=True)
    getAway_ip_address = models.GenericIPAddressField(blank=True,null=True)
    DNS_ip_address = models.GenericIPAddressField(blank=True,null=True)
    SSID_name = models.CharField(blank=True,max_length=100,null=True)
    core_version = models.CharField(blank=True,max_length=50,null=True)
    sdk_version = models.CharField(blank=True,max_length=50,null=True)
    cpu_freq_mHz = models.CharField(blank=True,max_length=50,null=True)
    flash_chip_id = models.CharField(blank=True,max_length=50,null=True)
    rest_reason = models.TextField(blank=True,null=True)

class ESPSensor(models.Model):
    board = models.ForeignKey(ESP8266,CASCADE)
    #... here we can put the sensor attributes ....
    name = models.CharField(max_length=200)
    data = HStoreField()
    
    SENSOR_TYPES = [
        ('ANALOG','analog'),
        ('INTERRUPTION_00','interruption0'),
        ('INTERRUPTION_01','interruption1'),
        ('SERIAL','serial'),
    ]
    type = models.CharField(max_length=16,choices=SENSOR_TYPES,default='ANALOG')
    #... unnecessary fields .... 
    status = models.CharField(max_length=100,blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    time_record = models.TimeField(blank=True,null=True)
    duration = models.DurationField(blank=True,null=True)



    