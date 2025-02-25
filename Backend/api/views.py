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
from .models import FundPost, Donation, FundRequest, NGORegistration
from django.utils.timezone import now
from .models import Notification
from django.views import View
from django.shortcuts import get_object_or_404
import random
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# User registration view
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = request.POST

            username = data.get('username', '').strip()
            email = data.get('email', '').strip().lower()
            password = data.get('password', '').strip()
            contact_number = data.get('contact_number', '').strip()
            profile_picture = request.FILES.get('profile_picture')  

            if not username or not email or not password or not contact_number:
                return JsonResponse({'error': 'Username, email, password, and contact number are required'}, status=400)

            # Check if email already exists
            user = CustomUser.objects.filter(email=email).first()
            #if user:
            #    if not user.otp_verified:
            #        otp_code = str(random.randint(100000, 999999))
            #        user.otp_code = otp_code
            #        user.save()

            #        send_mail(
            #            subject="Your OTP Code",
            #            message=f"Your OTP code is {otp_code}",
            #            from_email="your_email@example.com",
            #            recipient_list=[email],
            #            fail_silently=False,
            #        )

            #        return JsonResponse({'message': 'OTP resent. Please verify.'}, status=200)
            #    return JsonResponse({'error': 'User with this email already exists'}, status=400)
            # Generate OTP for new user
            #otp_code = str(random.randint(100000, 999999))

            if profile_picture:
                picture_path = default_storage.save(f'profile_pictures/{profile_picture.name}', ContentFile(profile_picture.read()))


            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                contact_number=contact_number,
                profile_picture=picture_path,  # Fixed variable name
                #otp_code=otp_code,
                #otp_verified=False
            )

            #send_mail(
            #    subject="Your OTP Code",
            #    message=f"Your OTP code is {otp_code}",
            #    from_email="your_email@example.com",
            #    recipient_list=[email],
            #    fail_silently=False,
            #)

            return JsonResponse({'message': 'User registered successfully.', 'user_id': user.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

#NGO registration view
@csrf_exempt
def ngo_registration(request):
    if request.method == 'POST':
        try:
            if not request.FILES:
                return JsonResponse({'error': 'Missing required files'}, status=400)

            data = request.POST

            organization_name = data.get('organization_name', '').strip()
            email = data.get('email', '').strip().lower()
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

            # Validate required fields
            if not all([organization_name, email, address, type_of_ngo, contact_number, organization_authority_name]):
                return JsonResponse({'error': 'All required fields must be filled'}, status=400)

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email format'}, status=400)

            # Check if NGO with the same email already exists
            if NGORegistration.objects.filter(email=email).exists():
                return JsonResponse({'error': 'NGO with this email already exists'}, status=400)            

            if not profile_picture:
                return JsonResponse({'error': 'Profile picture are required'}, status=400)


            hashed_password = make_password(password) 
            
            # Save the NGO registration
            ngo = NGORegistration.objects.create(
                organization_name=organization_name,
                email=email,
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
           
            return JsonResponse({'message': 'NGO registered successfully', 'ngo_id': ngo.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Login view
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
             # Authenticate using Django's built-in method
            
            ngo_user = NGORegistration.objects.filter(email=email).first()
            if ngo_user and check_password(password, ngo_user.password):  # Use check_password()
                refresh = RefreshToken.for_user(ngo_user)
                return JsonResponse({
                    "message": "Login successful",
                    "user_id": ngo_user.id,
                    # "username": ngo_user.username,  # Ensure this field exists in your model
                    "email": ngo_user.email,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "redirect_url": "/dashboard/stats"  # Redirect NGO user
                }, status=200)

            
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "message": "Login successful",
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "redirect_url": "/discover/home" 
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=401)          


        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


# View for creating fund request
class FundRequestView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        print("Received Data:", request.data) 
        print("Received Files:", request.FILES) 
        try:
            if not request.user or not request.user.is_authenticated:
                raise NotAuthenticated("User is not authenticated or token is invalid!")

            data = request.data
            reason = data.get('reason')
            amount = data.get('amount')
            ngo_name = data.get('ngo_name')
            title = data.get('title')
            image = request.FILES.get('image') 

            required_fields = [reason, amount, ngo_name, title, image]

            if not all(required_fields):
                return Response({'error': 'All fields (reason, amount, ngo_name, title, image) are required!', }, status=400)

            
            try:
                amount = float(amount)
                if amount <= 0:
                    return Response({'error': 'Amount must be greater than 0!'}, status=400)
            except ValueError:
                return Response({'error': 'Amount must be a valid number!'}, status=400)

            ngo_qs = NGORegistration.objects.filter(organization_name=ngo_name)
            if not ngo_qs.exists():
                return Response({'error': f'NGO with name "{ngo_name}" not found!'}, status=404)
            
            ngo = ngo_qs.first()  

            fund_request = FundRequest.objects.create(
                user=request.user,
                ngo=ngo,
                amount_requested=amount,
                reason=reason,
                title=title,
                image=image
            )

            image_url = request.build_absolute_uri(fund_request.image.url) if fund_request.image else None

            return Response({
                'message': 'Fund request created successfully!',
                'user': request.user.username,
                'ngo': ngo_name,
                'amount_requested': str(fund_request.amount_requested),
                'reason': fund_request.reason,
                'status': fund_request.status,
                'image_url': image_url,
                'created_at': fund_request.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=201)

        except InvalidToken as e:
            return Response({'error': 'Invalid token!', 'details': str(e)}, status=401)

        except TokenError as e:
            return Response({'error': 'Token error!', 'details': str(e)}, status=401)

        except AuthenticationFailed as e:
            return Response({'error': 'Authentication failed!', 'details': str(e)}, status=401)

        except NotAuthenticated as e:
            return Response({'error': 'User not authenticated!', 'details': str(e)}, status=401)

        except Exception as e:
            return Response({'error': 'An unexpected error occurred!', 'details': str(e)}, status=500)

# View for creating posts for funds
User = get_user_model()
@method_decorator(csrf_exempt, name='dispatch')
class CreateFundPostView(View):
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            data = request.POST
            ngo_id = data.get("id")
            ngo_name = data.get("ngo_name")
            title = data.get("title")
            description = data.get("description")
            target_amount = data.get("target_amount")
            image = request.FILES.get("image") 
            image_url = data.get("image_url") 

            if not all([title, description, target_amount]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            if ngo_id:
                try:
                    ngo = User.objects.get(id=ngo_id)
                except User.DoesNotExist:
                    return JsonResponse({"error": "NGO not found or invalid"}, status=404)

            # Create Fund Post
            fund_post = FundPost.objects.create(
                user=request.user,
                ngo_name=ngo_name,
                title=title,
                description=description,
                target_amount=target_amount,
                image=image if image else image_url,
            )

            return JsonResponse({
                "message": "Fund post created successfully!",
                "fund_post_id": fund_post.id,
                "image_url": fund_post.image if fund_post.image else None 
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# View for getting the details about the fund post
class FundPostDetailView(View):
    def get(self, request, post_id=None):
        if post_id:
            fund_post = get_object_or_404(FundPost, id=post_id)
            data = {
                "id": fund_post.id,
                "title": fund_post.title,
                "description": fund_post.description,
                "target_amount": fund_post.target_amount,
                "collected_amount": fund_post.collected_amount,
                "ngo_name": fund_post.ngo_name,
                "created_at": fund_post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "image": fund_post.image.url if fund_post.image and fund_post.image.name else None,  
            }
            return JsonResponse(data, safe=False)
        
        # Fetch all fund posts
        fund_posts = FundPost.objects.all()
        data = [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "target_amount": post.target_amount,
                "collected_amount": post.collected_amount,
                "ngo_name": post.ngo_name,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "image": post.image.url if post.image and post.image.name else None,  
            }
            for post in fund_posts
        ]
        return JsonResponse(data, safe=False)
    
# View of donation for the people 
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


# Views for getting the stats
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
    

# Notification view
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
    
