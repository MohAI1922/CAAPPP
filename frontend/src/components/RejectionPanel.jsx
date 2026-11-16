import React from 'react';
import { AlertTriangle, XCircle, ShieldAlert, Ban } from 'lucide-react';

export default function RejectionPanel({ result }) {
  if (!result || (result.status !== 'REJECTED' && result.status !== 'UNSUPPORTED' && result.status !== 'ERROR')) {
    return null;
  }

  const isUnsupported = result.status === 'UNSUPPORTED';

  return (
    <div className={`border rounded-2xl p-6 shadow-2xl space-y-4 ${
      isUnsupported
        ? 'bg-amber-950/20 border-amber-500/40'
        : 'bg-rose-950/20 border-rose-500/40'
    }`}>
      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-xl border ${
          isUnsupported
            ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
            : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
        }`}>
          {isUnsupported ? <Ban className="w-6 h-6" /> : <ShieldAlert className="w-6 h-6" />}
        </div>
        <div>
          <h2 className={`text-lg font-bold ${isUnsupported ? 'text-amber-200' : 'text-rose-200'}`}>
            {isUnsupported ? 'Outside Verified Domain (Refusal)' : 'Verification Failed (Hallucination Rejection)'}
          </h2>
          <span className="text-xs text-slate-400">
            {isUnsupported
              ? 'VeriMath refuses to answer unverifiable inputs to guarantee absolute reliability.'
              : 'The proposed answer could not be proved mathematically and has been safely intercepted.'}
          </span>
        </div>
      </div>

      <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-sm text-slate-300 leading-relaxed font-mono">
        {result.rejection_reason || 'Verification was unsuccessful. Please check your problem syntax.'}
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80">
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-rose-500 inline-block animate-ping"></span>
          Student protected from unverified AI hallucinations.
        </span>
        <span className="font-mono text-slate-500">Latency: {result.elapsed_ms} ms</span>
      </div>
    </div>
  );
}
