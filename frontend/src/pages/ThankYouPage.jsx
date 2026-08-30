import { useTranslation } from "react-i18next";

function ThankYouPage() {
  const { t } = useTranslation();
  return (
    <div className="min-h-screen bg-amber-50 flex items-center justify-center p-8">
  <div className="relative bg-white w-full max-w-3xl rounded-xl shadow-2xl p-12 rotate-[-1deg]">

    {/* Tape */}
    <div className="absolute -top-5 left-1/2 -translate-x-1/2 w-32 h-8 bg-yellow-200/70 rotate-2 rounded-sm"></div>

    {/* Paper holes */}
    <div className="absolute top-3 left-6 flex gap-4">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="w-3 h-3 rounded-full bg-amber-50 border border-gray-300"
        />
      ))}
    </div>

    <h1
      className="mt-8 text-6xl text-center font-black"
      style={{ fontFamily: "cursive" }}
    >
      {t("thankYou.title")}
    </h1>

    <p className="mt-10 text-xl text-center leading-9 text-gray-700">
      {t("thankYou.message")}
    </p>

    <div className="mt-12 flex justify-center">
      <div className="w-16 h-1 rounded-full bg-gray-300"></div>
    </div>

    <div className="mt-8 text-center text-red-500">
      <p>{t("thankYou.footer")}</p>
    </div>

    {/* Doodles */}
    <div className="absolute top-12 right-10 text-4xl">🙏</div>
    <div className="absolute bottom-12 left-10 text-4xl">😊</div>
    <div className="absolute bottom-8 right-16 text-3xl">✏️</div>

  </div>
</div>
  );
}

export default ThankYouPage;