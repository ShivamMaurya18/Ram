import os, uuid, base64, requests, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

try:
    from rembg import remove as rembg_remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "static", "templates_img", "ram_template.png")
LOGO_PATH     = os.path.join(BASE_DIR, "static", "templates_img", "logo.jpeg")
OUTPUT_DIR    = os.path.join(BASE_DIR, "static", "outputs")
UPLOAD_DIR    = os.path.join(BASE_DIR, "static", "uploads")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

POSTER_W = 1080
POSTER_H = 1350


RAM_VARIATIONS = [
    {
        "pose": "standing tall directly behind the person, both hands slightly raised in blessing pose, gentle divine smile",
        "light": "soft golden halo radiating around Lord Ram's entire body",
        "angle": "straight frontal view, symmetrical composition",
    },
    {
        "pose": "standing slightly to the right behind the person, right hand raised high in ashirwad, left hand holding bow, head slightly tilted with a warm smile",
        "light": "golden rays streaming from raised right hand onto person's head like a divine spotlight",
        "angle": "slight three-quarter angle, dynamic composition",
    },
    {
        "pose": "floating slightly above and behind, both arms open wide in a welcoming blessing gesture, serene majestic expression",
        "light": "bright divine aura surrounding Lord Ram, soft white-gold rays descending onto the devotee",
        "angle": "low-angle shot making Lord Ram look grand and towering",
    },
    {
        "pose": "standing to the left behind the person, leaning slightly forward, right palm facing outward in blessing, bow resting on ground, compassionate smile",
        "light": "warm amber golden glow emanating from Lord Ram's palm onto the person's head and shoulders",
        "angle": "slight diagonal composition with golden sunset lighting",
    },
    {
        "pose": "standing majestically behind with one foot slightly forward, right hand raised in abhay mudra blessing, bow held upright, radiant joyful expression",
        "light": "divine light beams in multiple rays from raised hand, particles of golden light floating in air",
        "angle": "wide cinematic shot with temple grandly visible behind",
    },
]


def _describe_face(user_img):
    if not OPENAI_API_KEY:
        return "a young Indian person with dark hair and warm skin tone"
    try:
        img_small = user_img.convert("RGB").copy()
        img_small.thumbnail((512, 512), Image.LANCZOS)
        buf = BytesIO()
        img_small.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        payload = {
            "model": "gpt-4o",
            "max_tokens": 200,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64}",
                            "detail": "low"
                        }
                    },
                    {
                        "type": "text",
                        "text": (
                            "Describe this person's physical appearance for an art prompt. "
                            "Include: face shape, skin tone, hair color and style, eye color, "
                            "approximate age, clothing color and style. "
                            "Be specific, max 60 words. Just the description, no intro."
                        )
                    }
                ]
            }]
        }

        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type":  "application/json"
            },
            json=payload,
            timeout=30
        )
        result = resp.json()
        desc   = result["choices"][0]["message"]["content"].strip()
        print(f"[image_utils] Face desc: {desc}")
        return desc

    except Exception as e:
        print(f"[image_utils] Face desc failed: {e}")
        return "a young Indian person with dark hair and warm brown skin tone"


