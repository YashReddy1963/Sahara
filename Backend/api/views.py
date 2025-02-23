from django.shortcuts import render

# Create your views here.
import json
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import FundPost, Donation, FundRequest,FundPost, DailyDonation
from django.utils.timezone import now
from .models import Notification
from django.views import View
from django.shortcuts import get_object_or_404
import random
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .models import NGORegistration
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render

# Create your views here.

from .models import CustomUser
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FundPost
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST


from .models import  NGO
from decimal import Decimal

User = get_user_model()  # Get the custom User model

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CreateFundPostView(View):
    def post(self, request):
        try:
            # Check user authentication
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            data = json.loads(request.body)

            ngo_id = data.get("id")  # NGO ID should be passed
            ngo_name = data.get("ngo_name")
            title = data.get("title")
            description = data.get("description")
            target_amount = data.get("target_amount")
            image = request.FILES.get("image")  # Handle file uploads properly

            # Validate required fields
            if not all([title, description, target_amount]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Fetch the NGO user
            if ngo_id:
                try:
                    ngo = User.objects.get(id=ngo_id,)
                except User.DoesNotExist:
                    return JsonResponse({"error": "NGO not found or invalid"}, status=404)


            # Create Fund Post
            fund_post = FundPost.objects.create(
                user=request.user,  # Logged-in user
                ngo_name = ngo_name,
                title=title,
                description=description,
                target_amount=target_amount,
                image=image,  # Handle image properly
            )

            return JsonResponse({
                "message": "Fund post created successfully!",
                "fund_post_id": fund_post.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            # Check if request contains JSON or form-data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST  # Handles form-data
            
            # Extracting fields
            username = data.get('username', '').strip()
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            contact_number = data.get('contact_number', '').strip()
            profile_picture = request.FILES.get('profile_picture')

            # Validation check
            if not username or not email or not password or not contact_number:
                return JsonResponse({'error': 'Username, email, password, and contact number are required'}, status=400)

            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'User with this email already exists'}, status=400)

            # Save profile picture if provided
            picture_path = None
            if profile_picture:
                picture_path = default_storage.save(f'profile_pictures/{uuid.uuid4()}_{profile_picture.name}', ContentFile(profile_picture.read()))

            # Create user
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                contact_number=contact_number,
                profile_picture=picture_path  # Save profile picture path
            )

            return JsonResponse({'message': 'User registered successfully.', 'user_id': user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_POST
def ngo_registration(request):
    if request.method == 'POST':
        try:
            if not request.FILES:
                return JsonResponse({'error': 'Missing required files'}, status=400)

            data = request.POST

            organization_name = data.get('organization_name', '').strip()
            official_email = data.get('official_email', '').strip().lower()
            address = data.get('address', '').strip()
            type_of_ngo = data.get('type_of_ngo', '').strip()
            social_link = data.get('social_link', '').strip()
            contact_number = data.get('contact_number', '').strip()
            organization_authority_name = data.get('organization_authority_name', '').strip()
            password = data.get('password', '').strip() 
            extra_field_1 = data.get('extra_field_1', '').strip()
            extra_field_2 = data.get('extra_field_2', '').strip()

            government_issued_id = data.get('government_issues_id', '')
            profile_picture = request.FILES.get('profile_picture')

            if not all([organization_name, official_email, address, type_of_ngo, contact_number, organization_authority_name]):
                return JsonResponse({'error': 'All required fields must be filled'}, status=400)

            try:
                validate_email(official_email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            
            if NGORegistration.objects.filter(official_email=official_email).exists():
                return JsonResponse({'error': 'NGO with this email already exists'}, status=400)            

            if not profile_picture:
                return JsonResponse({'error': 'Profile picture are required'}, status=400)


            hashed_password = make_password(password) 
            ngo = NGORegistration.objects.create(
                organization_name=organization_name,
                official_email=official_email,
                address=address,
                type_of_ngo=type_of_ngo,
                government_issued_id=government_issued_id,
                social_link=social_link,
                contact_number=contact_number,
                password=hashed_password,
                organization_authority_name=organization_authority_name,
                profile_picture=profile_picture,
                extra_field_1=extra_field_1,
                extra_field_2=extra_field_2
            )

            # Step 1: Generate a 6-digit OTP
            #otp = random.randint(100000, 999999)

            #sharing opt via email
           #send_mail(
           #    'NGO Registration OTP Verification',
           #    f'Hello {organization_name},\n\nYour OTP for NGO registration is: {otp}\n\nPlease enter this OTP to verify your NGO registration.',
           #    'your-email@example.com',
           #    [official_email],
           #    fail_silently=False
           #)
           
            return JsonResponse({'message': 'NGO registered successfully. OTP sent for verification.', 'ngo_id': ngo.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip().lower()
            password = data.get("password", "").strip()

            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            # Check in CustomUser table
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "message": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "redirect_url": "/user-dashboard"  # Redirect user
                }, status=200)

            # Check in NgoRegistration table
            ngo_user = NGORegistration.objects.filter(email=email).first()
            if ngo_user and ngo_user.check_password(password):  # Assuming NgoRegistration has password field
                refresh = RefreshToken.for_user(ngo_user)
                return JsonResponse({
                    "message": "Login successful",
                    "user_id": ngo_user.id,
                    "username": ngo_user.username,
                    "email": ngo_user.email,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "redirect_url": "/ngo-dashboard"  # Redirect NGO user
                }, status=200)

            return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)




@csrf_exempt
@login_required
def donate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from request

            fund_post_id = data.get("fund_post_id")
            amount = data.get("amount")

            # Validate input
            if not fund_post_id or not amount:
                return JsonResponse({"error": "FundPost ID and amount are required."}, status=400)

            fund_post = FundPost.objects.get(id=fund_post_id)

            # Create the donation entry
            donation = Donation.objects.create(
                donor=request.user, 
                fund_post=fund_post, 
                amount=amount,
                payment_status="PENDING"
            )

            return JsonResponse({
                "message": "Donation initiated successfully.",
                "donation_id": donation.id,
                "amount": donation.amount,
                "fund_post": fund_post.title,
                "status": donation.payment_status
            }, status=201)

        except FundPost.DoesNotExist:
            return JsonResponse({"error": "FundPost not found."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)











# class FundPostListView(View):
#     def get(self, request):
#         fund_posts = FundPost.objects.all().values(
#             "id", "title", "description", "target_amount", "collected_amount", "image", "created_at"
#         )
#         return JsonResponse(list(fund_posts), safe=False)


# class FundPostDetailView(View):
#     def get(self, request, fund_post_id):
#         try:
#             fund_post = FundPost.objects.get(id=fund_post_id)
#             return JsonResponse({
#                 "id": fund_post.id,
#                 "title": fund_post.title,
#                 "description": fund_post.description,
#                 "target_amount": str(fund_post.target_amount),
#                 "collected_amount": str(fund_post.collected_amount),
#                 "image": fund_post.image.url if fund_post.image else None,
#                 "created_at": fund_post.created_at.strftime("%Y-%m-%d %H:%M:%S")
#             })
#         except ObjectDoesNotExist:
#             return JsonResponse({"error": "Fund post not found"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class FundPostUpdateView(View):
    def put(self, request, fund_post_id):
        try:
            fund_post = FundPost.objects.get(id=fund_post_id, ngo=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Fund post not found or unauthorized"}, status=403)

        try:
            data = json.loads(request.body)
            fund_post.title = data.get("title", fund_post.title)
            fund_post.description = data.get("description", fund_post.description)
            fund_post.target_amount = data.get("target_amount", fund_post.target_amount)
            fund_post.collected_amount = data.get("collected_amount", fund_post.collected_amount)
            fund_post.save()

            return JsonResponse({"message": "Fund post updated successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class FundPostDeleteView(View):
    def delete(self, request, fund_post_id):
        try:
            fund_post = FundPost.objects.get(id=fund_post_id, ngo=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Fund post not found or unauthorized"}, status=403)

        fund_post.delete()
        return JsonResponse({"message": "Fund post deleted successfully!"}, status=204)



def ngo_stats(request, ngo_id):
    try:
        # Get the NGO
        ngo = User.objects.get(id=ngo_id, is_ngo=True)

        # Get the current month and year
        today = datetime.today()
        start_of_month = datetime(today.year, today.month, 1)
        
        # Count the total fundraisers created by this NGO in the current month
        total_fundraisers = FundPost.objects.filter(ngo=ngo, created_at__gte=start_of_month).count()
        
        # Count the total donations received
        total_donations = Donation.objects.filter(fund_post__ngo=ngo, timestamp__gte=start_of_month).count()

        # Calculate the total amount received
        total_funds_raised = Donation.objects.filter(fund_post__ngo=ngo, timestamp__gte=start_of_month).aggregate(models.Sum('amount'))['amount__sum'] or 0

        # Count the number of applicants who requested funds from this NGO
        total_applicants = FundRequest.objects.filter(ngo=ngo, created_at__gte=start_of_month).count()

        return JsonResponse({
            "total_fundraisers": total_fundraisers,
            "total_donations": total_donations,
            "total_funds_raised": total_funds_raised,
            "total_applicants": total_applicants
        }, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "NGO not found"}, status=404)
    

@method_decorator(login_required, name="dispatch")
class NotificationView(View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        data = [
            {
                "id": notif.id,
                "message": notif.message,
                "created_at": notif.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "is_read": notif.is_read,
            }
            for notif in notifications
        ]
        return JsonResponse({"notifications": data}, safe=False)
    


class FundPostDetailView(View):
    def get(self, request, post_id):
        fund_post = get_object_or_404(FundPost, id=post_id)
        
        data = {
            "id": fund_post.id,
            "title": fund_post.title,
            "description": fund_post.description,
            "amount_required": fund_post.amount_required,
            "amount_collected": fund_post.amount_collected,
            "ngo": fund_post.ngo.name,
            "created_at": fund_post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "image": fund_post.image.url if fund_post.image else None,
            "video": fund_post.video.url if fund_post.video else None,
        }

        return JsonResponse(data, safe=False)
    


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_required, name='dispatch')
class CreateDonationView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            donor_username = data.get("donor_username")
            fund_post_title = data.get("fund_post_title")
            amount = data.get("amount")
            transaction_id = data.get("transaction_id")

            # Validate input
            if not all([donor_username, fund_post_title, amount, transaction_id]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Fetch Donor
            try:
                donor = User.objects.get(username=donor_username)
            except User.DoesNotExist:
                return JsonResponse({"error": "Donor not found."}, status=404)

            # Fetch Fund Post by Title
            try:
                fund_post = FundPost.objects.get(title=fund_post_title)
                seeker = fund_post.user
            except FundPost.DoesNotExist:
                return JsonResponse({"error": "Fund post not found."}, status=404)

            # Prevent self-donation
            if donor == seeker:
                return JsonResponse({"error": "You cannot donate to your own fund post."}, status=400)

            # Create Donation
            donation = Donation.objects.create(
                donor=donor,
                seeker=seeker,
                fund_post=fund_post,
                amount=amount,
                transaction_id=transaction_id
            )

            return JsonResponse({
                "message": "Donation successful!",
                "donation_id": str(donation.id),
                "donor": donor.username,
                "seeker": seeker.username,
                "fund_post": fund_post.title,
                "amount": str(donation.amount),
                "transaction_id": donation.transaction_id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


import uuid

@method_decorator(csrf_exempt, name='dispatch')
class GetDailyDonationsView(View):
    def get(self, request, ngo_id, *args, **kwargs):
        try:
            try:
                ngo = NGO.objects.get(id=ngo_id)
            except NGO.DoesNotExist:
                return JsonResponse({"error": "NGO not found"}, status=404)

            today = now().date()
            donations = DailyDonation.objects.filter(ngo=ngo, date=today).values("date", "total_received")

            return JsonResponse({"donations": list(donations)}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'GET':
        # Fetch user profile
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "contact_number": user.contact_number,
            "profile_picture": user.profile_picture.url if user.profile_picture else None
        }, status=200)

    elif request.method == 'PUT':
        # Update user profile
        try:
            data = json.loads(request.body.decode('utf-8'))
            user.username = data.get('username', user.username)
            user.contact_number = data.get('contact_number', user.contact_number)
            user.save()

            return JsonResponse({"message": "User profile updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def ngo_profile(request, ngo_id):
    ngo = get_object_or_404(NGORegistration, id=ngo_id)

    if request.method == 'GET':
        # Fetch NGO profile
        return JsonResponse({
            "id": ngo.id,
            "organization_name": ngo.organization_name,
            "email": ngo.email,
            "contact_number": ngo.contact_number,
            "address": ngo.address,
            "type_of_ngo": ngo.type_of_ngo,
            "government_issued_id": ngo.government_issued_id,
            "social_link": ngo.social_link,
            "organization_authority_name": ngo.organization_authority_name,
            "profile_picture": ngo.profile_picture.url if ngo.profile_picture else None,
            "extra_field_1": ngo.extra_field_1,
            "extra_field_2": ngo.extra_field_2,
            "created_at": ngo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }, status=200)

    elif request.method == 'PUT':
        # Update NGO profile
        try:
            data = json.loads(request.body.decode('utf-8'))
            ngo.organization_name = data.get('organization_name', ngo.organization_name)
            ngo.email = data.get('email', ngo.email)
            ngo.contact_number = data.get('contact_number', ngo.contact_number)
            ngo.address = data.get('address', ngo.address)
            ngo.type_of_ngo = data.get('type_of_ngo', ngo.type_of_ngo)
            ngo.government_issued_id = data.get('government_issued_id', ngo.government_issued_id)
            ngo.social_link = data.get('social_link', ngo.social_link)
            ngo.organization_authority_name = data.get('organization_authority_name', ngo.organization_authority_name)
            ngo.extra_field_1 = data.get('extra_field_1', ngo.extra_field_1)
            ngo.extra_field_2 = data.get('extra_field_2', ngo.extra_field_2)
            ngo.save()

            return JsonResponse({"message": "NGO profile updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def ngo_profile(request, ngo_id):
    ngo = get_object_or_404(NGORegistration, id=ngo_id)

    if request.method == 'GET':
        # Fetch NGO profile
        return JsonResponse({
            "id": ngo.id,
            "organization_name": ngo.organization_name,
            "official_email": ngo.official_email,
            "contact_number": ngo.contact_number,
            "address": ngo.address,
            "type_of_ngo": ngo.type_of_ngo,
            "government_issued_id": ngo.government_issued_id,
            "social_link": ngo.social_link,
            "organization_authority_name": ngo.organization_authority_name,
            "profile_picture": ngo.profile_picture.url if ngo.profile_picture else None,
            "extra_field_1": ngo.extra_field_1,
            "extra_field_2": ngo.extra_field_2,
            "created_at": ngo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }, status=200)

    elif request.method == 'PUT':
        # Update NGO profile
        try:
            data = json.loads(request.body.decode('utf-8'))
            ngo.organization_name = data.get('organization_name', ngo.organization_name)
            ngo.email = data.get('email', ngo.email)
            ngo.contact_number = data.get('contact_number', ngo.contact_number)
            ngo.address = data.get('address', ngo.address)
            ngo.type_of_ngo = data.get('type_of_ngo', ngo.type_of_ngo)
            ngo.government_issued_id = data.get('government_issued_id', ngo.government_issued_id)
            ngo.social_link = data.get('social_link', ngo.social_link)
            ngo.organization_authority_name = data.get('organization_authority_name', ngo.organization_authority_name)
            ngo.extra_field_1 = data.get('extra_field_1', ngo.extra_field_1)
            ngo.extra_field_2 = data.get('extra_field_2', ngo.extra_field_2)
            ngo.save()

            return JsonResponse({"message": "NGO profile updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
