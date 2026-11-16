import React from 'react';
import { Send, Sparkles } from 'lucide-react';

const PRESET_EXAMPLES = [
  "Find the derivative of x² sin(x) with respect to x",
  "Evaluate the indefinite integral of x²",
  "Evaluate the definite integral of x² from 0 to 1",
  "A 10-foot ladder is leaning against a vertical wall. The bottom of the ladder slides away from the wall at a constant rate of 2 feet per second. How fast is the top of the ladder sliding down the wall at the exact moment when the bottom of the ladder is 6 feet away from the wall?",
  "find the zeros x^2 + x - 12 = 0",
  "Solve 3x + 7 = 22",
  "Simplify (x + 1)² − x²",
  "What is 47 × 89 + 123?",
  "Is 97 prime?",
  "Find the distance between the points (1, 2) and (4, 6)"
];

export default function ProblemInput({ problem, setProblem, onSubmit, isLoading }) {
  const handleKeyDown = (e) => {
    // Pressing Enter (without Shift) triggers immediate solve submission
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && problem.trim()) {
        onSubmit(e);
      }
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3">
        <label className="text-sm font-semibold text-slate-300 flex items-center gap-2">
          <span>Enter Math Problem</span>
          <span className="text-xs text-slate-500 font-normal">(Grade 10–12 Algebra, Calculus, Geometry)</span>
        </label>
        <span className="text-xs text-slate-400 flex items-center gap-1 font-mono">
          Press <kbd className="px-1.5 py-0.5 bg-slate-800 text-slate-300 rounded border border-slate-700 text-[10px]">Enter ↵</kbd> to solve, <kbd className="px-1.5 py-0.5 bg-slate-800 text-slate-300 rounded border border-slate-700 text-[10px]">Shift+Enter</kbd> for newline
        </span>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            placeholder="e.g. Find the derivative of x² sin(x) or solve 3x + 7 = 22..."
            rows={3}
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl p-4 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all resize-none font-mono text-sm"
          />
        </div>

        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2 overflow-x-auto py-1 max-w-[70%] no-scrollbar">
            <span className="text-xs text-slate-500 flex items-center gap-1 shrink-0">
              <Sparkles className="w-3 h-3 text-emerald-400" /> Demo:
            </span>
            {PRESET_EXAMPLES.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setProblem(ex)}
                disabled={isLoading}
                className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded-lg shrink-0 border border-slate-700 transition-colors truncate max-w-[200px]"
                title={ex}
              >
                {ex}
              </button>
            ))}
          </div>

          <button
            type="submit"
            disabled={isLoading || !problem.trim()}
            className="flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-600 text-white font-medium rounded-xl transition-all shadow-lg shadow-emerald-900/20 shrink-0"
          >
            <Send className="w-4 h-4" />
            <span>{isLoading ? 'Verifying...' : 'Solve & Verify'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
