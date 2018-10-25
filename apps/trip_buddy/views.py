from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
from django.db.models import Q
from .models import User, Trip
from datetime import datetime

def index(request):
    print('index')
    return render(request, "trip_buddy/index.html")

def flash_errors(errors, request):
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)

def register(request):
    errors = User.objects.validate_registration(request.POST)
    print('register works')
    context = {} 
    if errors: 
        flash_errors(errors, request)

    elif not errors:
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        request.session['password'] = request.POST['password']
        request.session['password_confirmation'] = request.POST['password_confirmation']
        
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = request.POST['password']
        )
        context = {'user' : user}
        print('user created...', user)
        request.session['id'] = user.id 
        return redirect('/show_dashboard')

    return redirect('/')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if errors: 
        flash_errors(errors, request)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        login_password = request.POST['password']
        request.POST['email'] == user.email
        context = {'user' : user}
        request.session['id'] = user.id 
        print('successful login')
        return redirect('/show_dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def show_dashboard(request):
    user = User.objects.get(id = request.session['id'])
    current_user_trips = Trip.objects.filter(Q(trip_creator = user) | Q(participant = request.session['id'])) 
    other_user_trips = Trip.objects.exclude(participant = request.session['id'])
    context = {
        'user' : user,
        'current_user_trips' : current_user_trips, 
        'other_user_trips' : other_user_trips
    }
    return render(request, 'trip_buddy/trip_dashboard.html', context)

def add_trip(request):
    user = User.objects.get(id = request.session['id'])
    context = {'user' : user}
    return render(request, 'trip_buddy/addtrip.html', context)

def create_trip(request):
    user = User.objects.get(id = request.session['id'])
    errors = Trip.objects.validate_trip(request.POST)
    context = {'user' : user}
    if len(errors) > 0:
        flash_errors(errors, request)
    elif not errors:
        trip = Trip.objects.create(
            location = request.POST['location'],
            plan = request.POST['plan'],
            trip_creator = user,
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date']
        )
        return redirect('/show_dashboard')
    return render(request, 'trip_buddy/addtrip.html', context)

def delete_trip(request, id):
    user = User.objects.get(id = request.session['id'])
    deleting_trip = Trip.objects.get(id = id)
    deleting_trip.delete()
    return redirect('/show_dashboard')

def show_trip_detail(request, id):
    user = User.objects.get(id = request.session['id'])
    trip = Trip.objects.get(id = id)
    others = User.objects.filter(member__id = trip.id)
    context = {
        'user' : user,
        'trip' : trip, 
        'others' : others
    }
    return render(request, 'trip_buddy/showtrip.html', context)

# Created Admin User that will inherit a trip that the current user drops from 
admin = User.objects.create(first_name = 'Admin',last_name = 'User', email = 'admin@admin.com',password = 'adminadmin')

def join_trip(request, id): 
    print('joining trip')
    trip_joiner = User.objects.get(id = request.session['id'])
    print('trip joiner')
    print(trip_joiner)
    joining_trip = Trip.objects.get(id = id)
    joining_trip.participant.add(trip_joiner)
    if joining_trip.trip_creator.first_name == 'Admin': 
        print('reassigning admin trip')
        joining_trip.trip_creator = trip_joiner
        joining_trip.trip_creator.save() 
    current_user_trips = Trip.objects.filter(Q(trip_creator = trip_joiner) | Q(participant = request.session['id'])) 
    other_user_trips = Trip.objects.exclude(participant = request.session['id'])
    context = {
        'user' : trip_joiner,
        'current_user_trips' : current_user_trips, 
        'other_user_trips' : other_user_trips
    }
    return render(request, 'trip_buddy/trip_dashboard.html', context)

def cancel_trip(request, id): 
    user = User.objects.get(id = request.session['id'])
    trip = Trip.objects.get(id = id)
    trip.participant.clear() 
    trip.save()
    if trip.trip_creator == user: 
        trip.trip_creator = admin
        trip.save() 
    return redirect('/show_dashboard')
