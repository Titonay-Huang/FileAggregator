import os
import sys
import toml
from pathlib import Path
from datetime import datetime
import fnmatch
from typing import Dict
import textwrap


class FileAggregator:
    def __init__(self, config_path: str = 'include.toml'):
        self.config = self._load_config(config_path)
        self.file_count = 0
        self.total_size = 0

    def _load_config(self, config_path: str) -> Dict:
        """加载并验证配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = toml.load(f)
        except FileNotFoundError:
            print(f"错误: 找不到配置文件 {config_path}")
            sys.exit(1)
        except toml.TomlDecodeError:
            print("错误: 配置文件格式不正确")
            sys.exit(1)

        # 设置默认值
        config.setdefault('output', {}).setdefault('filename', 'print.txt')
        config.setdefault('output', {}).setdefault('format', 'text')
        config.setdefault('output', {}).setdefault('separator', '\n\n')
        config.setdefault('exclude', [])
        config.setdefault('filters', {})

        return config

    def _format_file_size(self, size_bytes: int) -> str:
        """将文件大小转换为可读格式"""
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                if unit == 'bytes':
                    return f"{int(size_bytes)} {unit}"
                else:
                    return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def _should_include(self, filepath: Path) -> bool:
        """检查文件是否应该被包含"""
        # 排除检查
        for pattern in self.config['exclude']:
            if fnmatch.fnmatch(str(filepath), pattern):
                return False

        # 文件类型过滤
        if 'extensions' in self.config['filters']:
            if filepath.suffix.lower() not in self.config['filters']['extensions']:
                return False

        # 大小过滤
        file_size = filepath.stat().st_size
        if 'size_limit' in self.config['filters']:
            if file_size > self.config['filters']['size_limit'] * 1024:  # KB
                return False

        return True

    def _preprocess_content(self, content: str, filepath: Path) -> str:
        """预处理文件内容"""
        # 移除行尾空白
        if self.config.get('filters', {}).get('trim_trailing_whitespace', False):
            content = '\n'.join(line.rstrip() for line in content.split('\n'))

        # 移除空行
        if self.config.get('filters', {}).get('remove_empty_lines', False):
            content = '\n'.join(line for line in content.split('\n') if line.strip())

        return content

    def _get_file_header(self, filepath: Path, rel_path: str) -> str:
        """生成文件头信息"""
        stat = filepath.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = self._format_file_size(stat.st_size)

        if self.config['output']['format'] == 'markdown':
            return textwrap.dedent(f"""\
                ## {rel_path}
                - **Size**: {size}
                - **Modified**: {mtime}

                ```{filepath.suffix[1:] if filepath.suffix else 'text'}
                """)
        else:
            return textwrap.dedent(f"""\
                # {rel_path}
                # Size: {size}
                # Modified: {mtime}
                """)

    def _get_file_footer(self) -> str:
        """生成文件尾部信息"""
        if self.config['output']['format'] == 'markdown':
            return "\n```\n"
        return ""

    def process_files(self, base_dir: str):
        """处理文件并生成输出"""
        output_file = self.config['output']['filename']
        base_path = Path(base_dir)

        print(f"开始处理目录: {base_dir}")
        print(f"输出格式: {self.config['output']['format']}")

        with open(output_file, 'w', encoding='utf-8') as out_f:
            first_file = True

            # 处理包含模式
            for pattern in self.config['include']:
                matches = []

                # 目录模式
                if pattern.endswith('/'):
                    dir_pattern = pattern.rstrip('/')
                    dir_matches = [d for d in base_path.glob(dir_pattern) if d.is_dir()]
                    for directory in dir_matches:
                        matches.extend(directory.rglob('*'))
                else:
                    matches = list(base_path.rglob(pattern))

                if not matches:
                    print(f"警告: 没有找到匹配模式 '{pattern}' 的文件")
                    continue

                for filepath in sorted(matches):
                    if filepath.is_file() and self._should_include(filepath):
                        try:
                            rel_path = filepath.relative_to(base_path)

                            # 添加分隔符
                            if not first_file:
                                out_f.write(self.config['output']['separator'])
                            else:
                                first_file = False

                            # 写入文件头
                            out_f.write(self._get_file_header(filepath, str(rel_path)))

                            # 写入文件内容
                            with open(filepath, 'r', encoding='utf-8') as in_f:
                                content = in_f.read()
                                content = self._preprocess_content(content, filepath)
                                out_f.write(content)

                            # 写入文件尾
                            out_f.write(self._get_file_footer())

                            # 更新统计
                            self.file_count += 1
                            self.total_size += filepath.stat().st_size

                            print(f"已处理: {rel_path} ({self._format_file_size(filepath.stat().st_size)})")

                        except UnicodeDecodeError:
                            print(f"警告: 跳过二进制文件 {filepath}")
                        except Exception as e:
                            print(f"警告: 处理 {filepath} 时出错: {str(e)}")

        print(f"\n处理完成! 共合并 {self.file_count} 个文件, 总大小 {self._format_file_size(self.total_size)}")
        print(f"结果已保存到 {output_file}")


def main():
    if len(sys.argv) > 2:
        print("用法: python aggregator.py [项目目录]")
        sys.exit(1)

    base_directory = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()

    if not os.path.isdir(base_directory):
        print(f"错误: 目录 '{base_directory}' 不存在")
        sys.exit(1)

    aggregator = FileAggregator()
    aggregator.process_files(base_directory)


if __name__ == '__main__':
    main()