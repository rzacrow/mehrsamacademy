# backends.py
from django.contrib.auth.backends import ModelBackend
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        logger.info(f"Attempting to authenticate user with phone: {phone}")
        if phone is None or password is None:
            logger.warning("Phone or password is None")
            return None

        try:
            user = User.objects.get(phone=phone)  # Ensure `phone` is valid here
            logger.info(f"User found: {user}")

            if user.check_password(password):
                logger.info("Password is correct, user authenticated")
                return user
            else:
                logger.warning("Password is incorrect")
        except User.DoesNotExist:
            logger.warning("User does not exist")
            return None
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            return None
