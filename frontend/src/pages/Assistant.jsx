import { useState, useRef, useEffect } from "react";
import { Menu } from "lucide-react";
import AssistantSidebar from "../components/AssistantSidebar";
import ChatInput from "../components/ChatInput";
import UserMessage from "../components/UserMessage";
import AssistantResponse from "../components/AssistantResponse";
import api from "../services/api";
import toast from "react-hot-toast";

function Assistant() {
  const [messages, setMessages] = useState([]);
  const [currentFavoriteId, setCurrentFavoriteId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(false);
  const sidebarRef = useRef();

  useEffect(() => {
    const handleToggleSidebar = () => {
      setSidebarOpen(prev => !prev);
    };

    window.addEventListener('toggleSidebar', handleToggleSidebar);
    return () => window.removeEventListener('toggleSidebar', handleToggleSidebar);
  }, []);

  const submitQuery = async (query, isFavoriteQuery = false) => {
    const userMessage = {
      type: "user",
      query,
    };

    setMessages([userMessage]);
    setLoading(true);

    try {
      const response = await api.post(
        "/chat/query",
        { query },
        { withCredentials: true }
      );

      const assistantMessage = {
        type: "assistant",
        data: response.data,
        favoriteId: isFavoriteQuery ? currentFavoriteId : null,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
        "Something went wrong"
      );

      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleFavoriteAdded = () => {
    if (sidebarRef.current) {
      sidebarRef.current.refreshFavorites();
    }
  };

  const handleFavoriteClick = (favorite) => {
    setCurrentFavoriteId(favorite.id);
    submitQuery(favorite.query_name, true);
  };

  return (
    <div className="h-screen flex bg-white">

      {sidebarOpen && (
        <AssistantSidebar
          ref={sidebarRef}
          onFavoriteClick={handleFavoriteClick}
          currentFavoriteId={currentFavoriteId}
        />
      )}

      <div className="flex-1 flex flex-col">

        {!sidebarOpen && (
          <div className="
            border-b
            border-sky-100
            bg-white
            p-4
          ">
            <button
              onClick={() => setSidebarOpen(true)}
              className="
                p-2
                rounded-lg
                hover:bg-sky-50
                transition
              "
            >
              <Menu size={24} className="text-sky-600" />
            </button>
          </div>
        )}

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
                  onFavoriteAdded={handleFavoriteAdded}
                  isFavoritedQuery={msg.favoriteId !== null}
                  isLoading={loading}
                />
              );
            })}

            {loading && messages.length > 0 && messages[messages.length - 1].type === "user" && (
              <div className="mb-8">
                <div className="
                  bg-sky-50
                  border
                  border-sky-100
                  rounded-3xl
                  p-6
                ">
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1">
                      <div className="
                        w-2
                        h-2
                        bg-sky-500
                        rounded-full
                        animate-bounce
                      " style={{ animationDelay: '0s' }}></div>
                      <div className="
                        w-2
                        h-2
                        bg-sky-500
                        rounded-full
                        animate-bounce
                      " style={{ animationDelay: '0.2s' }}></div>
                      <div className="
                        w-2
                        h-2
                        bg-sky-500
                        rounded-full
                        animate-bounce
                      " style={{ animationDelay: '0.4s' }}></div>
                    </div>
                    <span className="text-sky-600 text-sm font-medium">
                      Generating results...
                    </span>
                  </div>
                </div>
              </div>
            )}

          </div>

        </div>

        <ChatInput onSubmit={submitQuery} disabled={loading} />

      </div>

    </div>
  );
}

export default Assistant;