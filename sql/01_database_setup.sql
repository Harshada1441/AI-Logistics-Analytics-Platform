CREATE DATABASE logistics_db;

USE logistics_db;

CREATE TABLE logistics_data (
    id INT,
    project_code VARCHAR(50),
    country VARCHAR(100),
    shipment_mode VARCHAR(50),
    product_group VARCHAR(50),
    vendor VARCHAR(255),
    line_item_quantity INT,
    line_item_value DECIMAL(15,2),
    pack_price DECIMAL(15,2),
    unit_price DECIMAL(15,2),
    weight_kg DECIMAL(15,2),
    freight_cost_usd DECIMAL(15,2),
    delay_days INT,
    delayed INT,
    risk_score DECIMAL(10,2)
);