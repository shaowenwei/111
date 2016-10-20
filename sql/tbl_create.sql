
CREATE DATABASE group75p2;
USE group75p2;
CREATE TABLE User (
	username VARCHAR(20) PRIMARY KEY,
    firstname VARCHAR(20),
    lastname VARCHAR(20),
    password VARCHAR(256),
    email VARCHAR(40)
);

CREATE TABLE Album(
	albumid INT AUTO_INCREMENT PRIMARY KEY, 
	title VARCHAR(50),
	created TIMESTAMP DEFAULT NOW(),
	lastupdated TIMESTAMP DEFAULT NOW(),
	username VARCHAR(20),
	access ENUM('private','public'),
	FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE Photo(
	picid VARCHAR(40) PRIMARY KEY,
	format CHAR(3),
	date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE Contain(
	sequencenum INT PRIMARY KEY DEFAULT 0,
	albumid INT,
	picid VARCHAR(40),
	caption VARCHAR(255),
	FOREIGN KEY(albumid) REFERENCES Album(albumid),
	FOREIGN KEY(picid) REFERENCES Photo(picid)
);

CREATE TABLE AlbumAccess(
	albumid INT,
	username VARCHAR(20),
	PRIMARY KEY (albumid, username)
);
