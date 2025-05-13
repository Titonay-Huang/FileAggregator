# 📂✨ 文件聚合魔法师 2.0 (File Aggregator Wizard Pro)

**全新升级的文件收集神器！** 现在支持更强大的魔法配方和更精美的报告生成~ 🪄

## 🎩 魔法新特性

- **智能表情符号**：自动为不同文件类型添加可爱emoji 🐍📜🌐
- **魔法水印**：为报告添加专属魔法印记 ✦━━━━━━━━◆◆◆━━━━━━━━✦
- **文件统计**：实时显示收集成果 📊
- **超强过滤**：按大小、类型、名称精准控制收集范围 🧂

```python
# 新魔法示例 🌟
aggregator = FileAggregator()
aggregator.process_project("你的魔法城堡")  # 咻~一键收集！
```

## 🚀 快速施法指南

### 安装魔法书

```bash
git clone https://github.com/Titonay-Huang/FileAggregator.git
cd FileAggregator
pip install -e .  # 安装魔法依赖
```

### 第一次施展收集术

1. 自动生成魔法配方：
   ```bash
   python main.py  # 会自动创建include.toml
   ```
2. 修改配方文件：
   ```bash
   nano include.toml  # 按你的需求调整
   ```
3. 释放收集魔法：
   ```bash
   python main.py /path/to/your/project
   ```

## 🔮 魔法配方大全 (include.toml)

```toml
# ========================
# 文件聚合魔法配方 2.0
# ========================

[include]
patterns = [
    "*.py",        # 收集Python咒语书
    "docs/*.md",   # 收集魔法指南
    "src/**/*.js"  # 收集所有JS魔法卷轴
]

[exclude]
patterns = [
    "test_*.py",   # 排除测试咒语
    "**/tmp/**"    # 避开临时魔法阵
]

[output]
filename = "魔法报告.txt"  # 报告文件名
separator = "\n\n✨✨✨\n\n"  # 文件分隔魔法

[features]
enable_emojis = true     # 启用可爱表情
show_watermark = true    # 显示魔法水印

[filters]
size_limit = 2048        # 只收集小于2MB的魔法卷轴
```

## 🌈 魔法效果展示

````markdown
🐍 src/spells/fireball.py
📅 修改时间: 2025-05-13 14:39
📏 文件大小: 1.2 KB

```python
def cast_fireball(target):
    """火球术咒语"""
    print(f"🔥 火球飞向 {target}！")
    return damage_calculator(100)
```

✨✨✨

📜 docs/magic_history.md 
📅 修改时间: 2025-05-12 09:15
📏 文件大小: 2.4 KB

```markdown
# 火球术的起源

这种破坏性魔法最早由...
```
````

## 🧰 魔法工具箱 Pro

### 核心咒语表

| 功能 | 配方选项 | 效果示例 |
|------|----------|----------|
| **文件匹配** | `patterns = ["*.py"]` | 收集所有Python文件 |
| **排除模式** | `patterns = ["test_*"]` | 跳过测试文件 |
| **大小过滤** | `size_limit = 1024` | 只收1MB以下文件 |
| **表情开关** | `enable_emojis = true` | 🐍📜🌐 文件图标 |

### 高级黑魔法

```toml
[advanced]
# 自定义预处理咒语
preprocess = """
def magic_filter(content):
    # 移除所有"TODO"标记
    return content.replace("TODO", "🎯")
"""

# 多环境配置
env = "dev"  # dev/test/prod
```

## 🤔 魔法学院Q&A

**Q: 为什么我的.csv文件没有📊表情？**  
A: 在utils.py的emoji_map中添加你需要的文件类型即可！

**Q: 能收集二进制魔法卷轴(.png/.exe)吗？**  
A: 目前只支持文本文件，二进制文件会被自动跳过哦~

**Q: 分隔符能更炫酷吗？**  
A: 当然！试试 `separator = "\n\n⚡⚡⚡\n\n"` 让你的报告闪闪发光！

**Q: 报告太大怎么办？**  
A: 使用 `size_limit` 控制文件大小，或者 `output.max_files = 100` 限制数量~

## 📜 魔法许可证 2.0

MIT License - 现在你还可以修改和分发这个魔法工具，但请保留原始魔法印记！⚡

---

> 新版本已经准备好释放你的文件收集潜能！  
> 记住：伟大的魔法师总是先读文档再施法~ 📖✨
