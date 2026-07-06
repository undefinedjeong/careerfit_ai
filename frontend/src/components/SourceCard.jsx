function SourceCard({ sources }) {
  if (!sources || sources.length === 0) {
    return <div className="bg-slate-50 rounded-xl border border-slate-200 p-4 text-sm text-slate-500">참고한 공고 데이터가 없습니다.</div>;
  }
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-bold text-slate-800 mb-4">📄 참고한 공고 출처</h2>
      <div className="space-y-4">
        {sources.map((source, index) => (
          <div key={index} className="bg-slate-50 rounded-lg p-4 border border-slate-100">
            <p className="text-sm font-semibold text-slate-800">{source.company} | {source.title}</p>
            <p className="text-xs text-slate-600 mt-2">
              <span className="font-medium text-slate-500">필수 스킬: </span>
              {source.required_skills || "정보 없음"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
  export default SourceCard;