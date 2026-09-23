import { useState } from "react";
import { MessageInput } from "./MessageInput";

const getBackendChatUrl = () => {
  const baseUrl =
    import.meta.env.VITE_BACKEND_ENDPOINT ||
    import.meta.env.BACKEND_ENDPOINT ||
    "";

  return `${baseUrl.replace(/\/$/, "")}/api/chat`;
};

export const MessageInputContainer = ({
  setMessages,
  threadId,
  setThreadId,
}) => {
  const [disabled, setDisabled] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    setDisabled(true);

    const newMessage = {
      id: Date.now(),
      type: "user",
      text: trimmedMessage,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prevMessages) => [...prevMessages, newMessage]);

    try {
      const body = {
        message: trimmedMessage,
      };
      if (threadId) {
        body.thread_id = threadId;
      }

      const response = await fetch(getBackendChatUrl(), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      console.log("data received:", data);
      const isApprovalRequired = data?.status === "approval_required";
      const pendingInterrupts =
        data?.pending_interrupts || data?.pending_interrupt || null;
      const assistantReply =
        data?.message ||
        data?.text ||
        (isApprovalRequired
          ? "Approval is required to continue."
          : "I received your message.");

      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now() + 1,
          type: "ai",
          text: assistantReply,
          status: data?.status,
          pendingInterrupts,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
      if (!threadId) {
        setThreadId(data.thread_id);
      }
    } catch (error) {
      console.error("Failed to send message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now() + 2,
          type: "ai",
          text: "Sorry, I could not reach the server right now.",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } finally {
      setMessage("");
      setDisabled(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <MessageInput
      disabled={disabled}
      setDisabled={setDisabled}
      handleSubmit={handleSubmit}
      handleKeyDown={handleKeyDown}
      message={message}
      setMessage={setMessage}
    />
  );
};
