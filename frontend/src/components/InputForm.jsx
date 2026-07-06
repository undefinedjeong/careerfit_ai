import { useState } from "react";

function InputForm({ onSubmit, isLoading }) {
  const [major, setMajor] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [jobType, setJobType] = useState("");

  function handleSubmit() {
    const skills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);
    onSubmit({ major, skills, jobType });
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-bold text-slate-800 mb-5">입력 정보</h2>
      <div className="space-y-5">
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1.5">전공</label>
          <input type="text" value={major} onChange={e => setMajor(e.target.value)}
            placeholder="예: 통계학과"
            className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1.5">보유 스킬 (쉼표 구분)</label>
          <input type="text" value={skillsInput} onChange={e => setSkillsInput(e.target.value)}
            placeholder="예: Python, SQL, R"
            className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1.5">관심 직무</label>
          <input type="text" value={jobType} onChange={e => setJobType(e.target.value)}
            placeholder="예: 데이터 분석"
            className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button onClick={handleSubmit}
          disabled={isLoading || !major || !skillsInput || !jobType}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-bold py-2.5 px-4 rounded-lg shadow-md transition-all text-sm">
          {isLoading ? "분석 중..." : "🚀 역량 분석 요청"}
        </button>
      </div>
    </div>
  );
}

export default InputForm;