import datetime
from openpyxl import Workbook


from .dbconnector import *


# Class to search for and download data

class searchdata(dbconnector):

       
    def countsamples(self,req):
        # Shows the number of sample available per project for the actual query
        # req: Dataset collected from a request object
        table='sample'
        self.preparequeryfields(table,req)
        sql="select projectid,count(sample.id),projects.name,projects.contact,projects.dataowner,projects.restrictions from sample left join projects on projectid=projects.id "
        if len(self.fields)>0:
            sql=sql+"where "+' and '.join(self.fields)
        sql=sql+" group by projects.name,projects.restrictions,projectid,projects.contact,projects.dataowner"
        self.cursor.execute(sql,self.values)
        res=self.cursor.fetchall()
        return(res)
    
     
    
    def preparequeryfields(self,table,req,ignoreZero=True):
        # Cleans out a request object and enumerates fields 
        # Table: Table to be queried
        # req: Requestobject
        # ignoreZero: True if numeric zero values from the request object should be ignored
        #             if this is set to false, a 0 value from the request object will be matched
        self.fielddata=tree()
        self.getcolnames(table)
        for k,v in req.items():
            if v=="" or (v=="0" and IgnoreZero):
                continue # Go to next value - considered non-significant
            if k in self.colnames:
            # Will only use this if k is a column name
                self.fielddata[k]=v
            elif v=="on":
            # A checkbox is codeded as Fieldname_value and will have the value "on" is checked
                p=k.split("_")
                if p[0] in self.colnames:
                    # There may be several values that are checked for one field
                    if self.fielddata[p[0]]=={}:
                        self.fielddata[p[0]]=[p[1]]
                    else:
                        self.fielddata[p[0]].append(p[1])
        self.fields=[]
        self.values=[]
        for k,v in self.fielddata.items():
            if type(v)==list: # From the checkbox, must possibly check for several values
                k=k+" in ("+",".join("?"*len(v)) +")"
                self.values.extend(v) # adds the values on to the list as separate items
            else:
                k=k+"=?"
                self.values.append(v)
            self.fields.append(k)
            
                
    def subtype(self,sql,subselect,idfield,prefix='x',selecttemplate=None,headertemplate=None):
        # Builds up sql fragments to get separate colums for the different nuclides, values and metadatatypes
        # subselect: A sql to find which of the actual valuetypes are used
        # idfield: id field in the queried table
        # prefix: Prefix to use for the queried table in the aliases 
        # selecttemplate: Template for the select part of the query
        # Headertemplate: Template for the header in the result table
        
        if selecttemplate==None:
            selecttemplate = "{0}.value '{1}'"
        if headertemplate==None:
            headertemplate="{0}"
        self.cursor.execute(sql,self.values)
        fetch=self.cursor.fetchall()
        metadata=[]
        select=[]
        where=[]
        header=[]
        for i in fetch:
            metadata.append([i[0],i[1]])
            if i[0]==None or i[1]==None:
                continue
            id=str(i[0])
            alias=prefix+id # alias to use for the table with the given metadatatype
            select.append(selecttemplate.format(alias,id))
            where.append(alias+" on "+alias+".sampleid=f.id and "+alias+"."+idfield+"="+id)
            header.append(headertemplate.format(i[1]))
        metadata=[select,where,header]
        return(metadata)
    
    
    def download(self,req,folder):
        # Builds up a sql command to fetch all the desired data making a pivot table on the results. Runs the sql and stores the data
        # req: request object
        # folder: Where to store the data
        self.preparequeryfields('sample',req)
        subselect="(select id from sample where "+' and '.join(self.fields)+")"
        sql="select distinct m.id,name from metadatalist m right join samplemetadata on m.id = metadataid where sampleid in "+subselect
        values=self.values
        metadata=self.subtype(sql,subselect,'metadataid','m')
        sql="select distinct q.id,name from quantitylist q right join samplevalue on q.id=quantityid where sampleid in "+subselect 
        headertemplate="{0};{0}_unit "
        selecttemplate="{0}.value '{1}_act',{0}.unit "
        quantitydata=self.subtype(sql,subselect,'quantityid','q',selecttemplate,headertemplate)
        sql="select distinct n.id,name from nuclidelist n right join samplevalue on n.id=nuclideid where  nuclideid is not null and sampleid in "+subselect
        headertemplate="{0};{0}_unit;{0}_unc;{0}_uncunit;{0}_mda;{0}_mdaunit;{0}_lab"
        selecttemplate="{0}.value '{1}_act',{0}.unit '{1}_unit', {0}.unc_value '{1}_unc' ,{0}.unc_unit '{1}_unc_unit' ,{0}.mda_value '{1}_mda', {0}.mda_unit '{1}_mda', {0}.laboratory  '{1}_lab'"
        nuclidedata=self.subtype(sql,subselect,'nuclideid','n',selecttemplate,headertemplate)
        sqlselect="select f.*  ,"+",".join(nuclidedata[0])+","+" , ".join(metadata[0])+","+" , ".join(quantitydata[0])
        sqlfrom="from fullsample f left join samplevalue_unit "+" left join samplevalue_unit ".join(nuclidedata[1]) +" left join samplemetadata "+" left join samplemetadata ".join(metadata[1]) +" left join samplevalue_unit "+" left join samplevalue_unit ".join(quantitydata[1]) 
        sqlwhere=" where f.id in "+subselect
        sql=sqlselect+sqlfrom+sqlwhere
        
        timestamp=datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.excelfile="resultatarkiv_"+timestamp+".xlsx"
        wb = Workbook(write_only=True)
        ws = wb.create_sheet()        
        self.filename="resultatarkiv_"+timestamp+".csv"
        wf=open(folder+"/"+self.filename,"w")
        sep=";"
        self.preparequeryfields('fullsample',req)
        nucheader=sep.join(nuclidedata[2]).split(sep)
        header=self.colnames+nucheader+metadata[2]
        wf.write(sep.join(header)+"\n")
        
        ws.append(header)
        self.cursor.execute(sql,values) 
        lastrow=[]
        while True: 
        # TODO: Write to an excel file
            row=self.cursor.fetchone()
            if row is None: 
                break
            row = map(lambda x: '' if x==None else x, row)
            row = list(map(str,row))
            if lastrow!=row:
                ws.append(row)
                wf.write(sep.join(row)+"\n")
            lastrow=row
        wb.save(folder+"/"+self.excelfile)
        
    def  overviewfields(self):
        return( ["Antall","Prosjekt","Kontaktperson","Dataeier","Restriksjoner"] )


    def __init__(self):
        self.connecttodb()        

        
    
        
    def search(self):
        True
    

    
