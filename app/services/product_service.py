from typing import Dict, Any, List
import uuid
from ..models.product import Product, ProductImage
from .. import db

class ProductService:
    def get_products(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        query = Product.query
        
        if filters.get('category'):
            query = query.filter(Product.category == filters['category'])
        if filters.get('type'):
            query = query.filter(Product.type == filters['type'])
        if filters.get('min_price'):
            query = query.filter(Product.price >= float(filters['min_price']))
        if filters.get('max_price'):
            query = query.filter(Product.price <= float(filters['max_price']))
        if filters.get('min_rating'):
            query = query.filter(Product.rating >= float(filters['min_rating']))
        if filters.get('search'):
            search = f"%{filters['search']}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(search),
                    Product.description.ilike(search)
                )
            )
            
        products = query.all()
        return [self._format_product(p) for p in products]
        
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        product = Product.query.get(product_id)
        if not product:
            return None
        return self._format_product(product)
        
    def create_product(self, seller_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validasi input
        if data['price'] <= 0 or data['stock'] < 0:
            raise ValueError("Price must be positive and stock cannot be negative")

        # Buat produk baru
        product = Product(
            id=str(uuid.uuid4()),
            seller_id=seller_id,
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            category=data['category'],
            type=data['type']
        )

        # Tambahkan gambar produk jika ada
        for image_url in data.get('images', []):
            image = ProductImage(
                id=str(uuid.uuid4()),
                product_id=product.id,
                image_url=image_url,
                is_primary=len(product.images) == 0
            )
            product.images.append(image)

        db.session.add(product)
        db.session.commit()

        return self._format_product(product)
        
    def _format_product(self, product: Product) -> Dict[str, Any]:
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock': product.stock,
            'category': product.category,
            'type': product.type,
            'rating': float(product.rating),
            'images': [img.image_url for img in product.images],
            'seller_id': product.seller_id,
            'created_at': product.created_at.isoformat()
        }