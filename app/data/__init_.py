from .users import users
from .products import products
# In-memory data stores
users = {}
products = {}
orders = {}
sellers = {}
addresses = {}
payment_methods = {}

# Make sure to export the users object
__all__ = ['users', 'products', 'orders', 'sellers', 'addresses', 'payment_methods']