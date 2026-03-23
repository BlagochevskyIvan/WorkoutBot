"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch(`/api/user`);
      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
      }
      const data = await res.json();
      setUserData(data);
    };

    fetchData();
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Главная</h1>
        
        {userData && <pre>{JSON.stringify(userData, null, 2)}</pre>}
        <a href="/vanya" className="text-blue-500 hover:underline">
          Ваня
        </a>
      </div>
    </div>
  );
}
