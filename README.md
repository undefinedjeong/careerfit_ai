# CareerFit AI

> 취업·공모전 데이터를 기반으로 개인 맞춤형 포트폴리오와 역량 향상 방향을 제안하는 AI 코치

URL: https://careerfit-ai-frontend-oz8z.onrender.com/

\* 백엔드 서버 부팅에 시간이 걸려 1분 내외로 시간 소요될 수 있음(이미 부팅된 경우 10초 이내)

## 프로젝트 개요

취업을 준비하는 과정에서 어떤 경험과 역량을 쌓아야 하는지 판단하기는 쉽지 않습니다.

CareerFit AI는 채용공고 데이터를 분석하여 사용자에게 필요한 역량과 포트폴리오 방향을 AI가 제안하는 프로젝트입니다.

### 어떤 부분이 다른가?

- 비교적 최적화된 LLM 모델 사용
- google.genai에서 제공하는 Interaction 객체 기반 LLM 상호작용
- 선순위 모델 사용 불가시 자동으로 후순위 모델로 폴백 시도 
- ChromaDB를 클라우드화 하여 데이터 노출 최소화

### TroubleShooting:

- Frontend의 SourceCard.jsx에 필수 스킬 부분이 출력되지 않음 (해결: DB 수정)
``` text
문제: chromadb 생성시 metadata 내에 required_skills가 포함되지 않음.

해결: preprocess.py에서 json 생성시 metadata 내에 required_skills 포함하게 수정한 후, chromadb 재생성
```

- render에서 appuser의 권한 설정 오류(해결: 권한 변경)
``` text
문제: appuser의 홈 디렉토리가 /nonexistent로 설정되어 chromaDB 캐시 생성 중 권한 오류가 발생.
해결: appuser의 홈 디렉토리를 /app으로 변경
```

- 데이터가 github에 노출됨(해결: 클라우드)
``` text
문제: rag_documents.json이 github에 노출됨
해결: chromaDB에서 제공하는 클라우드에 DB를 업로드하고 API로 DB를 받아옴으로써 데이터 노출 최소화
```

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
| 폴백 모델 | Gemma 4 31B |
| 로컬 폴백 모델 | llama 3.2 3B |

### 왜 이 모델을 선택하였는가?

> Gemini API에서 무료로 제공하는 사용량이 압도적으로 크고, Gemini 2.5 대비 성능도 좋음.

| 모델명 | 분당 요청수 제한 | 일간 요청수 제한 | 분당 토큰수 제한 |
|---|---|---|---|
| Gemini 2.5 Flash Lite | 10 | 20 | 250K |
| Gemini 2.5 Flash | 5 | 20 | 250K |
| Gemini 3.1 Flash Lite | 15 | 500 | 250K |
| Gemma 4 31B | 15 | 1,500 | 무제한 |

- 성능과 제공 사용량이 균형을 이루는 Gemini 3.1 Flash Lite를 **메인 모델**로 선택함.
- 성능은 비교적 떨어지나 제공되는 사용량이 많아 안정적으로 서비스를 제공할 수 있는 Gemma 4 31B를 **폴백 모델**로 선택함.
- 상세 평가 사항은 [MODEL_BENCHMARK.md](./docs/MODEL_BENCHMARK.md) 참고

## 사용 라이브러리 (백엔드)
| 라이브러리 | 버전 |│| 라이브러리 | 버전 |
|---|---|---|---|---|
|fastapi|0.115.5|│|uvicorn|0.32.1|
|python-dotenv|1.0.1|│|google-generativeai|0.8.3|
|pandas|2.2.3|│|chromadb|1.5.9|
|pydantic|2.10.3|│|transformers[torch]|5.12.1|
|huggingface-hub|1.21.0|│|google|3.0.0|
|google.genai|2.10.0|│|||

## 프로젝트 구조

