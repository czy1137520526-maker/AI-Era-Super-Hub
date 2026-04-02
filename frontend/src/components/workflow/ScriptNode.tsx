"use client";

import { memo } from "react";
import { Handle, Position, NodeProps } from "reactflow";

function ScriptNode({ data }: NodeProps) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-blue-500 border-2 border-blue-600 min-w-[200px]">
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
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <div className="font-bold text-white">{data.label}</div>
      </div>

      <div className="bg-white/20 rounded p-2 mb-2">
        <p className="text-xs text-white/80">
          场景数量: {data.scenes?.length || 0}
        </p>
      </div>

      <div className="text-xs text-white/90">
        AI 剧本生成引擎
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(ScriptNode);
