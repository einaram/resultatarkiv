alter table metadatalist alter column name varchar(250);
create index  mdl_name on metadatalist(name);

alter table sampletypelist alter column name varchar(250);
create index stl_name on sampletypelist(name);