#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "{BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$PROJECT_DIR/pipeline.log"

VENV_PYTHON=$PROJECT_DIR/venv/bin/python3


handle_error() {
	echo " === Pipeline FAILED at $(date) ===" >> "$LOG_FILE"
	exit 1
}
echo "=== Initiating the Pipeline: $(date) ===" >> "$LOG_FILE"



echo "Executing ingestion layer..." >> "$LOG_FILE"
"$VENV_PYTHON" "$PROJECT_DIR/extract.py" >> "$LOG_FILE" 2>&1



echo "Executing Transformation Layer..." >> "$LOG_FILE"
"$VENV_PYTHON" "$PROJECT_DIR/transform.py" >> "$LOG_FILE" 2>&1


echo "Executing database Load..." >> "$LOG_FILE"
"$VENV_PYTHON" "$PROJECT_DIR/load.py" >> "$LOG_FILE" 2>&1


echo "=== Pipeline completed successfully: ($date) ===" >> "$LOG_FILE"
echo "-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" >> "$LOG_FILE"


