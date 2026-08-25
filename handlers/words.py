from states.user_states import PersonSettings
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from db import Database

router=Router()
db=Database()
###LIST
@router.message(Command("list"))
async def show_list(message:Message)->None:
    words=db.get_pair_words(message.from_user.id)
    for i in range( len(words)):
        await message.answer(f"{words[i][0]} - {words[i][1]}")

###WORDS
@router.message(Command("words"))
async def set_words_request(message:Message, state:FSMContext)->None:
    await state.set_state(PersonSettings.waiting_words)
    await message.answer('Send me words (example "language being studied - native language"). \nEvery pair-new massage. \nTo stop send me DONE')

@router.message(PersonSettings.waiting_words)
async def set_words_function(message:Message, state:FSMContext)->None:
    curMes=message.text
    if curMes=="DONE":
        await state.clear()
        return
    separator=curMes.find('-')
    if separator==-1:
        await message.answer("Incorrect input")
        return
    w1=curMes[: separator].strip().lower()
    w2=curMes[separator+1:].strip().lower()
    if(len(w1)==0 or len(w2)==0):
        await message.answer("Incorrect input")
        return
    db.add_word_pair(message.from_user.id, w1, w2)
    await message.answer("Added")
###DELETE
@router.message(Command("delete"))
async def delete_request(message:Message, state:FSMContext)->None:
    await message.answer("Send me any words from pair, to delete pair\nTo stop deleting send DONE")
    await state.set_state(PersonSettings.waiting_deleted)

@router.message(PersonSettings.waiting_deleted)
async def deleting_process(message:Message, state:FSMContext)->None:
    word=message.text
    if word=="DONE":
        await state.clear()
        await message.answer("Deleting is ending")
        return
    db.delete_word(message.from_user.id, word)
    await message.answer("Pair deleted ")