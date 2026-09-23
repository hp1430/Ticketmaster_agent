import { Message } from "./Message";

export const MessageContainer = ({ type = "ai", text, timestamp, name }) => {
  const normalizedType = type === "user" ? "user" : "ai";

  return (
    <Message
      type={normalizedType}
      text={text}
      timestamp={timestamp}
      name={name}
    />
  );
};
