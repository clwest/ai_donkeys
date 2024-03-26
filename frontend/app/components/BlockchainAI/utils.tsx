const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;

export interface ChatMessage {
  content: string;
  role: "user" | "ai";
}

export interface ChatResponse {
  question: string;
  chat_history: Array<ChatMessage>;
  topic_name: string;
  answer: string;
}

export async function sendChatQuery(
  query: string,
  chatHistory: ChatMessage[],
  topicName: string
): Promise<ChatResponse> {
  try {
    const token = localStorage.getItem("userToken");
    console.log("Token:", token);
    const response = await fetch(`${API_URL}/users/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        query,
        chat_history: chatHistory,
        topic_name: topicName,
      }),
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    console.log("Response from sendChatQuery:", response);
    return response.json();
  } catch (error) {
    console.log("Error in sendChatQuery:", error);
  }
}
