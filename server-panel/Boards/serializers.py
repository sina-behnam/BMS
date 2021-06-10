
from rest_framework import serializers, status
from Boards.models import ESP8266,ESPSensor
from BMS.exceptions import CustomException
from users.serializers import UserSerializer
from django.core.mail import send_mail

class ESP8266Serializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ESP8266
        fields = '__all__'
        lookup_field = "chip_id"    

class ESPSensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ESPSensor
        fields = ['name','data','type','status','message','time_record','duration']

    def save(self, **kwargs):
        if self.validated_data['type']== ("INTERRUPTION_00" or "INTERRUPTION_01"):
            send_mail(self.validated_data['status'] + '  TYPE :' + self.validated_data['type'],self.validated_data['message'],'sina.behnam.ac@gmail.com',['sina20001378@gmail.com'])    
        esp = ESP8266.objects.get(chip_id=kwargs.pop('chip_id'))
        sensor = ESPSensor.objects.create(board = esp,**self.validated_data) 
        return sensor

class ESPSensorCreateSerializer(serializers.ModelSerializer):
    board = ESP8266Serializer(read_only=True)

    class Meta:
        model = ESPSensor
        fields = '__all__'
