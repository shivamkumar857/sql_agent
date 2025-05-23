-- use onlineshopping;
-- 1. Reset database
DROP DATABASE IF EXISTS OnlineShopping;
CREATE DATABASE OnlineShopping;
USE OnlineShopping;
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL
);

CREATE TABLE Country (
    CountryID INT AUTO_INCREMENT PRIMARY KEY,
    CountryName VARCHAR(255) NOT NULL
);

CREATE TABLE Province (
    ProvinceID INT AUTO_INCREMENT PRIMARY KEY,
    ProvinceName VARCHAR(255) NOT NULL
);

CREATE TABLE City (
    CityID INT AUTO_INCREMENT PRIMARY KEY,
    CityName VARCHAR(255) NOT NULL
);

CREATE TABLE ZipCode (
    ZipCodeID INT AUTO_INCREMENT PRIMARY KEY,
    CityID INT NOT NULL,
    ProvinceID INT NOT NULL,
    CountryID INT NOT NULL,
    FOREIGN KEY (CityID) REFERENCES City(CityID),
    FOREIGN KEY (ProvinceID) REFERENCES Province(ProvinceID),
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);


CREATE TABLE Address (
    AddressID INT AUTO_INCREMENT PRIMARY KEY,
    HouseNo VARCHAR(255) NOT NULL,
    Street VARCHAR(255) NOT NULL, -- Changed from INT to VARCHAR to support alphanumeric street names
    CustomerID INT NOT NULL,
    ZipCodeID INT NOT NULL,
    Area VARCHAR(255) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ZipCodeID) REFERENCES ZipCode(ZipCodeID)
);

CREATE TABLE Category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(255) NOT NULL
);

CREATE TABLE Vendor (
    VendorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address TEXT NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL
);

CREATE TABLE Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    CategoryID INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

CREATE TABLE VendorProduct (
    VendorProductID INT AUTO_INCREMENT PRIMARY KEY,
    VendorID INT NOT NULL,
    ProductID INT NOT NULL,
    Price DECIMAL(19, 2) NOT NULL,
    Quantity INT NOT NULL,
    Description TEXT NOT NULL,
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Courier (
    CourierID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL
);

CREATE TABLE VendorCourier (
    VendorCourierID INT AUTO_INCREMENT PRIMARY KEY,
    VendorID INT NOT NULL,
    CourierID INT NOT NULL,
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID),
    FOREIGN KEY (CourierID) REFERENCES Courier(CourierID)
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    AddressID INT NOT NULL,
    VendorCourierID INT NOT NULL,
    TrackingID VARCHAR(255) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID),
    FOREIGN KEY (VendorCourierID) REFERENCES VendorCourier(VendorCourierID)
);

CREATE TABLE OrderedProduct (
    OrderedProductID INT AUTO_INCREMENT PRIMARY KEY,
    VendorProductID INT NOT NULL,
    OrderID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (VendorProductID) REFERENCES VendorProduct(VendorProductID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    Rating TINYINT NOT NULL,
    Comment TEXT,
    CustomerID INT NOT NULL,
    OrderedProductID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (OrderedProductID) REFERENCES OrderedProduct(OrderedProductID)
);

CREATE TABLE Cart (
    CartID INT AUTO_INCREMENT PRIMARY KEY,
    DateCreated DATE NOT NULL,
    CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE CartProduct (
    CartProductID INT AUTO_INCREMENT PRIMARY KEY,
    VendorProductID INT NOT NULL,
    Quantity INT NOT NULL,
    CartID INT NOT NULL,
    FOREIGN KEY (VendorProductID) REFERENCES VendorProduct(VendorProductID),
    FOREIGN KEY (CartID) REFERENCES Cart(CartID));


