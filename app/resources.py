import json, werkzeug, os
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename

from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
    create_access_token, 
    create_refresh_token
    )
from flask import jsonify, request

from .models import User
from .face_model.helper import create_embeddings, recognize_image
from app import app


class BalanceResource(Resource):

    @jwt_required()
    def get(self):
        print('-------------------------')
        current_user = get_jwt_identity()
        print(f'---------------- User: {current_user}------------')

        user = User.find_by_username(current_user)
        print(f'---------------- Balance: {float("{0:.2f}".format(user.account_balance))}------------')

        return {'balance': float("{0:.2f}".format(user.account_balance))}, 200


class LoginResource(Resource):
    """
    User Login Resource to login and create new tokens
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='username cannot be blank', required=True)
        parser.add_argument('password', help='password cannot be blank', required=True)
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        # Check if user exists
        user = User.find_by_username(username)
        if user is None:
            return {'message': f'User {username} does not exist'}, 404
        
        # Check if user password is correct
        if user.verify_password(password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Incorrect password!'}, 401
  



class UserRegistration(Resource):
    """
    User Registration Resource to create user and initial tokens
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='username cannot be blank', required=True)
        parser.add_argument('password', help='password cannot be blank', required=True)
        parser.add_argument(
            'images',
            type=werkzeug.datastructures.FileStorage, 
            location='files', 
            action='append',
            required=True
        )
        data = parser.parse_args()
        username = data['username']
        password = data['password']
        images = data['images']

        # Check if user already exists or not
        if User.find_by_username(username):
            return {'message': f'User {username} already exists!'}, 400

        # create new user
        new_user = User(username=username, password=password, account_balance=100)

        try:
            # Save User and Generate Access and Refresh token
            new_user.save()
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            # Train face model using uploaded images
            for file_upload in images:
                filename = secure_filename(file_upload.filename)
                user_dataset_location = os.path.join(app.config['UPLOAD_FOLDER'], username)
                try:
                    os.makedirs(user_dataset_location)
                except OSError as e:
                    pass
                file_upload.save(os.path.join(user_dataset_location, filename))
            print('[INFO] Completed saving images')
            create_embeddings(username, app.config['UPLOAD_FOLDER']) 
            
            return {
                'message': f'User {username} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class FaceVerificationResource(Resource):
    """
    Verify User face for successful payment
    """

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'image',
            type=werkzeug.datastructures.FileStorage, 
            location='files',
            required=True
        )
        data = parser.parse_args()

        image = data['image']

        


       
        


      


#  saved_encodings.pickle
