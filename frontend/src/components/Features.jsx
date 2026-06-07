import {
  ShieldCheck,
  Mic,
  Brain,
  BarChart3,
  Mail,
  MapPinned
} from "lucide-react";

const features = [
  {
    icon: ShieldCheck,
    title: "Secure Authentication",
    desc: "JWT-based authentication with role-based access control."
  },
  {
    icon: Mic,
    title: "Voice Query",
    desc: "Ask questions in Telugu, Hindi or English."
  },
  {
    icon: Brain,
    title: "AI Powered SQL",
    desc: "Convert natural language questions into database queries."
  },
  {
    icon: BarChart3,
    title: "Healthcare Analytics",
    desc: "Access pregnancy, vaccination and disease insights."
  },
  {
    icon: Mail,
    title: "OTP Password Recovery",
    desc: "Secure email-based password reset."
  },
  {
    icon: MapPinned,
    title: "Area Based Security",
    desc: "ASHA workers only access their assigned health area."
  }
];

function Features() {
  return (
    <section
      id="features"
      className="bg-sky-50 py-24 px-6"
    >
      <div className="max-w-7xl mx-auto">

        <h2 className="text-4xl font-bold text-center mb-16">
          Core Features
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          {features.map((feature, index) => {
            const Icon = feature.icon;

            return (
              <div
                key={index}
                className="bg-white p-8 rounded-2xl shadow-sm border border-sky-100 hover:shadow-lg transition"
              >
                <Icon
                  className="text-sky-500 mb-4"
                  size={36}
                />

                <h3 className="font-semibold text-xl mb-3">
                  {feature.title}
                </h3>

                <p className="text-gray-600">
                  {feature.desc}
                </p>
              </div>
            );
          })}

        </div>
      </div>
    </section>
  );
}

export default Features;