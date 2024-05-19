from deep_translator import GoogleTranslator


def translate(text: str, language: str) -> str:
    try:
        translated_text = GoogleTranslator(source="auto", target=language).translate(
            text=text
        )
        return translated_text
    except Exception as e:
        raise e
