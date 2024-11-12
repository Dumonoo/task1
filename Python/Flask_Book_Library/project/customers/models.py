from project import db, app
import re

# Customer model
class Customer(db.Model):
    NAME_PATTERN = r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*$"

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    city = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, city, age):
        self.name = Customer.validate_name(name)
        self.city = city
        self.age = Customer.validate_age(int(age))

    def __repr__(self):
        return f"Customer(ID: {self.id}, Name: {self.name}, City: {self.city}, Age: {self.age})"


    @staticmethod
    def validate_name(name: str): 
        if not isinstance(name, str):
            raise ValueError("Parameter name - must be a valid string")
        if len(name) <= 2 or len(name) > 64:
            raise ValueError("Parameter name - length must be between 3 to 64 characters")
        if not re.match(Customer.NAME_PATTERN, name):
            raise ValueError("Parameter name - must contain only allowed characters A-Za-z'")
        return name
    
    @staticmethod
    def validate_age(age: int):

        if not isinstance(age, int):
            raise ValueError("Parameter age - must be a valid number")
        if age < 10:
            raise ValueError("Parameter age - our customers must be at least 10 years old ")
        if age > 100:
            raise ValueError("Parameter age - too old")    
        return age
    
with app.app_context():
    db.create_all()
