import { useState, useRef, useEffect } from "react";
import { Menu, BookOpen, Database } from "lucide-react";
import AssistantSidebar from "../components/AssistantSidebar";
import ChatInput from "../components/ChatInput";
import UserMessage from "../components/UserMessage";
import AssistantResponse from "../components/AssistantResponse";
import ErrorResponse from "../components/ErrorResponse";
import api from "../services/api";
import toast from "react-hot-toast";

function Assistant() {
  const [messages, setMessages] = useState([]);
  const [currentFavoriteId, setCurrentFavoriteId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("data"); // "data" | "knowledge"
  const sidebarRef = useRef();

  useEffect(() => {
    const handleToggleSidebar = () => {
      setSidebarOpen(prev => !prev);
    };
    window.addEventListener('toggleSidebar', handleToggleSidebar);
    return () => window.removeEventListener('toggleSidebar', handleToggleSidebar);
  }, []);

  const submitQuery = async (query, isFavoriteQuery = false) => {
    if (mode === "knowledge") {
      await submitKnowledgeQuery(query);
      return;
    }

    const userMessage = { type: "user", query };
    setMessages([userMessage]);
    setLoading(true);

    try {
      const response = await api.post("/chat/query", { query }, { withCredentials: true });
      const assistantMessage = {
        type: "assistant",
        data: response.data,
        favoriteId: isFavoriteQuery ? currentFavoriteId : null,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorData = {
        type: "error",
        error: {
          statusCode: error.response?.status || "Unknown",
          message: error.response?.data?.detail || "Query execution failed",
          details: error.response?.data?.detail || error.message || "",
        },
      };
      setMessages((prev) => [...prev, errorData]);
    } finally {
      setLoading(false);
    }
  };

  const submitKnowledgeQuery = async (query) => {
    const userMessage = { type: "user", query };
    setMessages([userMessage]);
    setLoading(true);

    try {
      const response = await api.post("/rag/query", { query }, { withCredentials: true });
      const knowledgeMessage = {
        type: "knowledge",
        answer: response.data.answer,
        sources: response.data.sources,
      };
      setMessages((prev) => [...prev, knowledgeMessage]);
    } catch (error) {
      const errorData = {
        type: "error",
        error: {
          statusCode: error.response?.status || "Unknown",
          message: error.response?.data?.detail || "Knowledge query failed",
          details: error.response?.data?.detail || error.message || "",
        },
      };
      setMessages((prev) => [...prev, errorData]);
    } finally {
      setLoading(false);
    }
  };

  const submitImageQuery = async (imageFile) => {
    const userMessage = { type: "user", query: "Processing image query..." };
    setMessages([userMessage]);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("image", imageFile, imageFile.name);
      const response = await api.post("/chat/image-query", formData, {
        withCredentials: true,
        headers: { "Content-Type": "multipart/form-data" },
      });

      const assistantMessage = {
        type: "assistant",
        data: {
          natual_language_query: response.data.extracted_text,
          generated_sql: response.data.generated_sql,
          row_count: response.data.row_count,
          results: response.data.results,
        },
        favoriteId: null,
      };

      setMessages((prev) => {
        const updated = [...prev];
        updated[0] = { type: "user", query: response.data.extracted_text };
        return [...updated, assistantMessage];
      });
    } catch (error) {
      const errorData = {
        type: "error",
        error: {
          statusCode: error.response?.status || "Unknown",
          message: error.response?.data?.detail || "Image query failed",
          details: error.response?.data?.detail || error.message || "",
        },
      };
      setMessages((prev) => {
        const updated = [...prev];
        updated[0] = { type: "user", query: "Image query" };
        return [...updated, errorData];
      });
    } finally {
      setLoading(false);
    }
  };

  const submitVoiceQuery = async (audioBlob) => {
    const userMessage = { type: "user", query: "Recording voice query..." };
    setMessages([userMessage]);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "audio.webm");
      const response = await api.post("/chat/voice-query", formData, {
        withCredentials: true,
        headers: { "Content-Type": "multipart/form-data" },
      });

      const assistantMessage = {
        type: "assistant",
        data: {
          natual_language_query: response.data.transcribed_text,
          generated_sql: response.data.generated_sql,
          row_count: response.data.row_count,
          results: response.data.results,
        },
        favoriteId: null,
      };

      setMessages((prev) => {
        const updated = [...prev];
        updated[0] = { type: "user", query: response.data.transcribed_text };
        return [...updated, assistantMessage];
      });
    } catch (error) {
      const errorData = {
        type: "error",
        error: {
          statusCode: error.response?.status || "Unknown",
          message: error.response?.data?.detail || "Voice query failed",
          details: error.response?.data?.detail || error.message || "",
        },
      };
      setMessages((prev) => {
        const updated = [...prev];
        updated[0] = { type: "user", query: "Voice query" };
        return [...updated, errorData];
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFavoriteAdded = () => {
    if (sidebarRef.current) sidebarRef.current.refreshFavorites();
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
          <div className="border-b border-sky-100 bg-white p-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 rounded-lg hover:bg-sky-50 transition"
            >
              <Menu size={24} className="text-sky-600" />
            </button>
          </div>
        )}

        {/* Mode Toggle */}
        <div className="border-b border-sky-100 bg-white px-6 py-3 flex items-center gap-2">
          <button
            onClick={() => { setMode("data"); setMessages([]); }}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
              mode === "data"
                ? "bg-sky-500 text-white shadow-sm"
                : "text-sky-600 hover:bg-sky-50"
            }`}
          >
            <Database size={15} />
            Data Query
          </button>
          <button
            onClick={() => { setMode("knowledge"); setMessages([]); }}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
              mode === "knowledge"
                ? "bg-emerald-500 text-white shadow-sm"
                : "text-emerald-600 hover:bg-emerald-50"
            }`}
          >
            <BookOpen size={15} />
            Knowledge Query
          </button>
          <span className="ml-2 text-xs text-gray-400">
            {mode === "data"
              ? "Query your village health records"
              : "Ask health protocols & guidelines"}
          </span>
        </div>

        <div className="flex-1 overflow-y-auto">
          <div className="max-w-5xl mx-auto px-6 py-8">

            {messages.map((msg, index) => {
              if (msg.type === "user") {
                return <UserMessage key={index} query={msg.query} />;
              }

              if (msg.type === "error") {
                return <ErrorResponse key={index} error={msg.error} />;
              }

              if (msg.type === "knowledge") {
                return (
                  <div key={index} className="mb-8">
                    <div className="bg-emerald-50 border border-emerald-100 rounded-3xl p-6">
                      <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                        {msg.answer}
                      </p>
                      {msg.sources?.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-emerald-100">
                          <p className="text-xs text-emerald-600 font-medium mb-2">Sources</p>
                          <div className="flex flex-wrap gap-2">
                            {msg.sources.map((src, i) => (
                              <span
                                key={i}
                                className="text-xs bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full"
                              >
                                {src}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
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
                <div className={`border rounded-3xl p-6 ${
                  mode === "knowledge"
                    ? "bg-emerald-50 border-emerald-100"
                    : "bg-sky-50 border-sky-100"
                }`}>
                  <div className="flex items-center gap-3">
                    <div className="flex gap-1">
                      {[0, 0.2, 0.4].map((delay, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full animate-bounce ${
                            mode === "knowledge" ? "bg-emerald-500" : "bg-sky-500"
                          }`}
                          style={{ animationDelay: `${delay}s` }}
                        />
                      ))}
                    </div>
                    <span className={`text-sm font-medium ${
                      mode === "knowledge" ? "text-emerald-600" : "text-sky-600"
                    }`}>
                      {mode === "knowledge" ? "Searching documents..." : "Generating results..."}
                    </span>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>

        <ChatInput
          onSubmit={submitQuery}
          onVoiceSubmit={submitVoiceQuery}
          onImageSubmit={submitImageQuery}
          disabled={loading}
          mode={mode}
        />

      </div>
    </div>
  );
}

export default Assistant;