# functions.py
import logging
import pandas as pd
from typing import List
import os

# Logger global
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

def configurar_logger(log_file_path: str):
    """
    Configura el logger global con el archivo y consola.
    Esta función debe ser llamada antes de usar print_log.
    """
    # Evitar múltiples handlers si se llama más de una vez
    if logger.handlers:
        return

    formatter = logging.Formatter('%(asctime)s [python] %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def print_log(message: str, level: str = "info"):
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)

def get_required_columns() -> List[str]:
    """
    Retorna la lista de columnas requeridas para el CSV.
    
    Returns:
        List[str]: Lista de nombres de columnas
    """
    return [
        "sociedadCod", "sociedadNom", "cproCod", "cproNom",
        "tipoMaquinaCod", "tipoMaquinaNom", "maquinaCod",
        "maquinaNom", "cPsRelacionadosCod", "cPsRelacionadosNom",
        "utmx", "utmy", "utmz", "numMaquinas", "potencia", "modeloParque"
    ]

def validate_csv_structure(df: pd.DataFrame) -> bool:
    """
    Valida que el DataFrame tenga todas las columnas requeridas.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        
    Returns:
        bool: True si la estructura es válida, False en caso contrario
    """
    required_columns = get_required_columns()
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print_log(f"Columnas faltantes: {', '.join(missing_columns)}", level="error")
        return False
    return True

def check_null_values(df: pd.DataFrame) -> None:
    """
    Analiza y reporta los valores nulos en el DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
    """
    null_counts = df.isnull().sum()
    columns_with_nulls = null_counts[null_counts > 0]
    
    if columns_with_nulls.empty:
        print_log("No se encontraron valores nulos en el dataset")
    else:
        print_log("Resumen de valores nulos por columna:")
        for column, count in columns_with_nulls.items():
            print_log(f"- {column}: {count} valores nulos")

def procesar_datos(csv_path: str = "datos.csv") -> None:
    """
    Procesa el archivo CSV, validando su estructura y analizando valores nulos.
    
    Args:
        csv_path (str): Ruta al archivo CSV a procesar
        
    Raises:
        FileNotFoundError: Si el archivo CSV no existe
        ValueError: Si el archivo no tiene la estructura correcta
        Exception: Para otros errores durante el procesamiento
    """
    try:
        print_log("Iniciando procesamiento de datos")
        
        # Verificar existencia del archivo
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")
        
        # Cargar el CSV
        print_log(f"Leyendo archivo: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Validar estructura
        if not validate_csv_structure(df):
            raise ValueError("El archivo CSV no tiene la estructura requerida")
        
        # Analizar valores nulos
        print_log("Analizando valores nulos...")
        check_null_values(df)
        
        print_log("Procesamiento de datos completado correctamente")
        
    except FileNotFoundError as e:
        print_log(str(e), level="error")
        raise
    except Exception as e:
        print_log(f"Error durante el procesamiento: {str(e)}", level="error")
        raise
