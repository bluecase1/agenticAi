# agenticAi

stock-agent/
├── .env                # API Keys (OpenAI, Brave, etc.)
├── main.py             # 전체 그래프 실행 및 엔트리 포인트
├── state.py            # TypedDict 기반의 공통 상태(State) 정의
│
├── nodes/              # 에이전트의 '행동'을 정의 (LangGraph Nodes)
│   ├── __init__.py
│   ├── identifier.py   # 시장 판별 노드 (KR vs US) LLM 이용
│   ├── researcher.py   # MCP 도구를 사용해 정보를 수집하는 노드
│   └── analyst.py      # 수집된 데이터를 분석하는 노드
│
├── mcp_servers/        # 외부 데이터를 가져오는 '도구' (MCP)
│   ├── kr_stock.py     # 한국 주식 데이터 서버
│   └── us_stock.py     # 미국 주식 데이터 서버
│
├── prompts/            # 에이전트에게 줄 지침들 (System Prompts)
│   └── analysis_guide.md
│
└── requirements.txt