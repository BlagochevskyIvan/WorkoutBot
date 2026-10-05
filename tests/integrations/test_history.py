from unittest.mock import  AsyncMock, MagicMock
from datetime import date
import pytest
from handlers.history import workout_history
from config.states import MENU
from handlers.history import HISTORY_PAGE_SIZE

def make_update(id, data):
    update = MagicMock()
    update.effective_user.id = id
    update.callback_query = AsyncMock()
    update.callback_query.data = data

    context = MagicMock()
    context.user_data = {}
    return update, context

def make_workouts(n, page_size=HISTORY_PAGE_SIZE):
    workouts = []
    for i in range(n):
        workout = MagicMock()
        workout.id = i + 1
        workout.created_at = date(2026, 1, i + 1)
        workouts.append(workout)
    return workouts[:page_size], n

@pytest.mark.asyncio
async def test_history_handler_with_workouts(monkeypatch):
    fake_get_fact_workouts = AsyncMock(return_value=make_workouts(10, 7))
    monkeypatch.setattr("handlers.history.get_fact_workouts_page", fake_get_fact_workouts)
    update, context = make_update(123, "history_page_1")
    state = await workout_history(update, context)

    assert state == MENU

    update.callback_query.answer.assert_awaited_once()
    fake_get_fact_workouts.assert_awaited_once_with(telegram_id=123, page=1, page_size=HISTORY_PAGE_SIZE)
    markup = update.callback_query.edit_message_text.call_args.kwargs["reply_markup"]

    buttons = [row for row in markup.inline_keyboard if row[0].callback_data.startswith("fact_workout_")]

    # Проверяем, что количество кнопок соответствует количеству тренировок на странице
    assert len(buttons) == 8

    text = update.callback_query.edit_message_text.call_args.kwargs["text"]
    assert "Страница 1 из 2" in text