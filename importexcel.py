from xlrd import open_workbook

class Arm(object):
    def __init__(self, id, dsp_name, dsp_code):
        self.id = id
        self.dsp_name = dsp_name
        self.dsp_code = dsp_code
  
    def __str__(self):
        return("Arm object:\n"
               "  Arm_id = {0}\n"
               "  DSPName = {1}\n"
               "  DSPCode = {2}\n"
               .format(self.id, self.dsp_name, self.dsp_code))


def checkworkbook(filename):
    wb = open_workbook(filename)
    sht = wb.sheet_by_index(0)
    projecttype=sht.cell(0,0)
    project=sht.cell(1,0)
    print(projecttype)
    print(project)
    number_of_rows = sht.nrows
    number_of_columns = sht.ncols
    items = []
    rows = []
    
    
    
    for row in range(1, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sht.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = Arm(*values)
        items.append(item)

    for item in items:
        print(item)
        print("Accessing one single value (eg. DSPName): {0}".format(item.dsp_name))
        print


checkworkbook('../resultat_test/RAME Tokt.xlsx')
