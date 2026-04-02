-- ManjuFlow AI Database Schema
-- PostgreSQL 16

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- 用于全文搜索

-- ============================
-- 用户表 (Users)
-- ============================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    avatar_url VARCHAR(500),
    bio TEXT,
    subscription_tier VARCHAR(50) DEFAULT 'free', -- free, pro, enterprise
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    api_quota_used INTEGER DEFAULT 0,
    api_quota_limit INTEGER DEFAULT 1000,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_subscription ON users(subscription_tier);

-- ============================
-- 项目表 (Projects)
-- ============================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50) DEFAULT 'comic', -- comic, animation, mixed
    status VARCHAR(50) DEFAULT 'draft', -- draft, production, completed, archived
    cover_image_url VARCHAR(500),
    settings JSONB DEFAULT '{}', -- 项目自定义设置
    total_scenes INTEGER DEFAULT 0,
    total_duration_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- ============================
-- 角色表 (Characters)
-- 关键设计: 项目与角色的强关联,确保跨镜头一致性
-- ============================
CREATE TABLE characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    reference_image_url VARCHAR(500), -- 参考图 (用于 LoRA 训练)
    lora_model_path VARCHAR(500), -- 训练完成的 LoRA 模型路径
    lora_training_status VARCHAR(50) DEFAULT 'not_started', -- not_started, training, completed, failed
    lora_trained_at TIMESTAMP WITH TIME ZONE,
    face_embedding VECTOR(512), -- FaceID 面部特征向量
    style_preset VARCHAR(100), -- 风格预设
    tags TEXT[] DEFAULT '{}',
    is_main_character BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT character_project_unique UNIQUE(project_id, name)
);

CREATE INDEX idx_characters_project_id ON characters(project_id);
CREATE INDEX idx_characters_user_id ON characters(user_id);
CREATE INDEX idx_characters_lora_status ON characters(lora_training_status);
CREATE INDEX idx_characters_face_embedding ON characters USING ivfflat(face_embedding vector_cosine_ops);

-- ============================
-- 资产表 (Assets)
-- 存储背景、道具、音效等素材
-- ============================
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL, -- background, prop, audio, music, effect
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER,
    file_format VARCHAR(50),
    thumbnail_url VARCHAR(500),
    tags TEXT[] DEFAULT '{}',
    style_preset VARCHAR(100),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assets_project_id ON assets(project_id);
CREATE INDEX idx_assets_user_id ON assets(user_id);
CREATE INDEX idx_assets_type ON assets(asset_type);
CREATE INDEX idx_assets_tags ON assets USING GIN(tags);

-- ============================
-- 剧本表 (Scripts)
-- ============================
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL, -- 原始文本内容
    generated_json JSONB, -- LLM 生成的结构化 JSON
    llm_model_used VARCHAR(100),
    style_preset VARCHAR(100),
    total_scenes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scripts_project_id ON scripts(project_id);
CREATE INDEX idx_scripts_user_id ON scripts(user_id);

-- ============================
-- 分镜表 (Scenes)
-- ============================
CREATE TABLE scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id) ON DELETE SET NULL,
    scene_number INTEGER NOT NULL,
    title VARCHAR(255),
    description TEXT NOT NULL,
    camera_angle VARCHAR(50), -- wide, medium, close-up, extreme_closeup
    characters UUID[] DEFAULT '{}', -- 关联角色 IDs
    background_asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    duration_seconds DECIMAL(5,2) DEFAULT 3.0,
    dialogue TEXT,
    emotion VARCHAR(50),
    action_description TEXT,
    order_position INTEGER NOT NULL,
    image_url VARCHAR(500), -- 生成的场景图片
    image_generation_status VARCHAR(50) DEFAULT 'pending', -- pending, generating, completed, failed
    generated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT scene_project_order_unique UNIQUE(project_id, order_position)
);

CREATE INDEX idx_scenes_project_id ON scenes(project_id);
CREATE INDEX idx_scenes_script_id ON scenes(script_id);
CREATE INDEX idx_scenes_order ON scenes(project_id, order_position);
CREATE INDEX idx_scenes_image_status ON scenes(image_generation_status);

-- ============================
-- 渲染任务表 (RenderJobs)
-- 记录所有 AI 生成任务
-- ============================
CREATE TABLE render_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL, -- script_generation, image_generation, video_generation, lora_training
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed, cancelled
    celery_task_id VARCHAR(255), -- Celery 任务 ID
    progress INTEGER DEFAULT 0, -- 0-100
    error_message TEXT,
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_render_jobs_project_id ON render_jobs(project_id);
CREATE INDEX idx_render_jobs_user_id ON render_jobs(user_id);
CREATE INDEX idx_render_jobs_status ON render_jobs(status);
CREATE INDEX idx_render_jobs_job_type ON render_jobs(job_type);
CREATE INDEX idx_render_jobs_created_at ON render_jobs(created_at DESC);
CREATE INDEX idx_render_jobs_celery_task_id ON render_jobs(celery_task_id);

