from django.contrib import admin
from Boards.models import ESP8266, ESPSensor


class ESP8266Admin(admin.ModelAdmin):
    list_display = ['id','name','chip_id','board_up_time','flash_free_space','ram_free_space','user_email']

    def user_email(self,obj):
        return obj.user.email
    pass


class ESPSensorsAdmin(admin.ModelAdmin):
    list_display = ['id','board_name','name','type','status','time_record','duration']

    def board_name(self,obj):
        return obj.board.name
    pass

admin.site.register(ESPSensor,ESPSensorsAdmin)
admin.site.register(ESP8266,ESP8266Admin)