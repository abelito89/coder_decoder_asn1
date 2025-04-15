from pathlib import Path
import gzip
import asn1tools
import re
from typing import Match
import pprint


def open_cdr_binary(ruta_cdr: Path) -> bytes:
    """
    Lee un archivo CDR en modo binario y retorna su contenido en forma de bytes.

    Parámetros:
        ruta_cdr (Path): Ruta al archivo CDR.

    Retorna:
        bytes: Contenido binario del archivo.
    """
    # Abre el archivo CDR en modo binario
    contenido = ruta_cdr.read_bytes()
    return contenido


def descomprimir_contenido_gzip(contenido: bytes) -> bytes:
    """
    Descomprime datos comprimidos en formato gzip.

    Este método intenta descomprimir el contenido proporcionado utilizando la 
    función gzip.decompress. Si la descompresión es exitosa, retorna los datos 
    descomprimidos; en caso de error, imprime un mensaje de error.

    Parámetros:
        contenido (bytes): Datos comprimidos en formato gzip.

    Retorna:
        bytes: Los datos descomprimidos.
    """
    if not contenido.startswith(b'\x1f\x8b'):
        print("Primeros 30 bytes:", contenido[:30].hex())
        print("El contenido no parece estar comprimido en formato gzip. Se utilizará tal cual.")
        return contenido
    try:
        descomprimido_gzip = gzip.decompress(contenido)
        print("Descompresión exitosa")
        return descomprimido_gzip
    except Exception as e:
        print(f"Error al descomprimir: {e}")
        return b""  # Se retorna un bytes vacío en caso de error


def fix_choice_optional(contenido: str) -> str:
    """
    Corrige la sintaxis de bloques CHOICE en la especificación ASN.1.

    Busca bloques definidos como CHOICE en la especificación (contenido comprendido 
    entre 'CHOICE {' y '}') y elimina la palabra 'OPTIONAL' de dichos bloques, ya que en 
    un CHOICE cada alternativa es implícitamente opcional y su presencia puede provocar
    errores en la compilación.

    Parámetros:
        contenido (str): Contenido del archivo de especificación ASN.1.

    Retorna:
        str: El contenido de la especificación con las correcciones aplicadas.
    """
    # Patrón para capturar bloques de CHOICE en notación ASN.1.
    # Se usa re.DOTALL para que el punto incluya saltos de línea.
    pattern = re.compile(r'(CHOICE\s*{.*?})', re.DOTALL)
    
    def reemplazar(match: Match[str]) -> str:
        """
        Función auxiliar para procesar un bloque CHOICE.

        Recibe un objeto match que contiene un bloque CHOICE completo. Dentro del bloque,
        elimina la palabra 'OPTIONAL' (junto con los espacios anteriores) para ajustarlo a
        la sintaxis estándar ASN.1, ya que en un CHOICE cada alternativa es implícitamente 
        opcional.

        Parámetros:
            match: Un objeto match de re que contiene el bloque CHOICE.

        Retorna:
            str: El bloque CHOICE corregido.
        """
        bloque = match.group(1)
        # Elimina la palabra 'OPTIONAL' junto con los espacios anteriores
        bloque_corregido = re.sub(r'\s+OPTIONAL', '', bloque)
        return bloque_corregido

    return pattern.sub(reemplazar, contenido)


def GprsHuaweiEM20_compiler(ruta_GprsHuaweiEM20: Path, descomprimido_gzip: bytes):
    """
    Procesa y decodifica un mensaje codificado en BER utilizando la especificación ASN.1
    de GprsHuaweiEM20.

    Pasos que realiza:
      1. Lee el contenido completo del archivo de especificación ASN.1.
      2. Aplica una corrección en memoria a los bloques CHOICE para eliminar la palabra
         'OPTIONAL', que de lo contrario provocaría errores en la compilación.
      3. Compila la especificación corregida usando asn1tools con la codificación BER.
      4. Decodifica el mensaje BER contenido en 'descomprimido_gzip' utilizando el tipo raíz
         'CallEventRecord'.
      5. Imprime el mensaje decodificado.

    Parámetros:
        ruta_GprsHuaweiEM20 (Path): Ruta al archivo de especificación ASN.1
                                     (por ejemplo, "GprsHuaweiEM20.CallEventRecord").
        descomprimido_gzip (bytes): Datos descomprimidos (mensaje en formato BER)
                                    obtenidos del CDR.

    Retorna:
        None
    """
    # Leer el contenido completo del archivo de especificación ASN.1
    contenido_asn1 = ruta_GprsHuaweiEM20.read_text()
    
    # Aplicar corrección únicamente a los bloques CHOICE
    contenido_corregido = fix_choice_optional(contenido_asn1)
    
    # Compilar la especificación corregida (usando BER)
    spec = asn1tools.compile_string(contenido_corregido, 'ber')
    
    # Decodificar el mensaje BER utilizando el tipo raíz 'CallEventRecord'
    decoded_message = spec.decode('CallEventRecord', descomprimido_gzip)

    # Usar pprint para formatear el mensaje de forma legible
    mensaje_legible = pprint.pformat(decoded_message, indent=4, width=80)

    # Crear la subcarpeta "Decodificados" usando pathlib
    carpeta_salida = Path("Decodificados")
    carpeta_salida.mkdir(exist_ok=True)
    
    # Definir la ruta del archivo de salida dentro de la carpeta
    ruta_archivo_decodificado = carpeta_salida / "CDR_GprsHuaweiEM20.txt"

    # Convertir el mensaje decodificado a cadena y guardarlo en un archivo de texto
    with open(ruta_archivo_decodificado, "w", encoding="utf-8") as f:
        f.write(str(mensaje_legible))


def colector(ruta_local: Path):
    """
    Función que orquesta el flujo completo de procesamiento:
      1. Define las rutas de la especificación ASN.1 y del CDR.
      2. Lee el CDR en modo binario y lo descomprime.
      3. Llama al compilador para corregir y decodificar la especificación ASN.1 junto
         con el mensaje BER.

    Parámetros:
        ruta_local (Path): Ruta local base donde se encuentran los directorios 'CDR' y 
                           'estructuras_ASN1'.

    Retorna:
        None
    """
    ruta_asn1 = ruta_local / "estructuras_ASN1"
    ruta_GprsHuaweiEM20 = ruta_asn1 / "GprsHuaweiEM20.CallEventRecord"
    ruta_cdr = ruta_local / "CDR/APR8AP65_220250311-095846-00000004.dat%3A56079"
    contenido_binario = open_cdr_binary(ruta_cdr)
    try:
        descomprimido_gzip = descomprimir_contenido_gzip(contenido_binario)
        GprsHuaweiEM20_compiler(ruta_GprsHuaweiEM20, descomprimido_gzip)
    except Exception as e:
        print(f"No se pudo colectar: {e}")


ruta_local = Path(".")

if __name__ == "__main__":
    colector(ruta_local)
