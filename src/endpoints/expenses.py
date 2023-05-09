from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.expense import Expense, expense_schema, expenses_schema
from datetime import datetime


expenses = Blueprint("expenses",__name__,url_prefix="/api/v1")

@expenses.get("/expenses")
def read_all():
    expenses = Expense.query.order_by(Expense.address).all()

    return {"data": expenses_schema.dump(expenses)}, HTTPStatus.OK

@expenses.get("/expenses/<int:id>")
def read_one(id):
    expense = expense.query.filter_by(id=id).first()
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": expense_schema.dump(expense)}, HTTPStatus.OK
    


@expenses.post("/users/<int:user_id>/expenses")
def create(user_id):
    post_data = None
    
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
               user_id   = user_id)
    try:
        db.session.add(expense)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST
    return {"data": expense_schema.dump(expense)}, HTTPStatus.CREATED



@expenses.put('/users/<int:user_id>/expenses/<int:expenses_id>')
@expenses.patch('/users/<int:user_id>/expenses/<int:expenses_id>')
def update(expenses_id,user_id):
    put_data = None
    
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    expense = Expense.query.filter_by(expenses_id=expenses_id).first()
    if (user_id==expense.user_id):
        user_id =expense.user_id
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    expense.value     = request.get_json().get("value",expense.value)
    expense.date      = request.get_json().get("date",expense.date),
    
    expense.user_id     = user_id
    
    try:
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "invalid resource values",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": expense_schema.dump(expense)}, HTTPStatus.OK


@expenses.delete('expenses/<int:expenses_id>')
def delete(expenses_id):
    
    expense = Expense.query.filter_by(expenses_id=expenses_id).first()
    
    if(not expense):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(expense)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT


