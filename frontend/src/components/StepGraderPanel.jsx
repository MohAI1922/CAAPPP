import React, { useState, useEffect } from 'react';
import { CheckCircle2, AlertTriangle, ListChecks, Loader2, Sparkles } from 'lucide-react';

const PRESETS = [
  {
    label: 'Valid Derivative',
    operation: 'derivative',
    problem: 'Find the derivative of f(x) = x^3 + 2*x',
    steps: 'd/dx(x^3 + 2*x)\n3*x^2 + 2',
  },
  {
    label: 'Catch Sign Error',
    operation: 'equation',
    problem: 'Solve 2*x - 6 = 4',
    steps: '2*x - 6 = 4\n2*x = -2\nx = -1',
  },
  {
    label: 'Algebra Expansion',
    operation: 'algebra',
    problem: 'Expand (x + 2)*(x - 3)',
    steps: '(x + 2)*(x - 3)\nx^2 - 3*x + 2*x - 6\nx^2 - x - 6',
  },
];

export default function StepGraderPanel({ apiBaseUrl, initialProblem = '' }) {
  const [problem, setProblem] = useState(initialProblem);
  const [operation, setOperation] = useState('auto');
  const [stepsText, setStepsText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [gradeResult, setGradeResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialProblem && !problem) {
      setProblem(initialProblem);
    }
  }, [initialProblem, problem]);

  const handleGrade = async (e) => {
    if (e) e.preventDefault();
    const stepLines = stepsText
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean);

    if (!problem.trim() || stepLines.length === 0 || isLoading) return;

    setIsLoading(true);
    setError(null);
    setGradeResult(null);

    try {
      const response = await fetch(`${apiBaseUrl}/grade-steps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem: problem.trim(),
          student_steps: stepLines,
          operation,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned HTTP ${response.status}`);
      }

      const data = await response.json();
      setGradeResult(data);
    } catch (err) {
      setError(err.message || 'Network error while grading derivation steps.');
    } finally {
      setIsLoading(false);
    }
  };

  const applyPreset = (preset) => {
    setProblem(preset.problem);
    setOperation(preset.operation);
    setStepsText(preset.steps);
    setGradeResult(null);
    setError(null);
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <ListChecks className="w-5 h-5 text-emerald-400" />
              <span>Check My Derivation Steps</span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Enter your original problem and each intermediate step on its own line to pinpoint exact equivalence or sign errors.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            {PRESETS.map((p) => (
              <button
                key={p.label}
                type="button"
                onClick={() => applyPreset(p)}
                className="text-xs px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors flex items-center gap-1"
              >
                <Sparkles className="w-3 h-3 text-amber-400" />
                {p.label}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleGrade} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-3">
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Original Problem Statement
              </label>
              <input
                type="text"
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                placeholder="e.g., Find the derivative of f(x) = x^3 + 2*x"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Operation Mode
              </label>
              <select
                value={operation}
                onChange={(e) => setOperation(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
              >
                <option value="auto">Auto-detect</option>
                <option value="algebra">Algebra</option>
                <option value="equation">Equation</option>
                <option value="derivative">Derivative</option>
                <option value="integral">Integral</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Your Steps (one step per line)
            </label>
            <textarea
              rows={5}
              value={stepsText}
              onChange={(e) => setStepsText(e.target.value)}
              placeholder={'(x + 2)*(x - 3)\nx^2 - 3*x + 2*x - 6\nx^2 - x - 6'}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-sm font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isLoading || !problem.trim() || !stepsText.trim()}
              className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold text-sm rounded-xl transition-all flex items-center gap-2 shadow-lg shadow-emerald-950/30"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Checking Steps...
                </>
              ) : (
                <>
                  <ListChecks className="w-4 h-4" />
                  Verify My Steps
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="bg-rose-950/40 border border-rose-800 rounded-2xl p-4 text-rose-300 text-sm font-mono">
          ⚠️ {error}
        </div>
      )}

      {gradeResult && (
        <div
          className={`border rounded-2xl p-6 shadow-xl space-y-4 ${
            gradeResult.overall_correct
              ? 'bg-emerald-950/20 border-emerald-500/30'
              : 'bg-rose-950/20 border-rose-500/30'
          }`}
        >
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2.5">
              {gradeResult.overall_correct ? (
                <CheckCircle2 className="w-6 h-6 text-emerald-400" />
              ) : (
                <AlertTriangle className="w-6 h-6 text-rose-400" />
              )}
              <div>
                <h3 className="text-base font-bold text-slate-100">
                  {gradeResult.overall_correct ? 'All Derivation Steps Verified' : 'Step Discrepancy Detected'}
                </h3>
                <p className="text-xs text-slate-400">{gradeResult.summary}</p>
              </div>
            </div>
            <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-slate-900 border border-slate-700 text-slate-300">
              mode: {gradeResult.operation}
            </span>
          </div>

          <div className="space-y-2.5">
            {(gradeResult.step_results || []).map((step) => (
              <div
                key={step.step_index}
                className={`p-4 rounded-xl border flex items-start justify-between gap-4 ${
                  step.valid
                    ? 'bg-slate-950/70 border-emerald-500/20'
                    : 'bg-rose-950/30 border-rose-500/40'
                }`}
              >
                <div className="flex items-start gap-3">
                  <span
                    className={`w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 ${
                      step.valid
                        ? 'bg-emerald-500/20 text-emerald-300'
                        : 'bg-rose-500/20 text-rose-300'
                    }`}
                  >
                    {step.step_index + 1}
                  </span>
                  <div>
                    <div className="font-mono text-sm text-slate-100">{step.step_text}</div>
                    <p className="text-xs text-slate-400 mt-1">{step.feedback}</p>
                  </div>
                </div>
                {step.error_type && (
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 shrink-0">
                    {step.error_type}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
