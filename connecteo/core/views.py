from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileUpdateForm, UserUpdateForm
from .models import Profile ,Post, Comment, Message, Notification
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions,filters
from .serializers import UserSerializer, PostSerializer, CommentSerializer, MessageSerializer, NotificationSerializer
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Crée un profil par défaut pour chaque utilisateur
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'core/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = Post.objects.create(user=request.user, content=content, image=image)
        return redirect('home')
    return render(request, 'core/create_post.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'core/post_detail.html', {'post': post, 'comments': comments})


def home(request):
    return render(request, 'core/home.html')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'core/profile.html', {'profile': profile})


def messages_view(request):
    return render(request, 'core/messages.html')

def notification_view(request):
    return render (request,'core/notifications.html')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'user__username']
    ordering_fields = ['created_at', 'user']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    return redirect('profile', username=username)

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'core/profile.html', {'profile': profile})



def send_message(request):
    if request.method == 'POST':
        # Logique pour envoyer un message
        
        pass
    return redirect('messages')