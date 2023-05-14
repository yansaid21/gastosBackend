from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.revenue import Revenue, revenue_schema, revenues_schema
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.endpoints.users import readUser


revenues = Blueprint("revenues",__name__,url_prefix="/api/v1")

@revenues.get("/revenues")
@jwt_required()
def read_all():
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    revenues = Revenue.query.filter_by(user_id=userId).order_by(Revenue.id).all()


    return {"data": revenues_schema.dump(revenues)}, HTTPStatus.OK

@revenues.get("/revenues/<int:id>")
@jwt_required()
def read_one(id):
    revenue = Revenue.query.filter_by(id=id).first()
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.OK
    


@revenues.post("/revenues")
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
    
    revenue= Revenue(
        value     = request.get_json().get("value",None),
        date      = date_,
        user_id   = userId)
    try:
        db.session.add(revenue)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.CREATED



@revenues.put('/revenues/<int:revenues_id>')
@revenues.patch('/revenues/<int:revenues_id>')
@jwt_required()
def update(revenues_id):
    put_data = None
    user=readUser()[0]['data']
    print(user)
    userId=user['id']
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    revenue = Revenue.query.filter_by(revenues_id=revenues_id).first()
    if (userId==revenue.user_id):
        userId =revenue.user_id
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    revenue.value     = request.get_json().get("value",revenue.value)
    revenue.date      = request.get_json().get("date",revenue.date),
    try:
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "invalid resource values",
            "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.OK


@revenues.delete('revenues/<int:revenues_id>')
@jwt_required()
def delete(revenues_id):
    
    revenue = Revenue.query.filter_by(id=revenues_id).first()
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(revenue)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
            "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT


