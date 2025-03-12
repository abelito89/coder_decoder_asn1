# Prueba de Concepto para la Decodificación de CDR con ASN.1

Este proyecto constituye una **prueba de concepto** (Proof-of-Concept, PoC) para demostrar el proceso de lectura, descompresión y decodificación de archivos CDR (Call Detail Records) utilizando especificaciones ASN.1.  
El objetivo principal es transformar datos crudos —comprimidos y codificados en BER— en una estructura semántica accesible en Python.

Esta iniciativa se plantea como un paso preliminar en el contexto de soluciones de mediación para sistemas de telecomunicaciones, enfocándose en el procesamiento y la interpretación de los datos recibidos.

---

## Descripción General

El flujo implementado en este PoC sigue los siguientes pasos:

1. **Lectura del CDR:**  
   Se lee el archivo en formato binario desde el sistema de archivos, ubicado en el directorio `CDR/`.

2. **Descompresión:**  
   Los datos leídos se descomprimen utilizando `gzip` para obtener el mensaje en formato BER.

3. **Corrección de la Especificación ASN.1:**  
   La especificación ASN.1, que se encuentra en el directorio `estructuras_ASN1/` (archivo `GprsHuaweiEM20.CallEventRecord`), contiene detalles no estándar (por ejemplo, el uso de `OPTIONAL` en bloques `CHOICE`).  
   Se aplica una transformación en memoria para corregir estas inconsistencias sin modificar el archivo original.

4. **Compilación y Decodificación:**  
   Se compila la especificación corregida utilizando la librería `asn1tools` con codificación BER, y se decodifica el mensaje, obteniendo así una estructura semántica (una tupla en la que el primer elemento indica la alternativa del CHOICE y el segundo un diccionario con los campos del registro).

---

## Características

- **Lectura y Descompresión:**  
  El proyecto permite abrir archivos CDR comprimidos, leerlos en modo binario y descomprimirlos utilizando `gzip`.

- **Corrección Automática de la Especificación:**  
  Se aplica una función de corrección que detecta bloques definidos como `CHOICE` y elimina la palabra `OPTIONAL` innecesaria, adaptando la especificación a la sintaxis ASN.1 estándar para permitir su compilación.

- **Decodificación del Mensaje BER:**  
  Con la especificación ASN.1 corregida, se utiliza `asn1tools` para compilar y decodificar el mensaje BER, transformándolo en una estructura de datos en Python que puede ser utilizada para posteriores análisis o transformaciones.

- **Contexto de Aplicación:**  
  Aunque la idea de mediación se encuentra en estudio, esta versión se centra exclusivamente en el proceso de decodificación y procesamiento de CDRs, sirviendo como base para desarrollos futuros.

---

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```
coder_decoder_asn1/
├── README.md
├── requirements.txt
├── .gitignore
├── functions.py
├── CDR/
│   ├── cdr1
│   ├── ...
│   └── cdrn
├── estructuras_ASN1/
│   └── GprsHuaweiEM20.CallEventRecord
└── venv_coder_asn1/
```

- **README.md:**  
  La documentación y descripción del proyecto.

- **requirements.txt:**  
  Lista de dependencias (actualmente, se requiere al menos `asn1tools`).

- **.gitignore:**  
  Archivos y directorios a excluir de Git (incluye `venv_coder_asn1/`, `CDR/` y `CDR_txt/`).

- **functions.py:**  
  Contiene el código Python que implementa:
  - Lectura del archivo CDR en modo binario.
  - Descompresión de archivos gzip.
  - Corrección de bloques `CHOICE` en la especificación ASN.1.
  - Compilación de la especificación y decodificación del mensaje BER.

- **CDR/**  
  Directorio que contiene los CDRs de entrada (ejemplos: `cdr1`, `cdr2`, ..., `cdrn`).

- **estructuras_ASN1/**  
  Directorio que contiene la especificación ASN.1 utilizada (archivo `GprsHuaweiEM20.CallEventRecord`).

- **venv_coder_asn1/**  
  Directorio del entorno virtual de Python.

---

## Requisitos

- **Python 3.7 o superior**
- Dependencias (definidas en `requirements.txt`):
  - `asn1tools`

---

## Instalación y Ejecución

### Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/abelito89/coder_decoder_asn1.git
   cd coder_decoder_asn1
   ```

2. **Crea y activa un entorno virtual (recomendado):**

   ```bash
   python -m venv venv_coder_asn1
   # En Linux/macOS:
   source venv_coder_asn1/bin/activate
   # En Windows:
   venv_coder_asn1\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
py functions.py
# En Windows
```

Esto iniciará el proceso:
- Lectura y descompresión del archivo CDR.
- Corrección en memoria de la especificación ASN.1.
- Compilación y decodificación del mensaje BER, mostrando el resultado en la salida estándar.

---

## Conclusión

Este proyecto presenta un proceso automatizado para la decodificación de CDRs utilizando una especificación ASN.1 que ha sido corregida en memoria para adherirse al estándar.  
Es una prueba de concepto diseñada para demostrar la transformación de datos crudos en estructuras semánticas en Python, proporcionando una base para futuras exploraciones e integraciones en el ámbito de telecomunicaciones.