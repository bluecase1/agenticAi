# test/test_nodes.py - LangGraph Node Structure Tests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_nodes_directory_exists():
    """Check if nodes directory exists"""
    nodes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nodes")
    assert os.path.isdir(nodes_dir)
    print("[OK] nodes directory exists")


def test_identifier_file_exists():
    """Check if identifier.py exists"""
    identifier_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "identifier.py"
    )
    assert os.path.isfile(identifier_path)
    print("[OK] identifier.py exists")


def test_researcher_file_exists():
    """Check if researcher.py exists"""
    researcher_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "researcher.py"
    )
    assert os.path.isfile(researcher_path)
    print("[OK] researcher.py exists")


def test_analyst_file_exists():
    """Check if analyst.py exists"""
    analyst_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "analyst.py"
    )
    assert os.path.isfile(analyst_path)
    print("[OK] analyst.py exists")


def test_identifier_has_node_function():
    """Check if identifier.py contains identifier_node function"""
    identifier_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "identifier.py"
    )
    with open(identifier_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "def identifier_node" in content
    print("[OK] identifier_node function exists in identifier.py")


def test_researcher_has_node_function():
    """Check if researcher.py contains researcher_node function"""
    researcher_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "researcher.py"
    )
    with open(researcher_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "def researcher_node" in content
    print("[OK] researcher_node function exists in researcher.py")


def test_analyst_has_node_function():
    """Check if analyst.py contains analyst_node function"""
    analyst_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "nodes", "analyst.py"
    )
    with open(analyst_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "def analyst_node" in content
    print("[OK] analyst_node function exists in analyst.py")


if __name__ == "__main__":
    test_nodes_directory_exists()
    test_identifier_file_exists()
    test_researcher_file_exists()
    test_analyst_file_exists()
    test_identifier_has_node_function()
    test_researcher_has_node_function()
    test_analyst_has_node_function()
    print("\n=== All node structure tests passed! ===")
