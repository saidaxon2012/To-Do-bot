import asyncio
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters.command import CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


# TOKEN = "8159277495:AAEXvM2K62hD4h1oFlWo87KymmZak87BaBs"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

tasks = {}

class AddTask(StatesGroup):
    waiting_task = State()

class TodoState(StatesGroup):
    waiting_task = State()
    waiting_delete = State()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "📝 Todo Bot\n\n"
        "Buyruqlar:\n"
        "/add vazifa\n"
        "/list\n"
        "/delete raqam"
    )

@dp.message(Command("add"))
async def add_command(message: types.Message, state: FSMContext):
    await message.answer("✏️ Vazifani yozing:")
    await state.set_state(AddTask.waiting_task)


@dp.message(AddTask.waiting_task)
async def save_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id not in tasks:
        tasks[user_id] = []

    tasks[user_id].append(message.text)

    await message.answer("✅ Vazifa qo'shildi!")
    await state.clear()


@dp.message(Command("list"))
async def list_tasks(message: types.Message):
    user_id = message.from_user.id

    if user_id not in tasks or not tasks[user_id]:
        await message.answer("📭 Vazifalar yo'q")
        return

    text = "📋 Vazifalar:\n\n"
    for i, task in enumerate(tasks[user_id], 1):
        text += f"{i}. {task}\n"

    await message.answer(text)


@dp.message(Command("delete"))
async def delete_command(message: types.Message, state: FSMContext):
    await message.answer("❌ O'chirmoqchi bo'lgan vazifa raqamini yozing:")
    await state.set_state(TodoState.waiting_delete)


@dp.message(TodoState.waiting_delete)
async def delete_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        number = int(message.text)

        if user_id not in tasks or number > len(tasks[user_id]):
            await message.answer("⚠️ Bunday raqam yo'q")
            return

        deleted = tasks[user_id].pop(number - 1)

        await message.answer(f"🗑 O'chirildi: {deleted}")
        await state.clear()

    except:
        await message.answer("⚠️ Raqam yozing (masalan: 1)")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())