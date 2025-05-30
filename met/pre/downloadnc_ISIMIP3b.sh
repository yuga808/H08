#!/bin/bash

LIST_FILE="../pre/ISIMIP3b_ssp126.txt"
OUT_DIR="../org/ISIMIP"
LOG_FILE="download_success.log"
ERR_FILE="download_failed.log"

mkdir -p "$OUT_DIR"
: > "$LOG_FILE"     # empty the success log
: > "$ERR_FILE"     # empty the error log

while IFS= read -r URL || [[ -n "$URL" ]]; do
    CLEAN_URL=$(echo "$URL" | tr -d '\r')
    FILE_NAME=$(basename "$CLEAN_URL")

    echo "Downloading: $CLEAN_URL"
    wget -c -P "$OUT_DIR" "$CLEAN_URL"

    if [[ $? -eq 0 ]]; then
        echo "$FILE_NAME" >> "$LOG_FILE"
    else
        echo "$CLEAN_URL" >> "$ERR_FILE"
    fi
done < "$LIST_FILE"
