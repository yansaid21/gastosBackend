from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required



users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@users.get("/")
def read_all():
    users = User.query.order_by(User.name).all()

    return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<int:id>")
@jwt_required()
def read_one(id):
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK
    


@users.post("/")
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    user= User(id        = request.get_json().get("id",None),
               name      = request.get_json().get("name",None),
               last_name = request.get_json().get("last_name",None),
               phone     = request.get_json().get("phone",None),
               email     = request.get_json().get("email",None),
               password  = request.get_json().get("password",None)
               )
    
    try:
        db.session.add(user)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"data": user_schema.dump(user)}, HTTPStatus.CREATED



@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    put_data = None
    
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    user.name      = request.get_json().get("name",user.name)
    user.last_name = request.get_json().get("last_name",user.last_name)
    user.phone     = request.get_json().get("phone",user.phone)
    user.email     = request.get_json().get("email",user.email)
    user.password  = request.get_json().get("id",user.password)
    
    try:
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "invalid resource values",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": user_schema.dump(user)}, HTTPStatus.OK


@users.delete("/<int:id>")
def delete(id):
    
    user = User.query.filter_by(id=id).first()
    
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(user)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT


