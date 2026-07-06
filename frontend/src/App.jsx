import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";

const API_BASE = "http://localhost:8000";
// ⚠️ API Key는 절대 여기에 넣지 않습니다

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(formData) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          major: formData.major,
          skills: formData.skills,
          job_type: formData.jobType,
        }),
      });

      if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
      const data = await response.json();
      setResult(data);

    } catch (err) {
      if (err.message.includes("Failed to fetch")) {
        setError("FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.");
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

// ... existing code ...

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-2xl mx-auto space-y-8">
        {/* 헤더 섹션 */}
        <header className="text-center">
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">CareerFit AI</h1>
          <p className="text-slate-600 text-sm">취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치</p>
        </header>

        {/* 메인 폼 */}
        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {/* 상태 및 결과 영역 */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm text-center">
            {error}
          </div>
        )}

        {isLoading && (
          <div className="text-center text-slate-500 py-10">
            <div className="animate-pulse">분석 중입니다...</div>
          </div>
        )}

        {result && (
          <div className="space-y-6 animate-in fade-in duration-500">
            <ResultCard answer={result.answer} />
            {result.sources?.length > 0 && (
              <SourceCard sources={result.sources} />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ... existing code ...

export default App;