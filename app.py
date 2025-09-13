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
FONT_EMOJI = "NotoColorEmoji.ttf"  # 修正文件名

def render_text_to_png(text):
    width, height = 600, 100
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    
    # 设置背景色为白色（可选）
    ctx.set_source_rgb(1, 1, 1)  # 白色背景
    ctx.paint()
    
    # 设置文字颜色为黑色
    ctx.set_source_rgb(0, 0, 0)  # 黑色文字

    layout = PangoCairo.create_layout(ctx)
    layout.set_text(text, -1)
    
    # 简化字体描述，使用系统默认字体作为备选
    font_desc = Pango.font_description_from_string("Sans 36")
    layout.set_font_description(font_desc)
    
    # 居中显示文字
    text_width, text_height = layout.get_pixel_size()
    ctx.move_to((width - text_width) / 2, (height - text_height) / 2)

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
