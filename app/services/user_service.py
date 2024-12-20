from typing import Dict, Any, List
import uuid
from ..models.user import User
from ..models.product import Product
from .. import db

def generate_user_id():
    """
    Generate a unique user ID with format 'u<number>'
    """
    # Ambil ID terakhir dari tabel User
    last_user = User.query.order_by(User.id.desc()).first()

    if last_user:
        # Ekstrak nomor dari ID terakhir, misalnya "u5" → 5
        last_number = int(last_user.id[1:])  # Hilangkan huruf "u"
        new_number = last_number + 1         # Tambahkan 1 ke nomor terakhir
    else:
        new_number = 1  # Jika tabel kosong, mulai dari 1

    # Buat ID baru dengan format "u" + nomor
    return f"u{new_number}"

class UserService:
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        return self._format_user(user)
        
    def update_user_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        # Update allowed fields
        for field in ['name', 'phone']:
            if field in data:
                setattr(user, field, data[field])
                
        db.session.commit()
        return self._format_user(user)
        
    def get_user_addresses(self, user_id: str) -> List[Dict[str, Any]]:
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        return [{
            'id': addr.id,
            'label': addr.label,
            'name': addr.name,
            'phone': addr.phone,
            'address': addr.address,
            'city': addr.city,
            'province': addr.province,
            'postal_code': addr.postal_code,
            'is_default': addr.is_default
        } for addr in user.addresses]
        
    def add_user_address(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        from ..models.address import Address
        
        address = Address(
            id=str(uuid.uuid4()),
            user_id=user_id,
            label=data['label'],
            name=data['name'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            province=data['province'],
            postal_code=data['postal_code'],
            is_default=data.get('is_default', False)
        )
        
        db.session.add(address)
        db.session.commit()
        
        return {
            'id': address.id,
            'label': address.label,
            'name': address.name,
            'phone': address.phone,
            'address': address.address,
            'city': address.city,
            'province': address.province,
            'postal_code': address.postal_code,
            'is_default': address.is_default
        }
        
    def get_user_wishlist(self, user_id: str) -> List[Dict[str, Any]]:
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        return [{
            'id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.images[0].image_url if item.product.images else None
        } for item in user.wishlist_items]
        
    def _format_user(self, user: User) -> Dict[str, Any]:
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'phone': user.phone,
            'created_at': user.created_at.isoformat()
        }
