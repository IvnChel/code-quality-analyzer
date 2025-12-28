import os
from analyzer import CodeAnalyzer

def run_main():
    analyzer = CodeAnalyzer()
    
    # Определяем путь к папке data относительно текущего файла
    # Это позволит коду работать и у тебя на ПК, и на сервере GitHub
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    target_folder = os.path.join(project_root, "data")
    
    # Проверяем, существует ли папка, чтобы не было ошибок
    if os.path.exists(target_folder):
        print(f"Анализируем папку: {target_folder}")
        analyzer.analyze_folder(target_folder)
    else:
        # Если папки data нет (например, запуск только из src), анализируем текущую директорию
        print(f"Папка data не найдена, анализируем: {current_dir}")
        analyzer.analyze_folder(current_dir)
    
    report = analyzer.get_report()
    
    # 1. Выводим в консоль (чтобы видеть в логах GitHub Actions)
    print(report)
    
    # 2. Сохраняем в файл (этот файл подхватит GitHub Artifacts)
    with open("full_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n✅ Анализ завершен. Отчет сохранен в full_report.txt")

if __name__ == "__main__":
    run_main()
