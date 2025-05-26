"""
Módulo principal para la aplicación de Procesamiento de Datos HGP de Acciona.

Este módulo gestiona la ejecución principal del proceso ETL para datos HGP de Acciona,
incluyendo la configuración de logs y el manejo de excepciones.
"""

import argparse
import logging
import sys
import traceback
from typing import NoReturn
from hgp.functions import print_log, procesar_datos, configurar_logger


def parse_arguments() -> argparse.Namespace:
    """
    Configura y procesa los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Objeto con los argumentos procesados
    """
    parser = argparse.ArgumentParser(
        description='Procesamiento de Datos HGP de Acciona'
    )
    parser.add_argument(
        '--log-file',
        required=True,
        help='Ruta del archivo de log',
        type=str
    )
    return parser.parse_args()


def run_process() -> None:
    """
    Ejecuta el proceso principal de la aplicación.
    
    Raises:
        Exception: Cualquier excepción no manejada durante el proceso
    """

    files = [
        "/usr/share/ssadata/csv_HGP/files/maquinas.csv"
    ]
    print_log("Iniciando ejecución del script.")

    for csv_file in files:
        print_log(f"Procesando archivo: {csv_file}")
        procesar_datos(csv_path=csv_file)
        
    print_log("Ejecución completada exitosamente.")


def main() -> NoReturn:
    """
    Función principal que coordina la ejecución del programa.
    """
    args = parse_arguments()
    configurar_logger(args.log_file)

    try:
        run_process()
    except Exception as e:
        print_log(str(e), level="error")
        print_log(traceback.format_exc(), level="error")
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()