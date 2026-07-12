"use client";

import Link from "next/link";

import { useTelegramUser } from "@/hooks/useTelegramUser";

export default function Home() {
  const { user, ready } = useTelegramUser();

  if (!ready) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-white">
        Загрузка...
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-black p-4 text-white">
      <div className="w-full max-w-sm space-y-3 text-center">
        <h1 className="mb-6 text-2xl font-bold">
          {user?.username || user?.first_name || "WorkoutBot"}
        </h1>
        <Link
          href="/programs"
          className="block rounded-xl bg-white px-4 py-3 font-semibold text-black"
        >
          Программы тренировок
        </Link>
        <Link
          href="/profile"
          className="block rounded-xl border border-zinc-700 px-4 py-3"
        >
          Профиль
        </Link>
      </div>
    </main>
  );
}
