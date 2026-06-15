"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

type Exercise = {
  id: number;
  name: string;
};

type WorkoutDetail = {
  id: number;
  name: string;
};

export default function WorkoutPageDetail() {
  const params = useParams();
  const workoutId = params.id;

  const [loading, setLoading] = useState(true);

  const [workout, setWorkout] =
    useState<WorkoutDetail | null>(null);

  const [exercises, setExercises] =
    useState<Exercise[]>([]);

  const [updateWorkoutOpen, setUpdateWorkoutOpen] =
    useState(false);

  const [workoutName, setWorkoutName] =
    useState("");

  useEffect(() => {
    const fetchData = async () => {
      const workoutResult = await fetch(
        `/api/workouts/${workoutId}`
      );

      const workoutData =
        await workoutResult.json();

      setWorkout(workoutData);
      setWorkoutName(workoutData.name);

      const exercisesResult = await fetch(
        `/api/workouts/${workoutId}/exercises`
      );

      const exercisesData =
        await exercisesResult.json();

      setExercises(exercisesData);

      setLoading(false);
    };

    fetchData();
  }, [workoutId]);

  const handleDeleteWorkout = async () => {
    try {
      const result = await fetch(
        `/api/workouts/${workoutId}`,
        {
          method: "DELETE",
        }
      );

      if (!result.ok) {
        throw new Error();
      }

      window.location.href = "/programs";
    } catch (error) {
      console.error(error);
    }
  };

  const handleUpdateWorkout = async (
    e?: React.FormEvent<HTMLFormElement>
  ) => {
    e?.preventDefault();

    try {
      const result = await fetch(
        `/api/workouts/${workoutId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: workoutName,
          }),
        }
      );

      if (!result.ok) {
        throw new Error();
      }

      const updatedWorkout =
        await result.json();

      setWorkout(updatedWorkout);
      setUpdateWorkoutOpen(false);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div>Загрузка...</div>;
  }

  return (
    <div className="min-h-screen bg-black text-white p-4">
      <Link href="/programs">
        Назад
      </Link>

      <h1 className="text-2xl font-bold mb-4">
        {workout?.name}
      </h1>

      <button
        onClick={handleDeleteWorkout}
      >
        удалить
      </button>

      <button
        onClick={() =>
          setUpdateWorkoutOpen(true)
        }
      >
        обновить
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-bold">
          Упражнения
        </h2>

        {exercises.length === 0 ? (
          <p>Упражнений нет</p>
        ) : (
          <ul>
            {exercises.map((exercise) => (
              <li
                key={exercise.id}
                className="border-b border-gray-700 py-3"
              >
                {exercise.name}
              </li>
            ))}
          </ul>
        )}
      </div>

      {updateWorkoutOpen && (
        <div className="modal">
          <h2>
            Обновить тренировку
          </h2>

          <form
            onSubmit={
              handleUpdateWorkout
            }
          >
            <input
              type="text"
              value={workoutName}
              onChange={(e) =>
                setWorkoutName(
                  e.target.value
                )
              }
            />

            <button type="submit">
              Сохранить
            </button>

            <button
              type="button"
              onClick={() =>
                setUpdateWorkoutOpen(
                  false
                )
              }
            >
              Отмена
            </button>
          </form>
        </div>
      )}
    </div>
  );
}