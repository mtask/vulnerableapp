CREATE TABLE user (
   userid int PRIMARY KEY,
   username text,
   password text
);

CREATE TABLE storage (
   userid int,
   private TEXT,
   data TEXT
);

INSERT INTO user(userid, username, password) VALUES (1,'teddy','Salasana123');

INSERT INTO user(userid, username, password) VALUES (2,'fred','Salasana23');

.exit
