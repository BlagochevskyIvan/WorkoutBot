"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [userData, setUserData] = useState(null);
  const [user2Data, setUser2Data] = useState(null);
  const [count, setCount] = useState(0);

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
  }, [count]);

  useEffect(() => {
    window.addEventListener("click", (event) => {
      const fetchData = async () => {
      const res = await fetch(`/api/user2`);
      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
      }
      const data = await res.json();
      setUserData(data);
    };

    fetchData();
    });
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Главная</h1>

        {userData && <pre>{JSON.stringify(userData, null, 2)}</pre>}
        <a href="/vanya" className="text-blue-500 hover:underline">
          Ваня
        </a>

        <div>
          <p>{count}</p>
          <button onClick={() => setCount(count + 1)}>Кнопка</button>
        </div>
        {user2Data && <pre>{JSON.stringify(user2Data, null, 2)}</pre>}
        <div style={{height:'2000px'}}>Скроль</div>
      </div>
    </div>
  );
}
