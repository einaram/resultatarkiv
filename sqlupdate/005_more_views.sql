create view nuclidelist_full as select * from nuclidelist;
create view metadatalist_full as select * from metadatalist;
create view habitatlist_full as select * from habitatlist;
create view projects_full as select * from projects;
create view quantitylist_full as select * from quantitylist;
create view unitlist_full as select * from unitlist;
create view topiclist_full as select * from topiclist;
create view sampletypelist_full as 
SELECT st.id
      ,st.name
      ,st.shortname
      ,st.description
      ,sc.name as samplecatid
      ,st.samplesubtype
  FROM [DataArkiv].[dbo].[SampletypeList] st left join samplecatlist sc on samplecatid = sc.id;
create view samplesubtypelist_full as select ss.id,ss.name,st.name as sampletypeid 
from samplesubtype ss left join sampletype st on sampletypeid=st.id;
create view samplecatlist_full as select * from samplecatlist;