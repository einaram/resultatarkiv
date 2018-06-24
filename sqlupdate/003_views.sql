create view specieslist_full as
select s.id,s.species_no,s.species_lat,s.species_en,h.name as habitatid,st.name as sampletypeid
from specieslist s left join habitatlist h on habitatid=h.id left join sampletypelist st on st.id=sampletypeid
