# NameTex - 文本转图片服务

一个基于 Flask 的文本转图片 API 服务，支持中文字体和 Emoji 表情符号渲染。

## 功能特性

- 🎨 支持自定义文本颜色（十六进制格式）
- 📏 可调节图片尺寸（宽度和高度）
- 🔤 支持多种字体大小
- 🤖 智能字体大小适配（Best Fit功能）
- 🎯 支持最大字体大小限制
- 🖼️ 支持文本描边效果（不影响Emoji显示）
- 📍 支持文本对齐方式（左对齐、居中、右对齐）
- ⬆️ 支持垂直对齐（顶部、中间、底部）
- 🌟 完美支持中文字体和 Emoji 表情
- 📊 支持Base64格式数据输出（JSON格式）
- 🐳 Docker 容器化部署

## 技术栈

- **后端框架**: Flask
- **图形渲染**: Cairo + Pango
- **字体支持**: ChillRoundFRegular.ttf (中文) + NotoColorEmoji.ttf (Emoji)
- **容器化**: Docker

## 快速开始

### 使用 Docker 部署（推荐）

1. 构建镜像：
```bash
./build.sh
```

2. 运行容器：
```bash
./docker_run_nametex.sh
```

服务将在 `http://localhost:5000` 启动。

### 本地开发

1. 安装系统依赖（Ubuntu/Debian）：
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev libgirepository1.0-dev
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 运行服务：
```bash
python app.py
```

## API 使用说明

### 生成用户名图片

**接口地址**: `GET /username_image`

**参数说明**:

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `name` | string | "默认昵称🌟" | 要渲染的文本内容，支持中文、英文、数字、符号和Emoji |
| `width` | int | 600 | 图片宽度（像素），建议范围：100-2000 |
| `height` | int | 100 | 图片高度（像素），建议范围：50-1000 |
| `size` | int | 0 | 字体大小（像素）。设为0时启用Best Fit自动适配功能 |
| `max_size` | int | 0 | 最大字体大小限制（像素）。仅在size=0时生效，0表示无限制 |
| `color` | string | "000000" | 文字颜色（十六进制格式，不含#号）。如：ff0000表示红色 |
| `stroke_color` | string | "ffffff" | 描边颜色（十六进制格式，不含#号）。如：000000表示黑色描边 |
| `stroke_width` | int | 0 | 描边宽度（像素）。0表示无描边，建议范围：1-10 |
| `align` | string | "center" | 水平对齐方式：left（左对齐）/center（居中）/right（右对齐） |
| `valign` | string | "middle" | 垂直对齐方式：top（顶部）/middle（居中）/bottom（底部） |

**功能说明**:

- **Best Fit自动适配**: 当`size=0`时，系统会自动计算最适合容器尺寸的字体大小，确保文本完美填充指定区域
- **最大字体限制**: 配合`max_size`参数可以控制自动适配时的字体大小上限，避免字体过大
- **智能描边效果**: 描边功能使用多次偏移渲染技术，确保不影响Emoji的原始显示效果
- **完美Emoji支持**: 使用NotoColorEmoji字体，支持最新Unicode标准的彩色表情符号

### 使用示例

1. **基础用法**：
```
http://localhost:5000/username_image?name=Hello世界🌍
```

2. **自定义样式**：
```
http://localhost:5000/username_image?name=用户名&width=800&height=150&size=48&color=ff6b6b&align=center&valign=middle
```

3. **Best Fit自动字体大小**：
```
http://localhost:5000/username_image?name=很长的用户名文本&width=400&height=80&size=0
```

4. **限制最大字体大小的自动适配**：
```
http://localhost:5000/username_image?name=文本内容&width=500&height=100&size=0&max_size=50
```

5. **带描边效果的文本**：
```
http://localhost:5000/username_image?name=描边文字🌟&color=ffffff&stroke_color=000000&stroke_width=2
```

6. **综合效果示例**：
```
http://localhost:5000/username_image?name=完美效果😊&width=600&height=120&size=0&max_size=60&color=ff6b6b&stroke_color=ffffff&stroke_width=3&align=center&valign=middle
```

### 获取Base64格式数据

**接口地址**: `GET /username_data`

**参数说明**: 与 `/username_image` 接口完全相同

**返回格式**: JSON格式，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `data` | string | Base64编码的PNG图片数据 |
| `format` | string | 图片格式，固定为"png" |
| `mime_type` | string | MIME类型，固定为"image/png" |

**返回示例**:
```json
{
  "data": "iVBORw0KGgoAAAANSUhEUgAAAlgAAABkCAYAAABfx...",
  "format": "png",
  "mime_type": "image/png"
}
```

**使用场景**:
- 前端需要直接处理图片数据
- 需要将图片数据存储到数据库
- API集成和数据传输
- 移动应用开发

**使用示例**:

1. **获取Base64数据**：
```
http://localhost:5000/username_data?name=Hello世界🌍
```

2. **前端JavaScript使用**：
```javascript
fetch('http://localhost:5000/username_data?name=用户名')
  .then(response => response.json())
  .then(data => {
    const img = document.createElement('img');
    img.src = `data:${data.mime_type};base64,${data.data}`;
    document.body.appendChild(img);
  });
```

3. **自定义样式的Base64数据**：
```
http://localhost:5000/username_data?name=用户名&width=800&height=150&size=48&color=ff6b6b&align=center&valign=middle
```

## 项目结构

```
nametex/
├── app.py                      # Flask 应用主文件
├── requirements.txt            # Python 依赖
├── Dockerfile                  # Docker 构建文件
├── build.sh                   # 构建脚本
├── docker_run_nametex.sh      # Docker 运行脚本
├── ChillRoundFRegular.ttf     # 中文字体文件
├── NotoColorEmoji.ttf         # Emoji 字体文件
└── README.md                  # 项目说明文档
```

## 字体说明

- **ChillRoundFRegular.ttf**: 支持中文字符的圆润字体
- **NotoColorEmoji.ttf**: Google 的彩色 Emoji 字体，支持最新的 Unicode Emoji 标准

## 部署说明

### Docker 部署

项目已配置完整的 Docker 支持：

- 基于 `python:3.9-alpine` 轻量级镜像
- 自动安装 Cairo、Pango 等图形库依赖
- 字体文件自动配置到系统字体目录
- 支持热重启和网络主机模式

### 生产环境建议

- 使用反向代理（如 Nginx）处理静态资源和负载均衡
- 配置适当的日志记录和监控
- 根据实际需求调整容器资源限制

## 开发说明

### 添加新字体

1. 将字体文件放入项目根目录
2. 修改 `Dockerfile` 中的字体复制命令
3. 在 `app.py` 中更新字体描述字符串

### 扩展功能

- 支持更多文本样式（粗体、斜体等）
- 添加背景图片或渐变背景
- 支持多行文本渲染
- 添加文本阴影效果

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！