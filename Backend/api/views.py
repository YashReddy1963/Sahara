import json
import uuid
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Donation, FundPost, CustomUser, NGORegistration
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password

# User registration view
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
                    "email": ngo_user.email,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "redirect_url": "/dashboard/stats"
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

# Creating posts(FundPosts) from requested fund view(FundRequest table)
User = get_user_model()
@method_decorator(csrf_exempt, name="dispatch")
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

            # Validate NGO ID
            if ngo_id:
                try:
                    ngo = User.objects.get(id=ngo_id)
                except User.DoesNotExist:
                    return JsonResponse({"error": "NGO not found or invalid"}, status=404)

            # Create and save the fund post
            fund_post = FundPost.objects.create(
                user=request.user,
                ngo_name=ngo_name,
                title=title,
                description=description,
                target_amount=target_amount,
                image=image if image else None, 
            )

            saved_image_url = request.build_absolute_uri(fund_post.image.url) if fund_post.image else image_url

            return JsonResponse(
                {
                    "message": "Fund post created successfully!",
                    "fund_post_id": fund_post.id,
                    "image_url": saved_image_url, 
                },
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Fetching posts from fundpost(FundPost table)
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