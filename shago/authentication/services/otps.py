import random 
from datetime import timedelta
from django.utils import timezone
from ..models import OTP # import required django models 

class SMSService:
    """
    A service class created for managing Otp generation, storage and validation
    Utilizes static methods, following the service-layer pattern, ensuring that 
    OTP logic is decoupled from views and models for better maintainability and testing.
    """

    @staticmethod
    def generate_otp():
        # generate a random 6-digit code (from 100000 to 999999) and converts into string
        return str(random.randint(100000,999999))
    
    @staticmethod
    def send_otp(phone_number, code):
        """
        Handles the external communication logic to send the OTP via SMS.

        NOTE : in a production environement , this method must integrate with a
        secure , external SMS gateway API (eg, , Twilio , Aws SNs, ...)
        """
        # Logging the OTP for local development/debugging purposes ONLY. 
        # This print statement must be removed or replaced with secure logging in production.
        print(f" OTP sent to {phone_number} : {code}") # for developpement purpose to see on logs

        # Placeholder for actual SMS gateway API call logic.
        # Handle exceptions, rate limiting, and delivery status checks here.
        return True # assume the sms was sent successfully for now
    
    @staticmethod
    def create_otp(user, purpose='verification'):
        """
        creates a new OTP entry, invalidates all prior unused OTPs for user/purpose
        and dispatches the SMS
        """
        # Security best practice: Invalidate (soft-delete) any existing, unused OTPs 
        # for this specific user and purpose to prevent replay attacks and ensure 
        # only the latest code is valid.
        OTP.objects.filter(user=user , purpose=purpose , is_used=False).update(is_used=True)

        # generates the new code
        code = SMSService.generate_otp()

        # set the expiration time
        expires_at = timezone.now() + timedelta(minutes=10)

        # create and save the new OTP object
        otp = OTP.objects.create(
            user=user,
            code=code,
            purpose=purpose,
            expires_at=expires_at,
        )

        # dispatch the SMS
        SMSService.send_otp(user.phone_number , code)
        return otp
    
    @staticmethod
    def verify_otp(user, code, purpose='verification'):
        """
        Validates the provided code against the database constraints.

        Checks for four critical conditions: user match, code match, not used, and not expired.
        If valid, marks the OTP as used and returns True.
        """
        try:
            # Atomic check: retrieve the unique, current, and unexpired OTP object.
            otp = OTP.objects.get(
                user=user,
                code=code,
                purpose=purpose,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            # If the OTP is found, mark it as used to prevent subsequent usage (single-use constraint).
            otp.is_used=True
            otp.save()
            return True
        except OTP.DoesNotExist :
            return False