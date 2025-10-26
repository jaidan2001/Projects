from typing import Any
from django.shortcuts import redirect
from django.urls import reverse
from .models import User


class CheckUserMiddleware:

    EXCLUDED_PATHS = ['/', '/signin/', '/signup/', '/admincreate/']
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path_info, "hy")

        if request.path_info in self.EXCLUDED_PATHS:
            if 'username' in request.session :
                if request.session['username'] != '' :
                    return redirect('/dashboard/')
                
            response = self.get_response(request)
            return response
        
        elif request.path_info == '/adminlogin/':
            if 'superusername' in request.session :
                if request.session['superusername'] != '' :
                    return redirect('/admindashboard/')
                    
            response = self.get_response(request)
            return response
        
        elif 'superusername' in request.session :

            if request.session['superusername'] != '':
                reaponse = self.get_response(request)
                return reaponse
            else:
                return redirect('adminlogin')
        
        elif 'username' in request.session :
            
            if request.session['username'] != ''  :
                if request.path_info in ['/admindashboard/']:
                    user = User.objects.get(username = request.session['username'] )
                    if user.role == 'admin':
                        reaponse = self.get_response(request)
                        return reaponse
                    return redirect('/dashboard/')
                else:
                    reaponse = self.get_response(request)
                    return reaponse
            else:
                
                return redirect('signin')
        else:
            return redirect('signin')