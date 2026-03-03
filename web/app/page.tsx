"use client";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    fetch("https://725a-109-71-244-92.ngrok-free.app/api/user")
      .then((res) => {
        alert(1);
        res.json();
      })
      .then((data) => {
        alert(data);
        setUserData(data);
      });
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      Главная
      <a href="/vanya">Ваня</a>
    </div>
  );
}
