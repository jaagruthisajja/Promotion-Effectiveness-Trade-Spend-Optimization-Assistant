DROP TABLE IF EXISTS promotion_performance;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS promotions;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL
);

CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL,
    zone_name TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE channels (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT NOT NULL
);

CREATE TABLE promotions (
    promotion_id INTEGER PRIMARY KEY,
    promotion_name TEXT NOT NULL,
    promotion_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    trade_spend REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE sales (
    sales_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    units_sold INTEGER NOT NULL,
    revenue REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

CREATE TABLE promotion_performance (
    promotion_id INTEGER PRIMARY KEY,
    baseline_sales REAL NOT NULL,
    promoted_sales REAL NOT NULL,
    incremental_sales REAL NOT NULL,
    roi REAL NOT NULL,
    sales_lift_percent REAL NOT NULL,
    FOREIGN KEY (promotion_id) REFERENCES promotions(promotion_id)
);
