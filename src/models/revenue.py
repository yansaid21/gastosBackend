from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

#from src.models.user import User

class Revenue(db.Model):
    id         = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    date       = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    value      = db.Column(db.Integer, nullable=False)
    
    
    user_id = db.Column(db.String(10), db.ForeignKey('user.id',
                        onupdate="CASCADE",
                        ondelete="RESTRICT"),
        nullable=False)
    
    
    def __init(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Revenue >>> {self.id}"
    
class RevenueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields=()
        model = Revenue
        include_fk =True
        
revenue_schema = RevenueSchema()
revenues_schema = RevenueSchema(many=True)

        