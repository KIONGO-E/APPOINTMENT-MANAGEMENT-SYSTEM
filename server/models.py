from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData,Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import validates,relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ ="users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    appointments = db.relationship('Appointment', backref='user', cascade="all, delete-orphan")
    
    
    serialize_rules = ('-password', '-appointments.user', '-created_at', '-updated_at')
    
    def __repr__(self):
        return f"<User {self.name}>"
    

class Profession(db.Model, SerializerMixin):
    __tablename__ ="professions"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    appointments = db.relationship('Appointment', backref='profession', cascade="all, delete-orphan")
    
    serialize_rules = ('-appointments.profession', '-created_at', '-updated_at')
    
    def __repr__(self):
        return f"<Profession {self.name}>"
    

class Appointment(db.Model, SerializerMixin):
    __tablename__ ="appointments"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))
    profession = db.relationship('Profession', backref=db.backref('profession_appointments', cascade="all, delete-orphan"))
    
    serialize_rules = ('-user.appointments', '-profession.appointments', '-created_at', '-updated_at')
    
    def __repr__(self):
        return f"Appointment {self.name}>"
