# CareerFit AI

> 취업·공모전 데이터를 기반으로 개인 맞춤형 포트폴리오와 역량 향상 방향을 제안하는 AI 코치


## 프로젝트 개요

취업을 준비하는 과정에서 어떤 경험과 역량을 쌓아야 하는지 판단하기는 쉽지 않습니다.

CareerFit AI는 채용공고와 공모전 데이터를 분석하여 사용자에게 필요한 역량과 포트폴리오 방향을 AI가 제안하는 프로젝트입니다.


## 기술 스택

| 영역 | 기술 |
|---|---|
| 백엔드 | Python, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite |
| 실행 환경 | Docker |

## 프로젝트 구조

```text
carrerfit_ai/
├── backend/
│   ├── data/
│   ├── routers/
│   │   ├── analayze.py
│   │   ├── health.py
│   │   └── jobs.py
│   ├── services/
│   ├── main.py
│   ├── .env (masked)
│   └── requirements.txt
├── frontend/
├── data/
├── docs/ (masked)
│   ├── CHECKLIST.md
│   ├── EVAL_QUESTIONS.md
│   ├── PROJECT_PLAN.md
│   └── PROMPTS.md
├── .gitignore
├── index.html
└── README.md
```

## 사용 라이브러리
| 라이브러리 | 버전 |
|---|---|
|fastapi|0.115.5|
|uvicorn|0.32.1|
|python-dotenv|1.0.1|
|google-generativeai|0.8.3|
|pandas|2.2.3|
|chromadb|1.5.9|
|pydantic|2.10.3|
|transformers[torch]|5.12.1|
|huggingface-hub|1.21.0|
|google|3.0.0|
|google.genai|2.10.0|

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