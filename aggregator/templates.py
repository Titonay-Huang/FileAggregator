# templates.py
import textwrap
from datetime import datetime


# 组合符号 + 动态信息
def get_watermark() -> str:
    return textwrap.dedent(f"""
        ✦━━━━━━━━◆◆◆━━━━━━━━✦
           FILE AGGREGATOR  
           v2.0 | {datetime.now():%Y-%m-%d}
        ✦━━━━━━━━◆◆◆━━━━━━━━✦
    """)