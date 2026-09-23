export const Message = ({
  type = "ai",
  text,
  status,
  pendingInterrupts,
  decision,
  approvalDisabled = false,
  onApprovalDecision,
  timestamp,
  name,
}) => {
  const isUser = type === "user";
  const actionRequests = pendingInterrupts?.action_requests || [];
  const reviewConfigs = pendingInterrupts?.review_configs || [];
  const isApprovalRequired = status === "approval_required";

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

        {isApprovalRequired && (
          <div className="mb-3 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-amber-950">
            <div className="mb-1 text-xs font-bold uppercase tracking-[0.12em] text-amber-800">
              Approval required
            </div>
            <p className="text-sm leading-6">
              {text || "Approval is required to continue."}
            </p>
          </div>
        )}

        {!isApprovalRequired && (
          <p className="whitespace-pre-wrap text-sm leading-6 text-current">
            {text}
          </p>
        )}

        {isApprovalRequired && actionRequests.length > 0 && (
          <div className="space-y-2">
            <div className="text-xs font-bold uppercase tracking-[0.12em] text-emerald-800">
              Pending actions
            </div>
            {actionRequests.map((request, index) => {
              const config = reviewConfigs.find(
                (reviewConfig) => reviewConfig.action_name === request.name,
              );

              return (
                <div
                  className="rounded-xl border border-emerald-200 bg-white/70 p-3"
                  key={`${request.name || "action"}-${index}`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="font-semibold text-emerald-950">
                      {request.name || "Unnamed action"}
                    </span>
                    {config?.allowed_decisions?.length > 0 && (
                      <span className="text-xs text-emerald-700">
                        {config.allowed_decisions.join(" / ")}
                      </span>
                    )}
                  </div>
                  {request.args && (
                    <pre className="mt-2 overflow-x-auto rounded-lg bg-emerald-950/[0.06] p-2 text-xs leading-5 text-emerald-950">
                      {JSON.stringify(request.args, null, 2)}
                    </pre>
                  )}
                </div>
              );
            })}

            {!decision && onApprovalDecision && (
              <div className="flex flex-wrap gap-2 pt-1">
                <button
                  className="rounded-lg bg-emerald-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"
                  disabled={approvalDisabled}
                  onClick={() => onApprovalDecision("approve")}
                  type="button"
                >
                  Approve
                </button>
                <button
                  className="rounded-lg border border-red-200 bg-white px-4 py-2 text-sm font-semibold text-red-700 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                  disabled={approvalDisabled}
                  onClick={() => onApprovalDecision("reject")}
                  type="button"
                >
                  Reject
                </button>
              </div>
            )}

            {decision && (
              <div className="pt-1 text-xs font-semibold uppercase tracking-[0.12em] text-emerald-700">
                Decision submitted: {decision}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
