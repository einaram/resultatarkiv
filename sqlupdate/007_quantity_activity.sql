alter table quantitylist add activity bit default 0;
update quantitylist set activity = 1 where name in ('Aktivitet','Dose');
update quantitylist set activity = 0 where activity is null;