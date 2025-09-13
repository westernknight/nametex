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
def _parse_color(color_hex, default_color=(0, 0, 0)):
    """解析十六进制颜色字符串 (RRGGBB) 并返回 Cairo 使用的 (r, g, b) 元组。"""
    try:
        color_hex = color_hex.lstrip('#')
        r = int(color_hex[0:2], 16) / 255.0
        g = int(color_hex[2:4], 16) / 255.0
        b = int(color_hex[4:6], 16) / 255.0
        return (r, g, b)
    except:
        return default_color

def render_text_to_png(text, width, height, font_size, color, alignment, valign, stroke_color, stroke_width):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    layout = PangoCairo.create_layout(ctx)
    layout.set_width(width * Pango.SCALE)

    # 水平对齐
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

    # 垂直对齐计算
    _ink_rect, logical_rect = layout.get_pixel_extents()
    text_height = logical_rect.height
    y_pos = 0
    if valign == "middle":
        y_pos = (height - text_height) / 2
    elif valign == "bottom":
        y_pos = height - text_height
    
    ctx.move_to(0, y_pos)

    # 创建文本路径
    PangoCairo.layout_path(ctx, layout)

    # 如果描边宽度大于0，则绘制描边
    if stroke_width > 0:
        r, g, b = _parse_color(stroke_color, default_color=(1, 1, 1))  # 默认白色描边
        ctx.set_source_rgb(r, g, b)
        ctx.set_line_width(stroke_width)
        ctx.stroke_preserve()  # 描边并保留路径用于填充

    # 绘制填充
    r, g, b = _parse_color(color, default_color=(0, 0, 0))  # 默认黑色填充
    ctx.set_source_rgb(r, g, b)
    ctx.fill()

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
    img_io = render_text_to_png(username, width, height, font_size, color, alignment, valign, stroke_color, stroke_width)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
