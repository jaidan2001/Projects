from django.shortcuts import render,redirect, HttpResponse
from .models import User,Movie, Theater, Showtime,Booked,Seats_booked
from .forms import UserForm,MovieForm,TheaterForm, ShowtimeForm, BookedForm
import razorpay
from MovieMagnet.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.http import JsonResponse
from datetime import date
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



def signup(request):
    print('signup')
    if request.method == "GET":
        return render(request, 'login_signup.html')
    
    elif request.method == "POST":

        username_from_signup = request.POST.get('username')
        password_from_signup = request.POST.get('password')
        email_from_signup = request.POST.get('email')

        user_check = User.objects.filter(username = username_from_signup)
        email_check = User.objects.filter( email= email_from_signup)
        
        if user_check.exists() or email_check.exists():
            response = f"""
                <script> 
                window.alert('User already exists')
                window.location.href = '/';
                </script>
                """
            return HttpResponse(response)
            
            
        else:
            user_obj = User(username = username_from_signup, password = password_from_signup, email = email_from_signup)
            user_obj.save()

            response = f"""
                <script> 
                window.alert('User created sucessfully')
                window.location.href = '/landing';
                </script>
                """
            return HttpResponse(response)


def signin(request):
    print("SIGNIN")
    if request.method == "POST":
       
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        # user = authenticate(request, username = username, password = password)
        user = User.objects.filter(username= username).first()
        if user is not None:
            if user.password and user.password == password:
                request.session['username'] = username
                # print(request.session.get('username'))
                
                movies= Movie.objects.all()
                data = {}
                in_movie ={}
                id= 0
                for movie in movies:
                    if movie.status == "soon":
                        id+=1
                        value = {
                            "id_m":movie.id,
                            "url":movie.poster,
                            "text":movie.name
                        }
                        data[str(id)] = value
                    elif movie.status == "in":
                        value = {
                            "url" : movie.poster,
                            "name" : movie.name,
                            "language" : movie.language
                        }
                        in_movie[movie.name] = value
                        


                return render(request, 'homepage.html', {"userInfo" :user,'data' :data, 'count':id, "in_movie":in_movie})
                
            else:
                response = f"""
                <script> 
                window.alert('WRONG PASSWORD')
                window.location.href = '/';
                </script>
                """
                return HttpResponse(response)
        else:
            response = f"""
                <script> 
                window.alert('No User Found')
                window.location.href = '/';
                </script>
                """
            return HttpResponse(response)
    else:
       return redirect('landing')
    
def landing_page(request):
    return render(request, "login_signup.html")
    


def dashboard(request):

    if request.method == "GET":
        
        if "username" in request.session :
            userinfo = request.session['username']
            user = User.objects.get(username = userinfo)
            
            
        else:
            userinfo = request.session['superusername']
            user = User.objects.get(username = userinfo )
            
        movies = Movie.objects.all()
        id = 0
        data={}
        in_movie = {}
        for movie in movies:
            if movie.status == "soon":
            
                id= id +1
                
                value =  {
                        "id":id,
                        "url":movie.poster,
                        'text':movie.name
                    }
                
                data[str(id)]= value
            
            elif movie.status == "in":
                value = {
                    "url" : movie.poster,
                    "name" : movie.name,
                    "language" : movie.language
                }
                in_movie[movie.name] = value

   
        return render(request, 'homepage.html', {"userInfo" :user, "data":data, "count":id, "in_movie":in_movie})
    
   

    else:
        print("HERE")

def movie_view_page(request, movie_name):
    movie = Movie.objects.get(name = movie_name)
    
    return render(request, "movieviewpage.html",{'movie' :movie} )
