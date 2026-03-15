from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState

from langchain_google_genai import ChatGoogleGenerativeAI
import os

# LLM 설정 (분석 능력과 문장력이 좋은 모델 추천)
# llm = ChatOpenAI(model="gpt-4o", temperature=0.7) # 리포트 작성이므로 온도를 약간 높여 자연스럽게 만듭니다.

# OpenAI 대신 Gemini 사용
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def analyst_node(state: AgentState) -> dict:
    """수집된 시장 데이터를 종합하여 최종 투자 분석 리포트를 작성합니다."""
    
    market = state.get("market", "UNKNOWN")
    stock_data = state.get("stock_data", {})
    user_input = state["messages"][0].content # 최초 질문
    
    print(f"--- [Node: Analyst] ---")
    print(f"Analyzing data for {market} market...")

    # 1. 분석 전문가 페르소나 및 지침 설정
    prompt = ChatPromptTemplate.from_messages([
        ("system", """당신은 전문 금융 분석가입니다. 
        제공된 주가 데이터와 시장 맥락을 바탕으로 사용자의 질문에 답변하는 전문 리포트를 작성하세요.
        
        [작성 가이드]
        1. 현재 주가와 등락률을 명확히 제시할 것.
        2. 해당 시장(KR/US)의 특성을 고려하여 현재 상황을 해석할 것.
        3. 단순 수치 전달을 넘어, 투자자가 주의 깊게 봐야 할 포인트(바이브)를 포함할 것.
        4. 친절하면서도 신뢰감 있는 전문가의 어조를 유지할 것.
        """),
        ("human", "질문: {input}\n수집된 데이터: {data}")
    ])
    
    # 2. 분석 수행
    chain = prompt | llm
    response = chain.invoke({
        "input": user_input,
        "data": str(stock_data)
    })
    
    report = response.content
    
    print("✅ 최종 리포트 작성 완료")
    
    # 3. 최종 리포트를 상태에 저장
    return {"final_report": report, "messages": [response]}