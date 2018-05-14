
create table samplesubtypelist(
	id integer primary key not null IDENTITY(1,1),
	name char(255),
	sampletypelistid integer not null references sampletypelist(id)
	);