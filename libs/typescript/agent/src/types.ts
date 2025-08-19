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

// Agent message types - can be one of several different message types
export type AgentMessage = 
  | UserMessage
  | AssistantMessage
  | ReasoningMessage
  | ComputerCallMessage
  | ComputerCallOutputMessage;

// User input message
export interface UserMessage {
  role: 'user';
  content: string;
}

// Assistant response message
export interface AssistantMessage {
  type: 'message';
  role: 'assistant';
  content: OutputContent[];
}

// Reasoning/thinking message
export interface ReasoningMessage {
  type: 'reasoning';
  summary: SummaryContent[];
}

// Computer action call
export interface ComputerCallMessage {
  type: 'computer_call';
  call_id: string;
  status: 'completed' | 'failed' | 'pending';
  action: ComputerAction;
}

// Computer action output (usually screenshot)
export interface ComputerCallOutputMessage {
  type: 'computer_call_output';
  call_id: string;
  output: InputContent;
}

// Content types
export interface OutputContent {
  type: 'output_text';
  text: string;
}

export interface SummaryContent {
  type: 'summary_text';
  text: string;
}

export interface InputContent {
  type: 'input_image' | 'input_text';
  text?: string;
  image_url?: string;
}

// Computer action types
export type ComputerAction = 
  | ClickAction
  | TypeAction
  | KeyAction
  | ScrollAction
  | WaitAction;

export interface ClickAction {
  type: 'click';
  coordinate: [number, number];
}

export interface TypeAction {
  type: 'type';
  text: string;
}

export interface KeyAction {
  type: 'key';
  key: string;
}

export interface ScrollAction {
  type: 'scroll';
  coordinate: [number, number];
  direction: 'up' | 'down' | 'left' | 'right';
}

export interface WaitAction {
  type: 'wait';
  seconds?: number;
}

// Usage information
export interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  response_cost: number;
}

// Response types
export interface AgentResponse {
  output: AgentMessage[];
  usage: Usage;
}

// Connection types
export type ConnectionType = 'http' | 'https' | 'peer';

export interface AgentClientOptions {
  timeout?: number;
  retries?: number;
}
