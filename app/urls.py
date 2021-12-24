from . import api
from .resources import *

api.add_resource(UserRegistration, '/api/v1/register')
api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(FaceVerificationResource, '/api/v1/face_verification')
api.add_resource(BalanceResource, '/api/v1/user_balance')