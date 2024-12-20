from typing import Dict, Any
import uuid
from ..models.user import User
from ..utils.security import generate_password_hash, check_password_hash, generate_token
from .. import db

class AuthService:
    def register_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            raise ValueError('Email already registered')
            
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            name=data['name'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data['role'],
            phone=data.get('phone', '')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
        
    def login_user(self, email: str, password: str, role: str) -> Dict[str, Any]:
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(password, user.password_hash):
            raise ValueError('Invalid email or password')
            
        if user.role != role:
            raise ValueError('Invalid role for this user')
            
        token = generate_token(user.id)
        
        return {
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }