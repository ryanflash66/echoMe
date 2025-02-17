from datetime import timedelta
import requests, base64
from django.utils import timezone
from core import settings

def refresh_spotify_token(user):
    if user.spotify_token_expires - timedelta(minutes=5) <= timezone.now():
        try:
            refresh_url = 'https://accounts.spotify.com/api/token'
            client_id = settings.SOCIAL_AUTH_SPOTIFY_KEY
            client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET
            auth_header = base64.b64encode(
                f"{client_id}:{client_secret}".encode()
            ).decode()
            
            headers = {
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': user.spotify_refresh_token
            }
            
            response = requests.post(refresh_url, data=data, headers=headers)
            
            if response.status_code != 200:
                print(f"Spotify refresh error: {response.text}")
                return False
            
            new_token_data = response.json()
            
            user.spotify_token = new_token_data['access_token']
            # Update refresh token if provided
            if 'refresh_token' in new_token_data:
                user.spotify_refresh_token = new_token_data['refresh_token']
            user.spotify_token_expires = timezone.now() + timedelta(
                seconds=new_token_data.get('expires_in', 3600)
            )
            user.save()
            return True
            
        except Exception as e:
            print(f"Token refresh failed: {str(e)}")
            return False
    return True