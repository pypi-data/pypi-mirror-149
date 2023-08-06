# CGR-PDFEXTRACT
Este paquete consta de dos librerias: 
- Extrae informacion de un solo archivo del "Informe de Control Posterior"
- Extrae informacion de un csv donde se ubican los urls de cada "Informe de Control Posterior"

## Instalacion

#### Requerimientos
Para el correcto funcionamiento del paquete y sus respectivos modulos, es necesario tener instalado los siguientes paquetes adicionales:
- os
- re
- time
- glob
- requests
- pdfplumber
- pandas 

#### Iniciamos la instalacion
```>> pip install cgr-pdfextract```

## Como usarlo

#### 1.- Extraer informacion de un solo informe

```
>> from cgrextract import pdfextractor 

>> pdfextractor(url, nomb_exp) 
```

Donde: 
- url     : es el valor de la url donde se aloja el informe de control
- nomb_exp: es el nombre que daremos al archivo que se generara

Luego de la ejecucion del modulo se generara un archivo ".csv" que tendra el siguiente formato "cgr_[nomb_exp].csv", este archivo estara alojado en el directorio de trabajo donde se viene trabajando. 

Ejemplo: 

```
>> from cgrextract import pdfextractor 

>> url = 'https://s3.amazonaws.com/spic-informes-publicados/resumen/2021/10/2021CPO043200043.pdf'

>> nomb_exp = 'informe'

>> pdfextractor(url, nomb_exp)
```



#### 2.- Extraer informacion de un csv

```
>> from cgrextract import pdfextractor_all

>> pdfextractor_all(nomb_arch, col_url, nomb_exp, registros) 
```

Donde:

- nomb_arch: nombre del archivo "csv" donde se ubican la lista de los informes de control con sus respectivos urls.

- col_url  : nombre de la variable donde se encuentran las urls donde se ubican los resumenes de los informes de control.

- nomb_exp : nombre que le asignamos al archivo que consolidara la informacion de todos los informes de control. 

- registros: cantidad de informes de control que se quiere trabajar.

Luego de ejecutar el modulo, se creara una carpeta con el nombre "pdf_extraccion" en donde se almacenara el archivo que consolide la informacion de los resumenes de los "Informes de Control Posterior" procesados.

Ejemplo: 

Para el ejemplo, es necesario descargar el archivo "informe_CGR.csv" (https://github.com/JelsinPalomino/Coordenadas-Geograficas/blob/master/informe_CGR.csv)

```
>> from cgrextract import pdfextractor_all

>> nomb_arch = 'informe_CGR.csv'  

>> col_url   = 'resumen'

>> nomb_exp  = "informes_CGR_nacional"

>> registros = 8

>> pdfextractor_all(nomb_arch, col_url, nomb_exp, registros)
```


## Licencia

Este repositorio esta autorizado bajo la licencia MIT. Ver LICENCIA para mas detalles.