# nexus_integra_api
Este repositorio tiene como propósito reunir en una única libería todas las funciones necesarias para trabajar con la API de Nexus en Python.
En lugar de importar los archivos a la carpeta del proyecto cada vez que se usan puede instalarse la librería en la PATH de Python 

## Table of Contents

* [Instalación](#chapter1)
* [Uso](#chapter2)
* [Ejemplos](#chapter3)
  * [GetFiltered](#chapter3.1)
  * [Uso de alarmas](#chapter3.2)
  * [Email Alerts](#chapter3.3)
* [Contribuir](#chapter4)
* [Change Log](#chapter5)
* [Contacto](#chapter6)

## Instalación <a class="anchor" id="chapter1"></a>

Usa el package manager pip para instalar la librería. Puede instalarse de forma local o desde el repositorio de PyPi

```
pip install nexus_integra_api
```

## Uso <a class="anchor" id="chapter2"></a>
Para importar todo el contenido de la librería, una vez instalada hay que realizar el siguiente import:

    import nexus_api
Si únicamente se desea la clase en la que residen las funciones que trabajan con la API:

    from nexus_api import APINexus
Lo que otorga acceso a la clase APINexus en la que residen todas las funciones necesarias.

## Ejemplo de uso <a class="anchor" id="chapter3"></a>

### GetFiltered <a class="anchor" id="chapter3.1"></a>
Un ejemplo de uso para la famosa función GetFiltered que permite filtrar el histórico de variables entre un periodo dado:

En primer lugar se especifican los parámetros de conexión y se crea el objeto Nexus, además de los imports necesarios
```
from nexus_api import APINexus
import pandas as pd
import datetime

API_Host = 'nexus-cdi-demo.globalomnium.com'  
API_Port = 56000 
NexusToken = 'xxxxxxxxxxxxxxxxx' 
version = 'v1'
NX = APINexus.APINexus(API_Host, API_Port, NexusToken, version)
```
Después es necesario obtener el uid de la vista de variables que se quiere leer (también existe función para leer desde instalación)
```
# Leer vistas de variables asociadas al token  
tagviews = NX.callGetDocuments()  
tagviews = json_normalize(tagviews)  
# Busqueda del uid de la vista
uid_tagview = tagviews.uid[0]
```
Se especifica la ventana temporal deseada:
```
# Profundidad del análisis en fechas desde hoy  
delta_days = xxx  
date_format = '%m/%d/%Y %H:%M:%S %Z'  
date_to = datetime.datetime.now()  
date_from = date_to - datetime.timedelta(days=delta_days)
```
Hay que especificar las variables deseadas de la vista de variables elegida. Con este código se obtienen todos los uids de las variables de la vista. Es necesario filtrar 
```
# Variables en la vista de variables  
vbles = NX.callGetTagViews(uid_tagview)  
df = pd.DataFrame(vbles)  
columnas = df['columns']  
columnas = json_normalize(columnas)  
uids_vbles = list(columnas['uid'])  # String with variables UIDS
```
Finalmente se obtiene el histórico llamando a la función:
```
filtered_hist = NX.filter_tagview(date_from, date_to, columnas, uid_tagview, 'variable')
```

### Uso de alarmas <a class="anchor" id="chapter3.2"></a>
Desde la versión **0.4** del encapsulado pueden modificarse alarmas en la API. Para ello se debe obtener el uid de la alarma a modificar y luego llamar a la función:
#### Obtener uids de alarmas del token
```
alarmas = NX.callGetAlarms()
```

#### Obtener información de alarma por uid
```
alarma = NX.callGetAlarmByuid(uid)
```

#### Obtener uids de alarmas por nombres. Puede usarse una lista de nombres o un string con un nombre
```
uids_alarmas = NX.get_alarms_uids_by_names([names])
```
#### Obtener uids de alarmas por grupos de alarmas. Puede usarse una lista de grupos o un string con un grupo
```
uids_grupo = NX.get_alarms_uids_by_groups([groups])
```

#### Cambiar el estado de la alarma. Debe especificarse el uid de la alarma y el estado a cambiar ('ARE' o 'EXR')
```
NX.callPostAckAlarm(uid, estado)
```

#### Cambiar el mensaje de estado de la alarma
```
NX.callPostAlarmEvent(uid, msg)
```

### Email Alerts <a class="anchor" id="chapter3.3"></a>
Desde la versión **0.5** se añade soporte para generar alarmas de correo eléctronico.

Para usar la función debe crearse un objeto de tipo EmailAlerts. Deben proporcionarse los parámetros de conexión.

Se recomienda usar variables de entorno para proteger las credenciales. En caso de no estar definidas se deben especificar (reemplazar las líneas de os.getenv()):

```
import os

smtp_address = 'outlook.office365.com'
smtp_port = 587

# datos de la cuenta de envio
sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")
receiver_email_address = os.getenv("RECEIVER_EMAIL_ADDRESS")

email_alerts = EmailAlerts(smtp_address, smtp_port, sender_email_address, email_password, receiver_email_address)
```

Una vez creado el objeto email_alerts puede usarse con libertad, bien con los parámetros predeterminados o moficiando los componentes del mensaje

El asunto y el cuerpo del mensaje tienen valores predeterminados en función del nombre del archivo, pero environment es una variable requerida con la que identificar el entorno de producción.
```
enviroment = 'NEXUS_PROD'
subject = 'ALARMA'
body = 'Alarma de ' + environment

email_alerts.set_email_alert_info(subject, body, environment)
```


Se puede usar la alerta de correo en cualquier función, sea de la API o no. Si la ejecución falla, 
se captura la excepción y se envía un correo con el error (mensaje predeterminado).

Si se quiere incorporar a un script entero, debe usarse la función main()

```
# Uso del decorador para generar el correo

@email_alerts.email_alert_decorator
def main():
    # Aquí va todo el código del programa...
    raise Exception('Error en la función')
    
if __name__ == '__main__':
    main() # Si aparece un error, se envía un correo con el error
```

## Contribuir <a class="anchor" id="chapter4"></a>

Cualquier función o sugerencia añadida es bien recibida.

Sugerencias:

- Falta documentar las funciones de la API
- Traducir documentación

## Change log <a class="anchor" id="chapter5"></a>

###v0.5.0 - 12/04/2022

**Added**

 - Email alerts functions

**Changed**

 - Documentation

###v0.4.0 - 30/03/2022

**Added**
  
- API V2 alarm functions
  * callPostAckAlarm(uid, status)
  * callPostAlarmEvent(uid, msg)
  * callGetAlarms()
  * callGetAlarmByuid(uid)
  * get_alarms_uids_by_names([names])
  * get_alarms_uids_by_groups([groups])
- Unit tests
- .env file in order protect credentials
- Bypassed 50k row limit in POST methods
- Added support to datetime objects in callPostValueHist
  
**Modified**
  
- Unified callPostValueHist and callPostValueHistmult (deprecated)
  
###v0.3.2 - 11/03/2022
**Added**
- Add filter_installation and filter_tagview as replacement for GetFiltered
- Add README.md

## Contacto <a class="anchor" id="chapter6"></a>
[**Pau Juan**](mailto:pau.juan@nexusintegra.io)
*Operaciones*


[**Laura Moreno**](mailto:laura.moreno@nexusintegra.io)
*Operaciones*


[**Ricardo Gómez**](mailto:ricardo.gomez.aldaravi@nexusintegra.io)
*Operaciones*

[Nexus Integra](https://nexusintegra.io/)