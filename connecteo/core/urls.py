from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet ,MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html')), 
    path('messages/', views.messages_view, name='messages'),
    path('notifications/', views.notification_view, name='notifications'),
    path('send_message/', views.send_message, name='send_message'),
    

]


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns += router.urls
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<str:username>/', views.follow, name='follow'),

]
