from django.db import models

# Create your models here.


class User(models.Model):
    role_choice = {'customer' : 'customer',
            'admin' : 'admin'}

    username = models.CharField(max_length = 20, unique=True)
    password = models.CharField(max_length = 8)
    email = models.EmailField(max_length = 50)
    role = models.CharField(max_length=100,choices = role_choice ,default= "customer")

    def __str__(self) -> str:
        return self.username
    
class Movie(models.Model):
    status_choice = {'in' : 'In', 
                     'out' : 'Out',
                     'soon' : 'Soon'}
    languages_choice = {'hindi':'Hindi',
                        'malayalam':'Malayalam',
                        'tamil':'Tamil',
                        'english':'English'}
    
    poster = models.ImageField(upload_to='picture', blank=True, null=True)
    trailer = models.URLField(default = None)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    cast = models.CharField(max_length = 255)
    language = models.CharField(max_length = 255, choices = languages_choice)
    release_date = models.DateField()
    runtime = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255, choices = status_choice)
    
    

    def __str__(self) -> str:
        return self.name
    

class Theater(models.Model):

    name = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    totalseats = models.CharField(max_length=255)
    price = models.CharField(max_length = 10)

    def __str__(self) -> str:
        return self.name

class Showtime(models.Model):
    time_choice = {
        '05:00':'05:00 AM',
        '10:10':'10:10 AM',
        '14:15':'02:15 PM',
        '17:30':'05:30 PM',
        '20:30':'08:30 PM',
        '23:45':'11:45 PM'
    }

    name = models.ForeignKey(Theater, on_delete=models.CASCADE)
    time = models.CharField(max_length=255, choices=time_choice)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return f"{self.name} - {self.time} - {self.movie}"
class Booked(models.Model):
    username = models.CharField(max_length =255)
    movie_name = models.CharField(max_length = 255)
    theater_name = models.CharField(max_length = 255)
    language = models.CharField(max_length = 255)
    time = models.CharField(max_length=255)
    seatnumber = models.CharField(max_length= 255)
    totalseats = models.CharField(max_length = 255)
    price = models.CharField(max_length = 255)
    date = models.CharField(max_length = 255)

class Seats_booked(models.Model):
    seat_number = models.CharField(max_length = 255)
    time = models.CharField(max_length = 255)
    date = models.CharField(max_length = 255)
    moviename = models.CharField(max_length = 255)
    tname = models.CharField(max_length = 255)

