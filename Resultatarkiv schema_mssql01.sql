
create table samplesubtypelist(
	id integer primary key not null IDENTITY(1,1),
	name char(255),
	sampletypelistid integer not null references sampletypelist(id)
	);
    
create table datafile(
 id int IDENTITY(1000,1) primary key,
 filename varchar(255) not null,
 md5 varchar(64) not null,
 analysed bit not null default 0,
 imported bit not null default 0);