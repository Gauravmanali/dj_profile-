from django.shortcuts import render,HttpResponseRedirect
#from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

def sign_up(request):
    if  request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm = SignUpForm()
    
    return render(request, 'enroll/signup.html',{'form':fm})

#Login view 
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
                fm = AuthenticationForm(request=request,data=request.POST)
                if fm.is_valid():
                    uname = fm.cleaned_data['username']
                    upass = fm.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request,user)
                        return HttpResponseRedirect('/profile/')
                
        else:
            fm=AuthenticationForm()
        return render(request,'enroll/userlogin.html',{'form': fm})
    else:
        return HttpResponseRedirect('/profile/')

#profile

def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'enroll/profile.html',{'name': request.user})
    else:
        return  HttpResponseRedirect("/login/")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'enroll/changepass.html',{'form':fm})

    else:
        return HttpResponseRedirect('/login/')
