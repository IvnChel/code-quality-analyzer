import ast
import os

class CodeAnalyzer:
    def __init__(self):
        self.metrics = {
            "total_lines": 0,
            "functions_count": 0,
            "complexity": 0,
            "docstrings_count": 0,
            "pep8_issues": 0,
            "recommendations": []
        }
        self.report_data = []

    def analyze_file(self, filepath):
        self.report_data.append(f"\n{'='*30}")
        self.report_data.append(f"АНАЛИЗ ФАЙЛА: {os.path.basename(filepath)}")
        self.report_data.append(f"{'='*30}\n")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            self.metrics["total_lines"] = len(content.splitlines())
        
        tree = ast.parse(content)
        self._analyze_node(tree)
        self._check_duplicates(filepath)
        self._generate_recommendations()

        m = self.metrics
        self.report_data.append(f"Строк кода: {m['total_lines']}")
        self.report_data.append(f"Функций: {m['functions_count']}")
        self.report_data.append(f"Сложность: {m['complexity']}")
        self.report_data.append(f"Docstrings: {m['docstrings_count']}/{m['functions_count']}")
        self.report_data.append("\nРЕКОМЕНДАЦИИ:")
        self.report_data.extend(m["recommendations"])
        self.report_data.append("-" * 30)

        return self.metrics

    def analyze_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self.analyze_file(full_path)

    def _analyze_node(self, tree):
        for node in ast.walk(tree):
            # 1. Считаем функции и Docstrings
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.metrics["functions_count"] += 1
                if ast.get_docstring(node):
                    self.metrics["docstrings_count"] += 1
                
                # 2. Базовая проверка PEP 8 (имена функций в snake_case)
                if not node.name.islower() and "_" not in node.name:
                    self.metrics["pep8_issues"] += 1

                # 3. Цикломатическая сложность (упрощенно: кол-во ветвлений)
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                        self.metrics["complexity"] += 1

    def _generate_recommendations(self):
        """Генерация отчета с рекомендациями (пункт ТЗ)"""
        m = self.metrics
        
        if m["functions_count"] > 0 and m["docstrings_count"] / m["functions_count"] < 0.8:
            m["recommendations"].append("- Добавьте docstrings (описания) ко всем функциям.")
        
        if m["complexity"] > 10:
            m["recommendations"].append("- Слишком высокая сложность. Разбейте большие функции на мелкие.")
            
        if m["pep8_issues"] > 0:
            m["recommendations"].append("- Используйте snake_case для именования функций (например, my_function).")
            
        if m["total_lines"] > 100:
            m["recommendations"].append("- Файл слишком длинный. Рассмотрите возможность разделения на модули.")

        if not m["recommendations"]:
            m["recommendations"].append("- Код выглядит отлично! Замечаний нет.")

    def _check_duplicates(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) != len(set(lines)):
            self.metrics["recommendations"].append("- Обнаружены дублирующиеся строки кода. Проверьте на copy-paste.")

    def get_report(self):
        """Просто возвращает всё, что мы насобирали в report_data"""
        if not self.report_data:
            return "Отчет пуст. Файлы не найдены или не проанализированы."

        header = "=== ИТОГОВЫЙ ОТЧЕТ О КАЧЕСТВЕ КОДА ===\n"
        return header + "\n".join(self.report_data)
