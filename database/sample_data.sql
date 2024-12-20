```sql
-- Sample Users
INSERT INTO users (id, name, email, password_hash, role, phone, created_at) VALUES
('u1', 'John Doe', 'john@example.com', 'hashed_password_1', 'consumer', '081234567890', '2024-01-15'),
('u2', 'Jane Smith', 'jane@example.com', 'hashed_password_2', 'consumer', '081234567891', '2024-01-20'),
('u3', 'Green Valley Farm', 'contact@greenvalley.com', 'hashed_password_3', 'seller', '081234567892', '2023-12-01'),
('u4', 'Artisan Bakery', 'hello@artisanbakery.com', 'hashed_password_4', 'seller', '081234567893', '2023-12-15'),
('u5', 'Mountain Apiaries', 'info@mountainapiaries.com', 'hashed_password_5', 'seller', '081234567894', '2023-12-20');

-- Sample Sellers
INSERT INTO sellers (id, user_id, store_name, description, image_url, location, province, rating, category, joined_date) VALUES
('s1', 'u3', 'Green Valley Farm', 'Fresh organic produce from local farmers', 'https://images.unsplash.com/photo-1488459716781-31db52582fe9', 'Bogor', 'Jawa Barat', 4.8, 'Farmers', '2023-12-01'),
('s2', 'u4', 'Artisan Bakery', 'Authentic European-style breads and pastries', 'https://images.unsplash.com/photo-1509440159596-0249088772ff', 'Bandung', 'Jawa Barat', 4.9, 'Bakers', '2023-12-15'),
('s3', 'u5', 'Mountain Apiaries', 'Premium honey and bee products', 'https://images.unsplash.com/photo-1587049352847-81a56d773cae', 'Malang', 'Jawa Timur', 4.7, 'Farmers', '2023-12-20');

-- Sample Products
INSERT INTO products (id, seller_id, name, description, price, stock, category, type, rating, created_at) VALUES
('p1', 's1', 'Organic Vegetable Box', 'Weekly selection of fresh organic vegetables', 150000, 50, 'Fresh Produce', 'premium', 4.8, '2024-03-01'),
('p2', 's1', 'Free Range Eggs', 'Farm fresh free-range eggs', 45000, 100, 'Fresh Produce', 'standard', 4.7, '2024-03-02'),
('p3', 's2', 'Sourdough Bread', 'Traditional sourdough bread', 85000, 30, 'Bakery', 'premium', 4.9, '2024-03-01'),
('p4', 's2', 'Croissant Pack', 'Pack of 4 butter croissants', 65000, 40, 'Bakery', 'standard', 4.8, '2024-03-02'),
('p5', 's3', 'Raw Forest Honey', 'Pure raw honey from mountain forests', 120000, 25, 'Condiments', 'premium', 4.9, '2024-03-01');

-- Sample Product Images
INSERT INTO product_images (id, product_id, image_url, is_primary) VALUES
('pi1', 'p1', 'https://images.unsplash.com/photo-1540420773420-3366772f4999', TRUE),
('pi2', 'p2', 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f', TRUE),
('pi3', 'p3', 'https://images.unsplash.com/photo-1585478259715-876acc5be8eb', TRUE),
('pi4', 'p4', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a', TRUE),
('pi5', 'p5', 'https://images.unsplash.com/photo-1587049352847-81a56d773cae', TRUE);

-- Sample Addresses
INSERT INTO addresses (id, user_id, label, name, phone, address, city, province, postal_code, is_default) VALUES
('a1', 'u1', 'Home', 'John Doe', '081234567890', 'Jl. Sudirman No. 123', 'Jakarta', 'DKI Jakarta', '12345', TRUE),
('a2', 'u1', 'Office', 'John Doe', '081234567890', 'Jl. Gatot Subroto No. 456', 'Jakarta', 'DKI Jakarta', '12346', FALSE),
('a3', 'u2', 'Home', 'Jane Smith', '081234567891', 'Jl. Asia Afrika No. 789', 'Bandung', 'Jawa Barat', '40112', TRUE);

-- Sample Orders
INSERT INTO orders (id, user_id, status, total_amount, shipping_address_id, payment_method, created_at) VALUES
('o1', 'u1', 'delivered', 250000, 'a1', 'credit_card', '2024-03-15'),
('o2', 'u1', 'processing', 175000, 'a1', 'bank_transfer', '2024-03-18'),
('o3', 'u2', 'pending', 320000, 'a3', 'e_wallet', '2024-03-20');

-- Sample Order Items
INSERT INTO order_items (id, order_id, product_id, quantity, price_at_time) VALUES
('oi1', 'o1', 'p1', 1, 150000),
('oi2', 'o1', 'p2', 2, 45000),
('oi3', 'o2', 'p3', 2, 85000),
('oi4', 'o3', 'p4', 3, 65000),
('oi5', 'o3', 'p5', 1, 120000);

-- Sample Order Status History
INSERT INTO order_status_history (id, order_id, status, note, updated_by, created_at) VALUES
('sh1', 'o1', 'pending', 'Order received', 'u3', '2024-03-15 10:00:00'),
('sh2', 'o1', 'processing', 'Order being prepared', 'u3', '2024-03-15 11:00:00'),
('sh3', 'o1', 'shipped', 'Order shipped via JNE', 'u3', '2024-03-16 09:00:00'),
('sh4', 'o1', 'delivered', 'Order delivered successfully', 'u3', '2024-03-17 14:00:00'),
('sh5', 'o2', 'pending', 'Order received', 'u4', '2024-03-18 15:00:00'),
('sh6', 'o2', 'processing', 'Order being prepared', 'u4', '2024-03-18 16:00:00');

-- Sample Wishlist Items
INSERT INTO wishlist_items (id, user_id, product_id, added_at) VALUES
('w1', 'u1', 'p3', '2024-03-10'),
('w2', 'u1', 'p5', '2024-03-11'),
('w3', 'u2', 'p1', '2024-03-12');

-- Sample Reviews
INSERT INTO reviews (id, product_id, user_id, rating, comment, created_at) VALUES
('r1', 'p1', 'u1', 5, 'Very fresh vegetables, great quality!', '2024-03-16'),
('r2', 'p3', 'u2', 5, 'Best sourdough bread in town', '2024-03-17'),
('r3', 'p5', 'u1', 4, 'Excellent honey, but a bit pricey', '2024-03-18');
```