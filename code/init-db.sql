-- Enable pgvector extension for AI embeddings

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'draft',
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB,
    uploaded_by VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ocr_text TEXT,
    embedding TEXT
);

-- Create bom_items table (Bill of Materials)
CREATE TABLE IF NOT EXISTS bom_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    child_product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    quantity DECIMAL(10, 3) DEFAULT 1,
    unit VARCHAR(50),
    reference VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table (simplified)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_products_product_code ON products(product_code);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_documents_product_id ON documents(product_id);
CREATE INDEX IF NOT EXISTS idx_bom_items_parent_product_id ON bom_items(parent_product_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert a default admin user (password: admin123)
INSERT INTO users (username, email, hashed_password, full_name, role)
VALUES (
    'admin',
    'admin@pdm.local',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', -- bcrypt hash for 'admin123'
    'Administrator',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Insert sample product for testing
INSERT INTO products (product_code, name, description, category, status)
VALUES (
    'P-1001',
    'Sample Product',
    'A sample product for demonstration',
    'Electronics',
    'released'
) ON CONFLICT (product_code) DO NOTHING;