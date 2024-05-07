from aiogram import Router, types, F
from aiogram.filters.command import Command
from utils.validate_input import validator
from utils.utils import find_salaries
from utils.strings import INVALID_MESSAGE

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello {message.from_user.first_name}!")


@router.message(F.text)
async def handle_message(message: types.Message):
    data_dict = validator(message.text)

    if data_dict == INVALID_MESSAGE:
        await message.answer(INVALID_MESSAGE)
        return

    answer = str(await find_salaries(
        data_dict.get("dt_from", None),
        data_dict.get("dt_upto", None),
        data_dict.get("group_type", None),
    )).replace("'", "\"")

    if len(answer) > 4096:
        for x in range(0, len(answer), 4096):
            await message.answer(f"{answer[x: x + 4096]}")
    else:
        await message.answer(f"{answer}")
