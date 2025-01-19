import os

def count_code_lines(directory, extensions=None, exclude_dirs=None):
    
    total_lines = 0
    file_count = 0
    details = []

    exclude_dirs = exclude_dirs or []

    
    for root, dirs, files in os.walk(directory):
        
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            
            if extensions is None or os.path.splitext(file)[1] in extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)  
                        total_lines += line_count
                        file_count += 1
                        details.append((file_path, line_count))
                except Exception as e:
                    print(f"Не удалось прочитать файл {file_path}: {e}")

    return total_lines, file_count, details



if __name__ == "__main__":
    directory = os.getcwd()  
    extensions = ['.py']  
    exclude_dirs = ['.venv', '__pycache__']  

    total_lines, file_count, details = count_code_lines(directory, extensions, exclude_dirs)

    print(f"Общее количество строк: {total_lines}")
    print(f"Количество файлов: {file_count}")
    print("Подробности:")
    for file_path, line_count in details:
        print(f"{file_path}: {line_count} строк")
import os
import re


def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    
    code = re.sub(r'

    
    code = re.sub(r'\'\'\'(.*?)\'\'\'', '', code, flags=re.DOTALL)
    code = re.sub(r'\"\"\"(.*?)\"\"\"', '', code, flags=re.DOTALL)

    
    return code


def remove_comments_from_project(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'Обрабатывается: {file_path}')

                
                cleaned_code = remove_comments_from_file(file_path)

                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_code)


project_directory = 'C:/Users/aroki/PycharmProjects/EchoesOfTime'
remove_comments_from_project(project_directory)