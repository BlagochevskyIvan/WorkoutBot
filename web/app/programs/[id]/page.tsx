"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import LongPressSortable, {
  orderItemsByIds,
} from "@/components/LongPressSortable";

type Exercise = {
  id: number;
  name: string;
};

type Workout = {
  id: number;
  name: string;
  exercises: Exercise[];
};

type Program = {
  id: number;
  name: string;
  description: string | null;
};

export default function ProgramPageDetail() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const programId = params.id;

  const [program, setProgram] = useState<Program | null>(null);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [editing, setEditing] = useState(false);
  const [programName, setProgramName] = useState("");
  const [programDescription, setProgramDescription] = useState("");
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [createWorkoutOpen, setCreateWorkoutOpen] = useState(false);
  const [workoutName, setWorkoutName] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const [programResult, workoutsResult] = await Promise.all([
          apiFetch(`/api/programs/${programId}`),
          apiFetch(`/api/programs/${programId}/workouts`),
        ]);

        if (!programResult.ok) {
          throw new Error(`Ошибка загрузки программы: ${programResult.status}`);
        }
        if (!workoutsResult.ok) {
          throw new Error(`Ошибка загрузки тренировок: ${workoutsResult.status}`);
        }

        const programData: Program = await programResult.json();
        const workoutsData: Omit<Workout, "exercises">[] =
          await workoutsResult.json();
        const workoutsWithExercises = await Promise.all(
          workoutsData.map(async (workout) => {
            const exercisesResult = await apiFetch(
              `/api/workouts/${workout.id}/exercises`,
            );
            const exercises: Exercise[] = exercisesResult.ok
              ? await exercisesResult.json()
              : [];
            return { ...workout, exercises };
          }),
        );

        setProgram(programData);
        setProgramName(programData.name);
        setProgramDescription(programData.description || "");
        setWorkouts(workoutsWithExercises);
      } catch (fetchError) {
        setError(
          fetchError instanceof Error
            ? fetchError.message
            : "Не удалось загрузить программу",
        );
      } finally {
        setLoading(false);
      }
    }

    void fetchData();
  }, [programId]);

  async function handleUpdateProgram(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = programName.trim();
    if (!name) {
      return;
    }

    try {
      const result = await apiFetch(`/api/programs/${programId}`, {
        method: "PUT",
        body: JSON.stringify({
          name,
          description: programDescription.trim(),
        }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка обновления: ${result.status}`);
      }

      const updatedProgram: Program = await result.json();
      setProgram(updatedProgram);
      setProgramName(updatedProgram.name);
      setProgramDescription(updatedProgram.description || "");
      setEditing(false);
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Не удалось обновить программу",
      );
    }
  }

  async function handleDeleteProgram() {
    try {
      const result = await apiFetch(`/api/programs/${programId}`, {
        method: "DELETE",
      });
      if (!result.ok) {
        throw new Error(`Ошибка удаления: ${result.status}`);
      }
      router.replace("/programs");
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Не удалось удалить программу",
      );
      setDeleteOpen(false);
    }
  }

  async function handleCreateWorkout(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = workoutName.trim();
    if (!name) {
      return;
    }

    try {
      const result = await apiFetch(`/api/programs/${programId}/workouts`, {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка создания: ${result.status}`);
      }

      const workout = await result.json();
      setWorkouts((current) => [...current, { ...workout, exercises: [] }]);
      setWorkoutName("");
      setCreateWorkoutOpen(false);
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Не удалось создать тренировку",
      );
    }
  }

  async function handleReorderWorkouts(ids: number[]) {
    try {
      const result = await apiFetch(
        `/api/order/programs/${programId}/workouts`,
        {
          method: "PUT",
          body: JSON.stringify({ ids }),
        },
      );
      if (!result.ok) {
        throw new Error(`Ошибка сохранения порядка: ${result.status}`);
      }
    } catch (reorderError) {
      setError(
        reorderError instanceof Error
          ? reorderError.message
          : "Не удалось сохранить порядок тренировок",
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

  if (!program) {
    return (
      <main className="min-h-screen bg-black p-4 text-white">
        <p>{error || "Программа не найдена"}</p>
        <Link href="/programs" className="mt-4 inline-block text-zinc-300">
          Назад к программам
        </Link>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-black px-4 pb-28 pt-6 text-white">
      <div className="mx-auto max-w-2xl">
        {error && (
          <p className="mb-4 rounded-xl bg-red-950 px-4 py-3 text-sm text-red-200">
            {error}
          </p>
        )}

        {editing ? (
          <form onSubmit={handleUpdateProgram} className="mb-8 space-y-3">
            <input
              autoFocus
              required
              maxLength={50}
              value={programName}
              onChange={(event) => setProgramName(event.target.value)}
              className="w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-2xl font-bold outline-none focus:border-white"
            />
            <textarea
              maxLength={200}
              value={programDescription}
              onChange={(event) => setProgramDescription(event.target.value)}
              placeholder="Описание программы"
              rows={4}
              className="w-full resize-none rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-zinc-200 outline-none focus:border-white"
            />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => {
                  setProgramName(program.name);
                  setProgramDescription(program.description || "");
                  setEditing(false);
                }}
                className="rounded-xl border border-zinc-700 px-4 py-2"
              >
                Отмена
              </button>
              <button
                type="submit"
                className="rounded-xl bg-white px-4 py-2 font-semibold text-black"
              >
                Сохранить
              </button>
            </div>
          </form>
        ) : (
          <>
            <div className="relative mb-3 flex items-start justify-between gap-4">
              <h1 className="text-2xl font-bold">{program.name}</h1>
              <button
                type="button"
                aria-label="Действия с программой"
                onClick={() => setMenuOpen((current) => !current)}
                className="rounded-lg px-3 py-1 text-2xl leading-none hover:bg-zinc-900"
              >
                ⋮
              </button>
              {menuOpen && (
                <div className="absolute right-0 top-10 z-10 w-40 overflow-hidden rounded-xl border border-zinc-700 bg-zinc-950 shadow-xl">
                  <button
                    type="button"
                    onClick={() => {
                      setMenuOpen(false);
                      setEditing(true);
                    }}
                    className="block w-full px-4 py-3 text-left hover:bg-zinc-900"
                  >
                    Редактировать
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setMenuOpen(false);
                      setDeleteOpen(true);
                    }}
                    className="block w-full px-4 py-3 text-left text-red-400 hover:bg-zinc-900"
                  >
                    Удалить
                  </button>
                </div>
              )}
            </div>
            <p className="mb-8 whitespace-pre-wrap text-zinc-400">
              {program.description || "Описание не добавлено"}
            </p>
          </>
        )}

        <section>
          <h2 className="mb-4 text-xl font-semibold">Тренировки</h2>
          {workouts.length === 0 ? (
            <div className="rounded-2xl border border-zinc-800 p-5 text-zinc-400">
              Тренировок пока нет
            </div>
          ) : (
            <LongPressSortable
              items={workouts}
              className="space-y-3"
              label="Тренировка"
              onPreview={(ids) =>
                setWorkouts((current) => orderItemsByIds(current, ids))
              }
              onCommit={handleReorderWorkouts}
              renderItem={(workout) => (
                <article
                  className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4"
                >
                  <Link
                    href={`/workouts/${workout.id}?programId=${programId}`}
                    className="text-lg font-semibold hover:text-zinc-300"
                  >
                    {workout.name}
                  </Link>
                  <div className="mt-3 space-y-1 border-l border-zinc-700 pl-3">
                    {workout.exercises.length === 0 ? (
                      <p className="text-sm text-zinc-500">Упражнений нет</p>
                    ) : (
                      workout.exercises.map((exercise) => (
                        <p key={exercise.id} className="text-sm text-zinc-300">
                          {exercise.name}
                        </p>
                      ))
                    )}
                  </div>
                </article>
              )}
            />
          )}
        </section>
      </div>

      <div className="fixed inset-x-0 bottom-0 border-t border-zinc-800 bg-black/95 p-4 pb-[max(1rem,env(safe-area-inset-bottom))] backdrop-blur">
        <div className="mx-auto flex max-w-2xl gap-2">
          <Link
            href="/programs"
            className="rounded-xl border border-zinc-700 px-4 py-3 text-center"
          >
            Назад
          </Link>
          <button
            type="button"
            onClick={() => setCreateWorkoutOpen(true)}
            className="flex-1 rounded-xl bg-white px-4 py-3 font-semibold text-black"
          >
            Создать тренировку
          </button>
        </div>
      </div>

      {deleteOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4">
          <div className="w-full max-w-sm rounded-2xl border border-zinc-700 bg-zinc-950 p-5">
            <h2 className="text-xl font-semibold">Удалить программу?</h2>
            <p className="mt-2 text-sm text-zinc-400">
              Все тренировки, упражнения и подходы внутри неё также будут удалены.
            </p>
            <div className="mt-5 flex gap-2">
              <button
                type="button"
                onClick={() => setDeleteOpen(false)}
                className="flex-1 rounded-xl border border-zinc-700 px-4 py-3"
              >
                Отмена
              </button>
              <button
                type="button"
                onClick={() => void handleDeleteProgram()}
                className="flex-1 rounded-xl bg-red-600 px-4 py-3 font-semibold"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      )}

      {createWorkoutOpen && (
        <div className="fixed inset-0 z-50 flex items-end bg-black/70 p-4 sm:items-center sm:justify-center">
          <form
            onSubmit={handleCreateWorkout}
            className="w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-950 p-5"
          >
            <h2 className="mb-4 text-xl font-semibold">Новая тренировка</h2>
            <input
              autoFocus
              required
              maxLength={50}
              value={workoutName}
              onChange={(event) => setWorkoutName(event.target.value)}
              placeholder="Название тренировки"
              className="mb-4 w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 outline-none focus:border-white"
            />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setCreateWorkoutOpen(false)}
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
