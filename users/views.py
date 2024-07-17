from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, FriendRequestSerializer
from django.db.models import Q
from django.utils import timezone
from .models import FriendRequest
from rest_framework.response import Response

# Create your views here.
User = get_user_model() #get the custom user model

#View for handling user signup
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#View for handling user login
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#View for handling user search by email or username
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return get_user_model().objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        )[:10]
    
#View to handle sending and responding to friend requests
class FriendRequestView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)

        # Check rate limit
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        friend_requests_count = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
        if friend_requests_count >= 3:
            return Response({'error': 'You cannot send more than 3 friend requests in a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return Response({'status': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

#View for handling accept/reject request
class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        status = request.data.get('status')
        if status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = status
        instance.save()
        return Response({'status': f'Friend request {status}.'})
    
#View to list friends of the current user
class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            (Q(from_user=user) | Q(to_user=user)) & Q(status='accepted')
        ).values_list('from_user', 'to_user')
        friend_ids = set([item for sublist in friends for item in sublist if item != user.id])
        return User.objects.filter(id__in=friend_ids)

# View to list pending friend requests received by the current user
class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')
