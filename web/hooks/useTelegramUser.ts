import { getTelegramUser } from "@/lib/telegram";
import { TelegramUser } from "@/lib/telegram";
import { useEffect, useState } from "react";

export function useTelegramUser() {
    const[user, setUser] = useState<TelegramUser | null>(null);
    const [ready, setReady] = useState(false)

    useEffect(() => {
        setUser(getTelegramUser())
        setReady(true)
    }, [])

    return {user, ready}
}