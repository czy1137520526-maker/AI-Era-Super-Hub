"use client";

import React, { useCallback, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  Connection,
  Edge,
  Node,
  useNodesState,
  useEdgesState,
  NodeTypes,
} from "reactflow";
import "reactflow/dist/style.css";

// Node Types
import { ScriptNode } from "./ScriptNode";
import { ImageGenNode } from "./ImageGenNode";
import { VideoGenNode } from "./VideoGenNode";
import { LoraTrainNode } from "./LoraTrainNode";

const nodeTypes: NodeTypes = {
  script: ScriptNode,
  imageGen: ImageGenNode,
  videoGen: VideoGenNode,
  loraTrain: LoraTrainNode,
};

// Initial nodes for template workflow
const initialNodes: Node[] = [
  {
    id: "1",
    type: "script",
    position: { x: 250, y: 50 },
    data: { label: "剧本生成", scenes: [] },
  },
  {
    id: "2",
    type: "loraTrain",
    position: { x: 50, y: 200 },
    data: { label: "角色训练" },
  },
  {
    id: "3",
    type: "imageGen",
    position: { x: 250, y: 200 },
    data: { label: "图像生成" },
  },
  {
    id: "4",
    type: "videoGen",
    position: { x: 450, y: 200 },
    data: { label: "视频生成" },
  },
];

const initialEdges: Edge[] = [
  { id: "e1-3", source: "1", target: "3", animated: true },
  { id: "e2-3", source: "2", target: "3", animated: true },
  { id: "e3-4", source: "3", target: "4", animated: true },
];

export interface WorkflowEditorProps {
  projectId?: number;
  onSave?: (nodes: Node[], edges: Edge[]) => void;
  onExecute?: () => void;
}

export default function WorkflowEditor({
  projectId,
  onSave,
  onExecute,
}: WorkflowEditorProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [isExecuting, setIsExecuting] = useState(false);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleSave = useCallback(() => {
    if (onSave) {
      onSave(nodes, edges);
    }
  }, [nodes, edges, onSave]);

  const handleExecute = useCallback(async () => {
    setIsExecuting(true);
    try {
      if (onExecute) {
        await onExecute();
      }
    } finally {
      setIsExecuting(false);
    }
  }, [onExecute]);

  return (
    <div className="w-full h-[800px] bg-slate-900 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap nodeColor="#60a5fa" />
      </ReactFlow>

      {/* Action Bar */}
      <div className="absolute top-4 right-4 flex gap-2">
        <button
          onClick={handleSave}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        >
          保存工作流
        </button>
        <button
          onClick={handleExecute}
          disabled={isExecuting}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 transition-colors"
        >
          {isExecuting ? "执行中..." : "执行工作流"}
        </button>
      </div>

      {/* Template Selector */}
      <div className="absolute bottom-4 left-4 p-4 bg-slate-800 rounded-md shadow-lg">
        <h3 className="text-white font-semibold mb-2">工作流模板</h3>
        <div className="space-y-2">
          <button
            onClick={() => {
              setNodes(initialNodes);
              setEdges(initialEdges);
            }}
            className="block w-full text-left px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-md transition-colors"
          >
            标准漫剧制作流程
          </button>
          <button
            onClick={() => {
              // Custom template for character-focused workflow
              setNodes([
                {
                  id: "1",
                  type: "loraTrain",
                  position: { x: 250, y: 50 },
                  data: { label: "角色训练" },
                },
                {
                  id: "2",
                  type: "imageGen",
                  position: { x: 250, y: 200 },
                  data: { label: "图像生成" },
                },
              ]);
              setEdges([
                { id: "e1-2", source: "1", target: "2", animated: true },
              ]);
            }}
            className="block w-full text-left px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-md transition-colors"
          >
            角色一致性流程
          </button>
        </div>
      </div>
    </div>
  );
}
