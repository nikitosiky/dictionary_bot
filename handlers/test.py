from states.user_states import PersonTest
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from db import Database

db=Database()
router=Router()

###TESTING
@router.message(Command("test"))
async def test_request(message:Message)->None:
    kb=[[
        KeyboardButton(text="From native to learning"),
        KeyboardButton(text="From learning to native")
    ]]
    keyboard=ReplyKeyboardMarkup(keyboard =kb, resize_keyboard=True)
    await message.answer("Select the test mode", reply_markup=keyboard)

#1
@router.message(F.text=="From native to learning")
async def test_answer12(message: Message,  state:FSMContext):

    words = db.get_pair_words(message.from_user.id)
    if len(words)==0:
        await message.answer("No words for testing", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    await state.update_data(
        index=len(words)-1,
        words=words,
        corrected=0
    )
    await message.answer(words[len(words)-1][1], reply_markup=ReplyKeyboardRemove())
    await state.set_state(PersonTest.waiting_test1_answer)

@router.message(PersonTest.waiting_test1_answer)
async def test_answer(message: Message, state:FSMContext)->None:
    data= await state.get_data()
    words=data["words"]
    current_index=data["index"]
    corrected_answ=data["corrected"]

    correct_answer=words[current_index][0]
    user_answer=message.text.strip()
    if user_answer=="DONE":
        await message.answer(f"Test is ending with corrected answer: {corrected_answ}")
        await state.clear()
        return
    user_answer=user_answer.lower()
    if correct_answer==user_answer:
        await message.answer("Corrected")
        corrected_answ+=1
    else:
        await message.answer(f"Uncorrected , corrected {correct_answer}")
    current_index-=1
    if current_index<0:
        await message.answer(f"Test is ending with corrected answer: {corrected_answ}")
        await state.clear()
    else:
        await state.update_data(
            index=current_index,
            corrected=corrected_answ
        )
        await message.answer(words[current_index][1])

#2
@router.message(F.text=="From learning to native")
async def test_answer12(message: Message, state: FSMContext):
    words = db.get_pair_words(message.from_user.id)
    if len(words) == 0:
        await message.answer("No words for testing",  reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    await state.update_data(
        index=len(words) - 1,
        words=words,
        corrected=0
    )
    await message.answer(words[len(words) - 1][0], reply_markup=ReplyKeyboardRemove())
    await state.set_state(PersonTest.waiting_test2_answer)


@router.message(PersonTest.waiting_test2_answer)
async def test_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    words = data["words"]
    current_index = data["index"]
    corrected_answ = data["corrected"]

    correct_answer = words[current_index][1]
    user_answer = message.text.strip()
    if user_answer == "DONE":
        await message.answer(f"Test is ending with corrected answer: {corrected_answ}")
        await state.clear()
        return
    user_answer = user_answer.lower()
    if correct_answer == user_answer:
        await message.answer("Corrected")
        corrected_answ += 1
    else:
        await message.answer(f"Uncorrected , corrected {correct_answer}")
    current_index -= 1
    if current_index < 0:
        await message.answer(f"Test is ending with corrected answer: {corrected_answ}")
        await state.clear()
    else:
        await state.update_data(
            index=current_index,
            corrected=corrected_answ
        )
        await message.answer(words[current_index][0])
