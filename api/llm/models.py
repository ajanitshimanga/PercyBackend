from enum import Enum

class OpenAIModels(str, Enum):
    GPT_4 = "gpt-4"
    GPT_4_O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    
    @classmethod
    def default(cls) -> "OpenAIModels":
        return cls.GPT_4_O
