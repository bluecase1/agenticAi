# mcp_servers/kr_stock.py
from mcp.server.fastmcp import FastMCP
from pykrx import stock
import datetime

# 1. FastMCP 서버 초기화
mcp = FastMCP("KR-Stock-Server")

@mcp.tool()
def get_kr_stock_price(ticker_name: str) -> str:
    """
    한국 주식 종목명을 입력받아 현재 주가와 등락률을 반환합니다.
    예: '삼성전자', 'SK하이닉스'
    """
    # 오늘 날짜 설정
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    # 종목명을 티커(숫자 코드)로 변환
    # (실무에서는 더 정교한 검색이 필요하지만, 실습용으로 가장 유사한 것 선택)
    tickers = stock.get_market_ticker_list(today, market="ALL")
    
    target_ticker = None
    for t in tickers:
        name = stock.get_market_ticker_name(t)
        if ticker_name in name:
            target_ticker = t
            break
            
    if not target_ticker:
        return f"'{ticker_name}'에 해당하는 종목을 찾지 못했습니다."

    # 주가 정보 가져오기
    df = stock.get_market_ohlcv_by_date(today, today, target_ticker)
    
    if df.empty:
        return f"{ticker_name}의 오늘 데이터를 불러올 수 없습니다. (장 개시 전일 수 있음)"

    price = df['종가'].iloc[0]
    change_rate = df['등락률'].iloc[0]
    
    return f"{ticker_name}({target_ticker})의 현재 주가: {price:,.0f}원 (등락률: {change_rate:.2f}%)"

if __name__ == "__main__":
    mcp.run()