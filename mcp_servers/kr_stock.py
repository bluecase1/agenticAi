# mcp_servers/kr_stock.py
import sys
import io
from types import ModuleType

# Fix Windows console encoding for Korean characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 1. pkg_resources가 없거나 망가져 있을 경우를 대비한 완전한 목킹(Mocking)
try:
    import pkg_resources
    if not hasattr(pkg_resources, 'resource_filename'):
        raise ImportError
except (ImportError, AttributeError):
    # 가짜 pkg_resources 모듈 생성
    m = ModuleType("pkg_resources")
    # pykrx가 내부적으로 호출하는 함수들을 빈 함수로 정의
    m.resource_filename = lambda pkg, res: "" 
    m.Requirement = lambda x: None
    m.get_distribution = lambda x: None
    sys.modules["pkg_resources"] = m
    print("[Python 3.14] pkg_resources patched")

from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
from pykrx import stock

# 1. FastMCP 서버 초기화
mcp = FastMCP("KR-Stock-Server")

@mcp.tool()
def get_kr_stock_price(ticker_name: str) -> str:
    # 1. 영업일 데이터를 찾기 위해 날짜를 뒤로 돌리며 시도합니다.
    search_date = datetime.now()
    tickers = None
    
    # 최대 7일 전까지 뒤져서 데이터가 있는 날을 찾습니다.
    for _ in range(7):
        today_str = search_date.strftime("%Y%m%d")
        try:
            tickers = stock.get_market_ticker_list(today_str, market="ALL")
            if len(tickers) > 0:
                break
        except:
            search_date -= timedelta(days=1)
            continue
        search_date -= timedelta(days=1)

    if not tickers:
        return "최근 영업일 데이터를 가져올 수 없습니다. 거래소 서버 상태를 확인하세요."

    # 2. 종목명으로 티커 찾기
    found_ticker = None
    for ticker in tickers:
        name = stock.get_market_ticker_name(ticker)
        if name == ticker_name:
            found_ticker = ticker
            break
            
    if not found_ticker:
        return f"'{ticker_name}'에 해당하는 종목을 찾지 못했습니다."

    # 3. 데이터 수집 (마지막 영업일 기준)
    df = stock.get_market_ohlcv(today_str, today_str, found_ticker)
    
    if df.empty:
        return f"{ticker_name}({found_ticker})의 {today_str} 주가 데이터가 없습니다."

    current_price = df['종가'].iloc[0]
    change_rate = df['등락률'].iloc[0]
    
    return f"기준일: {today_str} | {ticker_name}({found_ticker}) 현재가: {current_price}원 (등락률: {change_rate}%)"

if __name__ == "__main__":
    mcp.run()