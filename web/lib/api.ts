import { retrieveRawInitData } from "@tma.js/sdk-react";

export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const initData = retrieveRawInitData();

  if (!initData) {
    throw new Error("Нет initData — открой mini app через Telegram");
  }

  const headers = new Headers(options.headers);
  headers.set("X-Telegram-Auth", initData);

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  return fetch(path, {
    ...options,
    headers,
  });
}