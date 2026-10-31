#!/usr/bin/env python3
"""扫描 photos/ 文件夹，生成 photos.js，让 index.html 自动把照片放进对应日期。
命名规则（10 月份）：MMDD-序号[-图注].扩展名
  例：1009-1.jpg        → 10月9日，第 1 张，无图注
      1009-2-橘园睡莲.jpg → 10月9日，第 2 张，图注“橘园睡莲”
运行：python3 add_photos.py（在哪个目录运行都行，脚本会自动使用它自己所在的文件夹）
"""
import json, os, re
BASE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(BASE, "photos")
pat = re.compile(r"^(\d{2})(\d{2})-(\d+)(?:-(.+))?\.(jpe?g|png|webp|gif|avif)$", re.I)
out, skipped = {}, []
if not os.path.isdir(PH):
    raise SystemExit("找不到文件夹：" + PH + "（请在脚本旁边建一个 photos 文件夹）")
for f in sorted(os.listdir(PH)):
    m = pat.match(f)
    if not m or m.group(1) != "10":
        skipped.append(f); continue
    out.setdefault(int(m.group(2)), []).append((int(m.group(3)), "photos/" + f, m.group(4) or ""))
data = {d: [[p, c] for _, p, c in sorted(v)] for d, v in sorted(out.items())}
with open(os.path.join(BASE, "photos.js"), "w", encoding="utf-8") as fh:
    fh.write("window.PHOTOS=" + json.dumps(data, ensure_ascii=False) + ";\n")
print("已写入 photos.js：", {d: len(v) for d, v in data.items()})
if skipped: print("以下文件名不符合规则，已跳过：", skipped)
