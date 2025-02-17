from django.shortcuts import render
from rest_framework import generics 
from rest_framework.response import Response
from .models import Tribe , User
from .serializers import TribeSerializer , UserSerializer
from rest_framework.decorators import api_view
from social_django.utils import load_strategy, load_backend
import requests
from datetime import datetime, timedelta
from .spotify_utils import refresh_spotify_token
import secrets
from django.utils import timezone
from urllib.parse import urlencode
from django.conf import settings

class TribeListCreate(generics.ListCreateAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
class TribeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        try:
            print(f"Attempting to retrieve user with username: {kwargs.get('username')}")
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            print(f"Serialized data: {serializer.data}")
            return Response(serializer.data)
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            raise

@api_view(['GET'])
def spotify_login(request):
    try:
        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name='spotify',
            redirect_uri='http://localhost:8000/api/spotify/callback/'
        )
        
        scope = ' '.join([
            'user-read-email',
            'playlist-read-private',
            'playlist-read-collaborative',
            'user-library-read'
        ])
        
        params = {
            'response_type': 'code',
            'client_id': settings.SOCIAL_AUTH_SPOTIFY_KEY,
            'scope': scope,
            'redirect_uri': 'http://localhost:8000/api/spotify/callback/'
        }
        
        auth_url = f'https://accounts.spotify.com/authorize?{urlencode(params)}'
        return Response({'auth_url': auth_url})
        
    except Exception as e:
        print(f"Login initialization failed: {str(e)}")
        return Response({'error': 'Authentication setup failed'}, status=500)

@api_view(['GET'])
def spotify_callback(request):
    state = request.GET.get('state')
    stored_state = request.session.get('spotify_auth_state')
    
    if not state or state != stored_state:
        return Response({'error': 'State verification failed'}, status=400)
    
    # Clear the state after verification
    del request.session['spotify_auth_state']
    
    code = request.GET.get('code')
    if not code:
        return Response({'error': 'Authorization code missing'}, status=400)
    
    try:
        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name='spotify',
            redirect_uri='http://localhost:8000/api/spotify/callback/'
        )
        
        # Complete the OAuth flow
        user = backend.complete(request=request)
        spotify_data = user.social_auth.get(provider='spotify').extra_data
        
        # Update or create user with Spotify tokens
        user_instance, created = User.objects.get_or_create(username=user.username)
        user_instance.spotify_token = spotify_data.get('access_token')
        user_instance.spotify_refresh_token = spotify_data.get('refresh_token')
        user_instance.spotify_token_expires = timezone.now() + timedelta(
            seconds=spotify_data.get('expires_in', 3600)
        )
        user_instance.save()
        
        return Response({
            'status': 'success',
            'message': 'Spotify authentication successful'
        })
        
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['GET'])
def get_user_playlists(request, username):
    try:
        user = User.objects.get(username=username)
        if not refresh_spotify_token(user):
            return Response({'error': 'Failed to refresh token'}, status=401)
        
        # Reload user to ensure fresh data
        user.refresh_from_db()
        
        headers = {'Authorization': f'Bearer {user.spotify_token}'}
        response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        return Response(response.json())
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except requests.HTTPError as e:
        return Response({'error': f'Spotify API error: {str(e)}'}, status=e.response.status_code)
    