"use client";

import { memo } from "react";
import { Handle, Position, NodeProps } from "reactflow";

function VideoGenNode({ data }: NodeProps) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-green-500 border-2 border-green-600 min-w-[200px]">
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
            d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
          />
        </svg>
        <div className="font-bold text-white">{data.label}</div>
      </div>

      <div className="bg-white/20 rounded p-2 mb-2">
        <p className="text-xs text-white/80">
          时长: {data.duration || 3.0}s
        </p>
        <p className="text-xs text-white/80">
          FPS: {data.fps || 24}
        </p>
      </div>

      <div className="text-xs text-white/90">
        LTX-2.3 视频生成
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(VideoGenNode);