sdate = ""
def booking_page(request, movie_name):
    global sdate
    kdate=''
    current_time=''
    if request.method == "POST":
        sdate = request.POST["date"]
        kdate = sdate
        current_time = datetime.now().strftime("%H:%M")
        

    
    movie = Movie.objects.get(name = movie_name)
    theater = Showtime.objects.all()
    theaterlocation = Theater.objects.all()
    tdate=date.today()
    
    nextdate = date.today()+timedelta(1)
    afternextdate = date.today()+timedelta(2)
   
    print(current_time)
    def format_day_without_padding(date):
        formatted_date = date.strftime("%b. %d, %Y")
        return formatted_date.replace(" 0", " ")
    unique_time = {}
    formatted_date = format_day_without_padding(tdate)
    final_show_time= []
    
    if kdate == formatted_date:
        l=[]
        l2=[]
        current_time_store=''
        for i in current_time:
            if i in [':']:
                l.append(int(current_time_store))
                current_time_store = ''
            else:
                current_time_store += i
        if current_time_store:
            
            l.append(int(current_time_store))
            current_time_store =''
        


        for time in theater:
            unique_time[time.time] = time.time
        
        for time1 in unique_time:
            l1=[]
            for i in time1:
                
                if i in [':']:
                    l1.append(int(current_time_store))
                    current_time_store = ''
                else:
                    current_time_store += i
                
            if current_time_store:
                l1.append(int(current_time_store))
                unique_time[time1] =l1
                current_time_store =''
            l2.append(l1)
            
   
        current_time_compare = l[0]*100 + l[1]        
        
        
        for i in l2:
            show_time_compare = i[0]*100+i[1]
            
            if current_time_compare<show_time_compare  :
                for i in unique_time:
                    s = unique_time[i]
                    sum = s[0]*100+s[1]
                    if show_time_compare == sum:
                        final_show_time.append(i)
                    
    
    else:
        for time in theater:
            unique_time[time.time] = 1
        for i in unique_time:
            final_show_time.append(i)
        
    print(final_show_time)

    return render(request, "bookingpage.html", {"movie" : movie,  "theater_details" : theater, "theater_location":theaterlocation,"tdate":tdate,"t1date":nextdate,"t2date":afternextdate, "sdate":kdate, "current_time":current_time, "final_show_time":final_show_time})

def seats(request, name, price ,moviename, time):
    
    seats = Theater.objects.filter(name = name).first()
    seat_booked_l ={}
    print(sdate)
    booked_seat = Seats_booked.objects.filter(moviename= moviename, time = time,tname = name, date = sdate )
    print(booked_seat)
    seat_count = seats.totalseats
    seat_firt_two = int(seat_count)//10
    
    k= [10,9,8,7,6,5,4,3,2,1]
    seat = []
    for i in range(1,seat_firt_two+1):
        seat.append(i)

    for row in k:
        for s in seat:
            row_str = str(row)
            s_row = str(s)
            sum = row_str+'-'+s_row
            seat_booked_l[sum] = 0
    
    for i in booked_seat :
        if i.seat_number in seat_booked_l:
            seat_booked_l[i.seat_number] =1
    list_booked_seat = []
    for i in booked_seat:
        list_booked_seat.append(i.seat_number)
    
    context ={ 'booked_seat':seat_booked_l, 'theater':seats, "k" : list_booked_seat,'seats':seat,'seat_num':seat_firt_two, 'price':price, 'moviename':moviename , 'time':time}
    
    
    return render(request, 'seats.html',context )


def logout(request):
    request.session.clear()
    return redirect('/')

def create_admin(request):
    try:
        
        obj = User(username = "admin", password="admin", email="admin@gmail.com", role="admin")
        obj.save()
        response = f"""
                <script> 
                window.alert('admin created sucessfully')
                window.location.href = '/';
                </script>
                """
        return HttpResponse(response)
    except:
        print("username is already taken")

    return redirect('/')

def admin_login(request):
    print( request.path_info)
    

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username).first()
        if user is not None:
            if user.password and user.password == password and user.role == 'admin':
                request.session['superusername'] = username
                return render(request, 'admindashboad.html')
            else:

                response = f"""
                            <script> 
                            window.alert('Wrong Username or Password')
                            window.location.href = '/adminlogin/';
                            </script>
                            """
                return HttpResponse(response)
        else:
            response = f"""
                <script> 
                window.alert('No User Found')
                window.location.href = '/adminlogin/';
                </script>
                """
            return HttpResponse(response)
    return render(request, 'adminloginpage.html')

