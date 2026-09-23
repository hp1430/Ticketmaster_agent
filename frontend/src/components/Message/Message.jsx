export const Message = ({ type = "ai", text, timestamp, name }) => {
  const isUser = type === "user";

  return (
    <div className={`mb-4 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl border px-4 py-3 shadow-sm backdrop-blur-sm ${
          isUser
            ? "border-blue-200 bg-blue-50 text-blue-950"
            : "border-emerald-200 bg-emerald-50 text-emerald-950"
        }`}
      >
        <div className="mb-1 flex items-center justify-between gap-3 text-[10px] font-semibold uppercase tracking-[0.12em]">
          <span className={isUser ? "text-blue-700" : "text-emerald-700"}>
            {name || (isUser ? "You" : "AI Assistant")}
          </span>
          {timestamp && (
            <span
              className={isUser ? "text-blue-600/80" : "text-emerald-600/80"}
            >
              {timestamp}
            </span>
          )}
        </div>

        <p className="whitespace-pre-wrap text-sm leading-6 text-current">
          {text}
        </p>
      </div>
    </div>
  );
};
