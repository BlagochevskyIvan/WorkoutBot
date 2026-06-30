"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getTelegramWebApp } from "@/lib/telegram";
import { useTelegramUser } from "@/hooks/useTelegramUser";
import { apiFetch } from "@/lib/api";

type Program = {
  id: number;
  name: string;
  description: string | null;
};

export default function Home() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);
  const {user, ready} = useTelegramUser()

  useEffect(() => {
    if (!ready){
      return
    }
    async function fetchPrograms() {
      try {
      
        if (!user) {
          alert('Открой приложение через тг')
          return;
        }

        console.log("USER:", user);
        const URL = process.env.NEXT_PUBLIC_URL || "http://localhost:8000";

        const result = await apiFetch('/api/programs')

        if (!result.ok) {
          throw new Error(`API Error: ${result.status}`);
        }

        // Получаем массив тренировок
        const data: Program[] = await result.json();
        const programsWithDetails = await Promise.all(
          data.map(async (program) => {
            const res = await fetch(
              `${URL}/api/programs/${program.id}`
            );

            const details = await res.json();

            return {
              ...program,
              workouts: details.workouts ?? [],
            };
          })
        );

        setPrograms(programsWithDetails);

        console.log("PROGRAMS:", data);

        setPrograms(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchPrograms();
  }, [ready, user]);

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
      <h1 className="text-2xl font-bold mb-6">Программы тренировок</h1>

      {programs.length === 0 ? (
        <p>Программ нет</p>
      ) : (
        <ul>
          {programs.map((item) => (
            <li key={item.id} className="border-b border-gray-700 py-4">
              <Link href={`/programs/${item.id}`}>
                <h2 className="font-bold text-lg">{item.name}</h2>

                <p className="text-gray-400">
                  {item.description || "Нет описания"}
                </p>
              </Link> 
            </li>
          ))}
        </ul>
      )}

      <Link href={`/programs`}>Программы</Link> 
      <Link href={`/stats`}>Статистика</Link> 
      <Link href={`/profile`}>Профиль</Link> 
    </div>
  );
}
