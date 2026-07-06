# backend/services/llm_service.py

import os
from dotenv import load_dotenv
from google import genai
from services import ollama_service

# .env 파일에서 환경변수를 읽어온다
load_dotenv()

# mock mode 설정: .env의 MOCK_MODE=true 이면 Gemini를 호출하지 않는다
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def build_rag_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문 + RAG 검색 문서 → Gemini 프롬프트 구성
    요리 비유: 셰프(Gemini)에게 레시피 카드(context_docs)를 건네며 요청합니다.
    """
    if context_docs:
        context_text = "\n".join([
            f"[공고 {i+1}]\n{doc['text']}\n출처: {doc['metadata'].get('company', '')} — {doc['metadata'].get('title', '')}"
            for i, doc in enumerate(context_docs)
        ])
        context_section = f"""
            [참고 데이터 — 실제 취업·공모전 공고]
            {context_text}

            위 데이터를 반드시 근거로 사용해 답변하세요.
            답변에서 어떤 공고를 참고했는지 명시하세요.
        """

    else:
        context_section = "[참고 데이터 없음 — 일반적인 조언을 제공합니다]"

    return f"""당신은 취업·공모전 전문 커리어 코치입니다.
        다음 지원자 정보와 참고 데이터를 바탕으로 맞춤형 조언을 한국어로 제공하세요.

        [지원자 정보]
        {query}

        {context_section}

        [답변 형식]
        1. 현재 역량 평가 (2문장 이내)
        2. 추천 공고 또는 공모전 (1~2개, 이유 포함)
        3. 부족한 역량 및 준비 방향 (3가지 이내)

        간결하고 실용적으로 작성하세요.
    """

def get_llm_response(query: str, context_docs: list) -> dict:
    """
    사용자 질문과 검색된 문서를 받아 LLM 응답을 반환한다.

    Args:
        query: 사용자 질문 (예: "데이터 분석가가 되려면 뭘 준비해야 하나요?")
        context_docs: RAG로 검색된 관련 문서 목록 (3일차에 ChromaDB에서 가져옴)

    Returns:
        {"answer": str, "sources": list}
    """
    client = genai.Client(api_key = GEMINI_API_KEY) # HOW IT HAVE BEEN WORKED WITHOUT API KEY??

    if MOCK_MODE or client == None:
        # mock mode: Gemini API를 호출하지 않고 미리 정의된 응답을 반환한다
        # API Key가 없거나 한도 초과 시 이 모드로 전환한다
        return {
            "answer": (
                "[MOCK 응답] 이것은 테스트용 응답입니다. "
                f"질문: '{query}'에 대한 실제 Gemini 응답은 "
                "MOCK_MODE=false 로 설정하면 받을 수 있습니다."
            ),
            "sources": [
                { "company": doc["metadata"].get("company", ""), 
                    "title": doc["metadata"].get("title", ""), 
                    "required_skills": ""
                } for doc in context_docs
            ]
        }
    
    sources = [{ "company": doc["metadata"].get("company", ""), 
                "title": doc["metadata"].get("title", ""), 
                "required_skills": doc["metadata"].get("required_skills", ""), 
                "distance": doc.get("distance", 0)
            } for doc in context_docs
            ]

    
    return performInteraction(client, query, context_docs, sources)

'''
fallback_depth
0: 메인 모델(gemini 3.1 flash lite)
1: 폴백 모델(gamma 4 31b)
2: 로컬 폴백 모델(llama 3.2 3b)
'''
FALLBACK_MODELS = {
    0: os.getenv("LLM_MODEL"),
    1: os.getenv("FALLBACK_MODEL"),
    2: os.getenv("LOCAL_FALLBACK_MODEL"),
}

def performInteraction(client, query, context_docs, sources, fallback_depth=0):
    try:
        if fallback_depth <= 1:
            interaction = client.interactions.create(
                model = FALLBACK_MODELS[fallback_depth],
                input = build_rag_prompt(query, context_docs)
            )

            return {
                "answer": interaction.output_text,
                "sources": sources
            }

        else:
            return {
                "answer": ollama_service.get_ollama_response(
                    prompt = build_rag_prompt(query, context_docs)
                ),
                "sources": sources
            }

    except Exception as e:
        error_msg = str(e)

        # 429: 한도 초과 안내
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            if fallback_depth != 2:
                return performInteraction(client, query, context_docs, sources, fallback_depth+1) #fallback mode로 다시 시도

        # 그 외 오류
        return {
            "answer": f"[예기치 않은 오류 발생] {error_msg}. 강사에게 문의하거나 MOCK_MODE=true 로 전환하세요.",
            "sources": []
        }