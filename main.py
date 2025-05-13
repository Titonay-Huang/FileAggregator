# main.py
import sys
import os
from pathlib import Path
from aggregator.core import FileAggregator

def main():
    try:
        config_path = Path('include.toml')
        if not config_path.exists():
            FileAggregator.generate_config(config_path)

        base_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
        aggregator = FileAggregator()
        aggregator.process_project(base_dir)
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()