def admin_logout(request):
    request.session.clear()
    return redirect('/adminlogin/')

def admin_dashboard(request):
    
    return render(request, 'admindashboad.html')

def admin_user(request):
    user = User.objects.all()

    return render(request, 'adminuser.html', {'userinfos' : user})

def user_information(request, username):
    if request.method == "GET":
        user = User.objects.get(username = username)
        return render(request, 'adminuserinfo.html', {'user': user})
    if request.method == "POST":
        changing_username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        
        
        changing_user_info = User.objects.filter(username = username).first()

        changing_user_info.username = changing_username
        changing_user_info.email =email
        changing_user_info.password = password
        changing_user_info.role = role
        changing_user_info.save()

        rename = User.objects.get(username = changing_username )

        return render(request, 'adminuserinfo.html', {'user' : rename})

# def admin_changed_user_info(request):
#     if request.method == "POST":
#         changed_username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role ')
#         print(changed_username,email,password,role)
        
#         return render(request, 'adminuserinfo.html')
  

def admin_user_add(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'adminadduser.html', {'form' : form})
    elif request.method =='POST':
        form_recived = UserForm(request.POST)
        
        
        if form_recived.is_valid():
                form_recived.save()
                response = f"""
                    <script> 
                    window.alert('User created sucessfully')
                    window.location.href = '/adminuser/';
                    </script>
                    """
                return HttpResponse(response)

            
        else:
            response = f"""
                    <script> 
                    window.alert('User already exists')
                    window.location.href = '/adminuser/' ;
                    </script>
                    """
            return HttpResponse(response)
            
    
def admin_delete_user(request,user):
    print(user) 
    delete_user = User.objects.get(username = user)
    delete_user.delete()
    return redirect('/adminuser/')



#-----------MAnageMovie--------------------#

def admin_manage_movie(request):
    movieinfos = Movie.objects.all()
    return render(request, 'adminmanagemovie.html',{'movieinfos' : movieinfos})


def admin_add_movie(request):

    if request.method == "GET":
        form = MovieForm()
        return render(request, 'adminaddmovies.html', {'form' : form})
    elif request.method =='POST':
        form= MovieForm(request.POST, request.FILES)
    
        
        if form.is_valid():
            form.save()
            response = f"""
                    <script> 
                    window.alert('Movie added sucessfully')
                    window.location.href = '/adminmanagemovie/';
                    </script>
                    """
            return HttpResponse(response)

            
        else:
            response = f"""
                    <script> 
                    window.alert('Error')
                    window.location.href = '/adminaddmovie/' ;
                    </script>
                    """
            return HttpResponse(response)

def admin_edit_movie(request,id):
    if request.method=="GET":
        movie = Movie.objects.filter(id = id).first()
        return render(request, "admineditmovie.html", {'movie':movie})
    elif request.method == "POST":
        poster = request.FILES.get('poster')
        trailer = request.POST['trailer']
        name = request.POST['name']
        description = request.POST['description']
        cast = request.POST['cast']
        language = request.POST['language']
        release_date = request.POST['releasedate']
        status = request.POST['status']
        
        movie_changing = Movie.objects.filter(id = id).first()
        
        movie_changing.poster = poster
        movie_changing.trailer = trailer
        movie_changing.name = name
        movie_changing.description = description
        movie_changing.cast = cast
        movie_changing.language = language
        movie_changing.release_date = release_date
        movie_changing.status = status

        movie_changing.save()

    
        rename = Movie.objects.get(id = id )

        return render(request, 'admineditmovie.html', {'movie':rename})
        
def admin_delete_movie(request,id):
    
    movie = Movie.objects.filter(id = id).first()
    movie.delete()
    return redirect('/adminmanagemovie/')

