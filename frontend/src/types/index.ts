// Type definitions for frontend

export interface User {
  id: number;
  email: string;
  username: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  user_id: number;
  name: string;
  description?: string;
  status: string;
  style_preset?: string;
  created_at: string;
  updated_at: string;
}

export interface Character {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  role: string;
  lora_model_path?: string;
  is_trained: boolean;
  created_at: string;
  updated_at: string;
}

export interface Scene {
  id: number;
  project_id: number;
  scene_number: number;
  description: string;
  characters?: string[];
  emotion?: string;
  camera_angle?: string;
  dialogue?: Dialogue[];
  duration_seconds: number;
  generated_image_url?: string;
  generated_video_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Dialogue {
  speaker: string;
  text: string;
  emotion?: string;
}

export interface RenderJob {
  id: number;
  project_id: number;
  scene_id?: number;
  character_id?: number;
  job_type: string;
  status: string;
  progress: number;
  parameters?: Record<string, any>;
  result_url?: string;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface Asset {
  id: number;
  project_id: number;
  character_id?: number;
  asset_type: string;
  name: string;
  description?: string;
  file_path: string;
  file_url?: string;
  metadata?: Record<string, any>;
  created_at: string;
}
