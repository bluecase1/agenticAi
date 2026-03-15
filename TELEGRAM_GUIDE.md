# Telegram Bot 연동 가이드

이 문서는 주식 분석 에이전트를 Telegram Bot과 연동하는 방법을 설명합니다.

---

## 1. Telegram Bot 생성

### 1.1 BotFather로봇 생성

1. Telegram 앱에서 **@BotFather** 검색
2. `/newbot` 명령어 입력
3. 봇 이름 입력 (예: `Stock Analysis Bot`)
4. 봇 사용자명 입력 (예: `stock_analysis_bot`) - 반드시 `bot`으로 끝나야 함
5. **토큰을 복사**하여 저장 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 1.2 .env 파일 수정

```bash
# .env 파일에 다음 줄 추가
TELEGRAM_BOT_TOKEN=your_bot_token_here

# 기존 .env 예시
OPENAI_API_KEY=
GOOGLE_API_KEY=
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

---

## 2. 의존성 설치

```bash
# 가상환경 활성화
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 의존성 설치
pip install python-telegram-bot

# 또는 requirements.txt 사용
pip install -r requirements.txt
```

---

## 3. Bot 실행

### 3.1 로컬 실행

```bash
python telegram_bot.py
```

정상 실행 시 출력:
```
🤖 Telegram Bot 시작 중...
종료하려면 Ctrl+C를 누르세요.
```

### 3.2 테스트

1. Telegram에서 생성한 봇 검색
2. `/start` 명령어 전송
3. 다음과 같은 메시지 전송:
   - "삼성전자 주가 알려줘"
   - "Apple 주가 분석해줘"
   - "엔비디아 현재가"

---

## 4. 사용 가능한 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `/start` | 봇 시작 | `/start` |
| `/help` | 도움말 보기 | `/help` |
| `/analyze` | 명시적 분석 요청 | `/analyze 삼성전자` |
| (일반 메시지) | 자동으로 분석 | "네이버 주가" |

---

## 5. 지원 질문 유형

### 한국 주식
- "삼성전자 주가 알려줘"
- "카카오 주가 분석해줘"
- "네이버 최근动向"

### 미국 주식
- "AAPL 주가"
- "NVDA 분석해줘"
- "Tesla 현재가"

---

## 6. 프로덕션 배포 (선택사항)

### 6.1ngrok 사용 (로컬 테스트)

```bash
# ngrok 설치 후
ngrok http 8443

#Webhook 설정
curl -F "url=https://your-ngrok-url.ngrok-free.app/webhook" \
     https://api.telegram.org/bot<TOKEN>/setWebhook
```

### 6.2 VPS/서버 배포

```bash
# Ubuntu 서버에서 systemd 서비스로 실행
sudo nano /etc/systemd/system/stock-bot.service
```

```ini
[Unit]
Description=Stock Analysis Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agenticAi
ExecStart=/home/ubuntu/agenticAi/.venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable stock-bot
sudo systemctl start stock-bot
```

---

## 7. 문제 해결

### Bot이 응답하지 않는 경우

1. 토큰이 정확한지 확인
2. Bot이 활성화되어 있는지 확인
3. 로그 출력 확인

### 오류 발생 시

```bash
# 상세 로그 확인
python -v telegram_bot.py
```

### LangGraph 에러

- `GOOGLE_API_KEY`가 올바르게 설정되어 있는지 확인
- 네트워크 연결 확인

---

## 8. 코드 구조

```
telegram_bot.py
├── main()              # Application 생성 및 핸들러 등록
├── start_command()     # /start 명령어 처리
├── help_command()      # /help 명령어 처리  
├── analyze_command()   # /analyze 명령어 처리
├── handle_message()    # 일반 메시지 처리
└── run_agent()         # LangGraph 에이전트 실행
```

---

## 9. 확장 기능 추가 가능

- `/analyze` 명령어 외래 환율 정보 포함
- `/subscribe` 관심 종목 알림订阅
- `/news` 최신 뉴스 제공
- `/portfolio` 포트폴리오 분석

---

## 10. 참고 자료

- [python-telegram-bot 공식 문서](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
