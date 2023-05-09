from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

#from src.models.user import User

class Product(db.Model):
    code        = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    name        = db.Column(db.String(80), nullable=False)
    price       = db.Column(db.Float, unique=True,nullable=False)
    expiration  = db.Column(db.DateTime)
    created_at  = db.Column(db.DateTime, default=datetime.now())
    updated_at  = db.Column(db.DateTime, onupdate=datetime.now())
    
    
    user_id = db.Column(db.String(10), db.ForeignKey('user.id',
                        onupdate="CASCADE",
                        ondelete="RESTRICT"),
        nullable=False)
    
    
    def __init(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Product >>> {self.name}"
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields=()
        model = Product
        include_fk =True
        
user_schema = ProductSchema()
users_schema = ProductSchema(many=True)

        
    
