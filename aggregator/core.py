# core.py
import os
import sys
import toml
from pathlib import Path
from datetime import datetime
import fnmatch
from typing import Dict, List
import textwrap
from . import utils, templates


class FileAggregator:
    def __init__(self, config_path: str = 'include.toml'):
        self.config = self._load_config(config_path)
        self.stats = {
            'processed_files': [],
            'total_size': 0,
            'file_types': {}
        }

    @staticmethod
    def generate_config(config_path):
        """生成带完整注释的默认配置文件"""
        config_content = textwrap.dedent("""\
            # ========================
            # 文件聚合工具配置文件
            # 默认所有功能关闭
            # ========================

            [include]
            # 文件匹配模式（支持通配符）
            # "src/**/*.js"  - 匹配src目录所有js文件
            # "docs/*.md"    - 匹配docs目录的md文件
            patterns = ["*.py", "*.txt"]

            [exclude]
            # 需要排除的文件模式
            # "*.bak"       - 所有备份文件
            # "node_modules/" - 排除目录
            patterns = ["test_*"]

            [output]
            filename = "result.txt"    # 输出文件名（默认：result.txt）
            separator = "\\n\\n"    # 文件分隔符（默认空两行）
            
            [features]
            # 功能开关配置
            enable_emojis = false    # 启用表情符号（默认关闭）
            show_watermark = false    # 显示水印（默认关闭）
            
            [filters]
            # 过滤条件配置
            size_limit = 1024    # 文件大小限制（单位KB，0=无限制）

        """)

        try:
            config_path.write_text(config_content, encoding='utf-8')
            print(f"✅ 已生成带注释的配置文件 {config_path}")
            print("👉 使用建议：")
            print("1. 修改 [include] 包含你的目标文件")
            print("2. 开启需要的 [features] 功能")
        except PermissionError:
            print(f"❌ 无写入权限: {config_path}")
        except Exception as e:
            print(f"❌ 生成配置失败: {str(e)}")

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = toml.load(f)
        except toml.TomlDecodeError:
            raise RuntimeError("配置文件格式错误")

        defaults = {
            'include': {'patterns': []},  # 添加默认结构
            'exclude': {'patterns': []},  # 添加默认结构
            'output': {
                'filename': 'print.txt',
                'separator': '\n\n'
            },
            'features': {
                'enable_emojis': True,
                'show_watermark': True,
            },
            'filters': {}
        }

        return utils.deep_update(defaults, config)

    def process_project(self, base_dir: str):
        """处理整个项目"""
        base_path = Path(base_dir)
        output_file = self.config['output']['filename']

        with open(output_file, 'w', encoding='utf-8') as out_f:
            if self.config['features']['show_watermark']:
                out_f.write(templates.get_watermark() + '\n\n')

            for pattern in self.config['include']['patterns']:
                for filepath in self._find_files(base_path, pattern):
                    self._process_file(filepath, base_path, out_f)

        print(f"\n处理完成! {utils.format_stats(self.stats)}")

    def _find_files(self, base_path: Path, pattern: str) -> List[Path]:
        """查找匹配文件"""
        if pattern.endswith('/'):
            dir_pattern = pattern.rstrip('/')
            dirs = [d for d in base_path.glob(dir_pattern) if d.is_dir()]
            return [f for d in dirs for f in d.rglob('*') if f.is_file()]
        return [f for f in base_path.rglob(pattern) if f.is_file()]

    def _process_file(self, filepath: Path, base_path: Path, out_f):
        """处理单个文件"""
        if not self._should_include(filepath):
            return

        try:
            content = filepath.read_text(encoding='utf-8')
            rel_path = filepath.relative_to(base_path)

            self._update_stats(filepath, content)

            header = self._get_file_header(filepath, rel_path, content)
            processed_content = self._preprocess_content(content)
            footer = self._get_file_footer()

            out_f.write(f"{header}{processed_content}{footer}")
            print(f"✅ 已处理: {rel_path} {utils.get_file_emoji(filepath)}")

        except UnicodeDecodeError:
            print(f"⚠️ 跳过二进制文件: {filepath.name}")
        except Exception as e:
            print(f"❌ 处理失败: {filepath.name} - {str(e)}")

    def _should_include(self, filepath: Path) -> bool:
        """检查是否包含文件"""
        for pattern in self.config['exclude']:
            if fnmatch.fnmatch(str(filepath), pattern):
                return False

        if 'size_limit' in self.config['filters']:
            file_size = filepath.stat().st_size
            if file_size > self.config['filters']['size_limit'] * 1024:
                return False

        return True

    def _update_stats(self, filepath: Path, content: str):
        """更新统计信息"""
        file_stat = {
            'path': filepath,
            'size': filepath.stat().st_size,
            'modified': datetime.fromtimestamp(filepath.stat().st_mtime)
        }
        self.stats['processed_files'].append(file_stat)
        self.stats['total_size'] += file_stat['size']
        ext = filepath.suffix.lower()
        self.stats['file_types'][ext] = self.stats['file_types'].get(ext, 0) + 1

    def _get_file_header(self, filepath: Path, rel_path: str, content: str) -> str:
        """生成文件头部"""
        header = []
        if self.config['features']['enable_emojis']:
            header.append(f"{utils.get_file_emoji(filepath)} {rel_path}")
        else:
            header.append(str(rel_path))

        header.append(f"📅 修改时间: {datetime.fromtimestamp(filepath.stat().st_mtime):%Y-%m-%d %H:%M}")
        header.append(f"📏 文件大小: {utils.format_size(filepath.stat().st_size)}")

        return '\n'.join(header) + '\n\n'

    def _preprocess_content(self, content: str) -> str:
        """内容预处理"""
        if self.config['filters'].get('trim_trailing_whitespace', False):
            content = '\n'.join(line.rstrip() for line in content.split('\n'))
        if self.config['filters'].get('remove_empty_lines', False):
            content = '\n'.join(line for line in content.split('\n') if line.strip())
        return content

    def _get_file_footer(self) -> str:
        """生成文件尾部"""
        if self.config['output']['format'] == 'markdown':
            return "\n```"+self.config['output']['separator']
        return self.config['output']['separator']