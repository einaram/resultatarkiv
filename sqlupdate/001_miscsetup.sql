
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
 
 
 create table users(
  username varchar(40) not null primary key,
  fullname varchar(255) not null,
  email varchar(255),
  hashedpassword varchar(255),
  userclass integer not null default 0);

  
insert into users VALUES('admin','Administrator','','admin',255);

  
alter table projects alter column restrictions varchar(2048);
  
create view fullsample as
select sample.id,Projects.name,reftime,SampletypeList.name as sampletype,GeoAreas.name as Area,comment,species_no as art
,samplestart,samplestop,parentsampleid,sample_date,location.STY as latitude, location.STX as longitude
from sample left outer join projects on projectid=projects.id left join sampletypelist on sampletype=sampletypelist.id 
left outer join Geoareas on sample.areaid=GeoAreas.areaid 
left outer join SpeciesList on speciesid=SpeciesList.id;


