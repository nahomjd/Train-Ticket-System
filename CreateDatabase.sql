CREATE TABLE Passenger
(
  PID INT NOT NULL,
  PFirstName VARCHAR(25) NOT NULL,
  PEmail VARCHAR(50) NOT NULL,
  PLastName VARCHAR(25) NOT NULL,
  Ppassword VARCHAR(25) NOT NULL,
  PRIMARY KEY (PID)
);

CREATE TABLE TrainStations
(
  stationName VARCHAR(50) NOT NULL,
  stationID INT NOT NULL,
  Municipality VARCHAR(50) NOT NULL,
  zipCode INT NOT NULL,
  State/Province VARCHAR(50) NOT NULL,
  PRIMARY KEY (stationID)
);

CREATE TABLE Train
(
  trainID INT NOT NULL,
  numberOfFirstClassSeats INT NOT NULL,
  numberOfBusinessClassSeats INT NOT NULL,
  numberOfGeneralSeats INT NOT NULL,
  trainType VARCHAR(15) NOT NULL,
  company VARCHAR(50) NOT NULL,
  PRIMARY KEY (trainID)
);

CREATE TABLE Trip
(
  tripID INT NOT NULL,
  departTime INT NOT NULL,
  arrivalTime INT NOT NULL,
  numOfPassengers INT NOT NULL,
  departDate DATE NOT NULL,
  arrivalDate DATE NOT NULL,
  delayed VARCHAR(12) NOT NULL,
  delayedTime INT NOT NULL,
  Origin INT NOT NULL,
  Destination INT NOT NULL,
  trainID INT NOT NULL,
  PRIMARY KEY (tripID)
);

CREATE TABLE Ticket
(
  ticketID INT NOT NULL,
  seatType CHAR(6) NOT NULL,
  price NUMERIC(6,2) NOT NULL,
  ticketType CHAR(4) NOT NULL,
  PID INT NOT NULL,
  tripID INT NOT NULL,
  PRIMARY KEY (ticketID)
);