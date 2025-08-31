INSERT INTO users (username, email, password_hash, is_admin) VALUES
('admin','admin@example.com','PLACEHOLDER_HASH',1);

INSERT INTO products (name, description, price, stock, category, image_url) VALUES
('Paracetamol 500mg', 'Pain relief', 25.0, 200, 'Pain Killer', ''),
('Vitamin D3 60 Softgels', 'Bone health', 350.0, 50, 'Supplements', ''),
('Cough Syrup 100ml', 'For cough', 90.0, 80, 'Cold & Cough', '');
