import { Message } from "./Message";

export const MessageContainer = ({
  messageId,
  type = "ai",
  text,
  status,
  pendingInterrupts,
  decision,
  approvalDisabled,
  setMessages,
  threadId,
  setThreadId,
  setApprovingMessageId,
  timestamp,
  name,
}) => {
  const normalizedType = type === "user" ? "user" : "ai";
  const handleApprovalDecision = async (selectedDecision) => {
    console.log("selected decision: ", selectedDecision);
    console.log("thread_id is: ", threadId);
    console.log("approvalDisabled: ", approvalDisabled);
    if (!threadId || approvalDisabled) {
      return;
    }
    console.log("line 24");

    const actionRequests = pendingInterrupts?.action_requests || [];
    const decisions = (actionRequests.length > 0 ? actionRequests : [null]).map(
      () => ({ type: selectedDecision }),
    );
    const baseUrl =
      import.meta.env.VITE_BACKEND_ENDPOINT ||
      import.meta.env.BACKEND_ENDPOINT ||
      "";

    setApprovingMessageId(messageId);

    try {
        console.log("Going to hit the approve api with: ", threadId, decisions);
      const response = await fetch(
        `${baseUrl.replace(/\/$/, "")}/api/chat/approve`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            thread_id: threadId,
            decisions,
          }),
        },
      );

      if (!response.ok) {
        throw new Error(
          `Approval request failed with status ${response.status}`,
        );
      }

      const data = await response.json();
      console.log("Got data: ", data);
      setMessages((prevMessages) => [
        ...prevMessages.map((message) =>
          message.id === messageId
            ? { ...message, decision: selectedDecision }
            : message,
        ),
        {
          id: Date.now(),
          type: "ai",
          text:
            data?.message ||
            data?.text ||
            `Request ${selectedDecision === "approve" ? "approved" : "rejected"}.`,
          status: data?.status,
          pendingInterrupts:
            data?.pending_interrupts || data?.pending_interrupt || null,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);

      if (data?.thread_id) {
        setThreadId(data.thread_id);
      }
    } catch (error) {
      console.error("Failed to submit approval decision:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          id: Date.now(),
          type: "ai",
          text: "Sorry, I could not submit that decision right now.",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } finally {
      setApprovingMessageId(null);
    }
  };

  return (
    <Message
      type={normalizedType}
      text={text}
      status={status}
      pendingInterrupts={pendingInterrupts}
      decision={decision}
      approvalDisabled={approvalDisabled}
      onApprovalDecision={handleApprovalDecision}
      timestamp={timestamp}
      name={name}
    />
  );
};