def _ghibli_via_edit(user_img):
    try:
        print("[image_utils] Trying gpt-image-1 edit endpoint...")

        variation = random.choice(RAM_VARIATIONS)
        print(f"[image_utils] Ram variation: {variation['angle']}")

        rgb = user_img.convert("RGB")
        rgb.thumbnail((1024, 1024), Image.LANCZOS)
        buf = BytesIO()
        rgb.save(buf, format="PNG")
        buf.seek(0)

        prompt = (
            "Transform this entire image into a Studio Ghibli style animated illustration. "
            "Keep the person's face, features, hair, and clothing EXACTLY recognizable. "
            "COMPOSITION  very important: "
            "WIDE establishing shot, fully zoomed out so the entire scene fits in frame. "
            f"Camera angle: {variation['angle']}. "
            "The person (user) is in the FOREGROUND center, FRONT FACING, clearly visible. "
            f"Lord Ram (blue skin, warm SMILE, saffron dhoti, golden crown, holding bow)  {variation['pose']}. "
            "Lord Ram's ENTIRE body from head to feet must be FULLY visible, NOT cropped. "
            f"Lighting: {variation['light']}. "
            "Blessing rays land on person's HEAD and SHOULDERS ONLY  not entire body. "
            "Behind Lord Ram: GRAND ancient Hindu temple FULLY visible  "
            "tall shikhar spires reaching sky, "
            "saffron/orange triangular flags flying on ALL temple spires. "
            "Marigold flower decorations, lotus flowers on floor, golden ambient light. "
            "Painterly Ghibli textures, soft anime lines, warm saffron and gold palette. "
            "NO text, NO watermark, NO border anywhere."    
        )

        response = requests.post(
            "https://api.openai.com/v1/images/edits",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"image": ("photo.png", buf, "image/png")},
            data={
                "model":  "gpt-image-1",
                "prompt": prompt,
                "n":      "1",
                "size":   "1024x1024",
            },
            timeout=120
        )

        result = response.json()

        if "error" in result:
            print(f"[image_utils] Edit endpoint error: {result['error']['message']}")
            return None

        img_data = result["data"][0]
        if "b64_json" in img_data:
            return Image.open(
                BytesIO(base64.b64decode(img_data["b64_json"]))
            ).convert("RGBA")
        else:
            r = requests.get(img_data["url"], timeout=30)
            return Image.open(BytesIO(r.content)).convert("RGBA")

    except Exception as e:
        print(f"[image_utils] Edit endpoint failed: {e}")
        return None


def _ghibli_via_generation(face_desc):
    try:
        print("[image_utils] Trying dall-e-3 generation fallback...")

        variation = random.choice(RAM_VARIATIONS)
        print(f"[image_utils] Ram variation: {variation['angle']}")

        prompt = (
            f"Studio Ghibli style animated illustration, Hayao Miyazaki film aesthetic. "
            f"WIDE establishing shot  fully zoomed out, entire scene visible in frame. "
            f"Camera angle: {variation['angle']}. "
            f"COMPOSITION: "
            f"A young person ({face_desc}) stands in FOREGROUND center, "
            f"FRONT FACING THE VIEWER, clearly visible. "
            f"Lord Ram  blue skin, warm SMILE, saffron dhoti, golden crown, bow in hand  "
            f"{variation['pose']}. "
            f"Lord Ram ENTIRE body head to feet FULLY visible, NOT cropped. "
            f"Lighting: {variation['light']}. "
            f"Blessing rays land on person's HEAD and SHOULDERS ONLY. "
            f"Behind Lord Ram: GRAND ancient Hindu temple FULLY visible in background  "
            f"tall shikhar spires reaching the sky. "
            f"Saffron/orange triangular flags flying on ALL temple spires. "
            f"Stone carved arches, marigold garland decorations, "
            f"golden light, lotus flowers on marble floor. "
            f"Warm saffron, gold, cream color palette. "
            f"Soft painterly Ghibli textures, clean anime lines, cinematic wide framing. "
            f"NO text, NO watermark, NO border anywhere. "
            f"High detail, 4K quality illustration."
        )

        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type":  "application/json"
            },
            json={
                "model":   "dall-e-3",
                "prompt":  prompt,
                "n":       1,
                "size":    "1024x1024",
                "quality": "hd",
                "style":   "vivid",
            },
            timeout=120
        )

        result = response.json()

        if "error" in result:
            print(f"[image_utils] dall-e-3 error: {result['error']['message']}")
            return None

        img_url = result["data"][0]["url"]
        r       = requests.get(img_url, timeout=30)
        return Image.open(BytesIO(r.content)).convert("RGBA")

    except Exception as e:
        print(f"[image_utils] dall-e-3 failed: {e}")
        return None


def _cartoon_fallback(img):
    has_alpha = img.mode == "RGBA"
    if has_alpha:
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
    else:
        rgb = img.convert("RGB")
        a   = None

    for _ in range(3):
        rgb = rgb.filter(ImageFilter.SMOOTH_MORE)
    rgb = rgb.filter(ImageFilter.EDGE_ENHANCE_MORE)
    rgb = rgb.filter(ImageFilter.SMOOTH)
    rgb = ImageEnhance.Color(rgb).enhance(1.9)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.35)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    rgb = ImageEnhance.Sharpness(rgb).enhance(2.2)

    if has_alpha:
        rgb = rgb.convert("RGBA")
        rgb.putalpha(a)
    return rgb


