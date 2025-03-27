from django.urls import path
from .views import register_user
from .views import donate
from .views import login_view
from .views import FundPostDetailView
from .views import ngo_registration
from .views import CreateFundPostView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('api/ngo/register/', ngo_registration, name='ngo_registration'),
    path('api/create-fund-post/', CreateFundPostView.as_view(), name='create-fund-post'),
    path('api/fund- posts/', FundPostDetailView.as_view(), name='fund-posts'),
    path('api/fund-posts/<int:post_id>/', FundPostDetailView.as_view(), name='single-fund-post'),
    path('donate/', donate, name='donate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)