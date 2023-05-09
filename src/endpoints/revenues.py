from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug 
from src.database import db
from src.models.revenue import Revenue, revenue_schema, revenues_schema
from datetime import datetime


revenues = Blueprint("revenues",__name__,url_prefix="/api/v1")

@revenues.get("/revenues")
def read_all():
    revenues = Revenue.query.order_by(Revenue.address).all()

    return {"data": revenues_schema.dump(revenues)}, HTTPStatus.OK

@revenues.get("/revenues/<int:registration>")
def read_one(registration):
    revenue = revenue.query.filter_by(registration=registration).first()
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.OK
    


@revenues.post("/users/<int:user_id>/revenues")
def create(user_id):
    post_data = None
    
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
               user_id     = user_id)
    try:
        db.session.add(revenue)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.CREATED



@revenues.put('/users/<int:user_id>/revenues/<int:registration>')
@revenues.patch('/users/<int:user_id>/revenues/<int:registration>')
def update(registration,user_id):
    put_data = None
    
    try:
        put_data = request.get_json()
    
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "put body JSON data not found",
                "message": str(e)}, HTTPStatus.BAD_REQUEST
        
    revenue = Revenue.query.filter_by(registration=registration).first()
    if (user_id==revenue.user_id):
        user_id =revenue.user_id
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    revenue.value     = request.get_json().get("value",revenue.value)
    revenue.date      = request.get_json().get("date",revenue.date),
    revenue.user_id     = user_id
    
    try:
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "invalid resource values",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": revenue_schema.dump(revenue)}, HTTPStatus.OK


@revenues.delete('revenues/<int:registration>')
def delete(registration):
    
    revenue = Revenue.query.filter_by(registration=registration).first()
    
    if(not revenue):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        
    try:
        db.session.delete(revenue)
        db.session.commit()
    
    except sqlalchemy.exc.IntegrityError as e:
        return{"error": "Resource could not be deleted",
               "message": str(e)},HTTPStatus.BAD_REQUEST
            
    return {"data": ""}, HTTPStatus.NO_CONTENT

