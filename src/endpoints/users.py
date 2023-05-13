from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import url_for
from src.models.expense import Expense, expense_schema, expenses_schema
import requests
from datetime import datetime 


users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@users.get("/all")
def read_all():
    users = User.query.order_by(User.name).all()

    return {"data": users_schema.dump(users)}, HTTPStatus.OK
@users.get("/")
@jwt_required()
def readUser():
    user = User.query.filter_by(id=get_jwt_identity()['id']).one_or_none()
    #user = User.query.filter_by(id=get_jwt_identity()).one_or_none()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK
    


@users.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

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
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.CREATED



@users.put('/')
@users.patch('/')
@jwt_required()
def update():
    put_data = None
    
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    user = User.query.filter_by(id=get_jwt_identity()).first()
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


@users.delete("/")
@jwt_required()
def delete():
    
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(user)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT



@users.get("/expenses")
@jwt_required()
def rangoFechas():
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    inicio = request.args.get('inicio')
    final = request.args.get('final')
    user = User.query.filter_by(id=get_jwt_identity()).one_or_none()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    date_inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M').date()
    date_final  = datetime.strptime(final,  '%Y-%m-%d %H:%M').date()
    
    expense = Expense.query.order_by(Expense.id).filter(Expense.created_at >= date_inicio, Expense.created_at <= date_final,Expense.user_id==userId).all()

    return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK
    
    
    
    

    



