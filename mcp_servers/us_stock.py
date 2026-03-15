# mcp_servers/us_stock.py
from mcp.server.fastmcp import FastMCP
import yfinance as yf

# 1. FastMCP 서버 초기화
mcp = FastMCP("US-Stock-Server")

@mcp.tool()
def get_us_stock_price(symbol: str) -> str:
    """
    미국 주식 티커(Symbol)를 입력받아 현재 주가와 지표를 반환합니다.
    미국 주식은 반드시 티커 형태로 입력해야 합니다. (예: Apple -> 'AAPL', Nvidia -> 'NVDA')
    
    Args:
        symbol (str): 미국의 주식 티커 (예: 'TSLA', 'MSFT', 'GOOGL')
    """
    try:
        # 티커 정보를 통해 주식 객체 생성
        ticker = yf.Ticker(symbol)
        
        # 실시간 가격 정보 (fast_info 사용)
        info = ticker.fast_info
        current_price = info.last_price
        
        # 전일 종가 대비 변동 계산
        prev_close = info.previous_close
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100
        
        currency = info.currency # 보통 'USD'
        
        return (f"{symbol}의 현재 주가: {current_price:.2f} {currency} "
                f"(변동: {change:+.2f}, {change_percent:+.2f}%)")
                
    except Exception as e:
        return f"티커 '{symbol}'를 분석하는 중 오류가 발생했습니다: {str(e)}"

@mcp.tool()
def get_us_company_summary(symbol: str) -> str:
    """
    미국 기업의 티커를 입력받아 기업의 사업 개요를 요약하여 반환합니다.
    에이전트가 해당 기업이 무엇을 하는 회사인지 모를 때 사용합니다.
    """
    ticker = yf.Ticker(symbol)
    summary = ticker.info.get('longBusinessSummary', '정보가 없습니다.')
    return f"{symbol} 기업 요약: {summary[:300]}..." # 너무 길면 LLM 토큰을 많이 쓰므로 자릅니다.

if __name__ == "__main__":
    mcp.run()