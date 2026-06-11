import { useState } from "react";
import { Heart } from "lucide-react";
import ResultsTable from "./ResultsTable";
import api from "../services/api";
import toast from "react-hot-toast";

function AssistantResponse({ response, onFavoriteAdded, isFavoritedQuery }) {
  const [isFavored, setIsFavored] = useState(isFavoritedQuery || false);

  const toggleFavorite = async () => {
    if (isFavored) {
      toast.success("Removed from favorites");
      setIsFavored(false);
      return;
    }

    const queryName = response.natual_language_query.substring(0, 50) + (response.natual_language_query.length > 50 ? "..." : "");

    try {
      await api.post(
        "/favorites/add",
        {
          query_name: queryName,
          generated_sql: response.generated_sql,
        },
        { withCredentials: true }
      );

      toast.success("Added to favorites");
      setIsFavored(true);
      onFavoriteAdded?.();
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
        "Failed to add to favorites"
      );
    }
  };

  return (
    <div className="mb-8">

      <div className="
        bg-sky-50
        border
        border-sky-100
        rounded-3xl
        p-6
      ">

        <div className="
          flex
          justify-between
          mb-4
        ">
          <h3 className="font-semibold">
            Generated SQL
          </h3>

          <Heart
            size={20}
            className={`cursor-pointer transition ${
              isFavored
                ? "fill-red-500 text-red-500"
                : "text-sky-500 hover:text-red-500"
            }`}
            onClick={toggleFavorite}
          />
        </div>

        <pre className="
          bg-white
          p-4
          rounded-xl
          overflow-x-auto
          text-sm
          border
          border-sky-100
        ">
          {response.generated_sql}
        </pre>

        <div className="
          text-xs
          text-sky-600
          font-semibold
          mt-2
        ">
          {response.row_count} row{response.row_count !== 1 ? 's' : ''} returned
        </div>

        <div className="mt-6">

          <h3 className="
            font-semibold
            mb-3
          ">
            Results
          </h3>

          <ResultsTable
            rows={response.results}
          />

        </div>

      </div>

    </div>
  );
}

export default AssistantResponse;