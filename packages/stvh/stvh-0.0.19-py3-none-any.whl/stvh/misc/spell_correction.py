class SpellCorrection:
    def __init__(self, lang: str = "en-US") -> None:
        import language_tool_python

        self.tool = language_tool_python.LanguageTool(lang)

    def correct(self, text: str) -> str:
        return self.tool.correct(text)

    def __call__(self, text: str) -> str:
        return self.correct(text)
