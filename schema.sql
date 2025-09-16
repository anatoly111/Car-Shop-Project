DROP TABLE IF EXISTS cars;

CREATE TABLE cars
(
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    PRICE INTEGER NOT NULL,
    color TEXT NOT NULL,
    description TEXT,
    image BLOB, 
    make TEXT
    );

INSERT INTO cars(name,price,color,description,image,make)
VALUES
    ('Audi A5',59328,'Blue','Automatic transmission with a 2.0L Diesel engine and 3 year warranty','audiA5.jpg','Audi'),
    ('trolley',60000,'Grey','Tesco shopping trolley (slightly modified)','trolley.jpg','Trolley'),
    ('BMW i4',79336,'White','Electric BMW with automatic transmission and 3 year warranty','i4.jpg','BMW'),
    ('BMW X2',60004,'Blue','Automatic transmission with a 2.0L petrol engine and a 3 year warranty','x2.jpg','BMW'),
    ('Audi Q2',41407,'Grey','Manual transmission with a 2.0L Diesel engine and a 3 year warranty','q2.jpg','Audi'),
    ('Volkswagen Beetle',55000,'Pink','A 2024 car with automatic transmission and a 2.0L diesel engine','beetle.jpg','Volkswagen'),
    ('Volkswagen Tiguan', 66300,'Grey','A 2024 car with automatic transmission and a 2.0L diesel engine','tig.jpg','Volkswagen'),
    ('Mercedes-Benz EQS',122995,'Red','A 2024 electric car with automatic transmission','eqs.jpg','Mercedes'),
    ('Mercedes-Benz CLA-class',63495,'Red','A diesel hybrid with automatic transmission 2.0L engine','eqs.jpg','Mercedes'),
    ('Ford Focus',65950,'Grey','Manual transmission with a 2.3L petrol engine and a 5 year warranty','f.jpg','Ford');



DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS info;

CREATE TABLE info
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name INTEGER NOT NULL,
    AGE INTEGER, 
    email TEXT
);


DROP TABLE IF EXISTS contact;

CREATE TABLE contact
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL, 
    email TEXT NOT NULL,
    message TEXT NOT NULL

);

SELECT * from contact;