def admin_add_theater(request):
     if request.method == "GET":
        form = TheaterForm()
        context = {'form' : form}
        
        return render(request, 'adminaddtheater.html',context)
     elif request.method == "POST":
        form_recived = TheaterForm(request.POST)
        if form_recived.is_valid():
            form_recived.save()
            response = f"""
                    <script> 
                    window.alert('Theater added sucessfully')
                    window.location.href = '/adminaddtheater/';
                    </script>
                    """
            return HttpResponse(response)
        else:
            response = f"""
                    <script> 
                    window.alert('Error')
                    window.location.href = '/adminmanagetheater/';
                    </script>
                    """
            return HttpResponse(response)

def admin_manage_theater(request):
    theater = Theater.objects.all()
    context = {'theater' : theater}
    return render(request, "adminmanagetheater.html", context)

def admin_edit_theater(request,id):
    if request.method == "GET":
        thaeter = Theater.objects.get(id = id)
        return render(request, 'adminedittheater.html', {'theater' : thaeter})
    elif request.method == "POST":
        name = request.POST['name']
        location = request.POST['location']
        totalseats = request.POST['totalseats']
        price = request.POST['price']
        
        theater_changed = Theater.objects.filter(id = id).first()
       
        theater_changed.name = name
        theater_changed.location = location
        theater_changed.totalseats = totalseats
        theater_changed.price = price

        theater_changed.save()
        new_theater = Theater.objects.get(id = id)
        return render(request, 'adminedittheater.html', {'theater' : new_theater})




def admin_delete_theater(request, id):
    obj = Theater.objects.filter(id =id).first()
    obj.delete()
    return redirect('/adminmanagetheater/')

def admin_manage_showtime(request):
    showtime = Showtime.objects.all()
    context = {
        "showtimes":showtime
    }
    return render(request, 'adminmanageshowtime.html', context)

def admin_add_showtime(request):
    if request.method == "GET":
        form = ShowtimeForm()
        context = {'form' : form}
        
        return render(request, 'adminaddshowtime.html',context)
    if request.method == "POST":
        form_recived = ShowtimeForm(request.POST)
        if form_recived.is_valid():
            form_recived.save()
            response = f"""
                    <script> 
                    window.alert('Showtime added sucessfully')
                    window.location.href = '/adminaddshowtime/';
                    </script>
                    """
            return HttpResponse(response)
        else:
            response = f"""
                    <script> 
                    window.alert('Error')
                    window.location.href = '/adminmanageshowtime/';
                    </script>
                    """
            return HttpResponse(response)

def admin_edit_showtime(request,id):
    if request.method == "GET":
        showtime = Showtime.objects.get(id = id)
        return render(request, 'admineditshowtime.html', {'showtime' : showtime})
    # elif request.method == "POST":
    #     name = request.POST['name']
    #     time = request.POST['location']
    #     movie = request.POST['totalseats']
        
    #     showtime_changed = Showtime.objects.filter(id = id).first()
       
    #     showtime_changed.name = name
    #     showtime_changed.time = time
    #     showtime_changed.movie = movie
    

    #     showtime_changed.save()
    #     new_showtime = Showtime.objects.get(id = id)
    #     return render(request, 'adminedittheater.html', {'showtime' : new_showtime})


def admin_delete_showtime(request,id):
    deleteobj = Showtime.objects.filter(id = id ).first()
    deleteobj.delete()
    return redirect('/adminmanageshowtime/')

def admin_manage_booked(request):
    obj = Booked.objects.all()
    context = {
        "booked":obj
    }
    return render(request, 'adminmanagebooked.html', context)


def admin_add_booked(request):
    if request.method == "GET":
        form = BookedForm()
        context = {'form' : form}
        
        return render(request, 'adminaddbooked.html',context)
    if request.method == "POST":
        form_recived = BookedForm(request.POST)
        if form_recived.is_valid():
            form_recived.save()
            response = f"""
                    <script> 
                    window.alert('Booked sucessfully')
                    window.location.href = '/adminaddbooked/';
                    </script>
                    """
            return HttpResponse(response)
        else:
            response = f"""
                    <script> 
                    window.alert('Error')
                    window.location.href = '/adminmanagebooked/';
                    </script>
                    """
            return HttpResponse(response)

def admin_delete_booked(request,id):
    deleteobj = Booked.objects.filter(id = id ).first()
    deleteobj.delete()
    return redirect('/adminmanagebooked/')

