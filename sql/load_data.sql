INSERT INTO User
VALUES('sportslover','Paul','Walker','sha512$e4847126d4c74644b6f7f8e403472c81$613522315e62bbcd8139c2cc2fa5d388b4915586ac78765e87078598744216ad2b5ae0bb01486d16f52b5ae4ae25882390d83052471c1f41e0428981d3efbd56','sportslover@hotmail.com');
INSERT INTO User
VALUES('traveler','Rebecca','Travolta','sha512$982b17f8b1aa42ad8cbd15adfbd2d733$06cfc499ea5169394a1c6e2e178f3e08324d18f25516184e9cdce73ebe20b85769dbd7e3c67119515867942cbfc36f89ba453ea738694fd107273365470c3e1f','rebt@explorer.org');
INSERT INTO User
VALUES('spacejunkie','Bob','Spacey','sha512$e94c83a18b794ac6be01e4a5cd715dd0$f315bb546ca5ff71fd74da50db13cf180de41b2054d6461e348b69bdf53af3c012bcfdd5b57e12f95e985e488bc16f4762eb2550f39f87e7a29536300207e86e','bspace@spacejunkies.net');

INSERT INTO Album(title,username,access)
VALUES('I love sports','sportslover','public');
INSERT INTO Album(title,username,access)
VALUES('I love football','sportslover','private');
INSERT INTO Album(title,username,access)
VALUES('Around The World','traveler','public');
INSERT INTO Album(title,username,access)
VALUES('Cool Space Shots','spacejunkie','private');

INSERT INTO Photo(picid, format) VALUES ('001025dd643b0eb0661e359de86e3ea9', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (0, 2, '001025dd643b0eb0661e359de86e3ea9', '');
INSERT INTO Photo(picid, format) VALUES ('9a0a7d25af4f7a73f67dde74e8e54cff', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (1, 2, '9a0a7d25af4f7a73f67dde74e8e54cff', '');
INSERT INTO Photo(picid, format) VALUES ('c8e60100f13ffe374d59e39dc4b6a318', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (2, 2, 'c8e60100f13ffe374d59e39dc4b6a318', '');
INSERT INTO Photo(picid, format) VALUES ('5e8b6207f007338243d3e29d6b82acab', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (3, 2, '5e8b6207f007338243d3e29d6b82acab', '');
INSERT INTO Photo(picid, format) VALUES ('4ddba6e2f905e9778c6b6a48b6fc8e03', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (4, 4, '4ddba6e2f905e9778c6b6a48b6fc8e03', '');
INSERT INTO Photo(picid, format) VALUES ('09d8a979fa638125b02ae1578eb943fa', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (5, 4, '09d8a979fa638125b02ae1578eb943fa', '');
INSERT INTO Photo(picid, format) VALUES ('143ba34cb5c7e8f12420be1b576bda1a', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (6, 4, '143ba34cb5c7e8f12420be1b576bda1a', '');
INSERT INTO Photo(picid, format) VALUES ('e615a10fc4222ede59ca3316c3fb751c', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (7, 4, 'e615a10fc4222ede59ca3316c3fb751c', '');
INSERT INTO Photo(picid, format) VALUES ('65fb1e2aa4977d9414d1b3a7e4a3badd', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (8, 4, '65fb1e2aa4977d9414d1b3a7e4a3badd', '');
INSERT INTO Photo(picid, format) VALUES ('b94f256c23dec8a2c0da546849058d9e', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (9, 1, 'b94f256c23dec8a2c0da546849058d9e', '');
INSERT INTO Photo(picid, format) VALUES ('01e37cbdd55913df563f527860b364e8', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (10, 1, '01e37cbdd55913df563f527860b364e8', '');
INSERT INTO Photo(picid, format) VALUES ('8d554cd1d8bb7b49ca798381d1fc171b', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (11, 1, '8d554cd1d8bb7b49ca798381d1fc171b', '');
INSERT INTO Photo(picid, format) VALUES ('2e9e69e19342b98141789925e5f87f60', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (12, 1, '2e9e69e19342b98141789925e5f87f60', '');
INSERT INTO Photo(picid, format) VALUES ('298e8943ef1942159ef88be21c4619c9', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (13, 1, '298e8943ef1942159ef88be21c4619c9', '');
INSERT INTO Photo(picid, format) VALUES ('cefe45eaeaeb599256dda325c2e972da', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (14, 1, 'cefe45eaeaeb599256dda325c2e972da', '');
INSERT INTO Photo(picid, format) VALUES ('bf755d13bb78e1deb59ef66b6d5c6a70', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (15, 1, 'bf755d13bb78e1deb59ef66b6d5c6a70', '');
INSERT INTO Photo(picid, format) VALUES ('5f8d7957874f1303d8300e50f17e46d6', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (16, 1, '5f8d7957874f1303d8300e50f17e46d6', '');
INSERT INTO Photo(picid, format) VALUES ('bac4fca50bed35b9a5646f632bf4c2e8', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (17, 3, 'bac4fca50bed35b9a5646f632bf4c2e8', '');
INSERT INTO Photo(picid, format) VALUES ('f5b57bd7a2c962c54d55b5ddece37158', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (18, 3, 'f5b57bd7a2c962c54d55b5ddece37158', '');
INSERT INTO Photo(picid, format) VALUES ('b7d833dd3aae203ca618759fc6f4fc01', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (19, 3, 'b7d833dd3aae203ca618759fc6f4fc01', '');
INSERT INTO Photo(picid, format) VALUES ('faa20c04097d40cb10793a19246f2754', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (20, 3, 'faa20c04097d40cb10793a19246f2754', '');
INSERT INTO Photo(picid, format) VALUES ('aaaadd578c78d21defaa73e7d1f08235', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (21, 3, 'aaaadd578c78d21defaa73e7d1f08235', '');
INSERT INTO Photo(picid, format) VALUES ('adb5c3af19664129141268feda90a275', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (22, 3, 'adb5c3af19664129141268feda90a275', '');
INSERT INTO Photo(picid, format) VALUES ('abf97ffd1f964f42790fb358e5258e8d', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (23, 3, 'abf97ffd1f964f42790fb358e5258e8d', '');
INSERT INTO Photo(picid, format) VALUES ('ea2db8b970671856e43dd011d7df5fad', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (24, 3, 'ea2db8b970671856e43dd011d7df5fad', '');
INSERT INTO Photo(picid, format) VALUES ('76d79b81b9073a2323f0790965b00a68', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (25, 3, '76d79b81b9073a2323f0790965b00a68', '');
INSERT INTO Photo(picid, format) VALUES ('6510a4add59ef655ae3f0b6cdb24e140', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (26, 3, '6510a4add59ef655ae3f0b6cdb24e140', '');
INSERT INTO Photo(picid, format) VALUES ('28d38afca913a728b2a6bcf01aa011cd', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (27, 3, '28d38afca913a728b2a6bcf01aa011cd', '');
INSERT INTO Photo(picid, format) VALUES ('5fb04eb11cbf99429a05c12ce2f50615', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (28, 3, '5fb04eb11cbf99429a05c12ce2f50615', '');
INSERT INTO Photo(picid, format) VALUES ('39ee267d13ccd32b50c1de7c2ece54d6', 'jpg');
INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (29, 3, '39ee267d13ccd32b50c1de7c2ece54d6', '');
