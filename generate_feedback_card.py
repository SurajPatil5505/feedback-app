from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def generate_card(image_path, logo_path, name, feedback, output_path, theme="orange"):
    # Themes
    THEMES = {
        "orange": {
            "bg": (255, 255, 255),
            "accent": (255, 102, 0),
            "text": (59, 33, 123),
            "footer": (255, 102, 0),
            "inner_rect": (255, 240, 220)
        },
        "purple": {
            "bg": (235, 230, 255),
            "accent": (128, 0, 128),
            "text": (50, 0, 100),
            "footer": (200, 100, 0),
            "inner_rect": (220, 200, 255)
        },
        "blue": {
            "bg": (220, 240, 255),
            "accent": (0, 102, 204),
            "text": (0, 51, 102),
            "footer": (255, 102, 0),
            "inner_rect": (200, 225, 255)
        }
    }
    style = THEMES.get(theme, THEMES["orange"])

    # Constants
    CARD_W, CARD_H = 1000, 1100
    PHOTO_SIZE = 520
    MARGIN = 50
    INNER_MARGIN = 30
    BORDER_RADIUS = 60
    BUBBLE_PADDING = 50

    # Fonts
    font_dir = "fonts"
    try:
        company_font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), 34)
        feedback_font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans.ttf"), 28)
        name_font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), 28)
    except:
        company_font = feedback_font = name_font = ImageFont.load_default()

    # Base card
    card = Image.new("RGB", (CARD_W, CARD_H), style["bg"])
    draw = ImageDraw.Draw(card)

    # Draw inner rounded rectangle background
    inner_rect = (
        INNER_MARGIN,
        INNER_MARGIN,
        CARD_W - INNER_MARGIN,
        CARD_H - INNER_MARGIN
    )
    draw.rounded_rectangle(inner_rect, radius=BORDER_RADIUS, fill=style["inner_rect"])

    # Draw circular logo
    if logo_path and os.path.exists(logo_path):
        logo_size = 70
        logo = Image.open(logo_path).convert("RGBA").resize((logo_size, logo_size))

        # Mask logo to be circular
        mask = Image.new("L", (logo_size, logo_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, logo_size, logo_size), fill=255)

        circular_logo = Image.new("RGBA", (logo_size, logo_size))
        circular_logo.paste(logo, (0, 0), mask=mask)

        card.paste(circular_logo, (MARGIN, MARGIN), mask=mask)

    # Company name beside logo
    company_name = "ifm engineering pvt ltd"
    draw.text((MARGIN + 80, MARGIN + 20), company_name, font=company_font, fill=style["text"])

    # Create circular photo with speech bubble style background
    orig = Image.open(image_path).convert("RGBA").resize((PHOTO_SIZE, PHOTO_SIZE))
    mask = Image.new("L", (PHOTO_SIZE, PHOTO_SIZE), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, PHOTO_SIZE, PHOTO_SIZE), fill=255)

    circular_photo = Image.new("RGBA", (PHOTO_SIZE, PHOTO_SIZE))
    circular_photo.paste(orig, (0, 0), mask=mask)

    bubble_w = PHOTO_SIZE + BUBBLE_PADDING * 2
    bubble_h = PHOTO_SIZE + BUBBLE_PADDING * 2 + 40
    bubble = Image.new("RGBA", (bubble_w, bubble_h), (0, 0, 0, 0))
    bubble_draw = ImageDraw.Draw(bubble)
    bubble_draw.ellipse((0, 0, bubble_w - 40, bubble_h - 60), fill=style["accent"])
    bubble_draw.polygon(
        [(bubble_w - 80, bubble_h - 60), (bubble_w - 30, bubble_h - 40), (bubble_w - 60, bubble_h)],
        fill=style["accent"]
    )

    photo_x_in_bubble = ((bubble_w - 40) - PHOTO_SIZE) // 2
    photo_y_in_bubble = ((bubble_h - 60) - PHOTO_SIZE) // 2
    bubble.paste(circular_photo, (photo_x_in_bubble, photo_y_in_bubble), mask)

    photo_x = (CARD_W - bubble_w) // 2
    photo_y = MARGIN + 90
    card.paste(bubble, (photo_x, photo_y), bubble)

    # one-line spacing between photo and feedback text
    line_spacing = 10
    sample_line = "Sample"
    sample_h = draw.textbbox((0, 0), sample_line, font=feedback_font)[3]
    text_y = photo_y + bubble_h + line_spacing

    # Feedback
    quoted_feedback = f"“{feedback}”"
    wrapped_lines = textwrap.wrap(quoted_feedback, width=55)
    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=feedback_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((CARD_W - w) // 2, text_y), line, font=feedback_font, fill=style["text"])
        text_y += h + 5

    # Name(right-aligned)
    name_text = f"- {name}"
    bbox = draw.textbbox((0, 0), name_text, font=name_font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((CARD_W - MARGIN - w, text_y + 10), name_text, font=name_font, fill=style["text"])

    # Save
    card.save(output_path, format="JPEG", quality=100)
