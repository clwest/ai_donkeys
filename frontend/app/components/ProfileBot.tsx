"use client";
import { useState } from "react";

export default function ProfileBot() {
  const [theInput, setTheInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello, I'm DonkeyBot. How can I help you today?",
    },
  ]);

  const callGetResponse = async () => {
    setIsLoading(true);
    let temp = messages;
    temp.push({ role: "user", content: theInput });
    setMessages(temp);
    setTheInput("");
    console.log("Calling OpenAI API");

    const response = await fetch("/api", {
      method: "POST",
      headers: {
        "Conente-Type": "application/json",
      },
      body: JSON.stringify({ messages }),
    });

    const data = await response.json();
    const { output } = data;
    console.log("OpenAI Replied...", output.content);

    setMessages((prevMessages) => [...prevMessages, output]);
    setIsLoading(false);
  };

  const Submit = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      callGetResponse();
    }
  };

  return (
    <main className="flex flex-col items-center justify-between min-h-screen px-24 py-5">
      <h1 className="p-5 text-4xl italic font-extrabold text-center text-slate-400">
        Donkey Bot
      </h1>
      <div className="flex h-[35rem] w-[40rem] flex-col items=center bg-gray-600 rounded-xl">
        <div className="flex flex-col w-full h-full gap-2 px-3 py-8 overflow-y-auto">
          {messages.map((e) => {
            return (
              <div
                key={e.content}
                className={`w-max max-w-[18rem] rounded-md px-4 py-3 l-min ${
                  e.role === "assistant"
                    ? "self=start text-goldenrod-800"
                    : "self-end bg-gray-800 bg-goldenrod-500"
                }`}
              >
                {e.content}
              </div>
            );
          })}

          {isLoading ? (
            <div className="self-start text-goldenrod-500 w-max max-w-[18rem] rounded-md px-4 py-3 h-min">
              ***Thinking***
            </div>
          ) : (
            ""
          )}
        </div>
        <div className="relative w-[80%] bottom-4 flex justify-center">
          <textarea
            value={theInput}
            onChange={(event) => setTheInput(event.target.value)}
            className="w-[85%] h-10 px-3 py-2 resize-none overflow-y-auto bg-gray-200 rounded-xl"
            onKeyDown={Submit}
          />
          <button
            onClick={callGetResponse}
            className="w-[15%] bg-goldenrod-500 px-4 py-2 rounded-sm"
          >
            send
          </button>
        </div>
      </div>
      <div></div>
    </main>
  );
}
