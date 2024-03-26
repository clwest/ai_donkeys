import React, { useState, useEffect } from "react";
import { sendChatQuery, ChatResponse, ChatMessage } from "./utils";

interface ChatInputProps {
  onChatResponse: (response: ChatResponse) => void;
  chatHistory: ChatMessage[];
  topicName: string;
  updateChatHistory: (newHistory: ChatMessage[]) => void;
}

export default function ChatInput({
  onChatResponse,
  chatHistory,
  topicName,
  updateChatHistory,
}: ChatInputProps) {
  const [query, setQuery] = useState("");

  const handleSend = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const responseData = await sendChatQuery(query, chatHistory, topicName);
      console.log("Reponse Data:", responseData);
      const updatedChatHistory = [
        ...chatHistory,
        { content: query, role: "user" as const }, // const ensures 'role' is treated as a literal type
        { content: responseData.answer, role: "ai" as const },
      ];
      onChatResponse(responseData);
      updateChatHistory(updatedChatHistory);
      setQuery("");
    } catch (e) {
      console.error("Error in Chatbox ", e);
    }
    console.log("Chat history in ChatBox:", chatHistory);
  };

  useEffect(() => {
    console.log("Chat history in ChatBox:", chatHistory);
  }, [chatHistory]);

  return (
    <div id="chat" className="flex flex-col items-center">
      <>
        <form
          onSubmit={handleSend}
          className="mt-5 mb-5 relative bg-gray-700 rounded-lg"
        >
          <input
            type="text"
            className=" appearance-none border rounded py-2 px-3 text-gray-200 leading-tight focus:outline-none focus:shadow-outline pl-3 pr-10 bg-gray-600 border-gray-600 transition-shadow duration-200"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div>
            <span className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-400">
              Press ⮐ to send
            </span>
          </div>
        </form>
      </>
    </div>
  );
}
