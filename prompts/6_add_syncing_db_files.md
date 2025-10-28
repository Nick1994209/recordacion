### Добавь синхронизациюю db файлов и одной папки в другую

1. добавь скрипт background-sync-folders.sh
```bash
#!/bin/bash

# === Проверка аргументов ===
if [ "$#" -ne 2 ]; then
    echo "Передан только 1 или меньше аргументов, скрипт не будет синхронизировать данные"
    echo "Использование: $0 <SOURCE_DIR> <TARGET_DIR>"
    echo "Пример: $0 /путь/к/источнику /путь/к/цели"
    exit 0
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

# === Вспомогательная функция: есть ли обычные файлы в директории? ===
has_files() {
    local dir="$1"
    [ -d "$dir" ] || return 1
    for f in "$dir"/*; do
        [ -e "$f" ] && [ -f "$f" ] && return 0
    done
    return 1
}

# === Функция однократной синхронизации: SOURCE → TARGET ===
sync_once() {
    local src="$1"
    local tgt="$2"
    for f in "$src"/*; do
        [ -e "$f" ] || continue
        if [ -f "$f" ]; then
            cp "$f" "$tgt/"
        fi
    done
}

# === Инициализация ===
mkdir -p "$SOURCE_DIR" "$TARGET_DIR"

if ! has_files "$SOURCE_DIR"; then
    if has_files "$TARGET_DIR"; then
        echo "SOURCE_DIR пуста — копирую из TARGET_DIR..."
        sync_once "$TARGET_DIR" "$SOURCE_DIR"
        echo "SOURCE_DIR восстановлена."
    else
        echo "Обе директории пусты."
    fi
else
    echo "SOURCE_DIR содержит данные — используем как источник."
fi

# === Запуск бесконечной синхронизации в фоне ===
(
    while true; do
        sync_once "$SOURCE_DIR" "$TARGET_DIR"
        sleep 5
    done
) &

echo "Скрипт завершил инициализацию. Синхронизация работает в фоне."
```

Этот скрипт добавь в entrypoint.sh и запусти его перед выполнением миграции
./entrypoint.sh /app/db $MOUNTED_DB_FOLDER
