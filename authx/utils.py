
from rest_framework import serializers
from authx.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
                    style={'input_type': 'password'},
                    write_only=True # password not showing for the time being
                )
    
    class Meta:
        model = User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    """
    return {
        'token': token,
        'user': UserSerializer(user).data
    }