from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user_states import PersonSettings
from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import Database

db=Database()
router=Router()
scheduler=AsyncIOScheduler()
###START
@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a dictionary-bot\n"
                         "You can ... (send words with translate, then during the day i would help learn new words).\n"
                         "To show command use /command")

###COMMAND
@router.message(Command("command"))
async def command_show(message: Message)->None:
    await message.answer("/count - set count words in a day \n"
                         "/words - set N words\n"
                         "/test - start testing\n"
                         "/remind - set daily remind\n"
                         "/list - show all your dictionary\n"
                         "/delete - delete a pair from your dictionary")

###COUNT
@router.message(Command("count"))
async def set_count_request(message: Message, state:FSMContext)->None:
    await state.set_state(PersonSettings.waiting_count)
    await message.answer("Enter count more than 0 and less than 100")


@router.message(PersonSettings.waiting_count)
async def set_count_function(message:Message, state:FSMContext)->None:
    curEnter=(message.text)
    if curEnter.isdigit() :
        curEnter=int(curEnter)
    else:
        await message.answer("Incorrect count")
        return
    if(curEnter<=0 or curEnter>100):
        await message.answer("Incorrect count")
        return
    db.set_dailycount(message.from_user.id, curEnter)
    await state.clear()
    await message.answer(f"You would learn {curEnter} at one day")


###REMIND
async def send_remind(bot:Bot, user_id:int)->None:
    await bot.send_message(user_id, "Time to test!!!")

@router.message(Command("remind"))
async def reminder_request(message:Message, state:FSMContext)->None:
    await state.set_state(PersonSettings.waiting_time)
    await message.answer("Send me hour <= 24 and minute<60\nIn format 12:00")

@router.message(PersonSettings.waiting_time)
async def set_reminder(message:Message, state:FSMContext, bot:Bot)->None:
    userMes=message.text
    separatop=userMes.find(':')
    if separatop==-1:
        await message.answer("Incorrect input")
        return
    h=(userMes[:separatop].strip())
    m = (userMes[1+separatop:].strip())
    if  not(h.isdigit()) or not(m.isdigit()):
        await message.answer("Incorrect input")
        return
    h=int(h)
    m=int(m)
    if(h>=0 and h<24 and m>=0 and m<60):
        db.set_reminder(message.from_user.id, h, m)
        await message.answer("Accepted")
        await state.clear()
        scheduler.add_job(
            send_remind,
            trigger=CronTrigger(hour=h, minute=m),
            args=[bot, message.from_user.id],
            id=f"reminder_{message.from_user.id}",
            replace_existing=True
        )
        await state.clear()
    else:
        await message.answer("Incorrect time")
        return
