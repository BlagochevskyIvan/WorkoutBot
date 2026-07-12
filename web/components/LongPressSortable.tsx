"use client";

import {
  PointerEvent as ReactPointerEvent,
  ReactNode,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";

type SortableItem = {
  id: number;
};

type LongPressSortableProps<T extends SortableItem> = {
  items: T[];
  className?: string;
  label: string;
  onPreview: (ids: number[]) => void;
  onCommit: (ids: number[]) => void | Promise<void>;
  renderItem: (item: T, index: number, dragging: boolean) => ReactNode;
};

export function orderItemsByIds<T extends SortableItem>(
  items: T[],
  ids: number[],
) {
  const itemsById = new Map(items.map((item) => [item.id, item]));
  return ids
    .map((id) => itemsById.get(id))
    .filter((item): item is T => item !== undefined);
}

export default function LongPressSortable<T extends SortableItem>({
  items,
  className = "",
  label,
  onPreview,
  onCommit,
  renderItem,
}: LongPressSortableProps<T>) {
  const scopeId = useId();
  const [draggingId, setDraggingId] = useState<number | null>(null);
  const orderRef = useRef<number[]>(items.map((item) => item.id));
  const activeIdRef = useRef<number | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pointerIdRef = useRef<number | null>(null);

  useEffect(() => {
    if (activeIdRef.current === null) {
      orderRef.current = items.map((item) => item.id);
    }
  }, [items]);

  function clearTimer() {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }

  function handlePointerDown(
    event: ReactPointerEvent<HTMLButtonElement>,
    itemId: number,
  ) {
    if (event.button !== 0) {
      return;
    }

    pointerIdRef.current = event.pointerId;
    event.currentTarget.setPointerCapture(event.pointerId);
    clearTimer();
    timerRef.current = setTimeout(() => {
      activeIdRef.current = itemId;
      setDraggingId(itemId);
      timerRef.current = null;
    }, 320);
  }

  function handlePointerMove(event: ReactPointerEvent<HTMLButtonElement>) {
    const activeId = activeIdRef.current;
    if (activeId === null) {
      return;
    }

    event.preventDefault();
    let target = document
      .elementFromPoint(event.clientX, event.clientY)
      ?.closest<HTMLElement>("[data-sort-id]");
    while (target && target.dataset.sortScope !== scopeId) {
      target = target.parentElement?.closest<HTMLElement>("[data-sort-id]");
    }
    const targetId = Number(target?.dataset.sortId);
    if (!targetId || targetId === activeId) {
      return;
    }

    const currentOrder = [...orderRef.current];
    const fromIndex = currentOrder.indexOf(activeId);
    const toIndex = currentOrder.indexOf(targetId);
    if (fromIndex === -1 || toIndex === -1) {
      return;
    }

    currentOrder.splice(fromIndex, 1);
    currentOrder.splice(toIndex, 0, activeId);
    orderRef.current = currentOrder;
    onPreview(currentOrder);
  }

  function finishDragging(event: ReactPointerEvent<HTMLButtonElement>) {
    clearTimer();
    if (
      pointerIdRef.current !== null &&
      event.currentTarget.hasPointerCapture(pointerIdRef.current)
    ) {
      event.currentTarget.releasePointerCapture(pointerIdRef.current);
    }
    pointerIdRef.current = null;

    if (activeIdRef.current === null) {
      return;
    }

    activeIdRef.current = null;
    setDraggingId(null);
    void onCommit([...orderRef.current]);
  }

  return (
    <div className={className}>
      {items.map((item, index) => (
        <div
          key={item.id}
          data-sort-id={item.id}
          data-sort-scope={scopeId}
          className={`relative pl-8 transition ${
            draggingId === item.id ? "z-20 scale-[1.02] opacity-70" : ""
          }`}
        >
          <button
            type="button"
            aria-label={`${label}: изменить позицию`}
            onPointerDown={(event) => handlePointerDown(event, item.id)}
            onPointerMove={handlePointerMove}
            onPointerUp={finishDragging}
            onPointerCancel={finishDragging}
            onContextMenu={(event) => event.preventDefault()}
            style={{ touchAction: "none" }}
            className="absolute left-0 top-1/2 z-10 -translate-y-1/2 cursor-grab select-none rounded-lg px-1 py-3 text-xl text-zinc-500 active:cursor-grabbing active:text-white"
          >
            ⠿
          </button>
          {renderItem(item, index, draggingId === item.id)}
        </div>
      ))}
    </div>
  );
}
