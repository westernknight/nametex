import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo, cairo
from flask import Flask, request, send_file
import io

app = Flask(__name__)

FONT_MAIN = "ChillRoundFRegular.ttf"
FONT_EMOJI = "NotoColorEmoji_WindowsCompatible.ttf"

def render_text_to_png(text):
    width, height = 600, 100
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    layout = PangoCairo.create_layout(ctx)
    layout.set_text(text, -1)
    font_desc = Pango.font_description_from_string(f"{FONT_MAIN} 36, {FONT_EMOJI} 36")
    layout.set_font_description(font_desc)

    PangoCairo.show_layout(ctx, layout)

    img_io = io.BytesIO()
    surface.write_to_png(img_io)
    img_io.seek(0)
    return img_io

@app.route("/username_image")
def username_image():
    username = request.args.get("name", "默认昵称🌟")
    img_io = render_text_to_png(username)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
