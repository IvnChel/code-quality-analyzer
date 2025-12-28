from analyzer import CodeAnalyzer
import os

def run_main():
    analyzer = CodeAnalyzer()
    # Анализируем сам анализатор для примера
    current_dir = os.path.dirname(__file__)
    target = os.path.join(current_dir, "analyzer.py")
    
    analyzer.analyze_file(target)
    report = analyzer.get_report()
    
    # 1. Выводим в консоль
    print(report)
    
    # 2. Сохраняем в файл (для CI/CD)
    with open("full_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    run_main()