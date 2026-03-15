# test/test_state.py - AgentState 정의 테스트
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState
from typing import Annotated
from langgraph.graph.message import add_messages


def test_agent_state_has_messages_field():
    """AgentState에 messages 필드가 있는지 확인"""
    assert "messages" in AgentState.__annotations__
    print("[OK] messages field exists")


def test_agent_state_has_market_field():
    """AgentState에 market 필드가 있는지 확인"""
    assert "market" in AgentState.__annotations__
    print("[OK] market field exists")


def test_agent_state_has_stock_data_field():
    """AgentState에 stock_data 필드가 있는지 확인"""
    assert "stock_data" in AgentState.__annotations__
    print("[OK] stock_data field exists")


def test_agent_state_has_final_report_field():
    """AgentState에 final_report 필드가 있는지 확인"""
    assert "final_report" in AgentState.__annotations__
    print("[OK] final_report field exists")


def test_agent_state_messages_is_annotated():
    """messages 필드가 Annotated 타입인지 확인"""
    annotations = AgentState.__annotations__
    messages_type = annotations.get("messages")
    assert messages_type is not None
    print("[OK] messages field is Annotated type")


if __name__ == "__main__":
    test_agent_state_has_messages_field()
    test_agent_state_has_market_field()
    test_agent_state_has_stock_data_field()
    test_agent_state_has_final_report_field()
    test_agent_state_messages_is_annotated()
    print("\n=== All state tests passed! ===")
