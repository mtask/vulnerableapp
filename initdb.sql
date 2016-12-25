CREATE TABLE user (
   userid int PRIMARY KEY,
   username text,
   password text
);

CREATE TABLE userinfo (
   userid int PRIMARY KEY,
   email text,
   creditcardnum,
   cardtype
);

INSERT INTO user(userid, username, password) VALUES (1,'fred','salasana');

INSERT INTO user(userid, username, password) VALUES (2,'ned','qwerty');

INSERT INTO userinfo(userid, email, creditcardnum, cardtype) VALUES (1,'fred@example.com','9393-3456-3556', 'mastercard');

INSERT INTO userinfo(userid, email, creditcardnum, cardtype) VALUES (2,'ned@example.com','1359-3456-2455', 'visa');

.exit

