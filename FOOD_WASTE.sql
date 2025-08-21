create database food_wastage;
use food_wastage;

create table providers(
Provider_ID int primary key,
Name varchar(100),
Type varchar(50),
Address varchar(255),
City varchar(255),
Contact varchar(255)
);

create table receiver(
Receiver_ID int primary	key,
Name varchar(50),
Type varchar(50),
City varchar(50),
Contact varchar(255)
);

create table food_listings(
Food_ID int primary	key,
Food_Name varchar(100),
Quantity int,
Expiry_Date date,
Provider_ID int,
Provider_Type varchar(50),
Location varchar(255),
Food_Type varchar(50),
Meal_Type varchar(50)
);

create table claim_data(
Claim_ID int primary key,
Food_ID int,
Receiver_ID int,
Status varchar(50),
Timestamp datetime
);
select * from providers;

-- 1. How many food providers and receivers are there in each city?
Select City, count(*) as provider_count
from providers
group by City;

select City, count(*) as receiver_count
from receiver
group by City;

-- 2. Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
SELECT p.type, SUM(f.Quantity) AS total_food_quantity
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.type
ORDER BY total_food_quantity DESC
LIMIT 1;

-- 3. What is the contact information of food providers in a specific city?
SELECT name, contact
FROM providers
WHERE City = '';

-- 4. Which receivers have claimed the most food?
SELECT r.Name, r.Receiver_ID, SUM(f.Quantity) AS total_claimed
FROM receiver r
JOIN claim_data c ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Name, r.Receiver_ID
ORDER BY total_claimed DESC
LIMIT 10;

-- 5. What is the total quantity of food available from all providers?
SELECT SUM(Quantity) AS total_food_available
FROM food_listings;


-- 6. Which city has the highest number of food listings?
SELECT p.City, COUNT(*) AS listings_count
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.City
ORDER BY listings_count DESC
LIMIT 1;

-- 7. What are the most commonly available food types?
SELECT Food_Type, COUNT(*) AS count
FROM food_listings
GROUP BY Food_Type
ORDER BY count DESC;

-- 8. How many food claims have been made for each food item?
SELECT Food_ID, COUNT(*) AS claim_count
FROM claim_data
GROUP BY Food_ID
ORDER BY claim_count DESC;

-- 9. Which provider has had the highest number of successful food claims?
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS successful_claims
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
JOIN claim_data c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'completed'
GROUP BY p.Provider_ID, p.Name
ORDER BY successful_claims DESC
LIMIT 1;

-- 10. What percentage of food claims are completed vs. pending vs. canceled?
SELECT 
    Status,
    COUNT(*) AS count,
    ROUND((COUNT(*) * 100.0) / total_count, 2) AS percentage
FROM claim_data,
    (SELECT COUNT(*) AS total_count FROM claim_data) AS totals
GROUP BY Status;


-- 11. What is the average quantity of food claimed per receiver?
SELECT 
    AVG(receiver_total) AS avg_quantity_claimed_per_receiver
FROM (
    SELECT 
        c.Receiver_ID, 
        SUM(f.Quantity) AS receiver_total
    FROM claim_data c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY c.Receiver_ID
) AS subquery;

-- 12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
SELECT 
    f.Meal_Type,
    SUM(f.Quantity) AS total_quantity_claimed
FROM claim_data c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY total_quantity_claimed DESC
LIMIT 1;


-- 13. What is the total quantity of food donated by each provider?
SELECT 
    p.Provider_ID,
    p.type,
    SUM(f.Quantity) AS total_quantity_donated
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Provider_ID, p.type
ORDER BY total_quantity_donated DESC;

select Status, Claim_ID, Food_ID from claim_data;
select * from food_listings order by Provider_ID ASC;








