"""
Custom authentication backend for matric number-based login
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from hostels.models import StudentProfile

User = get_user_model()


class MatricNumberBackend(ModelBackend):
    """
    Custom authentication backend that allows login using matric number
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user using matric number or username
        """
        try:
            # Try to authenticate with matric number first
            student = StudentProfile.objects.get(matric_no=username)
            user = student.user
        except StudentProfile.DoesNotExist:
            # Fall back to regular username authentication
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # Verify password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
