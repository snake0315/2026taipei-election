"""把洋流版 artifact 的 HTML 包成可獨立放上網站的完整網頁。

用法:python3 build_site.py <洋流版本地 html> <輸出資料夾>
- 若輸入含 <!doctype html>…<body> 外框,先去掉
- 補上 <head>(charset、viewport、標題、描述、分享預覽)與基本 reset
- 頁尾加上發布說明
輸出:<輸出資料夾>/index.html
"""
import sys, os, re, datetime as dt

HEAD = '''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="2026 台北市長選情的每日整理:大事件、兩位候選人公開行程、民調走勢、12 區分析與預測模型。每天早晚各更新一次。">
<meta property="og:title" content="台北選情簡報 洋流版">
<meta property="og:description" content="2026 台北市長選情的每日整理:大事件、行程、民調、12 區分析與預測模型。">
<meta property="og:type" content="website">
<meta name="theme-color" content="#F26B1D">
<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}*,*::before,*::after{box-sizing:inherit}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
'''

FOOT = '''
<footer class="sitefoot" style="max-width:760px;margin:40px auto 0;padding-top:16px;border-top:1px solid var(--line);font-size:13px;line-height:1.7;color:var(--muted)">
  <p style="margin:0">本頁為個人整理的公開資料彙整,不代表任何候選人、政黨或媒體。每天台北時間約 08:20 與 20:20 更新,最後產生時間:{stamp}。</p>
  <p style="margin:6px 0 0">依《公職人員選舉罷免法》,11/18 起至 11/28 投票截止前,本頁不顯示任何民調與模型數字。</p>
</footer>
'''


def build(src, outdir):
    h = open(src, encoding="utf-8").read()
    if "<body>" in h:
        h = h[h.index("<body>") + len("<body>"):]
        if "</body>" in h:
            h = h[:h.rindex("</body>")]
    h = h.strip()
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    # 頁尾放在 .page 容器最後的 </div> 之前
    i = h.rindex("</div>\n\n<script>") if "</div>\n\n<script>" in h else h.rindex("<script>")
    body = h[:i] + FOOT.format(stamp=stamp) + h[i:]
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(HEAD + body + "\n</body>\n</html>\n")
    # GitHub Pages:不經 Jekyll 處理
    open(os.path.join(outdir, ".nojekyll"), "w").close()
    return out


if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2]))
