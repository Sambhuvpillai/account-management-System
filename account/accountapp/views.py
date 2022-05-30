from django.shortcuts import render,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import os
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def index(request):
    return render(request, 'index.html')

# ///////////////////////////sign_up

def register(request):
    return render(request, 'signup.html')
@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        address=request.POST.get('address')
        email=request.POST.get('email')
        uname=request.POST.get('uname')
        passw=request.POST.get('passw')
        cpassw=request.POST.get('cpassw')
        gender=request.POST.get('gender')
        mobile=request.POST.get('mobile')
        photo=request.FILES.get('photo')
        # if request.FILES.get('file') is not None:
        #     photo = request.FILES['file']
        # else:
        #     photo = "static/img/default.png"
        dob=request.POST.get('dob')
        if cpassw==passw:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'This Username is already taken!!!')
                return redirect('sign_up')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'This Email is already taken!!!')
                return redirect('sign_up')
            else:
                user = User.objects.create_user(first_name=fname,
                                                last_name=lname,
                                                email=email,
                                                username=uname,
                                                password=passw)
                subject = 'iNFox Technologies'
                message = 'you are successfully registered our company and dont replay this mail because it is an computer generated mail'
                recipient = user.email
                
                send_mail(subject, message,settings.EMAIL_HOST_USER, [recipient])
                print('send mail')
                user.save()
                
                u=User.objects.get(id=user.id)
                member=Employee(user_address=address,
                                    user_gender=gender,
                                    user_mobile=mobile,
                                    user=u,
                                    user_photo=photo,
                                    DOB=dob)
                member.save()
                
                return redirect('load_loginpage')
    return redirect('register')

# //////////////////////////////////////login

def load_loginpage(request):
    return render(request, 'login.html')
@csrf_exempt
def userlogin(request):

    if request.method =='POST':
        try:
            username = request.POST['uname']
            password = request.POST['passw']
            user = auth.authenticate(username=username,password=password)
            request.session["uid"]=user.id
            if user is not None:
                if user.is_staff:
                    login(request,user)
                    return redirect('load_admin_home')
                else:
                    login(request,user)
                    auth.login(request,user)
                    # messages.info(request,f'Welcome { username }')
                    return redirect('load_user_home')
            else:
                messages.info(request,'invalid username or password.Try again!')
                return redirect('login')
        except:
            messages.info(request,'invalid username or password.Try again!')
            return render(request,'login.html')
    else:
        return redirect('login') 
    
    
# //////////////////admin_page 
@login_required(login_url='userlogin')
def load_admin_home(request):
    users = Employee.objects.all()
    return render(request, 'load_admin.html',{'users':users})

# def load_user_home(request):
#     return render(request, 'load_user.html')

def emp_details(request,pk):
    users = Employee.objects.get(id=pk)
    return render(request,'emp_details.html',{'users':users} )

# //////////////////employee_page 
@login_required(login_url='userlogin')
def load_user_home(request):
    users=Employee.objects.filter(user=request.user)
    return render(request, 'load_user.html',{'users':users})

def user_profile(request):
    if request.user.is_authenticated:
        users=Employee.objects.filter(user=request.user)
        return render(request, 'profile.html',{'users':users})
    else:
        return redirect('load_user_home')
    
# /////////////////////edit_page
@login_required(login_url='userlogin')   
def editpage(request):
    users=Employee.objects.get(user=request.user)
    return render(request, 'edit.html',{'users':users})

def edit_profile(request):
    if request.method=='POST':
        users=Employee.objects.get(user=request.user)
        users.user.first_name=request.POST.get('first_name')
        users.user.last_name=request.POST.get('last_name')
        users.user.email=request.POST.get('email')
        users.user.username=request.POST.get('username')
        users.DOB=request.POST.get('DOB')
        users.user_address=request.POST.get('user_address')
        users.user_gender=request.POST.get('user_gender')
        users.user_mobile=request.POST.get('user_mobile')
        users.user_photo=request.FILES.get('user_photo')
        
        users.user.save()
        users.save()
        print('hii')
        
       
        return redirect('user_profile')
    
    return render(request, 'edit.html')


# log___out

@login_required(login_url='userlogin')
def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('index')

# delete____user


def delete_user(request,pk):
    users=Employee.objects.get(id=pk)
    #if users.user_photo is not None:
       ## if not users.user_photo =="/static/img/defult.png":
           # os.remove(users.user_photo.path)
       # else:
           # pass
    users.delete()
    return redirect('load_admin_home')

#/////////////////////////////////// leave
@csrf_exempt
def apply_leave(request):
    users=Leave.objects.filter(user=request.user)
    return render(request, 'leave_apply.html',{'users':users})
@csrf_exempt
def submit_leave(request):
    if request.method=='POST':
        usr=request.user
        # users = Leave.objects.filter(user=request.user)
        stdate=request.POST.get('stdate')
        edate=request.POST.get('edate')
        reson=request.POST.get('reson')
        leve = Leave(user=usr,
                        startdate=stdate,
                        enddate=edate,
                        reason=reson,)
        
        leve.save()
        
        
        messages.success(request,'Leave Request Sent,wait for Admins response',extra_tags = 'alert alert-success alert-dismissible show')
        return redirect('load_user_home')
    return render(request, 'leave_apply.html')

def load_leave_requests(request):
    users = Leave.objects.all().filter(status=False)
    return render(request, 'load_leave_requests.html',{'users':users})
def aprove_leave_req(request):
    aproved = Leave.objects.all().filter(status=True)
    return render(request,'aprove_leave.html',{'aproved':aproved})
def aprove_leave(request,pk):
    leaveStatus = Leave.objects.get(id=pk)
    leaveStatus.status = True
    leaveStatus.save()
    return redirect('aprove_leave_req')
def applied_leaves(request):
    applied = Leave.objects.filter(user=request.user)
    
    return render(request, 'applied_leaves.html',{'applied':applied})
def emp_aproved_leaves(request):
    leave_aproved = Leave.objects.filter(user=request.user).filter(status=True)
    return render(request, 'emp_leavestatus.html',{'leave_aproved':leave_aproved})

def delete_leave(request,pk):
    users=Leave.objects.get(id=pk)
    users.delete()
    return redirect('load_leave_requests')
    
     



