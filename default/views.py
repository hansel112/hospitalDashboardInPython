from django.core.paginator import Paginator
from django.db.models import Q
from . models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

# Create your views here.
def homepage(request, *args, **kwargs):
   if request.method == "POST":
      uname = request.POST['uname']
      pword = request.POST['pword']
      user = authenticate(request, username = uname, password = pword)
      if user is not None:
         login(request, user)
         return redirect("/dashboard/")
      else:
         messages.error(request, "Please provide valid credentials")
   context = {

   }
   if request.user.is_authenticated:
      return redirect('/dashboard/')
   response = render(request, "login.html", context)
   return HttpResponse(response)


def register(request, *args, **kwargs):
   if request.method == "POST":
      fname = request.POST['fname']
      lname = request.POST['lname']
      uname = request.POST['uname']
      email = request.POST['email']
      pword = request.POST['pword']
      patient_id = request.POST['pid']
      location = request.POST['loc']
        
      user = User.objects.filter(username = uname).exists()
      if user == True:
         messages.error(request,"Username already exists")
         return redirect('/register/')
      user = User.objects.create(
         first_name = fname,
         last_name = lname,
         username = uname,
         email = email
      )
      user.set_password(pword)
      PatientProfile.objects.create(
         user = user,
         patient_id = patient_id,
         location = location
      )
      messages.info(request, f"Hello {user.get_full_name()}, your registration was successfull")
   q = request.GET.get("username")
   if q:
      user = User.objects.filter(username = q).exists()
      if user == True:
         return HttpResponse(json.dumps({"message":"Username already taken up"}))
      return HttpResponse(json.dumps({"message":"Username is valid"}))
   context = {

   }
   response = render(request, "register.html", context)
   return HttpResponse(response)

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request, *args, **kwargs):
   all_hospitals = Hospital.objects.all()
   services = Services.objects.all()
   locations = all_hospitals.values("location")
    
   page = request.GET.get("page")
   search = request.GET.get("search")
   service = request.GET.get("service")
   location = request.GET.get("location")
   if service and location:
      all_hospitals = all_hospitals.filter(location = location, services = Services.objects.get(name=service))
   if search:
      all_hospitals = all_hospitals.filter(Q(name__icontains = search) | Q(location__icontains = search))
   all_hospital = Paginator(all_hospitals, 4)
   if page:
      all_hospitals = all_hospital.get_page(page)
   else:
      all_hospitals = all_hospital.get_page(1)
   context={
      "services":services,
      "locations":locations,
      "hospitals":all_hospitals
   }
   response = render(request, "dashboard.html", context)
   return HttpResponse(response)

@login_required(login_url=settings.LOGIN_URL)
def logout_view(request, *args, **kwargs):
   logout(request)
   return redirect("/")

@login_required(login_url=settings.LOGIN_URL)
def profile_view(request, *args, **kwargs):
   current_user = PatientProfile.objects.get(user = request.user)
   current_u = User.objects.get(username = request.user.username)
   print(current_user)
   if request.method == "POST":
      fname = request.POST['fname']
      lname = request.POST['lname']
      uname = request.POST['uname']
      email = request.POST['email']
      patient_id = request.POST['pid']
      location = request.POST['loc']
        
      current_user.patient_id = patient_id
      current_user.location = location
      current_u.first_name = fname
      current_u.last_name = lname
      current_u.email = email
      current_u.username = uname
      current_user.save()
      current_u.save()
      messages.info(request, f"Congratulations {current_user.user.get_full_name()}, your information was successfully updated!")
   context = {
      "current_user":current_user
   }
   response = render(request, "profile.html", context)
   return HttpResponse(response)

def aboutview(request, *args, **kwargs):
   response = "<h1>This is the about page of our hospital. do you wish to continue? <h1>"
   return HttpResponse(response)