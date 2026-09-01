from aiogram.fsm.state import State, StatesGroup

class PersonSettings(StatesGroup):
    waiting_count = State()
    waiting_words =State()
    waiting_time=State()
    waiting_deleted=State()


class PersonTest(StatesGroup):
    waiting_test1_answer=State()
    waiting_test2_answer = State()