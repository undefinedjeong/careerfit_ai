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

def build_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문과 RAG 문서를 결합해 Gemini에게 보낼 프롬프트를 만든다.
    요리 비유: 외부 셰프에게 주문서를 작성하는 단계
    """
    # 3일차에 context_docs가 실제 ChromaDB 검색 결과로 채워진다
    # 지금은 빈 컨텍스트로 테스트한다
    context_text = "\n".join([
        f"- {doc.get('content', '')}" for doc in context_docs
    ]) if context_docs else "관련 데이터 없음 (3일차에 추가 예정)"

    prompt = f"""
    당신은 취업·공모전 전문 커리어 코치입니다.
    다음 지원자 정보와 참고 데이터를 바탕으로 맞춤형 조언을 한국어로 제공하세요.

    [지원자 정보]
    {query}

    [참고 데이터]
    {context_text}

    [답변 형식]
    1. 현재 역량 평가 (2~3문장)
    2. 부족한 역량 및 준비 방향 (3가지 이내)
    3. 추천 프로젝트 또는 공모전 (1~2개)

    출처 데이터가 없는 경우 일반적인 커리어 조언을 제공하되,
    데이터가 있다면 반드시 그 데이터를 근거로 답변하세요.
    """
    return prompt.strip()

def get_llm_response(query: str, context_docs: list) -> dict:
    """
    사용자 질문과 검색된 문서를 받아 LLM 응답을 반환한다.

    Args:
        query: 사용자 질문 (예: "데이터 분석가가 되려면 뭘 준비해야 하나요?")
        context_docs: RAG로 검색된 관련 문서 목록 (3일차에 ChromaDB에서 가져옴)

    Returns:
        {"answer": str, "sources": list}
    """
    client = genai.Client()

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
                {"title": "mock 데이터", "content": "mock 출처 내용"}
            ]
        }
    
    return performInteraction(client, query, context_docs)

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
def performInteraction(client, query, context_docs, fallback_depth=0):
    try:
        if fallback_depth <= 1:
            interaction = client.interactions.create(
                model = FALLBACK_MODELS[fallback_depth],
                input = build_prompt(query, [])
            )

            return {
                "answer": interaction.output_text,
                "sources": context_docs if context_docs else []
            }

        else:
            return {
                "answer": ollama_service.get_ollama_response(
                    prompt = build_prompt(query, [])
                ),
                "sources": []
            }

    except Exception as e:
        error_msg = str(e)

        # 429: 한도 초과 안내
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            if fallback_depth != 2:
                return performInteraction(client, query, context_docs, fallback_depth+1) #fallback mode로 다시 시도

        # 그 외 오류
        return {
            "answer": f"[예기치 않은 오류 발생] {error_msg}. 강사에게 문의하거나 MOCK_MODE=true 로 전환하세요.",
            "sources": []
        }