import { useState } from "react";
import { MessageInput } from "./MessageInput";

export const MessageInputContainer = ({ setMessages }) => {
  const [disabled, setDisabled] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

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
    setMessage("");
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
