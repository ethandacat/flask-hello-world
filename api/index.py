# Official catscobot code
# By: ethandacat and ChatGPT
# Licensed under the Cat License 1.3
# PlayWrong software.
# DO NOT EDIT CODE, YOU MIGHT BREAK IT

from flask import Flask, render_template_string
import time
import asyncio
import random
from playwright.async_api import async_playwright, expect


expect.set_options(timeout=1_000)

app = Flask(__name__)

logs = ""


@app.route('/')
def display_logs():
    return render_template_string(f"""
    <html>
    <head><title>Automation Log</title></head>
    <body style="font-family: Arial, sans-serif;">
        <h2>Automation Logs</h2>
        <div>{logs}</div>
    </body>
    </html>
    """)


def log(message, log_type="INFO"):
    global logs
    timestamp = time.strftime("[%m/%d/%y %H:%M]")
    logs += f"{timestamp} [{log_type}] {message}<br>\n"


async def find_children(element):
    return await element.query_selector_all("*")


async def initialize_browser():
    log("Initializing browser")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False, devtools = True)
    context = await browser.new_context()
    page = await context.new_page()
    return page, browser


async def log_in(page, username, password):
    log("Navigating to login page")
    await page.goto('https://x-camp.discourse.group')

    try:
        await page.fill('#username', username)
        await page.fill('#password', password)
        await page.click("button[type='submit']")
        log("Login details submitted, waiting for confirmation")

        await page.wait_for_selector(".avatar", timeout=120000)
        log("Confirmed login success")
    except Exception as e:
        log(f"Error during login: {e}", log_type="ERROR")


async def create_post(page, title, content):
    log("Creating new post")
    await page.goto("https://x-camp.discourse.group")

    try:
        await page.click("#create-topic")
        await page.fill("#reply-title", title)
        await page.fill("#ember103", content)

        await page.click('div[data-name="Misc"]')
        await page.click("button.btn.btn-icon-text.btn-primary.create")
        log("Post created successfully")
    except Exception as e:
        log(f"Error during post creation: {e}", log_type="ERROR")

async def check_notifications(page):
    log("Checking notifications")
    url = "https://x-camp.discourse.group/u/catscobot/notifications"
    await page.goto(url)

    try:
        # Reduce timeout when trying to click notifications
        await page.click("li.notification.unread.mentioned a", timeout=3000)
        await reply(page, "AUTOMATED <" + random.choice(
            ["apple", "straw", "pineapple", "we love peaches", "@Ivan_Zong", "Whats up?", "Lolzies"]) + ">")
    except:
        log("No new mentions, trying PM")
        try:
            await page.click("li.notification.unread.private-message a", timeout=3000)
            await reply(page, "AUTOMATED <" + random.choice(
                ["apple", "straw", "pineapple", "we love peaches", "@Ivan_Zong", "Whats up?", "Lolzies"]) + ">")
        except:
            log("No PMs. Cycling...")


async def reply(page, message):
    try:
        # Await the query_selector_all coroutine to get the list of buttons
        buttons = await page.query_selector_all("button.btn.btn-icon-text.btn-primary.create")
        await buttons[-1].click()  # Click the 20th button (index 19)

        await page.fill("textarea", message)
        await page.click("button.btn.btn-icon-text.btn-primary.create[title='Or press Ctrl+Enter']")
        log(f"Replied with message: {message}")
    except Exception as e:
        log(f"Error during reply: {e}", log_type="ERROR")


async def main():
    page, browser = await initialize_browser()
    await log_in(page, 'catscobot', 'catscobot123')
    time.sleep(1)

    try:
        while True:
            await check_notifications(page)
    except Exception as e:
        log(f"Error during main loop: {e}", log_type="ERROR")
        raise SyntaxError("Cuz why not")
    finally:
        await browser.close()


if __name__ == "__main__":
    from threading import Thread

    # Run Flask in a separate thread
    flask_thread = Thread(target=lambda: app.run(debug=True, use_reloader=False))
    flask_thread.start()
    # Run Playwright automation
    asyncio.run(main())
