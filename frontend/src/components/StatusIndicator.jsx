import React from 'react';
import { CheckCircle2, ShieldCheck, Cpu, ArrowRight, Loader2 } from 'lucide-react';

const STAGES = [
  { id: 'classify', label: 'Domain Classification' },
  { id: 'solve', label: 'LLM Candidate Solver' },
  { id: 'formalize', label: 'Constrained Formalizer' },
  { id: 'judge', label: 'Faithfulness Judge' },
  { id: 'verify', label: 'Lean 4 Kernel Oracle' },
  { id: 'explain', label: 'Intuitive Explainer' },
];

export default function StatusIndicator({ isLoading, currentStage }) {
  if (!isLoading) return null;

  return (
    <div className="bg-slate-900/90 border border-emerald-500/30 rounded-2xl p-5 my-6 shadow-2xl backdrop-blur-md animate-pulse">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2.5">
          <Loader2 className="w-5 h-5 text-emerald-400 animate-spin" />
          <span className="font-semibold text-slate-200 text-sm">
            Executing VeriMath Verification Pipeline...
          </span>
        </div>
        <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2.5 py-0.5 rounded-full">
          Zero-Trust Formal Verification
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
        {STAGES.map((stage, idx) => (
          <div
            key={stage.id}
            className={`flex flex-col p-2.5 rounded-xl border text-center transition-all ${
              idx <= (currentStage ?? 4)
                ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
                : 'bg-slate-950/40 border-slate-800 text-slate-600'
            }`}
          >
            <div className="flex items-center justify-center gap-1 text-[11px] font-mono mb-1">
              <span>Step {idx + 1}</span>
            </div>
            <span className="text-xs font-medium truncate">{stage.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