context_payment_details = {}

def payment(request,tname,moviename,time):
    global context_payment_details
    if request.method == 'POST':
        seatnumber =  request.POST["seatnumbers"]
        numberofseats = request.POST.get("numberofseats")
        totalprice = request.POST.get("totalprice")
    
        client = razorpay.Client(auth=('rzp_test_tlIylwNekuL1h7', 'ixf977my2Ga4K5wkDDch2RFN'))
        
        totalprice_in_paisa = int(totalprice)*100
        
        data = { "amount": totalprice_in_paisa, "currency": "INR" }
        try:
            payment = client.order.create(data=data)
        except:
            print("Error occured")
        
        language_select = Movie.objects.get(name = moviename)
        language = language_select.language
        tdate = sdate
        
        context_payment_details = {
            'tname' : tname,
            'moviename': moviename,
            'language' : language,
            'seatnumbers':seatnumber,
            'totalprice':totalprice,
            "numberofseats" : numberofseats,
            'time':time,
            'date':tdate,
            'response':payment['id']
        }

        return render(request, 'payment.html', context_payment_details)
    elif request.method == "get":
        return render(request, 'paymentsucess.html')


def payment_sucess(request):
    if "username" in request.session :
        user_name = request.session['username']
   
    else:
        user_name = request.session['superusername']
    obj = Booked(username = user_name, movie_name = context_payment_details['moviename'],theater_name=context_payment_details['tname'],language=context_payment_details['language'],time=context_payment_details['time'],seatnumber=context_payment_details['seatnumbers'],totalseats=context_payment_details['numberofseats'],price=context_payment_details['totalprice'],date=context_payment_details['date'])
    obj.save()

    seat_num = context_payment_details['seatnumbers']
    seat = ''
    for char in seat_num:
        if char == ',':
            print(seat)
            obj2 = Seats_booked(seat_number = seat,time=context_payment_details['time'],date=context_payment_details['date'],moviename=context_payment_details['moviename'],tname=context_payment_details['tname'])
            obj2.save()
            seat = ''
        else :
            seat+=char
    if seat:
        obj2 = Seats_booked(seat_number = seat,time=context_payment_details['time'],date=context_payment_details['date'],moviename=context_payment_details['moviename'],tname=context_payment_details['tname'])
        obj2.save()
        print(seat)
        
    return render(request, 'paymentsucess.html')
def payment_error(request):
    return render(request, 'paymenterror.html')
def booked(request):
    
        

    return redirect('/dashboard/')

def your_order(request):
    dict ={}

    if "username" in request.session:
        user = request.session["username"]
    else:
        user = request.session["superusername"]

    your_order_from_booked = Booked.objects.filter(username = user)
    i=1
    for order in your_order_from_booked:
        
        movie_for_poster = Movie.objects.get(name = order.movie_name)
        location_theater = Theater.objects.get(name = order.theater_name)
        value = {
            "id":order.id,
            "poster" : movie_for_poster.poster,
            "movie_name" :order.movie_name,
            "theater_name":order.theater_name,
            'lang':order.language,
            'location':location_theater.location,
            'seatnumber':order.seatnumber,
            "date":order.date,
            "time":order.time

        }
        dict[str(i)] = value
        i+=1

        
    context={
        "dict":dict
    }
    print(dict)
    return render(request, "yourorders.html", context)

def view_ticket(request,id):

    booked_deatils = Booked.objects.get(id = id)
    movie_for_poster = Movie.objects.get(name =booked_deatils.movie_name)
    location_theater = Theater.objects.get(name = booked_deatils.theater_name)
    context = {
        "details":booked_deatils,
        "posterimg":movie_for_poster,
        'location':location_theater.location,
    }
    return render(request, 'viewticket.html',context)

def search_page(request):
    if request.method == "POST":
        search = request.POST['search']
        movies = Movie.objects.filter(name__contains = search)

        context = {
            "movies":movies,
            "search":search
        }
        return render(request, 'searchpage.html', context)
    else:
        return render(request, 'searchpage.html')
    