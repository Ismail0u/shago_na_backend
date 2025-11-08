# Necessary module imports
from django.db import models
# Import essential base classes to extend Django's default user model
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
# Imports a special field to standardize phone number storage and validation
from phonenumber_field.modelfields import PhoneNumberField 
# Imports the uuid library to generate Universally Unique Identifiers
import uuid

#----------------------------------------
# Class 1 : for User management
#-----------------------------------------

'''
This UserManager class , handles the creation of regular users(merchants or seller)
 and also superUsers like Admin .
 Here we are using the phone number as unique identifier instead of email, because
 we are in African , major reason , why create_user methods created
'''
class UserManager(BaseUserManager):
    # Method to create the regular User(merchants or seller)
    def create_user(self, phone_number, password=None,**extra_fields):
        # here we enforce the user to enter the phone number
        if not phone_number:
            raise ValueError("Le numéro de télephone est obligatoire")
        
        # create a new regular user instance with a phone_number and extra_fields
        user = self.model(phone_number = phone_number , **extra_fields)
        # Hash and set the user's password 
        user.set_password(password)
        # save the user on the database
        user.save(using=self._db)
        return user
    

    # The method that Create the superUser(administrator)
    def create_superuser(self, phone_number, password=None,**extra_fields):
        # we set the required fields for the superUser
        extra_fields.setdefault('is_staff', True)  # he can access the django admin page
        extra_fields.setdefault('is_superuser', True) # he has all administrator permission
        extra_fields.setdefault('role', 'ADMIN')  # he has the role as Administrator
        
        # we use the regular user's method to finish the creation of the superUser
        return self.create_user(phone_number, password, **extra_fields)

 #-------------------------------------
 # Class 2 : The User custom Model (User)
 #-------------------------------------

"""
the User class inherits from AbstractBaseUser (for core authentication functions)
Also inherits from permissionsMixin (for permissions , groups and superUser flag)
"""
class User(AbstractBaseUser, PermissionsMixin):
    # Different role that a User can have
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('MERCHANT', 'Commerçant'),
        ('SELLER', 'Vendeur'),
    ]
    
    # Authentication providers that can be used
    AUTH_PROVIDER_CHOICES = [
        ('phone', 'Téléphone'),
        ('google', 'Google'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    # All Users fields
    # Primary key, uses UUID for unique global identification, auto-generated, not editable
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # phone Number field : main identifier , must be unique ,and use regional validation
    phone_number = PhoneNumberField(unique=True, region='NE')  # Région par défaut Togo
    # email field : optional ( blank=true , null=true ) but must be unique
    email = models.EmailField(blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=150) # first Name field
    last_name = models.CharField(max_length=150)  # last name field
    # Role: Restricted to choices, defaults to 'MERCHANT'
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MERCHANT')
    # Auth Provider: Tracks how the user signed up, defaults to 'phone'
    auth_provider = models.CharField(max_length=20, choices=AUTH_PROVIDER_CHOICES, default='phone')

    # status and permission fields for the user
    is_active = models.BooleanField(default=True)  # User account is enabled
    is_staff = models.BooleanField(default=False)   # if he can access the django admin interface
    is_verified = models.BooleanField(default=False)  # Used for the OTP verification Status
    
    created_at = models.DateTimeField(auto_now_add=True)  # date that the user account is created
    updated_at = models.DateTimeField(auto_now=True)    # last update of the user account , date
    
    objects = UserManager()  # Tell Django to use our custom UserManager for queries
    
    USERNAME_FIELD = 'phone_number' # define the field used as the unique login identifier
    REQUIRED_FIELDS = ['first_name', 'last_name'] # fields required when creating user via a CLI
    

    # Meta Configuration (for Django Admin interface and database)
    class Meta:
        db_table = 'users'  # the table's name in the database
        verbose_name = 'Utilisateur'  # singular display name
        verbose_name_plural = 'Utilisateurs' # plural display name
    
    # for models representation on the amdin interface abd logs
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"