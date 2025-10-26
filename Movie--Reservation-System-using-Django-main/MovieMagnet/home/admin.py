from django.contrib import admin
from .models import User
from .models import Movie, Theater, Showtime,Booked,Seats_booked
# Register your models here.

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Showtime)
admin.site.register(Booked)
admin.site.register(Seats_booked)