import { initData } from "@tma.js/sdk-react";

export type TelegramUser = {
    id: number;
    first_name?: string;
    last_name?: string;
    username?: string;
}

export function getTelegramWebApp() {
    const tg = (window as any).Telegram?.WebApp;
    if (!tg) {
          alert("Открой приложение через Telegram");
          return;
        }
    tg?.ready();
    tg?.expand();
    return tg
}

export function getTelegramUser() {
    const tg = getTelegramWebApp();
    return tg?.initDataUnsafe?.user
}