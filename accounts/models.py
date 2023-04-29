from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point


# Create your models here.
# What is BaseUserManager: It will allow you to edit the way how the users and superusers are created
#                          It also gives a method to normalize the email addresses
# What is AbstractBaseUser: We get full control of editing the whole custom user model, including authentication functionality

class UserManager(BaseUserManager): # contains methods
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('You must provide an email address')
        
        if not username:
            raise ValueError('You must provide a username')
        
        user = self.model(
            email = self.normalize_email(email), # normalize email is used to convert upppercase email to lowercase
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password) # to encode and store passwords
        user.save(using=self._db) # save into database
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        # We first create a user and then assign him as a super admin
        # As we have already created method for creating user above so now we just need to pass the values into below function
        user = self.create_user(
            email = self.normalize_email(email), # normalize email is used to convert upppercase email to lowercase
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # Make him a super user
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db) # save into database
        return user


class User(AbstractBaseUser): # contains fields
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Required Fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # By default django has username as a login field but here we need email as a login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    # If user is an an active super user or is an admin then has_perm and has_module_perm will return True
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        user_role = ''
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    

class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) # We are using onetone because one user have only one user profile but for multiple profile we can use foreignkey
    #                                      CASCADE means when User is deleted then userprofile is also deleted              
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))
            return super(UserProfile, self).save(*args, **kwargs)
        return super(UserProfile, self).save(*args, **kwargs)

