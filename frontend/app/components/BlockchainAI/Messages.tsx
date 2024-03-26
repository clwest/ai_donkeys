import React, { useEffect, useRef } from "react";
import { ChatMessage } from "./utils";
import { useAuth } from "../../contexts/AuthContext";
// import hljs from "highlight.js";
// import "highlight.js/styles/foundation.css";
// import "./BlockchainAIStyles.css";

export default function Messages({ messages }: { messages: ChatMessage[] }) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    // hljs.highlightAll();
  }, [messages]);

  // Function to format message content
  const formatContent = (content: string) => {
    // Split content by line and then process each line
    return content.split("\n").map((line, index) => {
      // Check for code block start
      if (line.startsWith("```")) {
        // Extract language
        const language = line.substring(3).trim();
        // Find the end of the code block
        const endIndex = content.indexOf("```", index + 1);
        const codeBlock = content.substring(index, endIndex).trim();

        // Skip further processing of lines until the end of the code block
        index = endIndex;

        // Return formatted code block
        return (
          <pre
            key={index}
            className="flex flex-col bg-slate-600 text-cyan-300 p-3 overflow-x-auto"
          >
            <code className={`language-${language} flex`}>{codeBlock}</code>
          </pre>
        );
      }

      // Check for list items (numbered)
      if (line.match(/^\d+\./)) {
        return (
          <li key={index}>{line.substring(line.indexOf(".") + 1).trim()}</li>
        );
      }

      // Default to regular paragraph
      return (
        <p key={index} className="mb-2">
          {line}
        </p>
      );
    });
  };

  return (
    <div className="border-2 border-gray-600 p-6 rounded-lg overflow-y-scroll flex-grow flex flex-col justify-center bg-slate-400">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`${
            msg.role === "ai" ? "text-green-500" : "text-cyan-300"
          } my-2 p-3 rounded shadow-md hover:shadow-lg transition-shadow duration-200 flex slide-in-bottom bg-slate-400 border border-gray-600 message-glow`}
        >
          <div className="rounded-tl-lg bg-slate-400 p-2 border-r border-gray-600 flex items-center">
            {msg.role === "ai" ? "🤖" : "🧑‍💻"}
          </div>
          <div className="ml-2 flex flex-col p-5">
            {formatContent(msg.content)}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

