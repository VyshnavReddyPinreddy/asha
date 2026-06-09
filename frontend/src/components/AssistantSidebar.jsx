import {
  Heart,
  Menu
} from "lucide-react";

function AssistantSidebar() {

  const favorites = [
    "High Risk Pregnancies",
    "Vaccination Pending",
    "ANC Visits Due"
  ];

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
      ">
        <h1 className="
          text-xl
          font-bold
          text-sky-600
        ">
          ASHA Connect
        </h1>
      </div>

      <button className="
        mx-4
        mt-4
        p-3
        rounded-xl
        bg-sky-500
        text-white
      ">
        New Query
      </button>

      <div className="p-4">

        <h3 className="
          text-sm
          font-semibold
          text-sky-600
          mb-3
        ">
          FAVOURITES
        </h3>

        {favorites.map((item) => (
          <div
            key={item}
            className="
              flex
              gap-2
              items-center
              p-3
              rounded-lg
              hover:bg-sky-100
              cursor-pointer
            "
          >
            <Heart
              size={16}
              fill="#0EA5E9"
              color="#0EA5E9"
            />
            {item}
          </div>
        ))}

      </div>

    </div>
  );
}

export default AssistantSidebar;