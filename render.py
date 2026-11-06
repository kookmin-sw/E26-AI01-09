"""poster.html -> A0 PDF (841 x 1189 mm, 1 page).

사용법: python render.py [poster.html] [output/INNER_VOICE_A0.pdf]
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

A0_MM = (841, 1189)                      # 세로 A0
MM_TO_PT = 72 / 25.4
VIEWPORT = {"width": 3179, "height": 4494}  # 841 x 1189 mm @ 96 dpi

src = Path(sys.argv[1] if len(sys.argv) > 1 else "poster.html").resolve()
out = Path(sys.argv[2] if len(sys.argv) > 2 else "output/INNER_VOICE_A0.pdf").resolve()
out.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport=VIEWPORT)
    page.goto(src.as_uri())
    page.wait_for_timeout(800)

    # 내용이 A0 한 장을 넘치지 않는지 확인
    info = page.evaluate("""() => {
        const w = document.querySelector('.wrap');
        const f = document.querySelector('.foot');
        const last = [...document.querySelectorAll('.sec')].pop();
        return {overflow: w.scrollHeight > w.clientHeight,
                gap: f.getBoundingClientRect().top - last.getBoundingClientRect().bottom};
    }""")
    if info["overflow"] or info["gap"] < 0:
        sys.exit(f"내용이 A0 한 장을 넘칩니다: {info}")

    page.pdf(path=str(out), width=f"{A0_MM[0]}mm", height=f"{A0_MM[1]}mm",
             print_background=True)
    browser.close()

# 결과 규격 검사: 1페이지, 841 x 1189 mm
try:
    from pypdf import PdfReader
    r = PdfReader(str(out))
    box = r.pages[0].mediabox
    w_mm, h_mm = float(box.width) / MM_TO_PT, float(box.height) / MM_TO_PT
    assert len(r.pages) == 1, f"페이지 수 {len(r.pages)}"
    assert abs(w_mm - A0_MM[0]) < 1 and abs(h_mm - A0_MM[1]) < 1, f"{w_mm:.1f} x {h_mm:.1f} mm"
    print(f"OK  {out.name}: 1페이지, {w_mm:.0f} x {h_mm:.0f} mm (A0)")
except ImportError:
    print(f"저장됨: {out} (규격 검사는 pypdf 설치 시 실행)")
