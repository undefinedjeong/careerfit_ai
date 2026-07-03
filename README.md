# CareerFit AI

> 취업·공모전 데이터를 기반으로 개인 맞춤형 포트폴리오와 역량 향상 방향을 제안하는 AI 코치


## 프로젝트 개요

취업을 준비하는 과정에서 어떤 경험과 역량을 쌓아야 하는지 판단하기는 쉽지 않습니다.

CareerFit AI는 채용공고와 공모전 데이터를 분석하여 사용자에게 필요한 역량과 포트폴리오 방향을 AI가 제안하는 프로젝트입니다.

## 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| AI API | Gemini 3.1 Flash-Lite, Gemma 4 31B, (local) llama 3.2 3B |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite |
| 실행 환경 | Docker |

### 사용 LLM 모델
| 역할 | 모델명 |
|---|---|
| 메인 모델 | Gemini 3.1 Flash-Lite |
| 폴백 모델 | Gemma 4 31B|
| 로컬 폴백 모델 | llama 3.2 3B |

### 왜 이 모델을 선택하였는가?

> Gemini API에서 무료로 제공하는 사용량이 압도적으로 크고, Gemini 2.5 대비 성능도 좋음.

| 모델명 | 분당 요청수 제한 | 일간 요청수 제한 | 분당 토큰수 제한 |
|---|---|---|---|
| Gemini 2.5 Flash Lite | 10 | 20 | 250K |
| Gemini 2.5 Flash | 5 | 20 | 250K |
| Gemini 3.1 Flash Lite | 15 | 500 | 250K |
| Gemma 4 31B | 15 | 1,500 | 무제한

- 성능과 제공 사용량이 균형을 이루는 Gemini 3.1 Flash Lite를 **메인 모델**로 선택함.
- 성능은 비교적 떨어지나 제공되는 사용량이 많아 안정적으로 서비스를 제공할 수 있는 Gemma 4 31B를 **폴백 모델**로 선택함.

## 사용 라이브러리
| 라이브러리 | 버전 |│| 라이브러리 | 버전 |
|---|---|---|---|---|
|fastapi|0.115.5|│|uvicorn|0.32.1|
|python-dotenv|1.0.1|│|google-generativeai|0.8.3|
|pandas|2.2.3|│|chromadb|1.5.9|
|pydantic|2.10.3|│|transformers[torch]|5.12.1|
|huggingface-hub|1.21.0|│|google|3.0.0|
|google.genai|2.10.0|│|||

## 프로젝트 구조

```text
carrerfit_ai/
├── backend/
│   ├── data/ (ignored)
│   ├── routers/
│   │   ├── analayze.py
│   │   ├── health.py
│   │   └── jobs.py
│   ├── services/
│   │   ├── __init__.py 
│   │   └── llm_service.py
│   ├── main.py
│   ├── .env (ignored)
│   └── requirements.txt
├── frontend/
├── img/
├── data/
├── docs/ (ignored)
├── .gitignore
├── index.html
└── README.md
```

## 동작 흐름
1. backend/routers/analyze.py의 analyze_career 함수에서 사용자로부터 전공, 스킬(역량), 희망 직무를 입력받는다.

2. 입력받은 값을 LLM이 이해하기 쉬운 하나의 문자열로 변환한 뒤, get_llm_response 함수에 전달한다.

3. backend/services/llm_service.py의 get_llm_response 함수는 google.genai 라이브러리를 사용한다.

4. 해당 함수는 클라이언트를 생성한 후 client.interactions.create(model, input)을 호출해 Interaction을 생성하고, interaction.output_text에 담긴 결과를 반환한다.

5. LLM 텍스트 생성 과정에서 사용량 초과 오류 발생시 폴백 모델은 사용하여 다시 시도한다. 폴백 모델 사용량까지 초과하였다면 기존처럼 오류를 리턴한다.


## 진행 현황

- **1일차**
  - [x] 프로젝트 기획
  - [x] Python 개발 환경 구축
  - [x] GitHub 저장소 생성

- **2일차**
  - [x] FastAPI 서버 구축
  - [x] `/health`, `/jobs`, `/analyze` API 구현
  - [x] Gemini 2.5 Flash-Lite API 연동
  - [x] Mock Mode 환경변수 구성

- **3일차**
  - [ ] 채용공고 데이터 수집
  - [ ] Pandas 전처리
  - [ ] SQLite 저장
  - [ ] ChromaDB 구축

- **4일차**
  - [ ] RAG 검색 기능
  - [ ] React UI 개발
  - [ ] AI 분석 결과 화면 구현

- **5일차**
  - [ ] Docker 배포
  - [ ] 프로젝트 문서 정리
  - [ ] 포트폴리오 완성