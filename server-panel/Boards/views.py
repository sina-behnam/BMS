from BMS.exceptions import CustomException
from rest_framework.views import APIView
from Boards.serializers import ESP8266Serializer, ESPSensorSerializer
from Boards.models import ESP8266,ESPSensor
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status,generics
from django.http import Http404
import datetime

class ESPList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ESP8266.objects.all()
    serializer_class = ESP8266Serializer

class ESPDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,chip_id):
        try:
            return ESP8266.objects.get(chip_id=chip_id)
        except:    
            raise Http404

    def get(self,request,chip_id):
        esp = self.get_object(chip_id)       
        serializer = ESP8266Serializer(esp)
        return Response(serializer.data)

    def put(self,request,chip_id):
        esp = self.get_object(chip_id)
        request.data['chip_id'] = chip_id
        request.data['board_up_time'] = datetime.datetime.now().strftime("%H:%M:%S")
        serializer = ESP8266Serializer(instance=esp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ESPSensorApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,chip_id):
        try:
            esp = ESP8266.objects.get(chip_id=chip_id)
            query_set = ESPSensor.objects.filter(board=esp.id)
            if query_set.exists():
                return query_set.all()
            raise CustomException("there is no recorde has been done yet !!",status_code=status.HTTP_404_NOT_FOUND)        
        except ESP8266.DoesNotExist:    
            raise CustomException("this chip id does not exist",status_code=status.HTTP_404_NOT_FOUND)

    def get(self,request,chip_id):
        sensors = self.get_object(chip_id)
        serializer = ESPSensorSerializer(sensors,many=True)
        return Response(serializer.data)
        
    def post(self,request,chip_id):
        request.data['time_record'] = datetime.datetime.now().strftime("%H:%M:%S") 
        serializer = ESPSensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chip_id=chip_id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

