import pytest
import os
from src.analyzer import CodeAnalyzer

@pytest.fixture
def sample_file(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test_code.py"
    # Код с 1 функцией, 1 docstring и 1 ветвлением (if)
    content = """
def test_func():
    '''Docstring exists'''
    if True:
        pass
"""
    p.write_text(content)
    return str(p)

def test_analyze_metrics(sample_file):
    analyzer = CodeAnalyzer()
    metrics = analyzer.analyze_file(sample_file)
    
    assert metrics["functions_count"] == 1
    assert metrics["docstrings_count"] == 1
    assert metrics["complexity"] == 1  # 1 за наличие 'if'

def test_recommendations_logic(sample_file):
    analyzer = CodeAnalyzer()
    metrics = analyzer.analyze_file(sample_file)
    
    # Проверяем, что рекомендации — это список
    assert isinstance(metrics["recommendations"], list)
    assert len(metrics["recommendations"]) > 0

def test_file_not_found():
    analyzer = CodeAnalyzer()
    with pytest.raises(FileNotFoundError):
        analyzer.analyze_file("non_existent_file_123.py")