# telegram_bot.py
"""
Telegram Bot for Stock Analysis Agent

이 모듈은 Telegram Bot API를 통해 사용자의 메시지를 받아
LangGraph 기반 주식 분석 에이전트를 실행합니다.

사용 방법:
    1. .env 파일에 TELEGRAM_BOT_TOKEN 추가
    2. python telegram_bot.py 실행
    3. 텔레그램에서 봇에게 메시지 전송
"""
import os
import sys
import asyncio
from typing import Dict, Any

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# LangGraph workflow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import graph
from state import AgentState

# Load environment variables
load_dotenv()


# 전역 딕셔너리로 사용자 세션 관리
user_sessions: Dict[str, Dict[str, Any]] = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """시작 명령어 처리"""
    await update.message.reply_text(
        "📈 주식 분석 에이전트에 오신 것을 환영합니다!\n\n"
        "예시 질문:\n"
        "- 삼성전자 주가 알려줘\n"
        "- Apple 주가 분석해줘\n"
        "- 엔비디아 최근动向\n\n"
        "도움이 필요하면 /help 를 입력하세요."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """도움말 명령어 처리"""
    await update.message.reply_text(
        "📖 사용 방법\n\n"
        "/start - 시작하기\n"
        "/help - 도움말\n\n"
        "한국 주식: '삼성전자', '네이버', '카카오' 등\n"
        "미국 주식: 'AAPL', 'NVDA', 'TSLA' 등\n\n"
        "주식 종목을 포함한 질문을 보내면 분석해드립니다!"
    )


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """분석 명령어 처리 (명시적 분석 요청)"""
    user_message = " ".join(context.args) if context.args else ""
    
    if not user_message:
        await update.message.reply_text(
            "사용법: /analyze <종목명>\n"
            "예시: /analyze 삼성전자"
        )
        return
    
    # 분석 시작 메시지 전송
    await update.message.reply_text(f"🔍 '{user_message}' 분석 중...")
    
    # 에이전트 실행
    result = await run_agent(user_message, update.effective_user.id)
    
    # 결과 전송
    await update.message.reply_text(result, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """일반 메시지 처리 (주식 분석)"""
    user_message = update.message.text
    user_id = str(update.effective_user.id)
    
    # 사용자별 세션이 없으면 생성
    if user_id not in user_sessions:
        user_sessions[user_id] = {"history": []}
    
    # 분석 중 메시지 전송
    typing_message = await update.message.reply_text("🔍 분석 중...")
    
    try:
        # LangGraph 에이전트 실행
        result = await run_agent(user_message, user_id)
        
        # 결과 전송
        await update.message.reply_text(result, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ 오류가 발생했습니다: {str(e)}\n"
            "다시 시도해 주세요."
        )
    finally:
        # 타이핑 메시지 삭제
        await typing_message.delete()


async def run_agent(user_input: str, user_id: str) -> str:
    """
    LangGraph 에이전트를 실행하고 결과를 반환합니다.
    
    Args:
        user_input: 사용자의 질문
        user_id: 사용자 ID
    
    Returns:
        분석 결과 문자열
    """
    # 초기 상태 설정
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": user_input}],
        "market": "",
        "stock_data": {},
        "news_content": [],
        "final_report": ""
    }
    
    # 에이전트 실행 (비동기 스트림)
    final_result = ""
    
    async for output in graph.astream(initial_state):
        for key, value in output.items():
            if "final_report" in value:
                final_result = value["final_report"]
    
    if not final_result:
        final_result = "⚠️ 분석 결과를 생성하지 못했습니다. 다시 시도해 주세요."
    
    return final_result


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """오류 처리"""
    print(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "❗ 예상치 못한 오류가 발생했습니다.\n"
            "다시 시도해 주세요."
        )


def main():
    """Telegram Bot 메인 함수"""
    # Bot 토큰 가져오기
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("❌ 오류: .env 파일에 TELEGRAM_BOT_TOKEN이 없습니다.")
        print("\n설정 방법:")
        print("1. Telegram에서 @BotFather 검색")
        print("2. /newbot 명령어로 새 봇 생성")
        print("3. 토큰을 복사하여 .env 파일에 추가:")
        print("   TELEGRAM_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    # Application 생성
    application = Application.builder().token(bot_token).build()
    
    # 핸들러 등록
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyze", analyze_command))
    
    # 일반 텍스트 메시지 핸들러 (명령어 제외)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    
    # 오류 핸들러
    application.add_error_handler(error_handler)
    
    # Bot 시작
    print("🤖 Telegram Bot 시작 중...")
    print("종료하려면 Ctrl+C를 누르세요.")
    
    # 폴링 모드로 실행
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
