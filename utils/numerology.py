# utils/numerology.py
# ============================================================
#  Hardcoded Vedic Numerology (Mulank) Engine – No API needed
# ============================================================

MULANK_DATA = {
    1: {
        "planet": "☀️ Surya (Sun)",
        "ruling": "Sun",
        "traits": "Leadership, confidence, authority, originality",
        "positive": "Ambitious, bold, independent, natural leader, creative visionary",
        "negative": "Ego-driven, domineering, impatient, sometimes lonely at the top",
        "prediction": (
            "2026 is a year of powerful new beginnings for you. The Sun illuminates your path  "
            "expect recognition at work, a chance to lead a significant project, or a new role that "
            "puts your talents in the spotlight. Relationships deepen when you soften your need to "
            "always be right. A financial breakthrough is possible in the second half of the year."
        ),
        "advice": (
            "Channel your natural authority with humility. Collaborate instead of commanding. "
            "Morning sunlight meditation for 10 minutes will keep your energy centred and your "
            "decisions sharp."
        ),
        "blessing_style": "regal and empowering",
        "color": "#FF6B35",
        "lucky_number": 1,
        "lucky_day": "Sunday",
    },
    2: {
        "planet": "🌙 Chandra (Moon)",
        "ruling": "Moon",
        "traits": "Sensitivity, intuition, diplomacy, nurturing",
        "positive": "Empathetic, cooperative, artistic, deeply intuitive, loyal",
        "negative": "Moody, over-sensitive, indecisive, prone to self-doubt",
        "prediction": (
            "2026 brings emotional growth and meaningful connections. The Moon's influence deepens "
            "your intuition trust your gut feelings this year, especially in matters of the heart. "
            "A close relationship may evolve to a new level of commitment. Career-wise, your "
            "collaborative nature will be your greatest asset; partnerships formed this year "
            "could prove very fruitful."
        ),
        "advice": (
            "Stop second-guessing yourself  your first instinct is usually correct. Protect your "
            "emotional energy by setting gentle but firm boundaries. Journaling before bed helps "
            "you process feelings and wake up with clarity."
        ),
        "blessing_style": "gentle and nurturing",
        "color": "#C9D6FF",
        "lucky_number": 2,
        "lucky_day": "Monday",
    },
    3: {
        "planet": "♃ Brihaspati (Jupiter)",
        "ruling": "Jupiter",
        "traits": "Creativity, expression, joy, optimism, social charm",
        "positive": "Charismatic, witty, artistic, inspiring communicator, lucky",
        "negative": "Scattered energy, superficial at times, avoids deep responsibility",
        "prediction": (
            "2026 showers you with Jupiter's abundant blessings. Your creativity peaks  a personal "
            "project, a side hustle, or a creative endeavour started this year has real potential "
            "to take off. Social opportunities will be plentiful; say yes more often. A trip or "
            "educational pursuit in mid-year could completely change your perspective."
        ),
        "advice": (
            "Discipline your creative energy instead of spreading it thin. Pick one big idea and "
            "see it through to completion. Gratitude practice every morning amplifies Jupiter's "
            "expansion in your life."
        ),
        "blessing_style": "joyful and expansive",
        "color": "#F7DC6F",
        "lucky_number": 3,
        "lucky_day": "Thursday",
    },
    4: {
        "planet": "♄ Rahu (North Node)",
        "ruling": "Rahu",
        "traits": "Stability, discipline, hard work, practicality, loyalty",
        "positive": "Reliable, methodical, honest, patient, strong foundations-builder",
        "negative": "Rigid, stubborn, over-cautious, resistant to change",
        "prediction": (
            "2026 rewards your relentless hard work. The seeds you planted in past years are ready "
            "to bear fruit  expect tangible results in your career or finances around mid-year. "
            "Rahu pushes you out of your comfort zone; an unexpected opportunity may arrive "
            "disguised as disruption. Embrace it. Home and family matters also stabilise."
        ),
        "advice": (
            "Learn to bend without breaking  flexibility is your growth edge this year. Take "
            "calculated risks instead of waiting for a perfect moment that may never come. A "
            "structured weekly plan will keep you productive without burning out."
        ),
        "blessing_style": "grounding and steadfast",
        "color": "#85C1E9",
        "lucky_number": 4,
        "lucky_day": "Saturday",
    },
    5: {
        "planet": "☿ Budha (Mercury)",
        "ruling": "Mercury",
        "traits": "Freedom, adventure, versatility, quick thinking, communication",
        "positive": "Adaptable, curious, persuasive, energetic, multi-talented",
        "negative": "Restless, impulsive, inconsistent, commitment-averse",
        "prediction": (
            "2026 is your year of movement and discovery. Mercury blesses you with sharp wit and "
            "magnetic communication  public speaking, writing, or media could open major doors. "
            "Travel, whether physical or intellectual, will spark your most transformative ideas. "
            "Multiple income streams or a career pivot are strongly indicated."
        ),
        "advice": (
            "Ground your restless energy with a daily routine  even 30 minutes of stillness keeps "
            "you sharp. Finish what you start before chasing the next shiny opportunity. Your words "
            "carry enormous power in 2026; use them wisely."
        ),
        "blessing_style": "dynamic and adventurous",
        "color": "#A9DFBF",
        "lucky_number": 5,
        "lucky_day": "Wednesday",
    },
    6: {
        "planet": "♀ Shukra (Venus)",
        "ruling": "Venus",
        "traits": "Love, harmony, responsibility, beauty, family devotion",
        "positive": "Caring, artistic, compassionate, reliable, magnetically attractive",
        "negative": "Self-sacrificing to a fault, people-pleasing, possessive",
        "prediction": (
            "2026 wraps you in Venus's warm, golden light. Love and relationships are the central "
            "theme  whether deepening an existing bond, healing a past wound, or welcoming a new "
            "connection. Home improvements, creative projects, and artistic endeavours thrive. "
            "Financially, generosity flows back to you multiplied."
        ),
        "advice": (
            "Put yourself on your own care list. You give so freely to others that you sometimes "
            "forget to nourish your own soul. Saying no to energy-draining commitments is an act "
            "of self-love, not selfishness."
        ),
        "blessing_style": "loving and harmonious",
        "color": "#F1948A",
        "lucky_number": 6,
        "lucky_day": "Friday",
    },
    7: {
        "planet": "☽ Ketu (South Node)",
        "ruling": "Ketu",
        "traits": "Wisdom, introspection, spirituality, analysis, mystery",
        "positive": "Intellectual, perceptive, philosophical, spiritually gifted, truthful",
        "negative": "Withdrawn, overly secretive, prone to isolation, sceptical",
        "prediction": (
            "2026 is a deeply spiritual and introspective year for you. Ketu dissolves the "
            "unnecessary  old patterns, toxic connections, and limiting beliefs fall away, making "
            "room for profound inner growth. Research, study, or spiritual practice begun this "
            "year will yield life-changing insights. Trust the divine timing of everything."
        ),
        "advice": (
            "Spend time in nature and silence  your answers come in the quiet spaces, not in the "
            "noise. Don't resist solitude; it is your superpower. Share your wisdom more openly; "
            "the world benefits from your unique depth of understanding."
        ),
        "blessing_style": "mystical and profound",
        "color": "#A569BD",
        "lucky_number": 7,
        "lucky_day": "Monday",
    },
    8: {
        "planet": "♄ Shani (Saturn)",
        "ruling": "Saturn",
        "traits": "Power, ambition, karma, material mastery, resilience",
        "positive": "Strategic, disciplined, executive-minded, unstoppable, magnetically authoritative",
        "negative": "Workaholic, materialistic, controlling, slow to forgive",
        "prediction": (
            "2026 is a karmic turning point. Saturn's discipline pays off with major material "
            "rewards  a business expansion, a significant promotion, or a long-sought financial "
            "milestone becomes achievable. However, shortcuts will backfire; integrity is your "
            "currency this year. Health and work-life balance deserve equal attention alongside "
            "your ambitions."
        ),
        "advice": (
            "Success is inevitable for you  slow down enough to actually enjoy it. Delegate more, "
            "control less. The universe is asking you to trust the process rather than "
            "micromanage every outcome."
        ),
        "blessing_style": "powerful and karmic",
        "color": "#1C2833",
        "lucky_number": 8,
        "lucky_day": "Saturday",
    },
    9: {
        "planet": "♂ Mangal (Mars)",
        "ruling": "Mars",
        "traits": "Humanitarianism, compassion, completion, wisdom, courage",
        "positive": "Generous, idealistic, courageous, deeply empathetic, globally minded",
        "negative": "Over-idealistic, self-righteous, emotionally volatile, scattered",
        "prediction": (
            "2026 marks a powerful culmination for you. Mars fires your compassion and courage  "
            "you may feel called to serve a larger purpose, lead a community initiative, or "
            "complete a long-standing personal chapter. A cycle that began 9 years ago reaches "
            "its conclusion, clearing the way for an entirely new beginning. Let go gracefully."
        ),
        "advice": (
            "Release what no longer serves you  people, grudges, habits, and roles you have "
            "outgrown. Your greatest strength is your heart; lead with it. Forgiveness, both "
            "of yourself and others, is the master key to your 2026 transformation."
        ),
        "blessing_style": "compassionate and transcendent",
        "color": "#E74C3C",
        "lucky_number": 9,
        "lucky_day": "Tuesday",
    },
}


def calculate_mulank(dob: str) -> int:
    """
    Calculate Mulank from DOB.
    Accepts: DD-MM-YYYY | DD/MM/YYYY | YYYY-MM-DD
    Returns integer 1–9.
    """
    dob = dob.replace("/", "-").strip()
    parts = dob.split("-")
    day = int(parts[2]) if len(parts[0]) == 4 else int(parts[0])

    total = sum(int(d) for d in str(day))
    while total > 9:
        total = sum(int(d) for d in str(total))

    return total if total != 0 else 9


def get_numerology_data(dob: str) -> dict:
    mulank = calculate_mulank(dob)
    data = MULANK_DATA.get(mulank, MULANK_DATA[1]).copy()
    data["mulank"] = mulank
    return data