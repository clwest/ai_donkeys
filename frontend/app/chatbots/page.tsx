"use client";
import React, { useState } from "react";
import ChatInput from "../components/BlockchainAI/ChatInput"; // Adjust the path as per your project structure
import Messages from "../components/BlockchainAI/Messages";
import { Card } from "../components/BlockchainAI/Card";
import { ChatMessage, ChatResponse } from "../components/BlockchainAI/utils"; // Adjust the path as per your project structure

const BlockchainChatPage = () => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [chatResponse, setChatResponse] = useState<ChatResponse | null>(null);
  const [topicName, setTopicName] = useState("default_topic");

  const updateChatHistory = (newHistory: ChatMessage[]) => {
    setChatHistory(newHistory);
  };

  // Handle the chat response from ChatBox component
  const handleChatResponse = (response: ChatResponse) => {
    console.log("Before updating chat history:", chatHistory);
    const newChatHistory = setChatHistory([
      ...chatHistory,
      { content: response.answer, role: "ai" },
    ]);
    console.log("After updating chat history:", newChatHistory);
    // setChatHistory(newChatHistory);
    setChatResponse(response);
  };

  console.log("Chat history in BlockchainChatPage:", chatHistory);
  return (
    <div className="blockchain-chat-page">
      <header>
        <div className="flex items-center justify-between w-full h-16 mt-5"></div>
      </header>

      <Messages messages={chatHistory} />

      <ChatInput
        onChatResponse={handleChatResponse}
        chatHistory={chatHistory}
        updateChatHistory={updateChatHistory}
        topicName={topicName}
      />
    </div>
  );
};

export default BlockchainChatPage;
