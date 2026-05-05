from src.config.llm_settings import LLMSettings
from src.config.tableau_settings import TableauSettings


class Settings:
    def __init__(self):
        self.llm = LLMSettings()
        self.tableau = TableauSettings()


settings = Settings()
