from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.expense import Expense, expense_schema, expenses_schema
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.endpoints.users import readUser


expenses = Blueprint("expenses",__name__,url_prefix="/api/v1")

@expenses.get("/expenses")
@jwt_required()
def read_all():
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    expenses = Expense.query.filter_by(user_id=userId).order_by(Expense.id).all()


    return {"data": expenses_schema.dump(expenses)}, HTTPStatus.OK

@expenses.get("/expenses/<int:id>")
@jwt_required()
def read_one(id):
    expense = Expense.query.filter_by(id=id).first()
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": expense_schema.dump(expense)}, HTTPStatus.OK
    


@expenses.post("/expenses")
@jwt_required()
def create():
    post_data = None
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    try:
        
        post_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
                "message    ": str(e)}, HTTPStatus.BAD_REQUEST
    datte = request.get_json().get("date",None)
    date_ = datetime.strptime(datte, '%Y-%m-%d %H:%M').date()
    
    expense= Expense(
        value     = request.get_json().get("value",None),
        date      = date_,
        user_id   = userId)
    try:
        db.session.add(expense)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST
    return {"data": expense_schema.dump(expense)}, HTTPStatus.CREATED



@expenses.put('/expenses/<int:expenses_id>')
@expenses.patch('/expenses/<int:expenses_id>')
@jwt_required()
def update(expenses_id):
    put_data = None
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    expense = Expense.query.filter_by(expenses_id=expenses_id).first()
    if (userId==expense.user_id):
        userId =expense.user_id
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    expense.value     = request.get_json().get("value",expense.value)
    expense.date      = request.get_json().get("date",expense.date),
    try:
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "invalid resource values",
            "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": expense_schema.dump(expense)}, HTTPStatus.OK


@expenses.delete('expenses/<int:expenses_id>')
@jwt_required()
def delete(expenses_id):
    
    expense = Expense.query.filter_by(id=expenses_id).first()
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(expense)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
            "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT


