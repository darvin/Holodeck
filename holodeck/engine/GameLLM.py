


from enum import Enum

class GameLLMResponseType(str, Enum):
    ERROR = "error"
    IMMEDIATE_ACTION = "immediate_action"
    TURNS_START = "turns_start"

class GameLLMResponse:
    def __init__(self, 
                 type:GameLLMResponseType=GameLLMResponseType.IMMEDIATE_ACTION, 
                 text:str="", 
                 sql:str=None, 
                 sqls:list[str]=[]) -> None:
        self.type = type
        self.text = text
        self.sql = sql
        self.sqls = sqls
