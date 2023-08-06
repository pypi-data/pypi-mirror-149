import os
import re
import time
import glob
import requests
import pdfplumber
import pandas as pd
from collections import OrderedDict


def pdfextractor(url, csv):
    
    def download_file(url):
        local_filename=url.split('/')[-1]
        with requests.get(url) as r:
            with open(local_filename, 'wb') as f:
                f.write(r.content)
            
        return local_filename
    
    invoice = download_file(url)

    dni      = []
    nombre   = []
    procesos = []
    nombre_re = re.compile(r'(\d{8}) (.*?) X')

    with pdfplumber.open(invoice) as pdf:

        text   = pdf.pages[0].extract_text()
        text_  = text.split('Objetivo general: ')[-1]
        obj = text_.split('Entidad sujeta a control: ')[0]
        obj_ = obj.split('\n')
        objetivo = ' '.join(obj_)

        text_  = text.split('Ubigeo: Región:  Provincia:  Distrito: ')[-1]
        ubigeo = text_.split('Fecha de emisión del')[0]
        ubigeo = ubigeo.split('\n')[1]

        for page in pdf.pages:
            text = page.extract_text()
            for row in text.split('\n'):
                if   row.startswith('N° de informe'):
                    n_informe = row.split(':')[-1]
                elif row.startswith('Entidad sujeta a control'):
                    entidad_control = row.split(':')[-1]
                elif row.startswith('Monto objeto del'):
                    monto_objetivo = row.split('servicio')[-1]
                elif row.startswith('Fecha de emisión'):
                    fecha_emision = row.split('del')[-1]
                elif row.startswith('Unidad orgánica que'):
                    unidad_emite = row.split('emite')[-1]

                row_ = str(row)
                nomb = nombre_re.search(row_)
                if nomb:
                    dni_, name_ = nomb.group(1), nomb.group(2)
                    dni.append(dni_)
                    nombre.append(name_)
                    line_ = row_.split(nomb.group(2))[-1]
                    b_=sum(i == 'X' for i in line_)
                    procesos.append(b_)

    os.remove(invoice)

    cgr = pd.DataFrame({ 'n_informe'                  : n_informe,
                         'objetivo'                   : objetivo,
                         'entidad_sujeto_a_control'   : entidad_control,
                         'monto_objeto_del_servicio'  : monto_objetivo,
                         'ubigeo'                     : ubigeo,
                         'fecha_emision'              : fecha_emision,
                         'unidad_que_emite'           : unidad_emite,
                         'dni'                        : dni,
                         'nombre'                     : nombre,
                         'tipo_acusacion'             : procesos
                        })

    cgr.to_csv('cgr_'+csv+'.csv', encoding='utf-8', index=False)
    

def pdfextractor_all(nomb_arch, col_url, nomb_exp, registros):

    import pandas as pd
    url = pd.read_csv(nomb_arch, encoding='latin-1')
    url1 = url[col_url]
    url2 = url1[:registros]
    lista_url0 = url2.values.tolist()
    lista_url = list(map(str, lista_url0))

    def download_file(url):
        local_filename=url.split('/')[-1]

        with requests.get(url) as r:
            with open(local_filename, 'wb') as f:
                f.write(r.content)

        return local_filename

    nombre_re = re.compile(r'(\d{8}) (.*?) X')

    os.mkdir('pdf_extraccion')
    os.chdir('pdf_extraccion')
    print('Se creo y cambio carpeta de trabajo a "pdf_extraccion" con exito')
    print('Inicio del proceso de extracción')
    for i in range(len(lista_url)):
        print('Documento:',i)
        invoice = download_file(lista_url[i])

        dni      = []
        nombre   = []
        procesos = []

        with pdfplumber.open(invoice) as pdf:

            text   = pdf.pages[0].extract_text()
            text_  = text.split('Objetivo general: ')[-1]
            obj = text_.split('Entidad sujeta a control: ')[0]
            obj_ = obj.split('\n')
            objetivo = ' '.join(obj_)

            text_  = text.split('Ubigeo: Región:  Provincia:  Distrito: ')[-1]
            ubigeo = text_.split('Fecha de emisión del')[0]
            ubigeo = ubigeo.split('\n')[1]

            for page in pdf.pages:
                text = page.extract_text()
                for row in text.split('\n'):
                    if   row.startswith('N° de informe'):
                        n_informe = row.split(':')[-1]
                    elif row.startswith('Entidad sujeta a control'):
                        entidad_control = row.split(':')[-1]
                    elif row.startswith('Monto objeto del'):
                        monto_objetivo = row.split('servicio')[-1]
                    elif row.startswith('Fecha de emisión'):
                        fecha_emision = row.split('del')[-1]
                    elif row.startswith('Unidad orgánica que'):
                        unidad_emite = row.split('emite')[-1]

                    row_ = str(row)
                    nomb = nombre_re.search(row_)
                    if nomb:
                        dni_, name_ = nomb.group(1), nomb.group(2)
                        dni.append(dni_)
                        nombre.append(name_)
                        line_ = row_.split(nomb.group(2))[-1]
                        b_=sum(i == 'X' for i in line_)
                        procesos.append(b_)

        os.remove(invoice)

        cgr = pd.DataFrame({ 'n_informe'                  : n_informe,
                             'objetivo'                   : objetivo,
                             'entidad_sujeto_a_control'   : entidad_control,
                             'monto_objeto_del_servicio'  : monto_objetivo,
                             'ubigeo'                     : ubigeo,
                             'fecha_emision'              : fecha_emision,
                             'unidad_que_emite'           : unidad_emite,
                             'dni'                        : dni,
                             'nombre'                     : nombre,
                             'tipo_acusacion'             : procesos
                            })

        string = str(i)
        cgr.to_csv('cgr'+string+'.csv', encoding='utf-8', index=False)
    print('Fin del proceso de extracción y exportación de archivos')

    print('Concatenando los archivos')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('cgr*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    regist = str(registros)
    combined_csv.to_csv(nomb_exp+regist+'.csv', index=False, encoding='utf-8')

    #eliminamos archivos
    for k in all_filenames:
        os.remove(k)

    print('Fin del proceso de concatenación')
    print('\n')
    print('FIN DE TODO EL PROCESO, revisar la carpeta "pdf_extraccion" ;)')