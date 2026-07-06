import ReactMarkdown from "react-markdown";

function ResultCard({ answer }) {
  if (!answer) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      {/* 타이틀 영역 */}
      <div className="flex items-center gap-2 mb-4 pb-4 border-b border-slate-100">
        <span className="text-2xl">🤖</span>
        <h2 className="text-lg font-bold text-slate-800">CareerFit AI 분석 리포트</h2>
      </div>

      {/* 분석 내용 영역 */}
      <div className="text-slate-600 text-sm leading-relaxed whitespace-pre-line text-left">
        <ReactMarkdown>{answer}</ReactMarkdown>
      </div>
    </div>
  );
}

export default ResultCard;