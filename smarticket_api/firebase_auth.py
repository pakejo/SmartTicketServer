from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth, initialize_app, firestore

from smarticket_api.models import User

initialize_app()


class FirebaseBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")

        if not authorization_header:
            raise exceptions.AuthenticationFailed('Authorization credentials not provided')

        id_token = authorization_header.split(" ").pop()

        if not id_token:
            raise exceptions.AuthenticationFailed('Authorization credentials not provided')

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid ID Token')

        try:
            user_uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.AuthenticationFailed('No such user exists')

        # Get user data from document
        user, _ = User.objects.get(pk=user_uid)

        return user, None
