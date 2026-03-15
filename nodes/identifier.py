from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState

from langchain_google_genai import ChatGoogleGenerativeAI
import os


# LLM 설정 (OpenAI 외에 다른 모델로 교체 가능)
# llm = ChatOpenAI(model="gpt-4o", temperature=0)

# OpenAI 대신 Gemini 사용
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


def identifier_node(state: AgentState) -> dict:
    """사용자의 질문을 분석하여 어떤 시장(KR/US/BOTH)에 대한 것인지 판별합니다."""
    
    # 1. 마지막 사용자 메시지 가져오기
    user_input = state["messages"][-1].content
    
    # 2. 페르소나 및 지침 설정 (System Prompt)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """당신은 금융 시장 판별 전문가입니다. 
        사용자의 질문이 다음 중 어느 시장에 해당하는지 판단하여 'KR', 'US', 'BOTH', 'UNKNOWN' 중 하나만 대답하세요.
        
        - KR: 한국 주식, 코스피, 코스닥, 한국 기업(예: 삼성전자, 네이버 등)
        - US: 미국 주식, 나스닥, S&P500, 미국 기업(예: 엔비디아, 애플 등)
        - BOTH: 두 시장을 비교하거나 동시에 언급할 때
        - UNKNOWN: 주식/경제와 관련 없는 질문일 때
        """),
        ("human", "{input}")
    ])
    
    # 3. LLM 호출 및 결과 처리
    chain = prompt | llm
    response = chain.invoke({"input": user_input})
    market_result = response.content.strip().upper()
    
    print(f"--- [Node: Identifier] ---")
    print(f"Input: {user_input}")
    print(f"Result: {market_result}")
    
    # 4. 상태(State) 업데이트 값 반환
    return {"market": market_result}