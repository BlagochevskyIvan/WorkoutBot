export type TelegramUser = {
  id: number;
  first_name?: string;
  last_name?: string;
  username?: string;
};

type TelegramWebApp = {
  ready: () => void;
  expand: () => void;
  initDataUnsafe?: {
    user?: TelegramUser;
  };
};

declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
}

export function getTelegramWebApp() {
  if (typeof window === "undefined") {
    return undefined;
  }

  const tg = window.Telegram?.WebApp;
  if (!tg) {
    return undefined;
  }

  tg.ready();
  tg.expand();
  return tg;
}

export function getTelegramUser() {
  return getTelegramWebApp()?.initDataUnsafe?.user;
}
