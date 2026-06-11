import {
  Heart,
  Trash2,
  X,
  LogOut
} from "lucide-react";
import { useEffect, useState, forwardRef, useImperativeHandle } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import toast from "react-hot-toast";

const AssistantSidebar = forwardRef(({ onFavoriteClick, currentFavoriteId }, ref) => {

  const navigate = useNavigate();
  const [systemQueries, setSystemQueries] = useState([]);
  const [userFavorites, setUserFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useImperativeHandle(ref, () => ({
    refreshFavorites: fetchFavorites,
  }));

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      const response = await api.get(
        "/favorites/list",
        { withCredentials: true }
      );

      const favorites = response.data.favorites || [];
      setSystemQueries(favorites.filter(f => f.is_system === true));
      setUserFavorites(favorites.filter(f => f.is_system !== true));
    } catch (error) {
      console.error("Failed to fetch favorites:", error);
      setSystemQueries([]);
      setUserFavorites([]);
    } finally {
      setLoading(false);
    }
  };

  const removeFavorite = async (e, id) => {
    e.stopPropagation();
    try {
      await api.delete(
        `/favorites/remove/${id}`,
        { withCredentials: true }
      );

      setUserFavorites(userFavorites.filter(fav => fav.id !== id));
      toast.success("Favorite removed");
    } catch (error) {
      toast.error("Failed to remove favorite");
    }
  };

  const handleLogout = async () => {
    try {
      await api.post(
        "/auth/logout",
        {},
        { withCredentials: true }
      );

      toast.success("Logged out successfully");
      navigate("/login");
    } catch (error) {
      toast.error("Failed to logout");
      console.error(error);
    }
  };

  const renderFavoriteItem = (item, isSystem = false) => (
    <div
      key={item.id}
      onClick={() => onFavoriteClick?.(item)}
      className={`
        flex
        gap-2
        items-center
        justify-between
        p-3
        rounded-lg
        cursor-pointer
        group
        transition
        ${currentFavoriteId === item.id
          ? "bg-sky-200 border border-sky-400"
          : "hover:bg-sky-100"
        }
      `}
      title={item.query_name}
    >
      <div className="flex gap-2 items-center flex-1 min-w-0">
        <Heart
          size={16}
          fill="#0EA5E9"
          color="#0EA5E9"
          className="flex-shrink-0"
        />
        <span className="
          text-sm
          truncate
        ">
          {item.query_name}
        </span>
      </div>

      {!isSystem && (
        <button
          onClick={(e) => removeFavorite(e, item.id)}
          className="
            p-1
            opacity-0
            group-hover:opacity-100
            transition
            hover:text-red-500
            flex-shrink-0
          "
        >
          <Trash2 size={14} />
        </button>
      )}
    </div>
  );

  return (
    <div className="
      w-72
      border-r
      border-sky-100
      bg-sky-50
      flex
      flex-col
    ">

      <div className="
        p-6
        border-b
        border-sky-100
        flex
        justify-between
        items-center
      ">
        <h1 className="
          text-xl
          font-bold
          text-sky-600
        ">
          ASHA Connect
        </h1>
        <button
          onClick={() => window.dispatchEvent(new CustomEvent('toggleSidebar'))}
          className="
            p-1
            rounded-lg
            hover:bg-sky-200
            transition
            text-sky-600
          "
        >
          <X size={24} />
        </button>
      </div>

      <div className="
        p-4
        flex-1
        overflow-y-auto
      ">

        {loading ? (
          <div className="text-gray-500 text-sm">
            Loading...
          </div>
        ) : (
          <>
            {systemQueries.length > 0 && (
              <>
                <h3 className="
                  text-sm
                  font-semibold
                  text-sky-600
                  mb-3
                ">
                  QUICK QUERIES
                </h3>
                <div className="mb-4 space-y-2">
                  {systemQueries.map((item) =>
                    renderFavoriteItem(item, true)
                  )}
                </div>
              </>
            )}

            {userFavorites.length > 0 && (
              <>
                <h3 className="
                  text-sm
                  font-semibold
                  text-sky-600
                  mb-3
                ">
                  MY FAVOURITES
                </h3>
                <div className="space-y-2">
                  {userFavorites.map((item) =>
                    renderFavoriteItem(item, false)
                  )}
                </div>
              </>
            )}

            {systemQueries.length === 0 && userFavorites.length === 0 && (
              <div className="text-gray-500 text-sm">
                No queries available
              </div>
            )}
          </>
        )}

      </div>

      <div className="
        p-4
        border-t
        border-sky-100
      ">
        <button
          onClick={handleLogout}
          className="
            w-full
            flex
            items-center
            justify-center
            gap-2
            p-3
            rounded-lg
            bg-red-50
            text-red-600
            hover:bg-red-100
            transition
            font-medium
          "
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>

    </div>
  );
});

AssistantSidebar.displayName = "AssistantSidebar";

export default AssistantSidebar;