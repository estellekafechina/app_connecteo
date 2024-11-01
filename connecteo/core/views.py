from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileUpdateForm, UserUpdateForm ,CustomUserCreationForm
from .models import Profile ,Post, Comment, Message, Notification, User,Message
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions,filters
from .serializers import UserSerializer, PostSerializer, CommentSerializer, MessageSerializer, NotificationSerializer
from django.contrib.auth.models import User
from .forms import MessageForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm
from django.db.models import Q


from django.utils.crypto import get_random_string

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            confirmation_code = get_random_string(length=32)
            
            profile, created = Profile.objects.get_or_create(user=user, defaults={'confirmation_code': confirmation_code})

            if created:
                send_mail(
                    'Confirmation de votre compte Connecteo',
                    f'Bonjour {user.username},\n\nMerci de vous être inscrit sur Connecteo. Veuillez confirmer votre adresse en cliquant sur le lien suivant :\nhttp://127.0.0.1:8000/confirm/{profile.confirmation_code}/\n\nMerci !',
                    'noreply@connecteo.com',
                    [user.email],
                    fail_silently=False,
                )

            messages.success(request, "Veuillez vérifier votre email pour confirmer votre compte.")
            return redirect('login')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def home(request):
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Aucun profil associé à cet utilisateur.")
        return redirect('profile_update') 

    followed_users = request.user.profile.followers.all()

    if followed_users.exists():
        posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    else:
        posts = Post.objects.order_by('-created_at')[:2]

    return render(request, 'core/home.html', {'posts': posts, 'followed_users': followed_users})

@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', username=request.user.username)
    user_profile = get_object_or_404(User, username=username)
    posts = user_profile.posts.all().order_by('-created_at')
    is_own_profile = (request.user == user_profile)
    is_following = False
    if not is_own_profile:
        is_following = request.user.profile.following.filter(id=user_profile.id).exists()

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
    }
    return render(request, 'core/profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile
    user_profile = request.user.profile

    if user_to_follow in user_profile.following.all():
        user_profile.following.remove(user_to_follow)
        profile.followers.remove(request.user)
        messages.success(request, f"Vous ne suivez plus {user_to_follow.username}.")
    else:
        user_profile.following.add(user_to_follow)
        profile.followers.add(request.user)
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")

    return redirect('profile', username=username)

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Les modifications ont été enregistrées avec succès !')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/profile_update.html', context)



@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'core/post_detail.html', {'post': post, 'comments': comments})



@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = Post.objects.create(user=request.user, content=content, image=image)
        messages.success(request, 'Votre publication a été créée avec succès!')
        return redirect('profile', username=request.user.username)
    return render(request, 'core/create_post.html')



@login_required
def messages_view(request):
    user = request.user
    conversations = User.objects.filter(
        Q(received_messages__sender=user) | Q(sent_messages__receiver=user)
    ).distinct()

    selected_username = request.GET.get('user')
    messages = None
    selected_user = None

    if selected_username:
        selected_user = get_object_or_404(User, username=selected_username)
        messages = Message.objects.filter(
            Q(sender=user, receiver=selected_user) | Q(sender=selected_user, receiver=user)
        ).order_by('timestamp')

    context = {
        'conversations': conversations,
        'messages': messages,
        'selected_user': selected_user,
        'user': user,  
    }
    
    return render(request, 'core/messages.html', context)


@login_required
def notification_view(request):
    return render (request,'core/notifications.html')


@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = user_to_follow.profile

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        messages.success(request, f"Vous ne suivez plus {user_to_follow.username}.")
    else:
        profile.followers.add(request.user)
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")

    return redirect('profile', username=username)

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all()  
    context = {
        'user': user,
        'followers': followers,
    }
    return render(request, 'core/followers_list.html', context)

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = user.profile.following.all()
    context = {
        'user': user,
        'following': following,
    }
    return render(request, 'core/following_list.html', context)


@login_required
def send_message(request, username):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            message.success(request, 'Votre message a été envoyé avec succès.')
            return redirect('messages')
        else:
            message.error(request, 'Il y a eu une erreur dans l"envoi de votre message. Veuillez vérifier les champs.')
    else:
        form = MessageForm()
    
    return render(request, 'messages.html', {'form': form})




@login_required
def search_view(request):
    query = request.GET.get('q')
    users = None
    posts = None
    if query:
        users = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(content__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'core/search.html', context)


@login_required
def search_users_view(request):
    query = request.GET.get('q')
    users = None

    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)

    context = {
        'users': users,
        'query': query
    }
    return render(request, 'core/search.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        messages.error(request, "Vous n'avez pas l'autorisation de supprimer ce post.")
        return redirect('profile', username=request.user.username)
    
    post.delete()
    messages.success(request, "Le post a été supprimé avec succès.")
    return redirect('profile', username=request.user.username)

def confirm_email(request, code):
    try:
        profile = get_object_or_404(Profile, confirmation_code=code)
        profile.email_confirmed = True
        profile.save()
        messages.success(request, "Votre email a été confirmé avec succès !")
        return redirect('login')
    except Profile.DoesNotExist:
        messages.error(request, "Le code de confirmation est invalide.")
        return redirect('home')

#___________________________________________________VIEW SETS____________________________________________________________________


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

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'core/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        
        return self.request.user.profile