from django.contrib import admin
from models import UserDetail, Train, Station, DepartureDay, Reservation

admin.autodiscover()

# Register your models here.

admin.site.register(UserDetail)
admin.site.register(Train)
admin.site.register(Reservation)
admin.site.register(Station)
admin.site.register(DepartureDay)