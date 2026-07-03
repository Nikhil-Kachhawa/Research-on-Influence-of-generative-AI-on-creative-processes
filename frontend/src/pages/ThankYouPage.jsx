import { useTranslation } from "react-i18next";

function ThankYouPage() {
  const { t } = useTranslation();
  return (
    <div className="min-h-screen flex items-center justify-center">

      <div className="text-center">

        <h1 className="text-4xl font-bold mb-4">
          { t("thankYou.title") }
        </h1>

        <p className="text-lg">
          { t("thankYou.message")}
          
        </p>

      </div>

    </div>
  );
}

export default ThankYouPage;