import { useState } from "react";
import AssistantSidebar from "../components/AssistantSidebar";
import ChatInput from "../components/ChatInput";
import UserMessage from "../components/UserMessage";
import AssistantResponse from "../components/AssistantResponse";
import api from "../services/api";

function Assistant() {
  const [messages, setMessages] = useState([]);

  const submitQuery = async (query) => {
    const userMessage = {
      type: "user",
      query,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await api.post(
        "/chat/query",
        { query },
        { withCredentials: true }
      );

      const assistantMessage = {
        type: "assistant",
        data: response.data,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="h-screen flex bg-white">

      <AssistantSidebar />

      <div className="flex-1 flex flex-col">

        <div className="flex-1 overflow-y-auto">

          <div className="max-w-5xl mx-auto px-6 py-8">

            {messages.map((msg, index) => {

              if (msg.type === "user") {
                return (
                  <UserMessage
                    key={index}
                    query={msg.query}
                  />
                );
              }

              return (
                <AssistantResponse
                  key={index}
                  response={msg.data}
                />
              );
            })}

          </div>

        </div>

        <ChatInput onSubmit={submitQuery} />

      </div>

    </div>
  );
}

export default Assistant;