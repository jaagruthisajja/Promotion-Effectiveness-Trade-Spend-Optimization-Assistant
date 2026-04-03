INSERT INTO products (product_id, product_name, brand, category, subcategory) VALUES
(1, 'Silk Shine Shampoo 200ml', 'GlowCare', 'Shampoos', 'Daily Care'),
(2, 'FreshMint Toothpaste 150g', 'BrightSmile', 'Oral Care', 'Toothpaste'),
(3, 'PureSoft Soap 4-Pack', 'CleanWave', 'Bathing', 'Soap'),
(4, 'GlowCare Conditioner 180ml', 'GlowCare', 'Conditioners', 'Hair Care'),
(5, 'Sparkle Dishwash Gel 500ml', 'SparkHome', 'Home Care', 'Dishwash');

INSERT INTO regions (region_id, region_name, zone_name, country) VALUES
(1, 'South India', 'South', 'India'),
(2, 'West India', 'West', 'India'),
(3, 'North India', 'North', 'India'),
(4, 'East India', 'East', 'India');

INSERT INTO channels (channel_id, channel_name) VALUES
(1, 'General Trade'),
(2, 'Modern Trade'),
(3, 'E-commerce');

INSERT INTO promotions (
    promotion_id, promotion_name, promotion_type, start_date, end_date, product_id, region_id, channel_id, trade_spend
) VALUES
(101, 'Summer Saver', 'discount', '2025-01-10', '2025-02-05', 1, 1, 2, 20000),
(102, 'Salon Bundle Boost', 'bundle offer', '2025-02-01', '2025-03-15', 4, 2, 2, 26000),
(103, 'Fresh Start Cashback', 'cashback', '2025-01-18', '2025-02-28', 2, 3, 3, 18000),
(104, 'Festival Shelf Push', 'display support', '2025-03-01', '2025-03-31', 3, 1, 1, 22000),
(105, 'Mega Cart Weekend', 'discount', '2025-03-05', '2025-03-25', 5, 2, 3, 30000),
(106, 'Monsoon Shine', 'seasonal scheme', '2025-04-05', '2025-04-30', 1, 2, 1, 14000),
(107, 'Value Smile Pack', 'bundle offer', '2025-01-05', '2025-01-31', 2, 1, 2, 12000),
(108, 'Retail Spotlight', 'display support', '2025-02-10', '2025-03-10', 5, 4, 2, 15000);

INSERT INTO promotion_performance (
    promotion_id, baseline_sales, promoted_sales, incremental_sales, roi, sales_lift_percent
) VALUES
(101, 50000, 86000, 36000, 0.80, 72.00),
(102, 62000, 91000, 29000, 0.12, 46.77),
(103, 47000, 69000, 22000, 0.22, 46.81),
(104, 54000, 66000, 12000, -0.45, 22.22),
(105, 58000, 70000, 12000, -0.60, 20.69),
(106, 52000, 76000, 24000, 0.71, 46.15),
(107, 39000, 58000, 19000, 0.58, 48.72),
(108, 45000, 52000, 7000, -0.53, 15.56);

INSERT INTO sales (sales_id, product_id, region_id, channel_id, date, units_sold, revenue) VALUES
(1001, 1, 1, 2, '2025-01-15', 1800, 43000),
(1002, 1, 1, 2, '2025-02-01', 2100, 43000),
(1003, 4, 2, 2, '2025-02-20', 1600, 45500),
(1004, 2, 3, 3, '2025-02-10', 2400, 35000),
(1005, 3, 1, 1, '2025-03-18', 1300, 33000),
(1006, 5, 2, 3, '2025-03-14', 1750, 38000),
(1007, 1, 2, 1, '2025-04-18', 1500, 38000),
(1008, 2, 1, 2, '2025-01-21', 2200, 31000),
(1009, 5, 4, 2, '2025-02-24', 900, 24000);
