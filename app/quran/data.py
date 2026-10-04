AL_FATIHA = {
    1: "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    2: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
    3: "الرَّحْمَٰنِ الرَّحِيمِ",
    4: "مَالِكِ يَوْمِ الدِّينِ",
    5: "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
    6: "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
    7: "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
}

SURAHS = {
    1: {
        "name_ar": "الفاتحة",
        "name_en": "Al-Fatihah",
        "ayahs": AL_FATIHA,
    }
}


def get_ayah(surah: int, ayah: int) -> str | None:
    surah_data = SURAHS.get(surah)
    if not surah_data:
        return None
    return surah_data["ayahs"].get(ayah)


def get_surah(surah: int) -> dict | None:
    return SURAHS.get(surah)
