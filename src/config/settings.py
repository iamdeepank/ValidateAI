from src.config.llm_settings import LLMSettings
from src.config.tableau_settings import TableauSettings
from src.config.db_settings import DBSettings


class Settings:
    def __init__(self):
        self.llm = LLMSettings()
        self.tableau = TableauSettings()
        self.db=DBSettings()


settings = Settings()
