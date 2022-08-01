from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth, initialize_app, firestore

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
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.AuthenticationFailed('No such user exists')

        # Get user data from document
        document_db = firestore.client()
        user_document = document_db.collection(u'users').document(uid).get()

        user, _ = User.objects.get_or_create(user_document.to_dict())

        return user, None
