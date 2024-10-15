import os
from pathlib import Path
import shutil
import sys

def copy_file(source: Path, destination: Path) -> None:
    file_destination = destination / os.path.splitext(source.name)[1][1:] / str(source).replace("\\", "_") # для файлів з одинаковим іменем
    os.makedirs(os.path.dirname(file_destination), exist_ok=True)
    try:
        shutil.copyfile(source, file_destination)
        print(source, " скопійовано до ", file_destination)
    except PermissionError:
        print(f"Файл '{source}' не може бути скопійований, доступ заборонено.")

def sort_directory(source: Path, destination: Path) -> None:
    if source.is_dir():
        for child in sorted(source.iterdir(), key=lambda x: ("0" if x.is_dir() else "1") + x.name):
            if child.is_dir():
                sort_directory(child, destination)
            else:
                copy_file(child, destination)

if __name__ == "__main__":
    n = len(sys.argv)
    if n < 2:
        print("Шлях до вихідної директорії не заданий.")
    else:
        source, destination = Path(sys.argv[1]), Path(sys.argv[2] if n >= 3 else "dist")
        os.makedirs(destination, exist_ok=True)
        if os.access(source, os.R_OK):
            if os.access(destination, os.W_OK):
                if source.is_dir():
                    sort_directory(source, destination)
                else:
                    print("Вихідний шлях не є директорією.")
            else:
                print(f"Доступ до директорії призначення заборонено.")
        else:
            print(f"Доступ до вихідної директорії заборонено.")

