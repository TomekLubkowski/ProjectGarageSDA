from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Repairs, Car, Client
from .forms import RepairForm, carForm, UserTypeLoginForm, UserTypeRegistrationForm
# import requests

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserTypeLoginForm

def loginPage(request):
    if request.method == 'POST':
        form = UserTypeLoginForm(request, data=request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return redirect('login')  # przekierowanie na strone logowania

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user_type == 'customer':
                    return redirect('clientlogin')  # przekierowanie na stronę klienta
                elif user_type == 'mechanic':
                    return redirect('mechaniclogin')  # przekierowanie an strone mechanika
            else:
                messages.error(request, 'Incorrect username or password')
                return redirect('login')  # Przekierowanie z powrotem do strony logowania z komunikatem o błędzie
    else:
        form = UserTypeLoginForm(request)

    context = {'form': form}
    return render(request, 'garage/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')

def registerPage(request):
    if request.method == 'POST':
        form = UserTypeRegistrationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            user = form.save()
            if user_type == 'mechanic':
                specialization = request.POST.get('specialization')
                Mechanic.objects.create(user=user, specialization=specialization)
            return redirect('login')  # Przekierowanie do strony logowania po udanej rejestracji
    else:
        form = UserTypeRegistrationForm()

    context = {'form': form}
    return render(request, 'garage/login_register.html', context)

@login_required(login_url="login/")
def home(request):
    repairs = Repairs.objects.all()
    cars = Car.objects.all()
    active_repairs = Repairs.objects.filter(status__in=['New', 'Pending'])
    activeRepairsCount = Repairs.objects.filter(status__in=['New', 'Pending']).count()
    closedRepairsCount = Repairs.objects.filter(status__in=['End']).count()

def repair(request, pk):
    repair = Repairs.objects.get(id=pk)
    car = Car.objects.get(id=repair.car_id)

    context = {'repair': repair, 'car': car}
    return render(request, 'garage/repair.html', context)

def createRepair(request):
    form = RepairForm()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.user = request.user
            repair.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'garage/create_repair.html', context)

def updateRepair(request, pk):
    repair = Repairs.objects.get(id=pk)
    form = RepairForm(instance=repair)
    if request.method == 'POST':
        form = RepairForm(request.POST, instance=repair)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'garage/create_repair.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    repairs = user.repair_set.all()
    context = {'user': user, 'repairs': repairs}
    return render(request, 'garage/profile.html', context)

def addCar(request):
    form = carForm()
    if request.method == 'POST':
        form = carForm(request.POST)
        if form.is_valid():
            addcar = form.save(commit=False)
            addcar.user = request.user
            addcar.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'garage/add_car.html', context)

def car(request, pk):
    car = Car.objects.get(id=pk)
    repair = Repairs.objects.get(id=pk)
    context = {'car': car, 'repair': repair}
    return render(request, 'garage/car.html', context)

def activeRepairByCar(request, pk):
    car = Car.objects.get(id=pk)
    active_repairs = Repairs.objects.get().filter(id=car.id)

    context = {
        'car': car, 
        'active_repairs': active_repairs
    }
    return render(request, 'garage/active_repairs.html', context)

def repairstatus(request, pk):
    repair = Repairs.objects.get(id=pk)
    context = {'repair': repair}
    return render(request, "garage/repair_status.html", context)

def clientLogin(request):
    return render(request, 'garage/client_login.html')

def mechanicLogin(request):
    return render(request, 'garage/mechanic_login.html')

def index(request):
    return render(request, 'garage/index.html')

