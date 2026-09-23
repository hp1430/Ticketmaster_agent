import { useState } from "react";
import { MessageContainer } from "../Message/MessageContainer";
import { MessageInputContainer } from "../MessageInput/MessageInputContainer";

export const Home = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "ai",
      text: "Hi! I can help you find concerts, events, and tickets that match your interests.",
      timestamp: "09:41 AM",
    },
    {
      id: 2,
      type: "user",
      text: "Show me live jazz events happening this weekend in New York.",
      timestamp: "09:42 AM",
    },
  ]);

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      {/* Header */}
      <header className="flex w-full items-center justify-center border-b bg-white px-6 py-4">
        <h1 className="text-center text-xl font-bold text-gray-900">
          Ticketmaster Agent
        </h1>
      </header>

      {/* Chat Area */}
      <main className="flex flex-1 flex-col">
        <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-6 py-6">
          {messages.map((message) => (
            <MessageContainer
              key={message.id}
              type={message.type}
              text={message.text}
              timestamp={message.timestamp}
              name={message.name}
            />
          ))}
        </div>

        {/* Message Input - Bottom Center */}
        <div className="w-full px-6 pb-6">
          <div className="mx-auto w-full max-w-3xl">
            <MessageInputContainer
              messages={messages}
              setMessages={setMessages}
            />
          </div>
        </div>
      </main>
    </div>
  );
};
