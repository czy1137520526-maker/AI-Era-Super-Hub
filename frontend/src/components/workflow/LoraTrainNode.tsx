"use client";

import { memo } from "react";
import { Handle, Position, NodeProps } from "reactflow";

function LoraTrainNode({ data }: NodeProps) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-orange-500 border-2 border-orange-600 min-w-[200px]">
      <Handle type="target" position={Position.Top} />

      <div className="flex items-center gap-2 mb-2">
        <svg
          className="w-5 h-5 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
          />
        </svg>
        <div className="font-bold text-white">{data.label}</div>
      </div>

      <div className="bg-white/20 rounded p-2 mb-2">
        <p className="text-xs text-white/80">
          训练轮数: {data.epochs || 100}
        </p>
        <p className="text-xs text-white/80">
          学习率: {data.learningRate || 0.0001}
        </p>
      </div>

      <div className="text-xs text-white/90">
        LoRA 角色一致性训练
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(LoraTrainNode);
