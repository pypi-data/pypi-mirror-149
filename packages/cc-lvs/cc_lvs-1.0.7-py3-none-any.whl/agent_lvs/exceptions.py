from api_helper.exceptions import *


class AuthenticationError(BaseAuthenticationError):
    pass


class CaptchaError(BaseCaptchaError):
    pass
