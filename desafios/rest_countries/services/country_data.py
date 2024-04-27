import json, requests, csv, xmltodict, xlsxwriter
from numerize import numerize 

url = 'https://restcountries.com/v3.1/name/'

def get_data(nome):
    name =  url + f"{nome}"
    info = requests.get(name)
    tt = json.loads(info.text)
    mylist = []
    sem_dado = 'NO DATA'
    for t in tt:
        valores = ['nome_pais_en','bandeira','regiao','subregiao','populacao','fuso-horario',
                   'nome_nativo', 'populacao_compact', 'bandeira_svg', 'capital', 'area', 'moeda', 'linguas']
        
        moedas = t.get('currencies', sem_dado)
        moedas_valores = list(moedas.values())[0]

        linguas = t.get('languages', sem_dado)
        linguas_valores = list(linguas.values())

        items = [t.get('name', {}).get('common', sem_dado),
                 t.get('flags', {}).get('png', sem_dado),
                 t.get('region', sem_dado),
                 t.get('subregion', sem_dado),
                 t.get('population', sem_dado),
                 t.get('timezones', sem_dado)[0],
                 list(t.get('name',{}).get('nativeName', sem_dado).values())[0].get('common', sem_dado),
                 numerize.numerize(t.get('population'), 2),
                 t.get('flags', {}).get('svg', sem_dado),
                 t.get('capital', sem_dado),
                 t.get('area', sem_dado),
                 [list(moedas.keys())[0], moedas_valores['name'], moedas_valores['symbol']],
                 linguas_valores]
        mylist.append(dict(zip(valores,items)))
    return mylist


def criar_csv(pais):
    detalhes = get_data(pais)[0]
    items_list = ['nome_pais_en', "bandeira", 'regiao', 'subregiao', 'populacao', 'fuso-horario', 'nome_nativo']
    cabecalho = ["Pais", "Bandeira", "Regiao", "Sub Regiao", "Populacao", "Fuso-Horario", "Nome Local"]

    items = {field: detalhes.get(field, '') for field in items_list}
    csv_filename = f"{pais}_detalhes.csv"

    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerow(items.values())

    return csv_filename

def criar_xml(pais):
    detalhes = get_data(pais)[0]
    items_list = ['nome_pais_en', "bandeira", 'regiao', 'subregiao', 'populacao', 'fuso-horario', 'nome_nativo']
    items = {'country': {field: detalhes.get(field, '') for field in items_list}}
    
    xml_filename = f"{pais}_detalhes.xml"

    xml_file=open(xml_filename, 'w')
    xmltodict.unparse(items,output=xml_file)
    xml_file.close()

    return xml_filename

def criar_excel(pais):
    xls_filename = f"{pais}_detalhes.xls"
    workbook = xlsxwriter.Workbook(xls_filename)
    worksheet = workbook.add_worksheet()

    detalhes = get_data(pais)[0]
    items_list = ['nome_pais_en', "bandeira", 'regiao', 'subregiao', 'populacao', 'fuso-horario', 'nome_nativo']

    items_dict = {field: detalhes.get(field, '') for field in items_list}

    col_num = 0
    for key, value in items_dict.items():
        worksheet.write(0, col_num, key)
        worksheet.write(1, col_num, value)
        col_num += 1

    workbook.close()

    return xls_filename