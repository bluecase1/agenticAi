# 테스트 및 커밋 가이드라인

이 문서는 코드 변경 사항을 Git에 커밋하기 전에 수행해야 할 테스트 절차를 정의합니다.

---

## 1. 테스트 필수 사항

**모든 수정사항에 대해 테스트를 반드시 수행해야 합니다.**

- 테스트 코드는 `/test` 폴더 아래에 작성합니다.
- 테스트를 통과하지 못하면 커밋할 수 없습니다.
- 커밋 메시지에 테스트 실행 방법을 반드시 기록합니다.

---

## 2. 테스트 작성 규칙

### 테스트 파일 위치
```
agenticAi/
├── test/
│   ├── __init__.py
│   ├── test_kr_stock.py    # 한국 주식 MCP 서버 테스트
│   ├── test_us_stock.py    # 미국 주식 MCP 서버 테스트
│   ├── test_identifier.py  # 시장 식별 노드 테스트
│   ├── test_researcher.py  # 리서처 노드 테스트
│   └── test_analyst.py     # 분석가 노드 테스트
```

### 테스트 함수命名
```python
# 파일: test/test_kr_stock.py

def test_get_kr_stock_price_with_valid_ticker():
    """유효한 티커로 주가 조회 테스트"""
    pass

def test_get_kr_stock_price_with_invalid_ticker():
    """유효하지 않은 티커로 주가 조회 테스트"""
    pass
```

---

## 3. 테스트 실행 방법

### 전체 테스트 실행
```bash
pytest
```

### 단일 테스트 파일 실행
```bash
pytest test/test_kr_stock.py
```

### 단일 테스트 함수 실행
```bash
pytest test/test_kr_stock.py::test_get_kr_stock_price_with_valid_ticker
```

### 특정 패턴 테스트 실행
```bash
pytest -k "test_identifier"
```

---

## 4. 커밋 메시지 작성 규칙

### 형식
```
[type]: [简短 설명]

[상세 설명 (선택)]

Test: [테스트 실행 방법]
```

### 예시

```
feat: Add AGENTS.md for AI coding agent guidelines

AGENTS.md 파일에 코딩 에이전트를 위한 가이드라인을 추가했습니다.
- 빌드/테스트 명령어
- 코드 스타일 가이드라인
-命名 convention

Test: pytest (전체 테스트 통과 확인)
```

```
fix: Fix identifier node type error

Type annotation 오류 수정 및 state 접근 방식 개선

Test: pytest test/test_identifier.py (개별 테스트 통과 확인)
```

---

## 5. 커밋 전 체크리스트

- [ ] 코드 변경 완료
- [ ] 테스트 코드 작성 (`/test` 폴더)
- [ ] 테스트 실행 및 통과 확인
- [ ] 커밋 메시지에 테스트 방법 기록
- [ ] git add & commit & push 수행

---

## 6. 주의사항

1. **테스트 없이 커밋 금지**: 어떤 작은 변경이든 반드시 테스트를 수행하세요.
2. **테스트 실패시 커밋 금지**: 테스트가 실패하면 수정을 완료할 때까지 커밋하지 마세요.
3. **모든 테스트 통과시 작업 중단**: 테스트가 모두 통과하면 추가 변경 없이 바로 커밋하세요.
