import os
import sys
from dotenv import load_dotenv

# 1. 다른 무엇보다 "가장 먼저" 환경 변수를 로드합니다.
load_dotenv() 

# 2. 그 다음 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from state import AgentState

# 우리가 만든 노드들 불러오기
from nodes.identifier import identifier_node
from nodes.researcher import researcher_node
from nodes.analyst import analyst_node

# 1. 그래프 초기화
# AgentState 규격을 따르는 워크플로우를 생성합니다.
builder = StateGraph(AgentState)

# 2. 노드 등록
# "이름", 실행할_함수 순으로 등록합니다.
builder.add_node("identify", identifier_node)
builder.add_node("research", researcher_node)
builder.add_node("analyze", analyst_node)

# 3. 연결 관계(Edge) 설정
# START -> 시장 판별 -> 데이터 수집 -> 결과 분석 -> END
builder.add_edge(START, "identify")
builder.add_edge("identify", "research")
builder.add_edge("research", "analyze")
builder.add_edge("analyze", END)

# 4. 컴파일 (실행 가능한 앱으로 변환)
graph = builder.compile()

# 5. 실행 테스트 (바이브 코딩 확인!)
if __name__ == "__main__":
    print("🚀 주식 분석 에이전트 가동...")
    
    # 초기 상태 설정 (사용자의 첫 질문)
    initial_state = {
        "messages": [{"role": "user", "content": "삼성전자 주가 분석해줘"}]
    }
    
    # 에이전트 실행
    for output in graph.stream(initial_state):
        # 각 단계(노드)가 끝날 때마다 상태 변화를 출력합니다.
        for key, value in output.items():
            print(f"\n📍 작업 완료: [{key}]")
            if "final_report" in value:
                print(f"\n📊 최종 리포트:\n{value['final_report']}")