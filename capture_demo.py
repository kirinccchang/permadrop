"""
Capture PermaDrop demo screenshots and create a GIF.
Steps: API key → Connect → Folder → Upload docx → URL list → Archive → Download
"""
import os, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path(__file__).parent / "demo_frames"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

API_KEY   = "35c5991d91587403368776162d0030c774dc8b26"
DOCX_PATH = str(Path(__file__).parent / "demo.docx")
URL       = "https://permadrop.kirinchang.com"
WIDTH, HEIGHT = 1100, 750

frames = []

def save(page, name):
    path = SCREENSHOTS_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=False)
    frames.append(str(path))
    print(f"  ✓ {name}")
    return str(path)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT})
        page = ctx.new_page()

        # ── Step 1: Clean landing page ────────────────────────────────────
        print("Step 1: Landing page…")
        page.goto(URL, wait_until="networkidle")
        page.evaluate("localStorage.clear(); sessionStorage.clear()")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1200)
        page.evaluate("window.scrollTo(0, 0)")
        save(page, "01_landing")

        # ── Step 2: Paste API key ─────────────────────────────────────────
        print("Step 2: API key…")
        api_input = page.locator("input[placeholder*='API key']")
        api_input.click()
        api_input.fill(API_KEY)
        page.wait_for_timeout(600)
        save(page, "02_api_key")

        # ── Step 3: Connect ───────────────────────────────────────────────
        print("Step 3: Connect…")
        page.get_by_role("button", name="Connect").click()
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        save(page, "03_connected")

        # ── Step 4: Show folder selection ────────────────────────────────
        print("Step 4: Folder selection…")
        page.evaluate("window.scrollTo(0, 180)")
        page.wait_for_timeout(400)
        save(page, "04_folder")

        # ── Step 5: Upload docx ───────────────────────────────────────────
        print("Step 5: Uploading demo.docx…")
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(DOCX_PATH)
        page.wait_for_timeout(2000)
        # Scroll to show the file uploaded + URL count
        page.evaluate("window.scrollTo(0, 420)")
        page.wait_for_timeout(500)
        save(page, "05_file_uploaded")

        # ── Step 6: Scroll to show URL table ─────────────────────────────
        print("Step 6: URL list…")
        # Scroll down to reveal the URL rows
        page.evaluate("window.scrollTo(0, 620)")
        page.wait_for_timeout(600)
        save(page, "06_url_list")

        # ── Step 7: Scroll to Archive Selected button ─────────────────────
        print("Step 7: Ready to archive…")
        # Find and scroll to the Archive Selected button area
        page.evaluate("window.scrollTo(0, document.body.scrollHeight - 400)")
        page.wait_for_timeout(400)
        save(page, "07_ready_to_archive")

        # ── Step 8: Click Archive Selected ───────────────────────────────
        print("Step 8: Archiving…")
        archive_btn = page.locator("button", has_text="Archive Selected")
        archive_btn.scroll_into_view_if_needed()
        archive_btn.click()
        page.wait_for_timeout(1500)
        # Scroll to show progress
        page.evaluate("window.scrollTo(0, document.body.scrollHeight - 300)")
        page.wait_for_timeout(500)
        save(page, "08_archiving")

        # ── Step 9: Wait for completion ───────────────────────────────────
        print("Step 9: Waiting for completion (up to 75s)…")
        # Poll for status indicators
        for _ in range(15):
            page.wait_for_timeout(5000)
            # Check for download links or "done" text
            has_done = page.evaluate("""
                () => {
                    const text = document.body.innerText;
                    return text.includes('Download') &&
                           (text.includes('archived') || text.includes('perma.cc'));
                }
            """)
            if has_done:
                print("    → Done detected")
                break
            print("    → Still archiving…")

        page.wait_for_timeout(1000)
        # Scroll to show completed URL rows
        page.evaluate("window.scrollTo(0, 580)")
        page.wait_for_timeout(500)
        save(page, "09_done_url_rows")

        # ── Step 10: Scroll to show download links ────────────────────────
        print("Step 10: Download section…")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        save(page, "10_download")

        browser.close()

    print(f"\nCaptured {len(frames)} frames.")
    return frames

def make_gif(frames):
    """Two-pass ffmpeg: palette + encode for high-quality GIF."""
    output = Path(__file__).parent / "usage.gif"

    # Per-frame durations (seconds)
    durations = {
        "01_landing":         3.0,
        "02_api_key":         2.0,
        "03_connected":       2.5,
        "04_folder":          2.5,
        "05_file_uploaded":   2.5,
        "06_url_list":        3.0,
        "07_ready_to_archive":2.5,
        "08_archiving":       2.5,
        "09_done_url_rows":   3.0,
        "10_download":        4.0,
    }

    # Write ffmpeg concat file
    list_file = SCREENSHOTS_DIR / "frames.txt"
    with open(list_file, "w") as f:
        for i, fr in enumerate(frames):
            stem = Path(fr).stem
            dur = durations.get(stem, 2.5)
            f.write(f"file '{fr}'\nduration {dur}\n")
        f.write(f"file '{frames[-1]}'\n")  # ffmpeg needs trailing entry

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vf", (
            f"scale={WIDTH}:-1:flags=lanczos,"
            "split[s0][s1];"
            "[s0]palettegen=max_colors=256:stats_mode=diff[p];"
            "[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
        ),
        "-loop", "0",
        str(output)
    ]
    print("Creating GIF…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size_mb = output.stat().st_size / 1024 / 1024
        print(f"✓ usage.gif  ({size_mb:.1f} MB, {WIDTH}px wide)")
    else:
        print("ffmpeg error:", result.stderr[-800:])
    return str(output)

if __name__ == "__main__":
    print(f"PermaDrop demo capture → {URL}\n")
    frames = run()
    gif_path = make_gif(frames)
    print(f"\nDone: {gif_path}")
