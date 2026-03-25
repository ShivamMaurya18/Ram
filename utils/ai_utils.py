# utils/ai_utils.py
# ============================================================
#  Offline Blessing Message Generator  No API, No Internet
#  Uses name + Mulank to build personalised human-like messages
# ============================================================

import random
import hashlib


# ── Name-based seed so same person always gets same blessing ──────────────────
def _name_seed(name: str) -> int:
    return int(hashlib.md5(name.lower().strip().encode()).hexdigest(), 16)


# ── Blessing templates per Mulank ─────────────────────────────────────────────
# Each Mulank has multiple templates; one is picked based on name hash.
# {name} is replaced with the actual user name.

BLESSING_TEMPLATES = {
    1: [
        "May Lord Ram's radiant light forever guide your path, {name}. Just as the Sun rises without fail, your courage and leadership shall illuminate every room you enter. On this sacred Ram Navami, Prabhu Ram blesses you with the strength to lead and the grace to inspire. Jai Shri Ram!",
        "Dear {name}, on this divine Ram Navami, may Shri Ram crown your efforts with victory and your heart with peace. You were born to lead  may His blessings sharpen your vision and steady your hand in all that you pursue. Jai Shri Ram!",
        "Prabhu Ram smiles upon you today, {name}, for your fearless spirit mirrors His own. May this Ram Navami mark the beginning of your greatest chapter  one written in courage, purpose, and unshakeable faith. Jai Shri Ram!",
    ],
    2: [
        "Dear {name}, may Lord Ram's gentle grace wrap around your tender heart like a warm light on a quiet evening. Your compassion is a gift to this world  may Prabhu Ram multiply it a thousandfold this Ram Navami. Jai Shri Ram!",
        "On this blessed Ram Navami, may Shri Ram fill your days with harmony, love, and the deep peace that only devotion can bring, {name}. Your caring soul is seen and cherished by the divine. Jai Shri Ram!",
        "May Lord Ram bless your intuitive heart, {name}, for it carries His wisdom without even knowing. This Ram Navami, may every relationship in your life deepen with trust and every prayer be answered with love. Jai Shri Ram!",
    ],
    3: [
        "On this joyful Ram Navami, may Lord Ram bless your creative spirit with inspiration that never fades, {name}. Your laughter is seva, your art is prayer  may Prabhu Ram expand your world in beautiful, unexpected ways. Jai Shri Ram!",
        "Dear {name}, may Shri Ram's blessings flow through your words, your ideas, and your smile today and always. You carry joy wherever you go  may this Ram Navami fill your life with the same abundance you give to others. Jai Shri Ram!",
        "Prabhu Ram blesses those with a joyful heart, and yours, {name}, is one of the brightest. May this Ram Navami open doors of creativity, opportunity, and divine favour that lead you to your highest purpose. Jai Shri Ram!",
    ],
    4: [
        "Dear {name}, may Lord Ram honour your steadfast dedication on this sacred Ram Navami. Like the foundations of Ayodhya, your loyalty and hard work shall never crumble  may Prabhu Ram reward your patience with lasting prosperity. Jai Shri Ram!",
        "On this divine Ram Navami, may Shri Ram bless your disciplined hands and honest heart, {name}. Every brick you lay in life with sincerity is a prayer He hears  may this year bring the harvest of all your quiet efforts. Jai Shri Ram!",
        "May Lord Ram's blessings fortify your already unshakeable spirit, {name}. You build where others give up  may Prabhu Ram stand beside you on this Ram Navami and elevate everything you have worked so hard to create. Jai Shri Ram!",
    ],
    5: [
        "Dear {name}, may Lord Ram's blessings travel with you on every road you choose to walk. Your restless spirit is a divine gift  may this Ram Navami open the most unexpected and beautiful doors your adventurous heart has ever dreamed of. Jai Shri Ram!",
        "On this sacred Ram Navami, may Prabhu Ram bless your quick mind and free spirit, {name}. The world is your dharma  may He guide every leap of faith you take and turn every new beginning into a blessing. Jai Shri Ram!",
        "May Lord Ram's grace sharpen your many gifts, {name}, and grant you the wisdom to channel them with purpose. This Ram Navami, may Shri Ram walk beside you on your most exciting journey yet. Jai Shri Ram!",
    ],
    6: [
        "Dear {name}, may Lord Ram bless your loving heart and the beautiful home you nurture for those around you. On this Ram Navami, may Prabhu Ram fill every corner of your life with warmth, harmony, and the quiet joy of being truly loved. Jai Shri Ram!",
        "On this sacred Ram Navami, may Shri Ram honour your selfless devotion, {name}. You give without counting the cost  may the divine return every act of love you have offered, multiplied beyond measure. Jai Shri Ram!",
        "May Lord Ram's grace surround your family and fill your heart with peace, {name}. Your loving nature reflects Maa Sita's grace itself  may this Ram Navami be the most beautiful one your home has ever known. Jai Shri Ram!",
    ],
    7: [
        "Dear {name}, may Lord Ram illuminate the deep wisdom that already lives within your searching soul. On this Ram Navami, may Prabhu Ram draw back the veil and reveal the truths you have been quietly seeking all along. Jai Shri Ram!",
        "On this divine Ram Navami, may Shri Ram bless your contemplative mind and perceptive heart, {name}. You see what others miss  may His grace turn your deepest insights into your greatest gifts this year. Jai Shri Ram!",
        "May Lord Ram honour your spiritual journey, {name}, for it is walked with rare sincerity. This Ram Navami, may Prabhu Ram bring you the inner peace and the profound answers that your soul has long deserved. Jai Shri Ram!",
    ],
    8: [
        "Dear {name}, may Lord Ram bless your powerful resolve and unbreakable ambition on this sacred Ram Navami. You are built to create empires of meaning  may Prabhu Ram stand behind every bold decision you make this year. Jai Shri Ram!",
        "On this divine Ram Navami, may Shri Ram reward your discipline and strategic mind, {name}. Every sacrifice you have made in pursuit of your goals is known to the divine  may this year deliver what you have rightfully earned. Jai Shri Ram!",
        "May Lord Ram's justice and strength walk beside you always, {name}. On this Ram Navami, may Prabhu Ram bless your endeavours with unstoppable momentum and your heart with the humility to carry success with grace. Jai Shri Ram!",
    ],
    9: [
        "Dear {name}, may Lord Ram bless your generous soul and the boundless compassion that makes you a light for everyone around you. On this Ram Navami, may Prabhu Ram complete every noble chapter you have begun and open a magnificent new one. Jai Shri Ram!",
        "On this sacred Ram Navami, may Shri Ram honour your selfless heart, {name}. You carry the torch of dharma with rare courage  may His blessings bring you the peace and fulfilment that your giving spirit so deeply deserves. Jai Shri Ram!",
        "May Lord Ram's grace wrap around your compassionate heart, {name}. This Ram Navami, may every act of kindness you have offered return to you as divine blessing, and may Prabhu Ram guide you gently into your most purposeful chapter yet. Jai Shri Ram!",
    ],
}


def generate_blessing_message(name: str, mulank_data: dict) -> str:
    """
    Generate a personalised blessing using name + Mulank.
    Fully offline  no API, no internet required.
    Same name always gets the same blessing (consistent experience).
    """
    mulank    = mulank_data.get("mulank", 1)
    templates = BLESSING_TEMPLATES.get(mulank, BLESSING_TEMPLATES[1])

    # Use name-based hash to pick template  deterministic per person
    seed  = _name_seed(name)
    index = seed % len(templates)

    blessing = templates[index].format(name=name)
    return blessing


# Keep this as an alias so app.py needs zero changes
def get_fallback_blessing(name: str, mulank: int) -> str:
    templates = BLESSING_TEMPLATES.get(mulank, BLESSING_TEMPLATES[1])
    seed  = _name_seed(name)
    index = seed % len(templates)
    return templates[index].format(name=name)