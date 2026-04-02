"use client";

import React, { useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, Save, Play, FileText, Users, Film, Settings } from "lucide-react";
import Link from "next/link";
import WorkflowEditor from "@/components/workflow/WorkflowEditor";

export default function ProjectPage() {
  const params = useParams();
  const projectId = Number(params.id);
  const [activeTab, setActiveTab] = useState("workflow");

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/dashboard">
                <button className="p-2 hover:bg-muted rounded-md transition-colors">
                  <ArrowLeft className="w-5 h-5" />
                </button>
              </Link>
              <div>
                <h1 className="text-2xl font-bold">漫剧项目 #{projectId}</h1>
                <p className="text-sm text-muted-foreground">AI驱动的全流程制作</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
                <Save className="w-4 h-4" />
                保存
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
                <Play className="w-4 h-4" />
                执行
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-4">
          <nav className="flex gap-6">
            <button
              onClick={() => setActiveTab("workflow")}
              className={`py-4 px-2 border-b-2 font-medium transition-colors ${
                activeTab === "workflow"
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                工作流编辑器
              </div>
            </button>
            <button
              onClick={() => setActiveTab("script")}
              className={`py-4 px-2 border-b-2 font-medium transition-colors ${
                activeTab === "script"
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                剧本与分镜
              </div>
            </button>
            <button
              onClick={() => setActiveTab("characters")}
              className={`py-4 px-2 border-b-2 font-medium transition-colors ${
                activeTab === "characters"
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                角色管理
              </div>
            </button>
            <button
              onClick={() => setActiveTab("editor")}
              className={`py-4 px-2 border-b-2 font-medium transition-colors ${
                activeTab === "editor"
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <div className="flex items-center gap-2">
                <Film className="w-4 h-4" />
                视频编辑
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <main className="container mx-auto px-4 py-6">
        {activeTab === "workflow" && (
          <WorkflowEditor projectId={projectId} />
        )}
        {activeTab === "script" && (
          <div className="text-center py-12 text-muted-foreground">
            <FileText className="w-16 h-16 mx-auto mb-4" />
            <p>剧本与分镜编辑器 - 开发中</p>
          </div>
        )}
        {activeTab === "characters" && (
          <div className="text-center py-12 text-muted-foreground">
            <Users className="w-16 h-16 mx-auto mb-4" />
            <p>角色管理中心 - 开发中</p>
          </div>
        )}
        {activeTab === "editor" && (
          <div className="text-center py-12 text-muted-foreground">
            <Film className="w-16 h-16 mx-auto mb-4" />
            <p>视频非线性编辑器 - 开发中</p>
          </div>
        )}
      </main>
    </div>
  );
}
