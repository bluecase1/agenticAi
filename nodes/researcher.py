from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from state import AgentState

from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. LLM 설정 (도구 사용 능력이 뛰어난 모델 추천)
# llm = ChatOpenAI(model="gpt-4o", temperature=0)

# OpenAI 대신 Gemini 사용
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

def researcher_node(state: AgentState) -> dict:
    """판별된 시장에 따라 적절한 MCP 도구를 선택하여 데이터를 수집합니다."""
    
    market = state.get("market", "UNKNOWN")
    last_message = state["messages"][-1].content
    
    print(f"--- [Node: Researcher] ---")
    print(f"Current Market Context: {market}")

    # 2. 시장별로 사용할 수 있는 도구(Tool)를 LLM에게 바인딩
    # 실제 운영 시에는 MCP 서버를 연결한 'tools' 객체를 사용하지만, 
    # 지금은 개념 학습을 위해 흐름을 명시적으로 보여줍니다.
    
    if market == "KR":
        # 한국 시장일 때: kr_stock.py 서버의 도구를 사용하도록 유도
        system_msg = "당신은 한국 주식 전문가입니다. 'get_kr_stock_price' 도구를 사용하여 정보를 가져오세요."
    elif market == "US":
        # 미국 시장일 때: us_stock.py 서버의 도구를 사용하도록 유도
        system_msg = "당신은 미국 주식 전문가입니다. 'get_us_stock_price' 도구를 사용하여 정보를 가져오세요."
    else:
        return {"messages": [HumanMessage(content="분석할 시장을 특정할 수 없습니다.")]}

    # 3. LLM이 도구 호출 여부를 결정 (Binding tools)
    # (여기서는 실제 MCP 연결 전 단계이므로, LLM이 도구를 호출하려는 '의도'를 파악하는 로직을 시뮬레이션합니다)
    response = llm.invoke([
        ("system", system_msg),
        ("human", last_message)
    ])

    print(f"Researcher Action: {response.content[:100]}...")

    # 4. 수집된 데이터를 상태에 저장 (실제로는 도구 실행 결과가 들어감)
    # 나중에 MCP 서버와 완전히 연결되면 이 부분은 자동으로 업데이트됩니다.
    return {
        "messages": [response],
        "stock_data": {"raw": response.content} # 우선 응답 내용을 저장
    }