``` text
careerfit_ai/
├── backend/
│   ├── data/
│   │   └── careerfit.db (ignored)
│   ├── routers/
│   │   ├── analyze.py
│   │   ├── health.py
│   │   └── jobs.py
│   ├── services/
│   │   ├── __init__.py 
│   │   └── llm_service.py
│   ├── main.py
│   ├── .env (ignored)
│   ├── DOCKERFILE
│   └── requirements.txt
├── frontend/
│   ├── src
│   │   ├── InputForm.jsx
│   │   ├── ResultCard.jsx
│   │   └── SourceCard.jsx
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   ├── DOCKERFILE
│   └── main.jsx
├── data/
├── docs/
├── .gitignore
└── README.md
```

## 동작 흐름(백엔드)
1. backend/routers/analyze.py의 analyze_career 함수에서 사용자로부터 전공, 스킬(역량), 희망 직무를 입력받는다.

2. 입력받은 값을 LLM이 이해하기 쉬운 하나의 문자열로 변환한 뒤, get_llm_response 함수에 전달한다.

3. backend/services/llm_service.py의 get_llm_response 함수는 google.genai 라이브러리를 사용한다.

4. 해당 함수는 클라이언트를 생성한 후 client.interactions.create(model, input)을 호출해 Interaction을 생성하고, interaction.output_text에 담긴 결과를 반환한다.

5. LLM 텍스트 생성 과정에서 사용량 초과 오류 발생시 폴백 모델을 사용하여 다시 시도한다. 폴백 모델 사용량까지 초과하였다면 로컬 모델을 사용하여 답변한다.

## 사용법
### 백엔드 서버(로컬)
``` bash
cd backend
venv\Scripts\Activate.ps1 # venv 실행
uvicorn main:app --reload --port 8000
```
``` text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
```
### 백엔드 서버(배포)
``` text
https://careerfit-ai-lmxn.onrender.com/
https://careerfit-ai-lmxn.onrender.com/docs
```

### 프론트엔드 서버(로컬)
``` bash
npm run dev
```
```
http://127.0.0.1:5173
```

### 프론트엔드 서버(배포)
``` text
https://careerfit-ai-frontend-oz8z.onrender.com/
```

### ChromaDB 접근법
```Python
#ChromaDB Client 객체 생성
client = chromadb.CloudClient(              
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

#DB 내 콜렉션 선택
collection = client.get_collection(name="jobs")

#콜렉션 내 데이터 추가
collection.add(
    documents=[doc["text"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
    ids=[doc["doc_id"] for doc in documents]
)

#콜렉션 내 데이터 검색
results = collection.query(
    query_texts=[query],
    n_results=min(n_results, collection.count()),
    where= where_filter
)
```

### Google Genai (Interaction) 사용법
``` Python
#클라이언트 객체 생성
client = genai.Client(api_key = GEMINI_API_KEY)

#인터랙션 생성
interaction = client.interactions.create(
    model = FALLBACK_MODELS[fallback_depth],
    input = build_rag_prompt(query, context_docs)
)

#인터랙션 반환값 출력
return {
    "answer": interaction.output_text,
    "sources": sources
}
```
## 진행 현황

- **1일차**
  - [x] 프로젝트 기획
  - [x] Python 개발 환경 구축
  - [x] GitHub 저장소 생성

- **2일차**
  - [x] FastAPI 서버 구축
  - [x] `/health`, `/jobs`, `/analyze` API 구현
  - [x] Gemini 3.1 Flash-Lite API 연동
  - [x] Mock Mode 환경변수 구성

- **3일차**
  - [x] 채용공고 데이터 수집
  - [x] Pandas 전처리
  - [x] SQLite 저장
  - [x] ChromaDB 구축

- **4일차**
  - [x] RAG 검색 기능
  - [x] React UI 개발
  - [x] AI 분석 결과 화면 구현

- **5일차**
  - [x] Docker 배포
  - [x] 프로젝트 문서 정리
  - [x] 포트폴리오 완성

## 향후 개선 방안

- 프롬프트 인젝션 방어를 위한 코드 추가
