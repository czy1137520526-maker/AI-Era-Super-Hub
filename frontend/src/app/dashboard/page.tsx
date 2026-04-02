"use client";

import React, { useState, useEffect } from "react";
import { Plus, FolderOpen, Settings } from "lucide-react";
import Link from "next/link";

interface Project {
  id: number;
  name: string;
  description?: string;
  status: string;
  created_at: string;
}

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  // TODO: Fetch projects from API
  useEffect(() => {
    // Mock data for now
    setTimeout(() => {
      setProjects([
        {
          id: 1,
          name: "示例项目 1",
          description: "我的第一个漫剧项目",
          status: "active",
          created_at: "2024-01-15",
        },
      ]);
      setLoading(false);
    }, 500);
  }, []);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">漫剧智造局</h1>
          <div className="flex items-center gap-4">
            <Link href="/dashboard/projects">
              <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
                <FolderOpen className="w-4 h-4" />
                项目列表
              </button>
            </Link>
            <button className="p-2 hover:bg-muted rounded-md transition-colors">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold">欢迎回来!</h2>
            <p className="text-muted-foreground mt-2">创建您的下一个漫剧杰作</p>
          </div>
          <Link href="/dashboard/projects/new">
            <button className="flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
              <Plus className="w-5 h-5" />
              新建项目
            </button>
          </Link>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-card border rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">活跃项目</h3>
            <p className="text-4xl font-bold">{projects.length}</p>
          </div>
          <div className="bg-card border rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">已完成场景</h3>
            <p className="text-4xl font-bold">0</p>
          </div>
          <div className="bg-card border rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-2">渲染任务</h3>
            <p className="text-4xl font-bold">0</p>
          </div>
        </div>

        {/* Recent Projects */}
        <div className="bg-card border rounded-lg">
          <div className="p-6 border-b">
            <h3 className="text-xl font-bold">最近项目</h3>
          </div>
          {loading ? (
            <div className="p-6 text-center text-muted-foreground">加载中...</div>
          ) : projects.length === 0 ? (
            <div className="p-12 text-center">
              <FolderOpen className="w-16 h-16 mx-auto mb-4 text-muted-foreground/50" />
              <p className="text-muted-foreground mb-4">还没有项目</p>
              <Link href="/dashboard/projects/new">
                <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md">
                  创建第一个项目
                </button>
              </Link>
            </div>
          ) : (
            <div className="divide-y">
              {projects.map((project) => (
                <Link
                  key={project.id}
                  href={`/dashboard/projects/${project.id}`}
                  className="block p-6 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-lg font-semibold">{project.name}</h4>
                      <p className="text-muted-foreground mt-1">{project.description}</p>
                    </div>
                    <div className="text-right">
                      <span className="inline-flex px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        {project.status}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
