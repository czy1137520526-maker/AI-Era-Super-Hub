"use client";

import { memo } from "react";
import { Handle, Position, NodeProps } from "reactflow";

function ImageGenNode({ data }: NodeProps) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-purple-500 border-2 border-purple-600 min-w-[200px]">
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
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <div className="font-bold text-white">{data.label}</div>
      </div>

      <div className="bg-white/20 rounded p-2 mb-2">
        <p className="text-xs text-white/80">
          宽度: {data.width || 1024}px
        </p>
        <p className="text-xs text-white/80">
          高度: {data.height || 1024}px
        </p>
      </div>

      <div className="text-xs text-white/90">
        ComfyUI 图像生成
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(ImageGenNode);
