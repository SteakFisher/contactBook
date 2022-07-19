# Railway Management System

create table logininfo(userId int primary key NOT NULL AUTO_INCREMENT, username varchar(30) NOT NULL,
password varchar(30) NOT NULL, unique(username));

create table if not exists customerInfo(userid int, customerId int primary key NOT NULL AUTO_INCREMENT,
customerName varchar(30) NOT NULL, customerSurname varchar(30), customerLastName varchar(30),
NOT NULL, constraint foreign key (userid) references loginInfo(userId))

create table contactInfo(userId int NOT NULL, contactId int primary key NOT NULL
AUTO_INCREMENT, contactName varchar(30), contactSurname varchar(30),
contactLastName varchar(30), constraint userId foreign key(userId) references loginInfo(userid));
