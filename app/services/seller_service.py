from typing import Dict, Any, List
import uuid
from ..models.seller import Seller
from ..models.product import Product
from .. import db

class SellerService:
    def get_sellers(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        query = Seller.query
        
        if filters.get('category'):
            query = query.filter(Seller.category == filters['category'])
        if filters.get('province'):
            query = query.filter(Seller.province == filters['province'])
        if filters.get('min_rating'):
            query = query.filter(Seller.rating >= float(filters['min_rating']))
        if filters.get('search'):
            search = f"%{filters['search']}%"
            query = query.filter(
                db.or_(
                    Seller.store_name.ilike(search),
                    Seller.description.ilike(search)
                )
            )
            
        sellers = query.all()
        return [self._format_seller(s) for s in sellers]
        
    def get_seller_by_id(self, seller_id: str) -> Dict[str, Any]:
        seller = Seller.query.get(seller_id)
        if not seller:
            return None
        return self._format_seller(seller)
        
    def get_seller_products(self, seller_id: str) -> List[Dict[str, Any]]:
        products = Product.query.filter_by(seller_id=seller_id).all()
        return [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'stock': p.stock,
            'category': p.category,
            'type': p.type,
            'rating': float(p.rating),
            'images': [img.image_url for img in p.images]
        } for p in products]
        
    def update_seller_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        seller = Seller.query.filter_by(user_id=user_id).first()
        if not seller:
            raise ValueError('Seller profile not found')
            
        # Update fields
        for field in ['store_name', 'description', 'location', 'province', 'category']:
            if field in data:
                setattr(seller, field, data[field])
                
        # Handle profile image update
        if 'image_url' in data:
            seller.image_url = data['image_url']
            
        db.session.commit()
        return self._format_seller(seller)
        
    def _format_seller(self, seller: Seller) -> Dict[str, Any]:
        return {
            'id': seller.id,
            'user_id': seller.user_id,
            'store_name': seller.store_name,
            'description': seller.description,
            'image_url': seller.image_url,
            'location': seller.location,
            'province': seller.province,
            'rating': float(seller.rating),
            'category': seller.category,
            'joined_date': seller.joined_date.isoformat(),
            'total_products': len(seller.products)
        }
