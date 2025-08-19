// Export the main AgentClient class as default
export { AgentClient as default } from './client.js';

// Also export as named export for flexibility
export { AgentClient } from './client.js';

// Export types for TypeScript users
export type {
  AgentRequest,
  AgentResponse,
  AgentMessage,
  AgentContent,
  ConnectionType,
  AgentClientOptions,
} from './types.js';
