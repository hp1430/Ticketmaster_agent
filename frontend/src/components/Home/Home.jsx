import { MessageInputContainer } from "../MessageInput/MessageInputContainer";

export const Home = () => {
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
        <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-6">
          {/* Chat messages will be displayed here */}
        </div>

        {/* Message Input - Bottom Center */}
        <div className="w-full px-6 pb-6">
          <div className="mx-auto w-full max-w-3xl">
            <MessageInputContainer />
          </div>
        </div>
      </main>
    </div>
  );
};
