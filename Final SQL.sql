CREATE DATABASE restaurant_reservations;
USE restaurant_reservations;
CREATE TABLE Customers (
    customerId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerName VARCHAR(45) NOT NULL,
    contactInfo VARCHAR(200), -- Stores email or phone number
    PRIMARY KEY (customerId)
);
CREATE TABLE Reservations (
    reservationId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerId INT NOT NULL,
    reservationTime DATETIME NOT NULL,
    numberOfGuests INT NOT NULL,
    specialRequests VARCHAR(200),
    PRIMARY KEY (reservationId),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);
CREATE TABLE DiningPreferences (
    preferenceId INT NOT NULL UNIQUE AUTO_INCREMENT,
    customerId INT NOT NULL,
    favoriteTable VARCHAR(45),
    dietaryRestrictions VARCHAR(200),
    PRIMARY KEY (preferenceId),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);
DELIMITER //

CREATE PROCEDURE findReservations(IN customer_id INT)
BEGIN
    SELECT * FROM Reservations WHERE customerId = customer_id;
END //

CREATE PROCEDURE addSpecialRequest(IN reservation_id INT, IN requests VARCHAR(200))
BEGIN
    UPDATE Reservations SET specialRequests = requests WHERE reservationId = reservation_id;
END //

DELIMITER ;

