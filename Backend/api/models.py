from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    #otp_code = models.CharField(max_length=6, blank=True, null=True)
    #otp_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    #def generate_otp(self):
        """Generate and store a 6-digit OTP"""
    #    import random
    #   self.otp_code = str(random.randint(100000, 999999))
    #  self.save()
    # return self.otp_code

class NGORegistration(models.Model):
    organization_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    type_of_ngo = models.CharField(max_length=255)
    government_issued_id = models.TextField()
    social_link = models.URLField(blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128) 
    organization_authority_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='ngo_profiles/')
    password = models.CharField(max_length=255)
    extra_field_1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field_2 = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'): 
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    created_at = models.DateTimeField(default=now, blank=True)
    def __str__(self):
        return self.organization_name


class Meta:
        db_table = "api_customuser"

class FundRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGORegistration, on_delete=models.CASCADE, null=True, blank=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=255,null=True, blank=True)
    image = models.ImageField(upload_to='fund_requests/', null=True, blank=True) 
    reason = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected")
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Request {self.id} by {self.user.username}"

class FundPost(models.Model):
    id = models.BigAutoField(primary_key=True)  
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    
    ngo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_ngo': True},
        related_name="ngo_fund_posts",  
        null=True,  
        blank=True  
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_fund_posts",  
        null=True, 
        blank=True  
    )

    ngo_name=models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    image = models.ImageField(upload_to="img/fund_images/", blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def _str_(self):
        return f"{self.title} - {self.ngo.username}"


class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Donor (user who donated)
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='donations_made'
    )

    # Seeker (user who requested the fund)
    seeker = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='donations_received',
    null=True,  # Allow NULL in the database
    blank=True  # Allow empty in forms
)


    # Linked Fund Post
    fund_post = models.ForeignKey('FundPost', on_delete=models.CASCADE, related_name='donations')

    # Donation Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)  # Unique transaction identifier
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Donation of {self.amount} by {self.donor.username} to {self.seeker.username}"