-- ============================
-- 时间轴轨道表 (TimelineTracks)
-- 视频编辑器的时间轴管理
-- ============================
CREATE TABLE timeline_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    track_type VARCHAR(50) NOT NULL, -- video, audio, subtitle
    track_name VARCHAR(255) NOT NULL,
    track_order INTEGER NOT NULL,
    is_visible BOOLEAN DEFAULT true,
    is_locked BOOLEAN DEFAULT false,
    volume DECIMAL(3,2) DEFAULT 1.0, -- 音量 (0-1.0)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT track_project_order_unique UNIQUE(project_id, track_type, track_order)
);

CREATE INDEX idx_timeline_tracks_project_id ON timeline_tracks(project_id);
CREATE INDEX idx_timeline_tracks_type ON timeline_tracks(track_type);

-- ============================
-- 时间轴剪辑片段表 (TimelineClips)
-- ============================
CREATE TABLE timeline_clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    track_id UUID NOT NULL REFERENCES timeline_tracks(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    scene_id UUID REFERENCES scenes(id) ON DELETE SET NULL,
    asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    clip_type VARCHAR(50) NOT NULL, -- video, audio, subtitle
    name VARCHAR(255),
    start_time DECIMAL(10,2) NOT NULL, -- 轨道上的开始时间 (秒)
    duration DECIMAL(10,2) NOT NULL, -- 持续时间 (秒)
    source_start_time DECIMAL(10,2) DEFAULT 0.0, -- 源素材的开始时间
    source_end_time DECIMAL(10,2), -- 源素材的结束时间
    in_point DECIMAL(10,2) DEFAULT 0.0, -- 入点
    out_point DECIMAL(10,2), -- 出点
    speed DECIMAL(3,2) DEFAULT 1.0, -- 播放速度
    volume DECIMAL(3,2) DEFAULT 1.0, -- 音量 (0-1.0)
    opacity DECIMAL(3,2) DEFAULT 1.0, -- 不透明度 (0-1.0)
    transition_type VARCHAR(50), -- fade, dissolve, wipe
    transition_duration DECIMAL(5,2) DEFAULT 0.5,
    effects JSONB DEFAULT '[]', -- 特效列表
    is_locked BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timeline_clips_track_id ON timeline_clips(track_id);
CREATE INDEX idx_timeline_clips_project_id ON timeline_clips(project_id);
CREATE INDEX idx_timeline_clips_start_time ON timeline_clips(start_time);

-- ============================
-- 导出任务表 (ExportJobs)
-- ============================
CREATE TABLE export_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    export_format VARCHAR(50) DEFAULT 'mp4', -- mp4, mov, webm
    resolution VARCHAR(50) DEFAULT '1080p', -- 720p, 1080p, 4k
    frame_rate INTEGER DEFAULT 30, -- 24, 30, 60
    aspect_ratio VARCHAR(20) DEFAULT '16:9', -- 16:9, 9:16, 1:1
    quality VARCHAR(50) DEFAULT 'high', -- low, medium, high
    output_file_url VARCHAR(500),
    output_file_size INTEGER,
    duration_seconds INTEGER,
    thumbnail_url VARCHAR(500),
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_export_jobs_project_id ON export_jobs(project_id);
CREATE INDEX idx_export_jobs_user_id ON export_jobs(user_id);
CREATE INDEX idx_export_jobs_status ON export_jobs(status);

-- ============================
-- 触发器: 自动更新 updated_at
-- ============================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表添加 updated_at 触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_characters_updated_at BEFORE UPDATE ON characters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scripts_updated_at BEFORE UPDATE ON scripts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scenes_updated_at BEFORE UPDATE ON scenes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_render_jobs_updated_at BEFORE UPDATE ON render_jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_timeline_tracks_updated_at BEFORE UPDATE ON timeline_tracks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_timeline_clips_updated_at BEFORE UPDATE ON timeline_clips
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_export_jobs_updated_at BEFORE UPDATE ON export_jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================
-- 插入测试数据
-- ============================
INSERT INTO users (email, username, password_hash, full_name, is_verified) VALUES
('demo@manjuflow.ai', 'demo', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7B9J9a2.4m', 'Demo User', true)
ON CONFLICT (email) DO NOTHING;

-- ============================
-- 完成
-- ============================
