from django.urls import path
from Boards.views import  ESPDetails, ESPList,ESPSensorApiView

urlpatterns = [
    path('esp/', ESPList.as_view()),
    path('esp/<str:chip_id>', ESPDetails.as_view()),
    path('esp/sensors/<str:chip_id>', ESPSensorApiView.as_view()),
]