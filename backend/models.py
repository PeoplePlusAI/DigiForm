from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, auto_created=True, default = uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    father_name = models.CharField(max_length=100, null=True)
    mother_name = models.CharField(max_length=100, null=True)
    class Gender(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        OTHER = 'OTHER'
    gender = models.CharField(max_length=20,choices=Gender.choices, null=True)
    class MaritalStatus(models.TextChoices):
        UNMARRIED = 'UNMARRIED'
        MARRIED = 'MARRIED'
    marital_status = models.CharField(max_length=20,choices=MaritalStatus.choices, null=True)
    dob = models.DateField(null=True)
    mobile = models.BigIntegerField(db_index=True, null=True)
    nationality = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100, null=True)
    permanent_address_id = models.ForeignKey('Address', null=True, on_delete=models.CASCADE, related_name='permanent_address_id')
    mailing_address_id = models.ForeignKey('Address', null=True, on_delete=models.CASCADE, related_name='mailing_address_id')
    current_address_id = models.ForeignKey('Address', null=True, on_delete=models.CASCADE, related_name='current_address_id')
    user_photo_link = models.URLField(null=True)
    store_personal_data = models.BooleanField(null=True)
    consent_for_digiform = models.BooleanField(null=True)
    notifications_allowed = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PersonalData(models.Model):
    personal_data_id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    aadhar_card_number = models.BigIntegerField()
    pan_card_number = models.CharField(max_length=10,default=None)
    driving_license_number = models.CharField(max_length=20,default=None)
    voter_id_number = models.CharField(max_length=20,default=None)
    ration_card_number = models.CharField(max_length=20,default=None)
    passport_number = models.CharField(max_length=20,default=None)
    aadhaar_card_link = models.URLField()
    pan_card_link = models.URLField()
    driving_license_link = models.URLField()
    voter_id_link = models.URLField()
    ration_card_link = models.URLField()
    passport_link = models.URLField()


class Address(models.Model):
    address_id = models.UUIDField(primary_key=True)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.IntegerField()
    is_residence = models.BooleanField()
    is_permenant = models.BooleanField()
    is_mailing = models.BooleanField()


class Partner(models.Model):
    partner_id = models.UUIDField(primary_key=True)
    partner_name = models.CharField(max_length=100)
    partner_legal_name = models.CharField(max_length=100)
    partner_forms_list = models.ManyToManyField('Form', related_name='partner_forms_list')
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        PENDING = 'PENDING'
        INACTIVE = 'INACTIVE'
    status = models.CharField(max_length=20,choices=Status.choices)
    poc_1_name = models.CharField(max_length=100)
    poc_1_mobile = models.BigIntegerField()
    poc_1_email = models.EmailField(max_length=100)
    poc_2_name = models.CharField(max_length=100)
    poc_2_mobile = models.BigIntegerField()
    poc_2_email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Form(models.Model):
    form_id = models.UUIDField(primary_key=True)
    form_partner_id = models.ForeignKey('Partner', on_delete=models.CASCADE, related_name='form_partner_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
