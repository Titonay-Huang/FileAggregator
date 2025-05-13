# utils.py
from pathlib import Path
from typing import Dict
import textwrap

def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    units = ['bytes', 'KB', 'MB', 'GB']
    for unit in units:
        if size_bytes < 1024.0 or unit == 'GB':
            break
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} {unit}" if unit != 'bytes' else f"{int(size_bytes)} bytes"

def deep_update(source: Dict, overrides: Dict) -> Dict:
    """深度合并字典"""
    for key, value in overrides.items():
        if isinstance(value, dict):
            node = source.setdefault(key, {})
            deep_update(node, value)
        else:
            source[key] = value
    return source

def get_file_emoji(filepath: Path) -> str:
    """获取文件表情符号"""
    emoji_map = {
        '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
        '.md': '📖', '.txt': '📄', '.json': '📦', '.csv': '📊',
        '.jpg': '🖼', '.png': '🖼', '.toml': '⚙️', '.yml': '⚙️',
        '.xml': '📄', '.sql': '🗃️', '.log': '📰', '.gz': '📦'
    }
    return emoji_map.get(filepath.suffix.lower(), '📎')

def format_stats(stats: dict) -> str:
    """格式化统计信息"""
    return textwrap.dedent(f"""
        📁 总文件数: {len(stats['processed_files'])}
        📦 总大小: {format_size(stats['total_size'])}
        🔍 文件类型分布: {', '.join(f'{k}×{v}' for k,v in stats['file_types'].items())}
    """)