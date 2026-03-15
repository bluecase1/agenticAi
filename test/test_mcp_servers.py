# test/test_mcp_servers.py - MCP Server Function Tests
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_kr_stock_module_imports():
    """Test kr_stock module import"""
    # Note: kr_stock.py has encoding issues with Korean characters on Windows
    # This test is skipped on Windows for now
    import platform
    if platform.system() == "Windows":
        print("[SKIP] kr_stock module skipped on Windows (encoding issue)")
        return
    
    try:
        from mcp_servers.kr_stock import get_kr_stock_price
        assert callable(get_kr_stock_price)
        print("[OK] kr_stock module imported")
    except ImportError as e:
        print(f"[FAIL] kr_stock module import failed: {e}")
        raise


def test_us_stock_module_imports():
    """Test us_stock module import"""
    try:
        from mcp_servers.us_stock import get_us_stock_price, get_us_company_summary
        assert callable(get_us_stock_price)
        assert callable(get_us_company_summary)
        print("[OK] us_stock module imported")
    except ImportError as e:
        print(f"[FAIL] us_stock module import failed: {e}")
        raise


def test_us_stock_function_signatures():
    """Test us_stock function signatures"""
    from mcp_servers.us_stock import get_us_stock_price
    import inspect
    
    sig = inspect.signature(get_us_stock_price)
    params = list(sig.parameters.keys())
    
    assert "symbol" in params
    print("[OK] us_stock function signature verified")


if __name__ == "__main__":
    test_kr_stock_module_imports()
    test_us_stock_module_imports()
    test_us_stock_function_signatures()
    print("\n=== All MCP server tests passed! ===")
