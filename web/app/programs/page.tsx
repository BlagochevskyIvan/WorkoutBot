"use client";

import { useEffect, useState } from "react";

type Program = {
  id: number;
  name: string;
  description: string | null;
};

export default function Home() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPrograms() {
      try {
        // Telegram SDK
        const tg = (window as any).Telegram?.WebApp;

        if (!tg) {
          console.log("Открой приложение через Telegram");
          return;
        }

        tg.ready();

        // Telegram user
        const user = tg.initDataUnsafe?.user;

        if (!user) {
          console.log("Пользователь не найден");
          return;
        }

        console.log("USER:", user);

        // Запрос тренировок
        const result = await fetch(
          `/api/program?telegram_id=${user.id}`
        );

        if (!result.ok) {
          throw new Error(`API Error: ${result.status}`);
        }

        // Получаем массив тренировок
        const data: Program[] = await result.json();

        console.log("PROGRAMS:", data);

        setPrograms(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchPrograms();
  }, []);

  // Loader
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <h1 className="text-white">Загрузка...</h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-4">
      <h1 className="text-2xl font-bold mb-6">
        Программы тренировок
      </h1>

      {programs.length === 0 ? (
        <p>Тренировок нет</p>
      ) : (
        <ul>
          {programs.map((item) => (
            <li
              key={item.id}
              className="border-b border-gray-700 py-4"
            >
              <h2 className="font-bold text-lg">
                {item.name}
              </h2>

              <p className="text-gray-400">
                {item.description || "Нет описания"}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// "use client";
// import { useEffect, useState } from "react";

// type Program = {
//   id: number;
//   name: string;
//   descr: string | null;
// };

// export default function Home() {
//   const [programs, setPrograms] = useState<Program[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         setLoading(true);
//         setError(null);
        
//         // Замени на свой эндпоинт
//         const result = await fetch(
//           `/api/programs?telegram_id=962826986`
//         );

//         if (!result.ok) {
//           throw new Error(`API Error: ${result.status}`);
//         }

//         const data = (await result.json()) as Program[];
//         setPrograms(data);
//       } catch (err) {
//         setError(
//           err instanceof Error 
//             ? err.message 
//             : "Неизвестная ошибка"
//         );
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchData();
//   }, []);

//   // Загрузка
//   if (loading) {
//     return (
//       <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
//           <h1 className="text-xl text-zinc-800 dark:text-zinc-200">
//             Загрузка программ...
//           </h1>
//         </div>
//       </div>
//     );
//   }

//   // Ошибка
//   if (error) {
//     return (
//       <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//         <div className="text-center p-6 bg-red-50 dark:bg-red-900/20 rounded-lg max-w-md">
//           <p className="text-red-600 dark:text-red-400 text-lg mb-4">
//             ⚠️ {error}
//           </p>
//           <button
//             onClick={() => window.location.reload()}
//             className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
//           >
//             Попробовать снова
//           </button>
//         </div>
//       </div>
//     );
//   }

//   // Пустой список
//   if (programs.length === 0) {
//     return (
//       <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//         <div className="text-center">
//           <p className="text-xl text-zinc-500 dark:text-zinc-400 mb-4">
//             У вас пока нет программ
//           </p>
//           <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
//             Создать первую программу
//           </button>
//         </div>
//       </div>
//     );
//   }

//   // Список программ
//   return (
//     <div className="min-h-screen bg-zinc-50 font-sans dark:bg-black p-6">
//       <div className="max-w-4xl mx-auto">
//         <h1 className="text-2xl font-bold text-zinc-800 dark:text-zinc-200 mb-6">
//           Мои программы ({programs.length})
//         </h1>

//         <div className="grid gap-4 md:grid-cols-2">
//           {programs.map((program) => (
//             <div
//               key={program.id}
//               className="bg-white dark:bg-zinc-900 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow border border-zinc-200 dark:border-zinc-800"
//             >
//               <h2 className="text-lg font-semibold text-zinc-800 dark:text-zinc-200 mb-2">
//                 {program.name}
//               </h2>
              
//               {program.descr ? (
//                 <p className="text-zinc-600 dark:text-zinc-400 line-clamp-2">
//                   {program.descr}
//                 </p>
//               ) : (
//                 <p className="text-zinc-400 dark:text-zinc-500 italic">
//                   Нет описания
//                 </p>
//               )}

//               <button
//                 onClick={() => {
//                   // Переход к деталям программы
//                   // router.push(`/programs/${program.program_id}`);
//                   console.log("Открыть программу:", program.id);
//                 }}
//                 className="mt-3 text-blue-600 dark:text-blue-400 hover:underline text-sm"
//               >
//                 Подробнее
//               </button>
//             </div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// }