from django.db import models
from datetime import date, datetime

class UserManager(models.Manager): 
    def validate_registration(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 3: 
            errors['first_name_error'] = "First Name must be longer than 3 characters"
        if len(post_data['last_name']) < 3: 
            errors['last_name_error'] = "Last Name must be longer than 3 characters"
        if post_data['email'] == "": 
            errors['email_error'] = "Email cannot be blank"
        if User.objects.filter(email = post_data['email']):
            errors['email_error'] = "This email already exists in our database. Please use new email."
        
        password_confirmation = post_data['password_confirmation']
        if len(post_data['password']) == 0: 
            errors['password_error'] = "Password cannot be blank"
        elif len(post_data['password']) < 8: 
            errors['password_error'] = "Password must be at least 8 characters long"
        elif post_data['password'] != password_confirmation: 
            errors['password_error'] = "Password Confirmation does not match Password field"
        
        return errors
        
    def validate_login(self, post_data): 
        errors = {}
        if not User.objects.filter(email = post_data['email']): 
            errors['email_error'] = "This email has not been registered. Please register before logging in."
        elif len(post_data['email']) < 3: 
            errors['email_error'] = "First Name must be longer than 3 characters"
        elif not User.objects.filter(password = post_data['password']): 
            errors['password_error'] = "Password is not Correct. Please try again."
        
        return errors

class TripManager(models.Manager): 
    def validate_trip(self, post_data):
        errors = {}

        if len(post_data['location']) < 1 :
            errors['location_error'] = "Trip Location can not be empty"
        if len(post_data['plan']) < 5 :
            errors['plan_error'] = "Trip Plan can not be empty"
        if not len(post_data['start_date']):
            errors['start_date_error'] = "Trip Start Date cannot be empty"
        if not len(post_data['end_date']):
            errors['end_date_error'] = "Trip End Date cannot be empty"
        elif str(date.today()) > str(post_data['start_date']):
            errors['start_date_error'] = "Start Date cannot be in the past. Please enter a future date."
        elif post_data['start_date'] > post_data['end_date']:
            errors['end_date_error'] = "End Date can not be in the past. Please enter a future date."
        
        return errors 
        

class User(models.Model): 
    first_name = models.CharField (max_length=255, null = True)
    last_name = models.CharField (max_length=45, null = True)
    email = models.CharField (max_length = 45, null = True)
    password = models.CharField (max_length=100, null = True)
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Trip(models.Model):
    location = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    trip_creator = models.ForeignKey(User, related_name= "organizer", on_delete=models.CASCADE) 
    participant = models.ManyToManyField(User, related_name="member")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager() 

    def __str__(self):
        return self.location + " " + self.plan