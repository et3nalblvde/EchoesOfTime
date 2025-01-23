import os

def count_code_lines(directory, extensions=None, exclude_dirs=None):
    """
    Считает строки кода в файлах с заданными расширениями, исключая определённые директории.

    :param directory: Путь к директории для подсчёта строк.
    :param extensions: Список расширений файлов для подсчёта (например, ['.py']).
                       Если None, то учитываются все файлы.
    :param exclude_dirs: Список директорий, которые нужно исключить (например, ['venv']).
    :return: Общее количество строк, количество файлов и подробности по каждому файлу.
    """
    total_lines = 0
    file_count = 0
    details = []

    exclude_dirs = exclude_dirs or []

    # Рекурсивно обходим директорию
    for root, dirs, files in os.walk(directory):
        # Исключаем директории из обхода
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            # Проверяем расширение файла, если указано
            if extensions is None or os.path.splitext(file)[1] in extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)  # Считаем строки в файле
                        total_lines += line_count
                        file_count += 1
                        details.append((file_path, line_count))
                except Exception as e:
                    print(f"Не удалось прочитать файл {file_path}: {e}")

    return total_lines, file_count, details


# Использование
if __name__ == "__main__":
    directory = os.getcwd()  # Текущая директория
    extensions = ['.py']  # Считать только Python-файлы
    exclude_dirs = ['.venv', '__pycache__']  # Исключить venv и __pycache__

    total_lines, file_count, details = count_code_lines(directory, extensions, exclude_dirs)

    print(f"Общее количество строк: {total_lines}")
    print(f"Количество файлов: {file_count}")
    print("Подробности:")
    for file_path, line_count in details:
        print(f"{file_path}: {line_count} строк")
import os
import re

# Функция для удаления комментариев из файла
def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # Удаляем однострочные комментарии (начинаются с #)
    code = re.sub(r'#.*', '', code)

    # Удаляем многострочные комментарии (между ''' или """ и его концом)
    code = re.sub(r'\'\'\'(.*?)\'\'\'', '', code, flags=re.DOTALL)
    code = re.sub(r'\"\"\"(.*?)\"\"\"', '', code, flags=re.DOTALL)

    # Возвращаем очищенный код
    return code

# Функция для обработки всех файлов в проекте
def remove_comments_from_project(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Рассматриваем только Python файлы
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'Обрабатывается: {file_path}')

                # Убираем комментарии из файла
                cleaned_code = remove_comments_from_file(file_path)

                # Перезаписываем файл очищенным кодом
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_code)

# Укажите путь к корню вашего проекта
project_directory = 'C:/Users/aroki/PycharmProjects/EchoesOfTime'
remove_comments_from_project(project_directory)