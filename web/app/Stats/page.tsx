import Link from "next/link";

export default function StatsPage() {
  return (
    <main className="min-h-screen bg-black p-4 text-white">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-2xl font-bold">Статистика</h1>
        <p className="mt-3 text-zinc-400">Раздел находится в разработке</p>
        <Link href="/programs" className="mt-6 inline-block text-zinc-300">
          Назад к программам
        </Link>
      </div>
    </main>
  );
}
