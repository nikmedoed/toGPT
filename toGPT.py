import os
import sys
import pyperclip

exclude = {
    "__pycache__",
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "package-lock.json",
    ".gitignore",
    "Cargo.lock",
    "target",
    ".venv",
    "build",
    "dist",
}

def generate_directory_structure(paths):
    # Собираем все пути файлов и директорий для корректного определения общего префикса
    all_paths = []
    for path in paths:
        if os.path.isfile(path):
            all_paths.append(os.path.abspath(path))
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in exclude]
                all_paths.append(os.path.abspath(root))
                for file_name in files:
                    if file_name not in exclude:
                        file_path = os.path.join(root, file_name)
                        all_paths.append(os.path.abspath(file_path))
        else:
            continue  # Игнорируем пути, которые не существуют

    if not all_paths:
        print("Не найдено допустимых файлов или директорий.")
        return ""

    common_prefix = os.path.commonpath(all_paths)
    structure = []

    # Используем набор для отслеживания уже добавленных директорий и файлов
    added_paths = set()

    for path in sorted(all_paths):
        relative_path = os.path.relpath(path, common_prefix)
        parts = relative_path.split(os.sep)
        for i in range(len(parts)):
            sub_path = os.sep.join(parts[:i+1])
            if sub_path not in added_paths:
                indent = ' ' * 4 * i
                full_sub_path = os.path.join(common_prefix, sub_path)
                if os.path.isdir(full_sub_path):
                    structure.append(f"{indent}|-- {parts[i]}/")
                else:
                    structure.append(f"{indent}|-- {parts[i]}")
                added_paths.add(sub_path)

    return "\n".join(structure)

def read_files(paths):
    # Чтение файлов по заданным путям
    all_files = []
    for path in paths:
        if os.path.isfile(path):
            all_files.append(os.path.abspath(path))
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in exclude]
                for file_name in files:
                    if file_name not in exclude:
                        file_path = os.path.join(root, file_name)
                        all_files.append(os.path.abspath(file_path))
        else:
            continue  # Игнорируем несуществующие пути

    if not all_files:
        print("Не найдено допустимых файлов.")
        return ""

    common_prefix = os.path.commonpath(all_files)
    result = []

    for file_path in sorted(all_files):
        result.append(read_single_file(file_path, common_prefix))

    return "\n\n".join(result)

def _read_file_with_fallback(file_path):
    """Read file trying several encodings."""
    encodings = ["utf-8", "utf-8-sig", "utf-16", "cp1251"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception:
            # Other errors (e.g., file not found) should propagate
            raise

    # As a last resort read as bytes and decode replacing errors
    with open(file_path, "rb") as f:
        data = f.read()
    return data.decode("utf-8", errors="replace")


def read_single_file(file_path, common_prefix):
    try:
        content = _read_file_with_fallback(file_path)
    except Exception as e:
        content = f"Ошибка чтения файла: {e}"

    relative_path = os.path.relpath(file_path, common_prefix)
    separator = "=" * 10 + f" {relative_path} " + "=" * 10
    return f"{separator}\n{content}"

def main():
    # Считываем аргументы командной строки
    args = sys.argv[1:]
    paths = [arg for arg in args if not arg.startswith('-')]

    if not paths:
        print("Не указаны пути для обработки.")
        return

    only_structure = '-s' in args
    only_code = '-c' in args

    if only_structure:
        directory_structure = generate_directory_structure(paths)
        pyperclip.copy(directory_structure)
        print("Структура директорий скопирована в буфер обмена.")
    elif only_code:
        formatted_content = read_files(paths)
        pyperclip.copy(formatted_content)
        print("Содержимое файлов скопировано в буфер обмена.")
    else:
        directory_structure = generate_directory_structure(paths)
        formatted_content = read_files(paths)
        final_output = f"# СТРУКТУРА СВЯЗАННЫХ ФАЙЛОВ:\n{directory_structure}\n\nСОДЕРЖИМОЕ ФАЙЛОВ:\n{formatted_content}"
        pyperclip.copy(final_output)
        print("Содержимое структуры директорий и файлов скопировано в буфер обмена.")

if __name__ == "__main__":
    main()
