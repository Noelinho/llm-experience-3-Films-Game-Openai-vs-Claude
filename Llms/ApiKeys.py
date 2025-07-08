class ApiKeys:
    @staticmethod
    def open_ai_api_key():
        from dotenv import load_dotenv
        import os
        load_dotenv(override=True)
        return os.getenv('OPENAI_API_KEY')

    @staticmethod
    def anthropic_api_key():
        from dotenv import load_dotenv
        import os
        load_dotenv(override=True)
        return os.getenv('ANTHROPIC_API_KEY')