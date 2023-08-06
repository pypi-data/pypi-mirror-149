from alicefluentcheck import AliceEntity, AliceIntent
from alicefluentcheck.chain import chained

#########################################################
# ПОДГОТОВКА ЗАПРОСОВ
#########################################################


class AliceRequest:
    def __init__(
        self,
        has_screen=False,
        has_payments=False,
        has_account_linking=False,
        has_audio_player=False,
    ):
        self._new_session = False
        self._command = ""
        self._original_utterance = ""
        self._nlu_tokens = []
        self._intents = {}
        self._entities = []
        self._state_sessions = {}
        self._state_user = {}
        self._state_application = {}
        self._interfaces = {}
        self._access_token = None
        self._account_linking_complete_event = False
        if has_screen:
            self._interfaces["screen"] = {}
        if has_payments:
            self._interfaces["payments"] = {}
        if has_account_linking:
            self._interfaces["account_linking"] = {}
        if has_audio_player:
            self._interfaces["audio_player"] = {}

    @chained
    def new_session(self):
        self._new_session = True

    @chained
    def command(self, command=""):
        self._command = command.lower()
        self.original_utterance(command)

    @chained
    def original_utterance(self, original_utterance=""):
        self._original_utterance = original_utterance
        self.nlu_token(original_utterance.lower().split(" "))

    @chained
    def access_token(self, access_token="777"):
        self._access_token = access_token

    @chained
    def nlu_token(self, tokens: list):
        self._nlu_tokens = tokens

    @chained
    def add_intent(self, intent: AliceIntent):
        self._intents.update(intent.val)

    @chained
    def add_entity(self, entity: AliceEntity):
        self._entities.append(entity.val)

    @chained
    def add_to_state_session(self, name: str, value):
        self._state_sessions[name] = value

    @chained
    def add_to_state_user(self, name: str, value):
        self._state_user[name] = value

    @chained
    def add_to_state_application(self, name: str, value):
        self._state_application[name] = value

    @chained
    def from_scene(self, scene: str):
        self.add_to_state_session("scene", scene)

    @chained
    def account_linking_complete(self):
        self._account_linking_complete_event = True

    def build(self):
        def meta():
            return {
                "locale": "ru-RU",
                "timezone": "UTC",
                "client_id": "AliceMock",
                "interfaces": self._interfaces,
            }

        def session(new=False):
            temp = {
                "message_id": 3,
                "session_id": "d825cbef-e7d6-4af9-9810-3ff3f358ac16",
                "skill_id": "3308dc06-b901-4f7e-8882-beb1b84c0753",
                "user": {"user_id": "000"},
                "application": {"application_id": "000"},
                "user_id": "000",
                "new": new,
            }
            if self._access_token is not None:
                temp["user"]["access_token"] = self._access_token

            return temp

        if self._account_linking_complete_event:
            req = {
                "meta": meta(),
                "session": session(self._new_session),
                "account_linking_complete_event": {},
                "version": "1.0",
                "state": {
                    "session": self._state_sessions,
                    "user": self._state_user,
                    "applications": self._state_application,
                },
            }

        else:
            req = {
                "meta": meta(),
                "session": session(self._new_session),
                "request": {
                    "command": self._command,
                    "original_utterance": self._original_utterance,
                    "nlu": {
                        "tokens": self._nlu_tokens,
                        "entities": self._entities,
                        "intents": self._intents,
                    },
                    "markup": {"dangerous_context": False},
                    "type": "SimpleUtterance",
                },
                "version": "1.0",
                "state": {
                    "session": self._state_sessions,
                    "user": self._state_user,
                    "applications": self._state_application,
                },
            }
        return req
