from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 1. 대화 기록: 이전 메시지들을 리스트로 관리 (add_messages는 새 메시지를 기존 리스트에 추가함)
    messages: Annotated[List[Dict[str, Any]], add_messages]
    
    # 2. 시장 분류: 'KR' (한국), 'US' (미국), 'BOTH', 'UNKNOWN'
    market: str
    
    # 3. 주가 데이터: MCP 서버로부터 가져온 원본 데이터를 저장
    stock_data: Dict[str, Any]
    
    # 4. 뉴스 데이터: 수집된 뉴스 기사 및 심리 분석 결과 저장
    news_content: List[Dict[str, Any]]
    
    # 5. 최종 리포트: 분석가가 작성한 최종 결과물
    final_report: str