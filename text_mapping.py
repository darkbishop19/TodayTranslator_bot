import text_samples


def pick_langs(chosen_language, initial_language):
    if chosen_language == text_samples.english_text:   #1Английский
        chosen_language = 'en'
    if initial_language == text_samples.english_text:
        initial_language = 'en'

    if chosen_language == text_samples.russian_text:  #2Русский
        chosen_language = 'ru'
    if initial_language == text_samples.russian_text:
        initial_language = 'ru'

    if chosen_language == text_samples.german_text:  #3Немецкий
        chosen_language = 'de'
    if initial_language == text_samples.german_text:
        initial_language = 'de'

    if chosen_language == text_samples.chinese_text:  #4Китайский
        chosen_language = 'zh'
    if initial_language == text_samples.chinese_text:
        initial_language = 'zh'

    if chosen_language == text_samples.spanish_text:  #5spanish
        chosen_language = 'es'
    if initial_language == text_samples.spanish_text:
        initial_language = 'es'

    if chosen_language == text_samples.korean_text:  #6korean
        chosen_language = 'ko'
    if initial_language == text_samples.korean_text:
        initial_language = 'ko'

    if chosen_language == text_samples.serbian_text:  #7serbian
        chosen_language = 'sr'
    if initial_language == text_samples.serbian_text:
        initial_language = 'sr'

    if chosen_language == text_samples.polish_text:  #8polish
        chosen_language = 'pl'
    if initial_language == text_samples.polish_text:
        initial_language = 'pl'

    if chosen_language == text_samples.french_text:  #9french
        chosen_language = 'fr'
    if initial_language == text_samples.french_text:
        initial_language = 'fr'

    if chosen_language == text_samples.turkish_text:  #10turkish
        chosen_language = 'tr'
    if initial_language == text_samples.turkish_text:
        initial_language = 'tr'

    if chosen_language == text_samples.swedish_text:  #11swedish
        chosen_language = 'sv'
    if initial_language == text_samples.swedish_text:
        initial_language = 'sv'

    if chosen_language == text_samples.ukrainian_text:  #12ukrainian
        chosen_language = 'uk'
    if initial_language == text_samples.ukrainian_text:
        initial_language = 'uk'

    list_langs = [chosen_language, initial_language]
    return list_langs
