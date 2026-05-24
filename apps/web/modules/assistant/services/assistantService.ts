import { api, type AssistantChatResult } from "../../../lib/api";

export async function sendAssistantMessage(token: string, message: string): Promise<AssistantChatResult> {
  return api.assistantChat(token, message);
}
