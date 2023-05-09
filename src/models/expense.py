from datetime import datetime
from src.database import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

#from src.models.user import User

class Expense(db.Model):
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
        return f"Expense >>> {self.id}"
    
class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields=()
        model = Expense
        include_fk =True
        
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

        