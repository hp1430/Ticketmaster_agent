import { useState } from "react";
import { MessageInput } from "./MessageInput";

export const MessageInputContainer = () => {
  const [message, setMessage] = useState("");
  const [disabled, setDisabled] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

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
  )
};