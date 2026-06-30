"use client";
import { apiFetch } from "@/lib/api";
import Image from "next/image";
import { useEffect, useState } from "react";

type UserProfile = {
  telegram_id: number;
  username: string;
  gender: string | null;
  experience: string | null;
  place: string | null;
  birth_date: string | null;
};

export default function Home() {
  const [userData, setUserData] = useState<UserProfile | null>(null);
  useEffect(() => {
    async function fetchData() {
      const tg = (window as any).Telegram?.WebApp;

      if (!tg) {
        console.log("Открой приложение через тг");
        return;
      }
      tg.ready();
    
      const user = tg.initDataUnsafe?.user;
     
      const result = await apiFetch('/api/me');
      if (!result.ok) {
        throw new Error(`API Error: ${result.status}`);
      }
      const data = (await result.json()) as UserProfile;
      setUserData(data);
    }

    fetchData();
  }, []);
  
  if (!userData) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <h1>Загрузка</h1>
      </div>
    );
  }
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      {userData.username}<br />
      Дата рождения {userData.birth_date}<br />
      Пол {userData.gender}<br />
      {/* в нашем приложение с*/}
      {/* тренировок проведено */}
      {/* вес */}
      {/* цель */}
    </div>
  );
}
