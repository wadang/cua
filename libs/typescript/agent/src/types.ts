// Request types matching the Python proxy API
export interface AgentRequest {
  model: string;
  input: string | AgentMessage[];
  agent_kwargs?: {
    save_trajectory?: boolean;
    verbosity?: number;
    [key: string]: any;
  };
  computer_kwargs?: {
    os_type?: string;
    provider_type?: string;
    [key: string]: any;
  };
}

// Multi-modal message types
export interface AgentMessage {
  role: 'user' | 'assistant';
  content: AgentContent[];
}

export interface AgentContent {
  type: 'input_text' | 'input_image';
  text?: string;
  image_url?: string;
}

// Response types
export interface AgentResponse {
  success: boolean;
  result?: any;
  model: string;
  error?: string;
}

// Connection types
export type ConnectionType = 'http' | 'https' | 'peer';

export interface AgentClientOptions {
  timeout?: number;
  retries?: number;
}
