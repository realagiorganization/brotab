import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright
from pytest_bdd import given, scenarios, then, when

scenarios("../features/clickthrough.feature")


DEMO_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Brotab Demo</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 32px; }
      #count { font-size: 48px; margin-top: 16px; }
      button { font-size: 18px; padding: 8px 16px; }
    </style>
  </head>
  <body>
    <h1>Brotab Click-Through</h1>
    <button id="add-tab">Add Tab</button>
    <div id="count">0</div>
    <script>
      let count = 0;
      document.getElementById("add-tab").addEventListener("click", () => {
        count += 1;
        document.getElementById("count").textContent = String(count);
      });
    </script>
  </body>
</html>
"""


@pytest.fixture
def page(request):
    headless = os.environ.get("PLAYWRIGHT_HEADLESS", "1") != "0"
    video_dir = Path(os.environ.get("PLAYWRIGHT_VIDEO_DIR", "artifacts/playwright"))
    screenshot_dir = Path(
        os.environ.get("PLAYWRIGHT_SCREENSHOT_DIR", "artifacts/screenshots")
    )
    video_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        yield page
        safe_name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", request.node.name)
        screenshot_path = screenshot_dir / f"{safe_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        context.close()
        browser.close()


@given("a demo page with a tab counter")
def demo_page(page):
    page.set_content(DEMO_HTML)
    page.wait_for_selector("#add-tab")


@when('I click the "Add Tab" button')
def click_button(page):
    page.click("#add-tab")


@then('the counter shows "1"')
def counter_shows_one(page):
    expect(page.locator("#count")).to_have_text("1")
