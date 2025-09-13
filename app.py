import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
# 修改这里：直接导入 cairo 而不是从 gi.repository 导入
import cairo
from gi.repository import Pango, PangoCairo
from flask import Flask, request, send_file
import io

app = Flask(__name__)

FONT_MAIN = "ChillRoundFRegular.ttf"
FONT_EMOJI = "NotoColorEmoji.ttf"

def render_text_to_png(text, width, height, font_size, color, alignment, valign):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    layout = PangoCairo.create_layout(ctx)
    # 必须设置布局宽度，对齐方式才能生效
    layout.set_width(width * Pango.SCALE)

    if alignment == "center":
        layout.set_alignment(Pango.Alignment.CENTER)
    elif alignment == "right":
        layout.set_alignment(Pango.Alignment.RIGHT)
    else:
        layout.set_alignment(Pango.Alignment.LEFT)

    layout.set_text(text, -1)
    font_desc_str = f"ChillRoundFRegular, Noto Color Emoji {font_size}"
    font_desc = Pango.font_description_from_string(font_desc_str)
    layout.set_font_description(font_desc)

    # 计算垂直位置
    _ink_rect, logical_rect = layout.get_pixel_extents()
    text_height = logical_rect.height
    y_pos = 0
    if valign == "middle":
        y_pos = (height - text_height) / 2
    elif valign == "bottom":
        y_pos = height - text_height
    
    ctx.move_to(0, y_pos)

    # 解析十六进制颜色
    try:
        color = color.lstrip('#')
        r = int(color[0:2], 16) / 255.0
        g = int(color[2:4], 16) / 255.0
        b = int(color[4:6], 16) / 255.0
        ctx.set_source_rgb(r, g, b)
    except:
        ctx.set_source_rgb(0, 0, 0)  # 如果颜色格式错误，默认为黑色

    PangoCairo.show_layout(ctx, layout)

    img_io = io.BytesIO()
    surface.write_to_png(img_io)
    img_io.seek(0)
    return img_io

@app.route("/username_image")
def username_image():
    username = request.args.get("name", "默认昵称🌟")
    width = request.args.get("width", 600, type=int)
    height = request.args.get("height", 100, type=int)
    font_size = request.args.get("size", 36, type=int)
    color = request.args.get("color", "000000")  # 默认黑色
    alignment = request.args.get("align", "center")  # 默认居中对齐
    valign = request.args.get("valign", "middle") # 默认垂直居中
    stroke_color = request.args.get("stroke_color", "ffffff")  # 默认白色描边
    stroke_width = request.args.get("stroke_width", 0, type=int)  # 默认无描边
    img_io = render_text_to_png(username, width, height, font_size, color, alignment, valign)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
