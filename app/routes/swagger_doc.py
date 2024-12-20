
"""
Swagger documentation for all API routes
"""

# Orders
order_routes = {
    "/api/orders": {
        "get": {
            "tags": ["Orders"],
            "summary": "Get all orders",
            "security": [{"Bearer": []}],
            "parameters": [
                {
                    "name": "status",
                    "in": "query",
                    "type": "string",
                    "enum": ["pending", "processing", "shipped", "delivered", "cancelled"]
                },
                {
                    "name": "from_date",
                    "in": "query",
                    "type": "string",
                    "format": "date"
                },
                {
                    "name": "to_date",
                    "in": "query", 
                    "type": "string",
                    "format": "date"
                }
            ],
            "responses": {
                "200": {
                    "description": "List of orders",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Order"}
                    }
                }
            }
        },
        "post": {
            "tags": ["Orders"],
            "summary": "Create new order",
            "security": [{"Bearer": []}],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "required": ["items", "shipping_address_id", "payment_method"],
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["product_id", "quantity"],
                                "properties": {
                                    "product_id": {"type": "string"},
                                    "quantity": {"type": "integer", "minimum": 1}
                                }
                            }
                        },
                        "shipping_address_id": {"type": "string"},
                        "payment_method": {"type": "string"}
                    }
                }
            }],
            "responses": {
                "201": {
                    "description": "Order created successfully",
                    "schema": {"$ref": "#/definitions/Order"}
                }
            }
        }
    },
    "/api/orders/{id}": {
        "get": {
            "tags": ["Orders"],
            "summary": "Get order details",
            "security": [{"Bearer": []}],
            "parameters": [{
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string"
            }],
            "responses": {
                "200": {
                    "description": "Order details",
                    "schema": {"$ref": "#/definitions/Order"}
                }
            }
        },
        "put": {
            "tags": ["Orders"],
            "summary": "Update order status",
            "security": [{"Bearer": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "type": "string"
                },
                {
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["status"],
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "processing", "shipped", "delivered", "cancelled"]
                            },
                            "note": {"type": "string"}
                        }
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Order updated successfully",
                    "schema": {"$ref": "#/definitions/Order"}
                }
            }
        }
    },

    # Products
    "/api/products": {
        "get": {
            "tags": ["Products"],
            "summary": "Get all products",
            "parameters": [
                {
                    "name": "category",
                    "in": "query",
                    "type": "string"
                },
                {
                    "name": "type",
                    "in": "query",
                    "type": "string",
                    "enum": ["standard", "premium"]
                },
                {
                    "name": "min_price",
                    "in": "query",
                    "type": "number"
                },
                {
                    "name": "max_price",
                    "in": "query",
                    "type": "number"
                },
                {
                    "name": "min_rating",
                    "in": "query",
                    "type": "number"
                },
                {
                    "name": "search",
                    "in": "query",
                    "type": "string"
                }
            ],
            "responses": {
                "200": {
                    "description": "List of products",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Product"}
                    }
                }
            }
        },
        "post": {
            "tags": ["Products"],
            "summary": "Create new product (Seller only)",
            "security": [{"Bearer": []}],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {"$ref": "#/definitions/Product"}
            }],
            "responses": {
                "201": {
                    "description": "Product created successfully",
                    "schema": {"$ref": "#/definitions/Product"}
                }
            }
        }
    },

    # Sellers
    "/api/sellers": {
        "get": {
            "tags": ["Sellers"],
            "summary": "Get all sellers",
            "parameters": [
                {
                    "name": "category",
                    "in": "query",
                    "type": "string"
                },
                {
                    "name": "province",
                    "in": "query",
                    "type": "string"
                },
                {
                    "name": "min_rating",
                    "in": "query",
                    "type": "number"
                }
            ],
            "responses": {
                "200": {
                    "description": "List of sellers",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Seller"}
                    }
                }
            }
        }
    },

    # Reviews
    "/api/products/{id}/reviews": {
        "get": {
            "tags": ["Reviews"],
            "summary": "Get product reviews",
            "parameters": [{
                "name": "id",
                "in": "path",
                "required": True,
                "type": "string"
            }],
            "responses": {
                "200": {
                    "description": "List of reviews",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Review"}
                    }
                }
            }
        },
        "post": {
            "tags": ["Reviews"],
            "summary": "Add product review",
            "security": [{"Bearer": []}],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "type": "string"
                },
                {
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["rating"],
                        "properties": {
                            "rating": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5
                            },
                            "comment": {"type": "string"}
                        }
                    }
                }
            ],
            "responses": {
                "201": {
                    "description": "Review added successfully",
                    "schema": {"$ref": "#/definitions/Review"}
                }
            }
        }
    },

    # Wishlist
    "/api/users/wishlist": {
        "get": {
            "tags": ["Wishlist"],
            "summary": "Get user's wishlist",
            "security": [{"Bearer": []}],
            "responses": {
                "200": {
                    "description": "User's wishlist items",
                    "schema": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/WishlistItem"}
                    }
                }
            }
        },
        "post": {
            "tags": ["Wishlist"],
            "summary": "Add item to wishlist",
            "security": [{"Bearer": []}],
            "parameters": [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "required": ["product_id"],
                    "properties": {
                        "product_id": {"type": "string"}
                    }
                }
            }],
            "responses": {
                "201": {
                    "description": "Item added to wishlist",
                    "schema": {"$ref": "#/definitions/WishlistItem"}
                }
            }
        }
    }
}
