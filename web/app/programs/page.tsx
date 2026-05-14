"use client";

import { useEffect, useState } from "react";

type Program = {
  id: number;
  name: string;
  description: string | null;
};

export default function Home() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPrograms() {
      try {
        const tg = (window as any).Telegram?.WebApp;

        if (!tg) {
          console.log("Открой приложение через Telegram");
          return;
        }

        tg.ready();

        const user = tg.initDataUnsafe?.user;

        if (!user) {
          console.log("Пользователь не найден");
          return;
        }

        console.log("USER:", user);
        const URL = process.env.URL || "http://localhost:8000";
        const result = await fetch(
          `{URL}/api/programs?telegram_id=${user.id}`
        );

        if (!result.ok) {
          throw new Error(`API Error: ${result.status}`);
        }

        // Получаем массив тренировок
        const data: Program[] = await result.json();

        console.log("PROGRAMS:", data);

        setPrograms(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchPrograms();
  }, []);

  // Loader
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <h1 className="text-white">Загрузка...</h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-4">
      <h1 className="text-2xl font-bold mb-6">
        Программы тренировок
      </h1>

      {programs.length === 0 ? (
        <p>Тренировок нет</p>
      ) : (
        <ul>
          {programs.map((item) => (
            <li
              key={item.id}
              className="border-b border-gray-700 py-4"
            >
              <h2 className="font-bold text-lg">
                {item.name}
              </h2>

              <p className="text-gray-400">
                {item.description || "Нет описания"}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}