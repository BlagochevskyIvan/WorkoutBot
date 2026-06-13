"use client";
import Image from "next/image";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

type Workout = {
  id: number;
  name: string;
};

type ProgramDetail = {
  id: number;
  name: string;
  description: string | null;
};

export default function ProgramPageDetail() {
  const [loading, setLoading] = useState(true);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [addWorkoutOpen, setAddWorkoutOpen] = useState(false);
  const [workoutName, setWorkoutName] = useState("");
  const params = useParams();
  const programId = params.id;
  const [program, setProgram] = useState<ProgramDetail | null>(null);
  const [updateProgramOpen, setUpdateProgramOpen] = useState(false);
  const [programName, setProgramName] = useState("");
  const [programDescription, setProgramDescription] = useState("");


  useEffect(() => {
    const fetchData = async () => {
      const result = await fetch(`/api/programs/${programId}/workouts`);
      if (!result.ok) {
        throw new Error(`API Error: ${result.status}`);
      }
      const data: Workout[] = await result.json();
      setWorkouts(data);

      const programResult = await fetch(`/api/programs/${programId}`);
      if (!programResult.ok) {
        throw new Error(`API Error: ${programResult.status}`);
      }
      const programData: ProgramDetail = await programResult.json();
      setProgram(programData);
      setProgramName(programData.name);
      setProgramDescription(programData.description || "");
      setLoading(false);
      const tg = (window as any).Telegram?.WebApp;

      if (!tg) {
        console.log("Открой приложение через тг");
        return;
      }
      tg.ready();
    };

    fetchData();
  }, []);
  const handleDeleteProgram = async () => {
    try {
      const result = await fetch(`/api/programs/${programId}`, {
        method: "DELETE",
      });
      if (!result.ok) {
        throw new Error(`API Error: ${result.status}`);
      }
      window.location.href = "/programs";
    } catch (error) {
      console.error("Error deleting program:", error);
    }
  };
  const handleAddWorkout = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const result = await fetch(`/api/programs/${programId}/workouts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: workoutName }),
      });
    } catch (error) {
      console.error("Error adding workout:", error);
    }
  };
  const handleUpdateProgram = async (e?: React.FormEvent<HTMLFormElement>) => {
    e?.preventDefault();
    try {
      const result = await fetch(`/api/programs/${programId}`, {
        method: "PUT", // или PATCH, если у тебя PATCH в API
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: programName,
          description: programDescription,
        }),
      });

      if (!result.ok) {
        throw new Error(`API Error: ${result.status}`);
      }

      const updatedProgram = await result.json();

      setProgram(updatedProgram);
      setUpdateProgramOpen(false);
    } catch (error) {
      console.error("Error updating program:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <h1>Загрузка</h1>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-black text-white p-4">
      <Link href={`/programs`}>Назад к программам</Link>
      <h1 className="text-2xl font-bold mb-6">{program?.name}</h1>
      <button onClick={() => {handleDeleteProgram()}}>удалить</button>
      <button
        onClick={() => {
          setUpdateProgramOpen(true);
        }}
      >
        обновить
      </button>

      {workouts.length === 0 ? (
        <p>Тренировок нет</p>
      ) : (
        <div>
          <h1>Тренировки</h1>
          <button
            onClick={() => {
              setAddWorkoutOpen(true);
            }}
          >
            + добавить
          </button>
          <ul>
            {workouts.map((item) => (
              <li key={item.id} className="border-b border-gray-700 py-4">
                <Link href={`/workouts/${item.id}`}>
                  <h2 className="font-bold text-lg">{item.name}</h2>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
      {addWorkoutOpen && (
        <div className="modal">
          <h2>Добавить тренировку</h2>
          <form onSubmit={(e) => {handleAddWorkout(e)}}>
            <input type="text" placeholder="Название тренировки" onChange={(e) => {setWorkoutName(e.target.value)}} />
            <button type="submit">Добавить</button>
          </form>
        </div>
      )}
      {updateProgramOpen && (
        <div className="modal">
          <h2>Обновить программу</h2>

          <form onSubmit={handleUpdateProgram}>
            <input
              type="text"
              placeholder="Название программы"
              value={programName}
              onChange={(e) => setProgramName(e.target.value)}
            />

            <textarea
              placeholder="Описание программы"
              value={programDescription}
              onChange={(e) => setProgramDescription(e.target.value)}
            />

            <button type="submit">Сохранить</button>

            <button
              type="button"
              onClick={() => setUpdateProgramOpen(false)}
            >
              Отмена
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
