#!/bin/bash

set -euo pipefail

# === Configuración ===
export LANG="en_US.UTF-8"
export PYTHONIOENCODING="utf-8"

# Obtener ruta absoluta del directorio donde está este script
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${PROJECT_DIR}/python_env/hgp"
PYTHON_SCRIPT="${PROJECT_DIR}/main.py"
LOG_DIR="${PROJECT_DIR}/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/hgp_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Función para log desde Bash
log_message() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') [bash] $message" | tee -a "$LOG_FILE"
}

# Verificar entorno virtual
if [[ ! -f "${VENV_PATH}/bin/activate" ]]; then
    log_message "Error: No se encontró el entorno virtual en ${VENV_PATH}"
    exit 1
fi

# Activar entorno virtual
# shellcheck disable=SC1090
source "${VENV_PATH}/bin/activate"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    log_message "Error: Falló la activación del entorno virtual."
    exit 1
fi

log_message "Entorno virtual activado: ${VIRTUAL_ENV}"

# Verificar existencia del script Python
if [[ ! -f "${PYTHON_SCRIPT}" ]]; then
    log_message "Error: No se encontró el script Python en ${PYTHON_SCRIPT}"
    exit 1
fi

# Ejecutar script Python con la ruta del archivo de log como argumento
log_message "Ejecutando script Python..."
python "${PYTHON_SCRIPT}" --log-file "${LOG_FILE}"

if [[ $? -eq 0 ]]; then
    log_message "Script Python ejecutado exitosamente."
else
    log_message "Error: Falló la ejecución del script Python."
    exit 1
fi
