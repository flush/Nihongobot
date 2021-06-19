
SET CHARACTER_SET_SERVER = 'utf8';
drop table IF EXISTS VALOR_CARACTERISTICA;
drop table IF EXISTS CARACTERISTICAS_CATEGORIAS;
drop table IF EXISTS  USUARIOS;
drop table IF EXISTS  CATEGORIAS;
drop table IF EXISTS  CARACTERISTICAS;
drop table IF EXISTS  ITEM_INFO;


CREATE TABLE USUARIOS(
       id INTEGER UNSIGNED,
       nombre varchar(50),
       constraint usuarios_pk PRIMARY KEY (id)

);


CREATE TABLE CATEGORIAS(
	id SERIAL,
	nombre VARCHAR(100),
	constraint categorias_pk PRIMARY KEY (id)
);

INSERT INTO CATEGORIAS (id,nombre) VALUES (1,'onomatopeyas');
INSERT INTO CATEGORIAS (id,nombre) VALUES (2,'adverbios');
INSERT INTO CATEGORIAS (id,nombre) VALUES (3,'kanjis');

CREATE TABLE CARACTERISTICAS(
	id SERIAL,
	nombre VARCHAR(100),
	constraint caracteristicas_pk PRIMARY KEY (id)
);
INSERT INTO CARACTERISTICAS (id,nombre) VALUES (1,'hiragana');
INSERT INTO CARACTERISTICAS (id,nombre) VALUES (2,'kanji');
INSERT INTO CARACTERISTICAS (id,nombre) VALUES (3,'significado');

CREATE TABLE CARACTERISTICAS_CATEGORIAS(
	idCategoria BIGINT UNSIGNED ,
	idCaracteristica BIGINT UNSIGNED,
	pregunta BOOLEAN,
	respuesta BOOLEAN,
	constraint caract_cate_cate_fk FOREIGN KEY (idCategoria) REFERENCES CATEGORIAS(id),  
	constraint caract_cate_caract_fk FOREIGN KEY (idCaracteristica) REFERENCES CARACTERISTICAS(id)
);
-- Las onomomatopyeas tienen hiragana y significado
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(1,1,TRUE,TRUE);
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(1,3,TRUE,TRUE);

-- Las adverbios tienen hiragana y significado
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(2,1,TRUE,TRUE);
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(2,3,TRUE,TRUE);

-- Los Kanjis tienen hiragana, kanji y significado
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(3,1,TRUE,TRUE);
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(3,2,TRUE,TRUE);
INSERT INTO CARACTERISTICAS_CATEGORIAS VALUES(3,3,TRUE,TRUE);




CREATE TABLE ITEM_INFO(
	id SERIAL,
	idCategoria BIGINT UNSIGNED
);

CREATE TABLE VALOR_CARACTERISTICA(

	idItem BIGINT UNSIGNED,
	idCaracteristica BIGINT UNSIGNED,
	valor VARCHAR (300),
	constraint valor_caract_item_fk FOREIGN KEY (idItem) REFERENCES ITEM_INFO(id),  
	constraint valor_caract_caract_fk FOREIGN KEY (idCaracteristica) REFERENCES CARACTERISTICAS(id)

);




insert into USUARIOS values (252231615,'Isa');
insert into USUARIOS values (709463079,'Alfredo');
