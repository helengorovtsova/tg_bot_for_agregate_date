from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from json import loads
from datetime import datetime
from services.services import get_agregated_data

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот для агрегации данных'
                         'о зарплатах сотрудников компании по временным промежуткам.\n'
                        'Чтобы начать, пришлите мне данные в формате JSON.\n\n'
                        'Например: \n'
                            '<b>{"dt_from":"2022-09-01T00:00:00", \n'
                            '"dt_upto":"2022-12-31T23:59:00", \n'
                            '"group_type":"month"} </b> \n'
    )


@router.message()
async def echo(message: Message):
    data = loads(message.text)
    print(data)

    dt_from = datetime.strptime(data["dt_from"], '%Y-%m-%dT%H:%M:%S')
    dt_upto = datetime.strptime(data["dt_upto"], '%Y-%m-%dT%H:%M:%S')
    group_type = data['group_type']

    await get_agregated_data(dt_from, dt_upto, group_type)