'''Wayback Puppeteer
adapted from https://github.com/reyesayala/wa_screenshot_compare/blob/master/archive_screenshot.py'''
from uuid import uuid4
from pyppeteer import launch
from pyppeteer import errors
import urllib
import logging
import asyncio

def fetch(url, output_path="/tmp/", screenshot_method=1, timeout_duration=100):
    # command which takes the screenshots
    command = ""
    output_path = "{}{}.png".format(output_path, uuid4())
    asyncio.get_event_loop().run_until_complete(
        puppeteer_screenshot(url, output_path, timeout_duration))
    logging.info("Screenshot successful")
    return open(output_path)

async def puppeteer_screenshot(url, output_path, timeout_duration):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'height': 768, 'width': 1024})
    await page.goto(url, timeout=(int(timeout_duration) * 1000))
    await page.screenshot(path=output_path)
    await browser.close()
    
