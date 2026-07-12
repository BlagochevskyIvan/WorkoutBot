"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import LongPressSortable, {
  orderItemsByIds,
} from "@/components/LongPressSortable";

type SetItem = {
  id: number;
  weight: number;
  reps: number;
};

type Exercise = {
  id: number;
  name: string;
  sets: SetItem[];
};

type Workout = {
  id: number;
  name: string;
};

type SetDraft = {
  id: number;
  weight: string;
  reps: string;
};

export default function WorkoutPageDetail() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const workoutId = params.id;

  const [programId, setProgramId] = useState<string | null>(null);
  const [workout, setWorkout] = useState<Workout | null>(null);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [workoutMenuOpen, setWorkoutMenuOpen] = useState(false);
  const [editingWorkout, setEditingWorkout] = useState(false);
  const [workoutName, setWorkoutName] = useState("");
  const [deleteWorkoutOpen, setDeleteWorkoutOpen] = useState(false);
  const [exerciseMenuId, setExerciseMenuId] = useState<number | null>(null);
  const [editingExerciseId, setEditingExerciseId] = useState<number | null>(
    null,
  );
  const [exerciseName, setExerciseName] = useState("");
  const [draftSets, setDraftSets] = useState<SetDraft[]>([]);
  const [createExerciseOpen, setCreateExerciseOpen] = useState(false);
  const [newExerciseName, setNewExerciseName] = useState("");

  const backHref = programId ? `/programs/${programId}` : "/programs";

  useEffect(() => {
    setProgramId(new URLSearchParams(window.location.search).get("programId"));

    async function fetchData() {
      try {
        const [workoutResult, exercisesResult] = await Promise.all([
          apiFetch(`/api/workouts/${workoutId}`),
          apiFetch(`/api/workouts/${workoutId}/exercises`),
        ]);

        if (!workoutResult.ok) {
          throw new Error(`Ошибка загрузки тренировки: ${workoutResult.status}`);
        }
        if (!exercisesResult.ok) {
          throw new Error(`Ошибка загрузки упражнений: ${exercisesResult.status}`);
        }

        const workoutData: Workout = await workoutResult.json();
        const exercisesData: Omit<Exercise, "sets">[] =
          await exercisesResult.json();
        const exercisesWithSets = await Promise.all(
          exercisesData.map(async (exercise) => {
            const setsResult = await apiFetch(
              `/api/exercises/${exercise.id}/sets`,
            );
            const sets: SetItem[] = setsResult.ok ? await setsResult.json() : [];
            return { ...exercise, sets };
          }),
        );

        setWorkout(workoutData);
        setWorkoutName(workoutData.name);
        setExercises(exercisesWithSets);
      } catch (fetchError) {
        setError(
          fetchError instanceof Error
            ? fetchError.message
            : "Не удалось загрузить тренировку",
        );
      } finally {
        setLoading(false);
      }
    }

    void fetchData();
  }, [workoutId]);

  async function handleUpdateWorkout(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = workoutName.trim();
    if (!name) {
      return;
    }

    try {
      const result = await apiFetch(`/api/workouts/${workoutId}`, {
        method: "PUT",
        body: JSON.stringify({ name }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка обновления: ${result.status}`);
      }

      const updatedWorkout: Workout = await result.json();
      setWorkout(updatedWorkout);
      setWorkoutName(updatedWorkout.name);
      setEditingWorkout(false);
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Не удалось обновить тренировку",
      );
    }
  }

  async function handleDeleteWorkout() {
    try {
      const result = await apiFetch(`/api/workouts/${workoutId}`, {
        method: "DELETE",
      });
      if (!result.ok) {
        throw new Error(`Ошибка удаления: ${result.status}`);
      }
      router.replace(backHref);
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Не удалось удалить тренировку",
      );
      setDeleteWorkoutOpen(false);
    }
  }

  function startEditingExercise(exercise: Exercise) {
    setExerciseMenuId(null);
    setEditingExerciseId(exercise.id);
    setExerciseName(exercise.name);
    setDraftSets(
      exercise.sets.map((set) => ({
        id: set.id,
        weight: String(set.weight),
        reps: String(set.reps),
      })),
    );
  }

  async function handleSaveExercise(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (editingExerciseId === null || !exerciseName.trim()) {
      return;
    }

    const parsedSets = draftSets.map((set) => ({
      id: set.id,
      weight: Number(set.weight),
      reps: Number(set.reps),
    }));
    if (
      parsedSets.some(
        (set) =>
          !Number.isFinite(set.weight) ||
          !Number.isInteger(set.reps) ||
          set.reps < 1,
      )
    ) {
      setError("Проверь вес и количество повторений");
      return;
    }

    try {
      const exerciseResult = await apiFetch(
        `/api/exercises/${editingExerciseId}`,
        {
          method: "PUT",
          body: JSON.stringify({ name: exerciseName.trim() }),
        },
      );
      if (!exerciseResult.ok) {
        throw new Error(`Ошибка обновления: ${exerciseResult.status}`);
      }

      const setResults = await Promise.all(
        parsedSets.map((set) =>
          apiFetch(`/api/sets/${set.id}`, {
            method: "PUT",
            body: JSON.stringify({ weight: set.weight, reps: set.reps }),
          }),
        ),
      );
      if (setResults.some((result) => !result.ok)) {
        throw new Error("Не удалось обновить один из подходов");
      }

      const updatedExercise: Omit<Exercise, "sets"> =
        await exerciseResult.json();
      const updatedSets: SetItem[] = await Promise.all(
        setResults.map((result) => result.json()),
      );

      setExercises((current) =>
        current.map((exercise) =>
          exercise.id === editingExerciseId
            ? { ...updatedExercise, sets: updatedSets }
            : exercise,
        ),
      );
      setEditingExerciseId(null);
      setDraftSets([]);
    } catch (updateError) {
      setError(
        updateError instanceof Error
          ? updateError.message
          : "Не удалось обновить упражнение",
      );
    }
  }

  async function handleDeleteExercise(exerciseId: number) {
    setExerciseMenuId(null);
    if (!window.confirm("Удалить упражнение и все его подходы?")) {
      return;
    }

    try {
      const result = await apiFetch(`/api/exercises/${exerciseId}`, {
        method: "DELETE",
      });
      if (!result.ok) {
        throw new Error(`Ошибка удаления: ${result.status}`);
      }
      setExercises((current) =>
        current.filter((exercise) => exercise.id !== exerciseId),
      );
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Не удалось удалить упражнение",
      );
    }
  }

  async function handleDeleteSet(setId: number) {
    try {
      const result = await apiFetch(`/api/sets/${setId}`, {
        method: "DELETE",
      });
      if (!result.ok) {
        throw new Error(`Ошибка удаления: ${result.status}`);
      }

      setDraftSets((current) => current.filter((set) => set.id !== setId));
      setExercises((current) =>
        current.map((exercise) =>
          exercise.id === editingExerciseId
            ? {
                ...exercise,
                sets: exercise.sets.filter((set) => set.id !== setId),
              }
            : exercise,
        ),
      );
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Не удалось удалить подход",
      );
    }
  }

  async function handleAddSet() {
    if (editingExerciseId === null) {
      return;
    }

    try {
      const result = await apiFetch(
        `/api/exercises/${editingExerciseId}/sets`,
        {
          method: "POST",
          body: JSON.stringify({ weight: 0, reps: 1 }),
        },
      );
      if (!result.ok) {
        throw new Error(`Ошибка создания: ${result.status}`);
      }

      const newSet: SetItem = await result.json();
      setDraftSets((current) => [
        ...current,
        { id: newSet.id, weight: String(newSet.weight), reps: String(newSet.reps) },
      ]);
      setExercises((current) =>
        current.map((exercise) =>
          exercise.id === editingExerciseId
            ? { ...exercise, sets: [...exercise.sets, newSet] }
            : exercise,
        ),
      );
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Не удалось добавить подход",
      );
    }
  }

  async function handleCreateExercise(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = newExerciseName.trim();
    if (!name) {
      return;
    }

    try {
      const result = await apiFetch(`/api/workouts/${workoutId}/exercises`, {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      if (!result.ok) {
        throw new Error(`Ошибка создания: ${result.status}`);
      }

      const exercise = await result.json();
      setExercises((current) => [...current, { ...exercise, sets: [] }]);
      setNewExerciseName("");
      setCreateExerciseOpen(false);
    } catch (createError) {
      setError(
        createError instanceof Error
          ? createError.message
          : "Не удалось создать упражнение",
      );
    }
  }

  async function handleReorderExercises(ids: number[]) {
    try {
      const result = await apiFetch(
        `/api/order/workouts/${workoutId}/exercises`,
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
          : "Не удалось сохранить порядок упражнений",
      );
    }
  }

  function previewSetOrder(exerciseId: number, ids: number[]) {
    setExercises((current) =>
      current.map((exercise) =>
        exercise.id === exerciseId
          ? { ...exercise, sets: orderItemsByIds(exercise.sets, ids) }
          : exercise,
      ),
    );
    if (editingExerciseId === exerciseId) {
      setDraftSets((current) => orderItemsByIds(current, ids));
    }
  }

  async function handleReorderSets(exerciseId: number, ids: number[]) {
    try {
      const result = await apiFetch(
        `/api/order/exercises/${exerciseId}/sets`,
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
          : "Не удалось сохранить порядок подходов",
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

  if (!workout) {
    return (
      <main className="min-h-screen bg-black p-4 text-white">
        <p>{error || "Тренировка не найдена"}</p>
        <Link href={backHref} className="mt-4 inline-block text-zinc-300">
          Назад
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

        {editingWorkout ? (
          <form onSubmit={handleUpdateWorkout} className="mb-8 flex gap-2">
            <input
              autoFocus
              required
              maxLength={50}
              value={workoutName}
              onChange={(event) => setWorkoutName(event.target.value)}
              className="min-w-0 flex-1 rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-xl font-bold outline-none focus:border-white"
            />
            <button
              type="button"
              onClick={() => {
                setWorkoutName(workout.name);
                setEditingWorkout(false);
              }}
              className="rounded-xl border border-zinc-700 px-3"
            >
              Отмена
            </button>
            <button
              type="submit"
              className="rounded-xl bg-white px-3 font-semibold text-black"
            >
              Сохранить
            </button>
          </form>
        ) : (
          <div className="relative mb-8 flex items-start justify-between gap-4">
            <h1 className="text-2xl font-bold">{workout.name}</h1>
            <button
              type="button"
              aria-label="Действия с тренировкой"
              onClick={() => setWorkoutMenuOpen((current) => !current)}
              className="rounded-lg px-3 py-1 text-2xl leading-none hover:bg-zinc-900"
            >
              ⋮
            </button>
            {workoutMenuOpen && (
              <div className="absolute right-0 top-10 z-20 w-40 overflow-hidden rounded-xl border border-zinc-700 bg-zinc-950 shadow-xl">
                <button
                  type="button"
                  onClick={() => {
                    setWorkoutMenuOpen(false);
                    setEditingWorkout(true);
                  }}
                  className="block w-full px-4 py-3 text-left hover:bg-zinc-900"
                >
                  Редактировать
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setWorkoutMenuOpen(false);
                    setDeleteWorkoutOpen(true);
                  }}
                  className="block w-full px-4 py-3 text-left text-red-400 hover:bg-zinc-900"
                >
                  Удалить
                </button>
              </div>
            )}
          </div>
        )}

        <section>
          <h2 className="mb-4 text-xl font-semibold">Упражнения</h2>
          {exercises.length === 0 ? (
            <div className="rounded-2xl border border-zinc-800 p-5 text-zinc-400">
              Упражнений пока нет
            </div>
          ) : (
            <LongPressSortable
              items={exercises}
              className="space-y-4"
              label="Упражнение"
              onPreview={(ids) =>
                setExercises((current) => orderItemsByIds(current, ids))
              }
              onCommit={handleReorderExercises}
              renderItem={(exercise) => {
                const isEditing = editingExerciseId === exercise.id;

                return (
                  <article
                    className="rounded-2xl border border-zinc-800 bg-zinc-950 p-4"
                  >
                    {isEditing ? (
                      <form onSubmit={handleSaveExercise}>
                        <input
                          autoFocus
                          required
                          maxLength={80}
                          value={exerciseName}
                          onChange={(event) => setExerciseName(event.target.value)}
                          className="mb-4 w-full rounded-xl border border-zinc-700 bg-black px-3 py-2 text-lg font-semibold outline-none focus:border-white"
                        />

                        <LongPressSortable
                          items={draftSets}
                          className="space-y-2"
                          label="Подход"
                          onPreview={(ids) =>
                            previewSetOrder(exercise.id, ids)
                          }
                          onCommit={(ids) =>
                            handleReorderSets(exercise.id, ids)
                          }
                          renderItem={(set, index) => (
                            <div className="flex items-center gap-2">
                              <span className="w-6 text-sm text-zinc-500">
                                {index + 1}
                              </span>
                              <input
                                aria-label={`Вес в подходе ${index + 1}`}
                                type="number"
                                min="0"
                                step="0.5"
                                value={set.weight}
                                onChange={(event) =>
                                  setDraftSets((current) =>
                                    current.map((item) =>
                                      item.id === set.id
                                        ? { ...item, weight: event.target.value }
                                        : item,
                                    ),
                                  )
                                }
                                className="min-w-0 flex-1 rounded-lg border border-zinc-700 bg-black px-3 py-2 outline-none focus:border-white"
                              />
                              <span className="text-zinc-500">кг</span>
                              <input
                                aria-label={`Повторения в подходе ${index + 1}`}
                                type="number"
                                min="1"
                                step="1"
                                value={set.reps}
                                onChange={(event) =>
                                  setDraftSets((current) =>
                                    current.map((item) =>
                                      item.id === set.id
                                        ? { ...item, reps: event.target.value }
                                        : item,
                                    ),
                                  )
                                }
                                className="w-20 rounded-lg border border-zinc-700 bg-black px-3 py-2 outline-none focus:border-white"
                              />
                              <button
                                type="button"
                                aria-label={`Удалить подход ${index + 1}`}
                                onClick={() => void handleDeleteSet(set.id)}
                                className="rounded-lg px-2 py-2 text-red-400 hover:bg-zinc-900"
                              >
                                ×
                              </button>
                            </div>
                          )}
                        />

                        <button
                          type="button"
                          onClick={() => void handleAddSet()}
                          className="mt-4 w-full rounded-xl border border-dashed border-zinc-600 px-4 py-3 text-zinc-300"
                        >
                          Добавить подход
                        </button>

                        <div className="mt-4 flex gap-2">
                          <button
                            type="button"
                            onClick={() => {
                              setEditingExerciseId(null);
                              setDraftSets([]);
                            }}
                            className="flex-1 rounded-xl border border-zinc-700 px-4 py-2"
                          >
                            Отмена
                          </button>
                          <button
                            type="submit"
                            className="flex-1 rounded-xl bg-white px-4 py-2 font-semibold text-black"
                          >
                            Сохранить
                          </button>
                        </div>
                      </form>
                    ) : (
                      <>
                        <div className="relative flex items-start justify-between gap-3">
                          <h3 className="text-lg font-semibold">{exercise.name}</h3>
                          <button
                            type="button"
                            aria-label={`Действия с упражнением ${exercise.name}`}
                            onClick={() =>
                              setExerciseMenuId((current) =>
                                current === exercise.id ? null : exercise.id,
                              )
                            }
                            className="rounded-lg px-3 py-1 text-2xl leading-none hover:bg-zinc-900"
                          >
                            ⋮
                          </button>
                          {exerciseMenuId === exercise.id && (
                            <div className="absolute right-0 top-9 z-10 w-40 overflow-hidden rounded-xl border border-zinc-700 bg-black shadow-xl">
                              <button
                                type="button"
                                onClick={() => startEditingExercise(exercise)}
                                className="block w-full px-4 py-3 text-left hover:bg-zinc-900"
                              >
                                Редактировать
                              </button>
                              <button
                                type="button"
                                onClick={() => void handleDeleteExercise(exercise.id)}
                                className="block w-full px-4 py-3 text-left text-red-400 hover:bg-zinc-900"
                              >
                                Удалить
                              </button>
                            </div>
                          )}
                        </div>

                        <div className="mt-3 space-y-2">
                          {exercise.sets.length === 0 ? (
                            <p className="text-sm text-zinc-500">Подходов нет</p>
                          ) : (
                            <LongPressSortable
                              items={exercise.sets}
                              className="space-y-2"
                              label="Подход"
                              onPreview={(ids) =>
                                previewSetOrder(exercise.id, ids)
                              }
                              onCommit={(ids) =>
                                handleReorderSets(exercise.id, ids)
                              }
                              renderItem={(set, index) => (
                                <div className="flex justify-between rounded-lg bg-black px-3 py-2 text-sm">
                                  <span className="text-zinc-500">
                                    Подход {index + 1}
                                  </span>
                                  <span>
                                    {set.weight} кг × {set.reps}
                                  </span>
                                </div>
                              )}
                            />
                          )}
                        </div>
                      </>
                    )}
                  </article>
                );
              }}
            />
          )}
        </section>
      </div>

      <div className="fixed inset-x-0 bottom-0 border-t border-zinc-800 bg-black/95 p-4 pb-[max(1rem,env(safe-area-inset-bottom))] backdrop-blur">
        <div className="mx-auto flex max-w-2xl gap-2">
          <Link
            href={backHref}
            className="rounded-xl border border-zinc-700 px-4 py-3 text-center"
          >
            Назад
          </Link>
          <button
            type="button"
            onClick={() => setCreateExerciseOpen(true)}
            className="flex-1 rounded-xl bg-white px-4 py-3 font-semibold text-black"
          >
            Создать упражнение
          </button>
        </div>
      </div>

      {deleteWorkoutOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4">
          <div className="w-full max-w-sm rounded-2xl border border-zinc-700 bg-zinc-950 p-5">
            <h2 className="text-xl font-semibold">Удалить тренировку?</h2>
            <p className="mt-2 text-sm text-zinc-400">
              Все упражнения и подходы внутри неё также будут удалены.
            </p>
            <div className="mt-5 flex gap-2">
              <button
                type="button"
                onClick={() => setDeleteWorkoutOpen(false)}
                className="flex-1 rounded-xl border border-zinc-700 px-4 py-3"
              >
                Отмена
              </button>
              <button
                type="button"
                onClick={() => void handleDeleteWorkout()}
                className="flex-1 rounded-xl bg-red-600 px-4 py-3 font-semibold"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      )}

      {createExerciseOpen && (
        <div className="fixed inset-0 z-50 flex items-end bg-black/70 p-4 sm:items-center sm:justify-center">
          <form
            onSubmit={handleCreateExercise}
            className="w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-950 p-5"
          >
            <h2 className="mb-4 text-xl font-semibold">Новое упражнение</h2>
            <input
              autoFocus
              required
              maxLength={80}
              value={newExerciseName}
              onChange={(event) => setNewExerciseName(event.target.value)}
              placeholder="Название упражнения"
              className="mb-4 w-full rounded-xl border border-zinc-700 bg-black px-4 py-3 outline-none focus:border-white"
            />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setCreateExerciseOpen(false)}
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
