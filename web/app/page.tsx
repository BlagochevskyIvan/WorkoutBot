"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [userData, setUserData] = useState(null);
  const [user2Data, setUser2Data] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`/api/user`);
      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
      }
      const data = await res.json();
      setUserData(data);

      const tg = (window as any).Telegram?.WebApp

      if (!tg){
        console.log('Открой приложение через тг')
        return;
      }
      tg.ready()
      const user = tg.initDataUnsafe?.user
      setUserData(user.username)
    };

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
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">{userData}</h1>
        <a href="/profile" className="text-blue-500 hover:underline">
          Профиль
        </a>
        <div>
          <a href="/programs" className="text-blue-500 hover:underline"> Программы тренировок</a>
        </div>
      </div>
    </div>
  );
}
