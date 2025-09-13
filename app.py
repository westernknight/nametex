import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
# 修改这里：直接导入 cairo 而不是从 gi.repository 导入
import cairo
from gi.repository import Pango, PangoCairo
from flask import Flask, request, send_file, jsonify
import io
import base64

app = Flask(__name__)

FONT_MAIN = "ChillRoundFRegular.ttf"
FONT_EMOJI = "NotoColorEmoji.ttf"

def render_text_to_png(name, width, height, font_size, max_size, color, alignment, valign, stroke_color, stroke_width):
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

    layout.set_text(name, -1)

     # Best Fit功能：当font_size为0时，自动计算最适合的字体大小
    if font_size == 0:
        # 二分查找最适合的字体大小
        min_size = 1
        # 如果设置了max_size，则使用它作为上限，否则使用容器尺寸
        if max_size !=0:
            search_max_size = max_size
        else:
            search_max_size = min(width, height)  # 初始最大尺寸
        best_size = min_size
        
        while min_size <= search_max_size:
            test_size = (min_size + search_max_size) // 2
            font_desc_str = f"ChillRoundFRegular, Noto Color Emoji {test_size}"
            font_desc = Pango.font_description_from_string(font_desc_str)
            layout.set_font_description(font_desc)
            
            # 获取文本尺寸
            _ink_rect, logical_rect = layout.get_pixel_extents()
            text_width = logical_rect.width
            text_height = logical_rect.height
            
            # 检查是否适合容器
            if text_width <= width and text_height <= height:
                best_size = test_size
                min_size = test_size + 1
            else:
                search_max_size = test_size - 1
        
        font_size = best_size

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

    # 解析十六进制颜色的辅助函数
    def parse_color(color_str):
        try:
            color_str = color_str.lstrip('#')
            r = int(color_str[0:2], 16) / 255.0
            g = int(color_str[2:4], 16) / 255.0
            b = int(color_str[4:6], 16) / 255.0
            return (r, g, b)
        except:
            return (0, 0, 0)  # 默认黑色

    # 如果有描边效果且描边宽度大于0
    if stroke_width > 0:
        # 使用多次渲染的方式创建描边效果，避免影响emoji
        stroke_r, stroke_g, stroke_b = parse_color(stroke_color)
        
        # 在多个偏移位置绘制描边
        offsets = []
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx != 0 or dy != 0:  # 排除中心位置
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance <= stroke_width:
                        offsets.append((dx, dy))
        
        # 绘制描边
        ctx.set_source_rgb(stroke_r, stroke_g, stroke_b)
        for dx, dy in offsets:
            ctx.save()
            ctx.move_to(dx, y_pos + dy)
            PangoCairo.show_layout(ctx, layout)
            ctx.restore()
        
        # 绘制主文本
        fill_r, fill_g, fill_b = parse_color(color)
        ctx.set_source_rgb(fill_r, fill_g, fill_b)
        ctx.move_to(0, y_pos)
        PangoCairo.show_layout(ctx, layout)
    else:
        # 没有描边，直接绘制填充文本
        fill_r, fill_g, fill_b = parse_color(color)
        ctx.set_source_rgb(fill_r, fill_g, fill_b)
        PangoCairo.show_layout(ctx, layout)



    img_io = io.BytesIO()
    surface.write_to_png(img_io)
    img_io.seek(0)
    return img_io

def get_render_params():
    """提取公共的参数解析逻辑"""
    return {
        'name': request.args.get("name", "默认昵称🌟"),
        'width': request.args.get("width", 600, type=int),
        'height': request.args.get("height", 100, type=int),
        'font_size': request.args.get("size", 0, type=int),
        'color': request.args.get("color", "000000"),
        'alignment': request.args.get("align", "center"),
        'valign': request.args.get("valign", "middle"),
        'stroke_color': request.args.get("stroke_color", "ffffff"),
        'stroke_width': request.args.get("stroke_width", 0, type=int),
        'max_size': request.args.get("max_size", 0, type=int)
    }

@app.route("/username_image")
def username_image():
    params = get_render_params()
    img_io = render_text_to_png(**params)
    return send_file(img_io, mimetype="image/png")

@app.route("/username_data")
def username_data():
    params = get_render_params()
    img_io = render_text_to_png(**params)
    
    # 返回base64字符串
    img_bytes = img_io.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return jsonify({
        "data": img_base64,
        "format": "base64",
        "mime_type": "image/png"
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
