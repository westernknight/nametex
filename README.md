# NameTex - 文本转图片服务

一个基于 Flask 的文本转图片 API 服务，支持中文字体和 Emoji 表情符号渲染。

## 功能特性

- 🎨 支持自定义文本颜色（十六进制格式）
- 📏 可调节图片尺寸（宽度和高度）
- 🔤 支持多种字体大小
- 📍 支持文本对齐方式（左对齐、居中、右对齐）
- ⬆️ 支持垂直对齐（顶部、中间、底部）
- 🌟 完美支持中文字体和 Emoji 表情
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
| `name` | string | "默认昵称🌟" | 要渲染的文本内容 |
| `width` | int | 600 | 图片宽度（像素） |
| `height` | int | 100 | 图片高度（像素） |
| `size` | int | 36 | 字体大小 |
| `color` | string | "000000" | 文字颜色（十六进制，不含#） |
| `align` | string | "center" | 水平对齐方式：left/center/right |
| `valign` | string | "middle" | 垂直对齐方式：top/middle/bottom |
| `stroke_color` | string | "ffffff" | 描边颜色（十六进制，不含#） |
| `stroke_width` | int | 0 | 描边宽度（0为无描边） |

### 使用示例

1. **基础用法**：
```
http://localhost:5000/username_image?name=Hello世界🌍
```

2. **自定义样式**：
```
http://localhost:5000/username_image?name=用户名&width=800&height=150&size=48&color=ff6b6b&align=center&valign=middle
```

3. **带描边效果**：
```
http://localhost:5000/username_image?name=炫酷文字&color=ffffff&stroke_color=000000&stroke_width=2
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