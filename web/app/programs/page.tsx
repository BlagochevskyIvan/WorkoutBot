"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";

import { useTelegramUser } from "@/hooks/useTelegramUser";
import { apiFetch } from "@/lib/api";
import LongPressSortable, {
  orderItemsByIds,
} from "@/components/LongPressSortable";

type Workout = {
  id: number;
  name: string;
};

type Program = {
  id: number;
  name: string;
  description: string | null;
  workouts: Workout[];
};

export default function ProgramsPage() {
  const { user, ready } = useTelegramUser();
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [programName, setProgramName] = useState("");
  const [programDescription, setProgramDescription] = useState("");

  useEffect(() => {
    if (!ready) {
      return;
    }

    async function fetchPrograms() {
      try {
        if (!user) {
          throw new Error("Открой приложение через Telegram");
        }

        const result = await apiFetch("/api/programs");
        if (result.status === 404) {
          setPrograms([]);
          return;
        }
        if (!result.ok) {
          throw new Error(`Ошибка загрузки: ${result.status}`);
        }

        const data: Omit<Program, "workouts">[] = await result.json();
        const programsWithWorkouts = await Promise.all(
          data.map(async (program) => {
            const workoutsResult = await apiFetch(
              `/api/programs/${program.id}/workouts`,
            );
            const workouts: Workout[] = workoutsResult.ok
              ? await workoutsResult.json()
              : [];

            return { ...program, workouts };
          }),
        );

        setPrograms(programsWithWorkouts);
      } catch (fetchError) {
        setError(
          fetchError instanceof Error
            ? fetchError.message
            : "Не удалось загрузить программы",
        );
      } finally {
        setLoading(false);
      }
    }

    void fetchPrograms();
  }, [ready, user]);

  async function handleCreateProgram(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = programName.trim();
    if (!name) {
      return;
    }

    try {
      const result = await apiFetch("/api/programs", {
        method: "POST",
        body: JSON.stringify({
          name,
          description: programDescription.trim() || null,
        }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка создания: ${result.status}`);
      }

      const program = await result.json();
      setPrograms((current) => [...current, { ...program, workouts: [] }]);
      setProgramName("");
      setProgramDescription("");
      setCreateOpen(false);
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Не удалось создать программу",
      );
    }
  }

  async function handleReorderPrograms(ids: number[]) {
    try {
      const result = await apiFetch("/api/order/programs", {
        method: "PUT",
        body: JSON.stringify({ ids }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка сохранения порядка: ${result.status}`);
      }
    } catch (reorderError) {
      setError(
        reorderError instanceof Error
          ? reorderError.message
          : "Не удалось сохранить порядок программ",
      );
    }
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-white">
        Загрузка...
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-black px-4 pb-28 pt-6 text-white">
      <div className="mx-auto max-w-2xl">
        <h1 className="mb-6 text-2xl font-bold">Программы тренировок</h1>

        {error && (
          <p className="mb-4 rounded-xl bg-red-950 px-4 py-3 text-sm text-red-200">
            {error}
          </p>
        )}

        {programs.length === 0 ? (
          <div className="rounded-2xl border border-zinc-800 p-5 text-zinc-400">
            Программ пока нет
          </div>
        ) : (
          <LongPressSortable
            items={programs}
            className="space-y-3"
            label="Программа"
            onPreview={(ids) =>
              setPrograms((current) => orderItemsByIds(current, ids))
            }
            onCommit={handleReorderPrograms}
            renderItem={(program) => (
              <Link
                href={`/programs/${program.id}`}
                className="block rounded-2xl border border-zinc-800 bg-zinc-950 p-4 transition hover:border-zinc-600"
              >
                <h2 className="text-lg font-semibold">{program.name}</h2>
                <div className="mt-3 space-y-1">
                  {program.workouts.length === 0 ? (
                    <p className="text-sm text-zinc-500">Тренировок нет</p>
                  ) : (
                    program.workouts.map((workout) => (
                      <p key={workout.id} className="text-sm text-zinc-300">
                        {workout.name}
                      </p>
                    ))
                  )}
                </div>
              </Link>
            )}
          />
        )}
      </div>

      <div className="fixed inset-x-0 bottom-0 border-t border-zinc-800 bg-black/95 p-4 pb-[max(1rem,env(safe-area-inset-bottom))] backdrop-blur">
        <button
          type="button"
          onClick={() => setCreateOpen(true)}
          className="mx-auto block w-full max-w-2xl rounded-xl bg-white px-4 py-3 font-semibold text-black"
        >
          Создать программу
        </button>
      </div>

      {createOpen && (
        <div className="fixed inset-0 z-50 flex items-end bg-black/70 p-4 sm:items-center sm:justify-center">
          <form
            onSubmit={handleCreateProgram}
            className="w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-950 p-5"
          >
            <h2 className="mb-4 text-xl font-semibold">Новая программа</h2>
            <input
              autoFocus
              required
              maxLength={50}
              value={programName}
              onChange={(event) => setProgramName(event.target.value)}
              placeholder="Название"
              className="mb-3 w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 outline-none focus:border-white"
            />
            <textarea
              maxLength={200}
              value={programDescription}
              onChange={(event) => setProgramDescription(event.target.value)}
              placeholder="Описание"
              rows={4}
              className="mb-4 w-full resize-none rounded-xl border border-zinc-700 bg-black px-4 py-3 outline-none focus:border-white"
            />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setCreateOpen(false)}
                className="flex-1 rounded-xl border border-zinc-700 px-4 py-3"
              >
                Отмена
              </button>
              <button
                type="submit"
                className="flex-1 rounded-xl bg-white px-4 py-3 font-semibold text-black"
              >
                Создать
              </button>
            </div>
          </form>
        </div>
      )}
    </main>
  );
}
