"""ID Generator utility for database tables"""

from typing import Dict

# ID Prefix constants
ID_PREFIX = {
    'USER': 'u',
    'SELLER': 's',
    'ORDER': 'o',
    'ORDER_ITEM': 'oi',
    'ORDER_STATUS_HISTORY': 'sh',
    'PAYMENT_METHOD': 'pm',
    'PRODUCT': 'p',
    'PRODUCT_IMAGE': 'pi',
    'REVIEW': 'r',
    'WISHLIST_ITEM': 'w'
}

# Track last used ID for each prefix
last_ids: Dict[str, int] = {}

def generate_id(prefix: str) -> str:
    """Generate next ID for a given prefix"""
    # Get or initialize counter for this prefix
    current_id = last_ids.get(prefix, 0) + 1
    last_ids[prefix] = current_id
    
    return f"{ID_PREFIX[prefix]}{current_id}"

def get_id_number(id: str) -> int:
    """Extract numeric part from ID"""
    return int(''.join(filter(str.isdigit, id)))

def get_id_prefix(id: str) -> str:
    """Get prefix from ID"""
    return ''.join(filter(str.isalpha, id))

def is_valid_id(id: str, prefix: str) -> bool:
    """Validate ID format"""
    if not id.startswith(ID_PREFIX[prefix]):
        return False
    
    # Check if remaining part is numeric
    num_part = id[len(ID_PREFIX[prefix]):]
    return num_part.isdigit()