def remove_background(path):
    with open(path, "rb") as f:
        raw = f.read()
    if REMBG_AVAILABLE:
        return Image.open(BytesIO(rembg_remove(raw))).convert("RGBA")
    return Image.open(path).convert("RGBA")


def _place_user_fallback(user_img):
    max_h = int(POSTER_H * 0.85)
    max_w = int(POSTER_W * 0.70)
    scale = min(max_h / user_img.height, max_w / user_img.width)
    nw    = int(user_img.width  * scale)
    nh    = int(user_img.height * scale)
    user_img = user_img.resize((nw, nh), Image.LANCZOS)
    x = (POSTER_W - nw) // 2
    y = POSTER_H - nh - 20
    return user_img, (x, y)


def _shadow(img, off=10, blur=16):
    sh = Image.new("RGBA", img.size, (0,0,0,0))
    sc = Image.new("RGBA", img.size, (0,0,0,120))
    sc.putalpha(img.split()[3])
    sh.paste(sc, (off, off))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", img.size, (0,0,0,0))
    out.paste(sh)
    out.paste(img, (0,0), img)
    return out


def _gradient_bg(w, h):
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    for row in range(h):
        t = row / h
        arr[row,:] = [int(165*(1-t)+8*t), int(52*(1-t)+4*t), int(8*(1-t)+2*t), 255]
    return Image.fromarray(arr, "RGBA")


def _vignette(img, strength=0.30):
    w, h = img.size
    v    = Image.new("L", (w, h), 0)
    dv   = ImageDraw.Draw(v)
    half = min(w,h) // 2
    for i in range(half):
        t = i / half
        dv.rectangle([i,i,w-i,h-i], outline=int(255*strength*(1-t)**1.6))
    v   = v.filter(ImageFilter.GaussianBlur(55))
    drk = Image.new("RGBA", (w,h), (0,0,0,0))
    drk.putalpha(v)
    return Image.alpha_composite(img.convert("RGBA"), drk)


def _add_logo_watermark(poster):
    """
    Background removed logo  directly overlay on poster.
    Semi-transparent, bottom right corner.
    """
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")

        # Resize logo  170px wide
        logo_w = 170
        ratio  = logo_w / logo.width
        logo_h = int(logo.height * ratio)
        logo   = logo.resize((logo_w, logo_h), Image.LANCZOS)

        # Make semi-transparent (65% opacity)
        r, g, b, a = logo.split()
        a = a.point(lambda x: int(x * 0.65))
        logo.putalpha(a)

        # Position  bottom right, 20px padding
        x = POSTER_W - logo_w - 20
        y = POSTER_H - logo_h - 20

        result = poster.copy()
        result.paste(logo, (x, y), logo)
        return result

    except Exception as e:
        print(f"[image_utils] Logo watermark failed: {e}")
        return poster


def generate_poster(user_image_path, name, blessing_message, mulank_data):

    user_raw   = Image.open(user_image_path).convert("RGBA")
    ghibli_img = None

    if OPENAI_API_KEY:
        ghibli_img = _ghibli_via_edit(user_raw)
        if ghibli_img is None:
            face_desc  = _describe_face(user_raw)
            ghibli_img = _ghibli_via_generation(face_desc)

    if ghibli_img:
        poster = ghibli_img.convert("RGBA").resize(
            (POSTER_W, POSTER_H), Image.LANCZOS
        )
        poster = _vignette(poster)

    else:
        print("[image_utils] All API methods failed  using cartoon fallback.")
        try:
            bg = Image.open(TEMPLATE_PATH).convert("RGBA")
        except FileNotFoundError:
            bg = _gradient_bg(POSTER_W, POSTER_H)

        bg = bg.resize((POSTER_W, POSTER_H), Image.LANCZOS)
        bg = _vignette(bg)

        user_cut     = remove_background(user_image_path)
        user_cartoon = _cartoon_fallback(user_cut)
        user_cartoon = _shadow(user_cartoon)
        user_cartoon, pos = _place_user_fallback(user_cartoon)

        poster = bg.copy()
        poster.paste(user_cartoon, pos, user_cartoon)

    poster = _add_logo_watermark(poster)

    out      = poster.convert("RGB")
    filename = f"poster_{uuid.uuid4().hex[:10]}.jpg"
    out.save(os.path.join(OUTPUT_DIR, filename), "JPEG", quality=95)
    return f"static/outputs/{filename}"