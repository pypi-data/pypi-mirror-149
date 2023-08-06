import json
from typing import Dict, Union

from fluentcheck import Check

#########################################################
# ВАЛИДАЦИЯ ОТВЕТОВ
#########################################################


class AliceAnswer:
    def __init__(self, answer: Union[str, Dict]):

        if type(answer) is str:
            temp_answer = json.loads(answer)
        else:
            temp_answer = answer

        self.answer = temp_answer

    @property
    def response(self):
        return self.answer.get("response", {})

    @property
    def text(self):
        return self.response.get("text", {})

    @property
    def tts(self):
        return self.response.get("tts", {})

    @property
    def session_state(self):
        return self.answer.get("session_state", {})

    @property
    def user_state(self):
        return self.answer.get("user_state_update", {})

    @property
    def next_scene(self):
        return self.session_state.get("scene")

    @property
    def is_end_of_session(self):
        return self.response.get("end_session", False)

    def get_state_session(self, state: str):
        return self.session_state.get(state, None)

    def get_state_user(self, state: str):
        return self.user_state.get(state, None)

    def has_button(self, name: str) -> bool:
        for button in self.response.get("buttons", []):
            if button.name == name:
                return True
        return False
