import { useState } from "react";
import { MessageContainer } from "../Message/MessageContainer";
import { MessageInputContainer } from "../MessageInput/MessageInputContainer";

export const Home = () => {
  const [messages, setMessages] = useState([]);
  const [threadId, setThreadId] = useState(null);
  const [approvingMessageId, setApprovingMessageId] = useState(null);

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
              messageId={message.id}
              type={message.type}
              text={message.text}
              status={message.status}
              pendingInterrupts={message.pendingInterrupts}
              decision={message.decision}
              approvalDisabled={approvingMessageId !== null}
              setMessages={setMessages}
              threadId={threadId}
              setThreadId={setThreadId}
              setApprovingMessageId={setApprovingMessageId}
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
              threadId={threadId}
              setThreadId={setThreadId}
            />
          </div>
        </div>
      </main>
    </div>
  );
};
