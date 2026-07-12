import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import Script from "next/script";

export const metadata: Metadata = {
  title: "WorkoutBot",
  description: "Программы и дневник тренировок",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  
  return (
    <html lang="ru">
      <body>
        <Script
          src="https://telegram.org/js/telegram-web-app.js"
          strategy="beforeInteractive"
        />

        {children}
      </body>
    </html>
  );
}
