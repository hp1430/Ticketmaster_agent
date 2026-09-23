export const MessageInput = ({
    disabled,
    setDisabled,
    handleSubmit,
    handleKeyDown,
    message,
    setMessage
}) => {
  

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-end gap-3 rounded-2xl border border-gray-300 bg-white p-3 shadow-sm focus-within:border-blue-500"
    >
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask your AI agent anything..."
        rows={1}
        disabled={disabled}
        className="max-h-32 min-h-10 flex-1 resize-none bg-transparent px-2 py-2 text-sm text-gray-900 outline-none placeholder:text-gray-400 disabled:cursor-not-allowed disabled:opacity-50"
        aria-label="Message input"
      />

      <button
        type="submit"
        disabled={disabled || !message.trim()}
        className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-300"
      >
        {disabled ? "Sending..." : "Send"}
      </button>
    </form>
  );
}
