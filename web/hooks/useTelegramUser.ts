import { getTelegramUser, TelegramUser } from "@/lib/telegram";
import { useEffect, useState } from "react";

export function useTelegramUser() {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setUser(getTelegramUser() || null);
      setReady(true);
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  return { user, ready };
}
