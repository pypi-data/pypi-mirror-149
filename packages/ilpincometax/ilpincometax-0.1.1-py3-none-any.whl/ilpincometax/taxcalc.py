import enum

taxrates_2022=[
{"taxrate":.10,"single":(0,10275),"single_max_tax":0,"married":(0,20550),"married_max_tax":0},
{"taxrate":.12,"single":(10276,41775),"single_max_tax":1027.5,"married":(20551,83550),"married_max_tax":2055},
{"taxrate":.22,"single":(41776,89075),"single_max_tax":4807.38,"married":(83551,178150),"married_max_tax":9614.88},
{"taxrate":.24,"single":(89076,170050),"single_max_tax":15213.16,"married":(178151,340100),"married_max_tax":30426.66},
{"taxrate":.32,"single":(170051,215950),"single_max_tax":34646.92,"married":(340101,431900),"married_max_tax":69294.42},
{"taxrate":.35,"single":(215951,539900),"single_max_tax":49334.6,"married":(431901,647850),"married_max_tax":98670.1},
{"taxrate":.37,"single":(539901,-1),"single_max_tax":152310.97,"married":(647851,-1),"married_max_tax":174252.25}
]

class tax_type(enum.Enum):
    single='single'
    married='married'

def calculate_federal_tax(income,tax_typ=tax_type.single.name):
    max_tax = tax_typ+"_max_tax"
    return [{"taxbracket":x['taxrate']*100,"tax":x[max_tax]+(income-x[tax_typ][0])*x['taxrate']} for x in taxrates_2022 if (x[tax_typ][0] < income < x[tax_typ][1]) or (x[tax_typ][0] < income and x[tax_typ][1]==-1)]

def usage():
    print("Sample call :\n tax=calculate_federal_tax(50000,tax_type.single.name)")
    print(" tax=calculate_federal_tax(50000,tax_type.married.name)")




