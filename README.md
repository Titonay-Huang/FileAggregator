# 📂✨ 文件聚合魔法师 (File Aggregator Wizard) 

**一键收集你的代码宝藏！** 让散落各处的文件乖乖排好队，变成一份精美的文档报告~

## 🎩 这个工具能做什么？

- **文件大搜罗**：像魔法一样从各个角落找出你要的文件
- **智能整理术**：自动过滤、排序、美化你的代码
- **精美报告**：生成带元数据的漂亮文档（支持Markdown！）
- **超强定制**：想怎么收就怎么收，全听你的！

```python
# 举个栗子 🌰
files = find_files("你的项目")
report = make_pretty_report(files)
save_as_markdown(report)  # 哇！真简单！
```

## 🚀 快速开始

### 安装咒语

```
git clone https://github.com/Titonay-Huang/FileAggregator.git
cd FileAggregator
```

### 第一次施法

1. 创建魔法配方 (`include.toml`)
2. 挥动你的魔法棒：
   ```bash
   python aggregator.py [你的项目路径]
   ```
3. 见证奇迹时刻！✨

## 🔮 魔法配方示例

```toml
# include.toml - 你的文件收集配方

[spells]
include = [
    "src/**/*.py",  # 抓取所有Python文件
    "docs/**/*.md", # 收集Markdown文档
    "configs/"      # 整个配置文件夹
]

[protection_charms]
exclude = [
    "**/__pycache__/**",  # 避开缓存目录
    "**/*.secret"         # 忽略秘密文件
]

[magic_enhancements]
format = "markdown"          # 生成漂亮的Markdown
separator = "\n\n---\n\n"    # 用魔法分隔线分开文件
show_spell_info = true       # 显示文件魔法信息
```

## 🌈 魔法效果预览

````markdown
## 🧙 src/spells/levitation.py
- **魔法强度**: 2.1 KB 
- **施法时间**: 2023-11-15 14:30:00
- **魔法类型**: Python咒语

```python
def make_it_float(target):
    """让物体漂浮的魔法"""
    print(f"{target} 开始漂浮啦！✨")
```

---

## 📜 docs/ancient_scroll.md
- **魔法强度**: 1.4 KB
- **施法时间**: 2023-11-10 09:15:00  
- **魔法类型**: 古老卷轴

```markdown
# 悬浮咒语的历史

这种魔法最早记载于...
```
````

## 🧰 魔法工具箱

### 超能力选项

| 功能 | 魔法咒语 | 效果 |
|------|----------|------|
| **智能过滤** | `extensions = [".py", ".md"]` | 只收集特定类型文件 |
| **大小限制** | `size_limit = 100` | 不超过100KB的魔法卷轴 |
| **内容净化** | `trim_trailing_whitespace = true` | 自动清理咒语杂质 |
| **格式转换** | `format = "markdown"` | 生成精美魔法书 |

### 进阶魔法

```toml
[advanced_magic]
# 多环境配方
env = "production"

# 自定义预处理咒语
preprocess_spell = """
def enhance(content):
    return content.upper()
"""
```

## 🤔 常见魔法问题

**Q: 我的文件被诅咒了，收集不了怎么办？**  
A: 试试加上`force = true`参数，破除简单的魔法防御！

**Q: 能让生成的报告发光吗？**  
A: 虽然不能真的发光...但Markdown格式在GitHub上会很好看哦！✨

**Q: 这个工具会吃掉我的文件吗？**  
A: 放心！我们只是"读取"文件，绝对不会"写入"或修改原文件！

## 📜 魔法许可证

MIT License - 你可以自由使用这个魔法，但请别用它做坏事哦！

---

> 准备好开始你的文件收集冒险了吗？ 🧙✨  
> 记住：能力越大，责任越大！
