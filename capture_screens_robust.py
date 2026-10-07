import asyncio
from playwright.async_api import async_playwright
import os

OUT_DIR = r"F:\Annadata Mitra\Annadata_Mitra_Report\images_new"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        page.set_default_timeout(10000)
        
        # 1. Login Screenshot
        print("Capturing Login...")
        try:
            await page.goto("http://localhost:5173/login", wait_until='networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_login.png"))
        except Exception as e:
            print("Error capturing Login:", e)
        
        # 2. Register Screenshot & Perform Registration
        print("Capturing Register...")
        try:
            await page.goto("http://localhost:5173/register", wait_until='networkidle')
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_register.png"))
        except Exception as e:
            print("Error capturing Register:", e)
        
        print("Filling register form...")
        try:
            await page.fill("input[name='fullName']", "Test Farmer")
            await page.fill("input[name='mobileNumber']", "9876543210")
            await page.fill("input[name='password']", "password123")
            await page.click("button[type='submit']")
            print("Waiting for dashboard redirect...")
            await page.wait_for_url("http://localhost:5173/", timeout=5000)
            await asyncio.sleep(2)
        except Exception as e:
            print("Could not register:", e)
            print("Trying to login instead...")
            try:
                await page.goto("http://localhost:5173/login", wait_until='networkidle')
                await asyncio.sleep(1)
                await page.fill("input[name='identifier']", "9876543210")
                await page.fill("input[name='password']", "password123")
                await page.click("button[type='submit']")
                await page.wait_for_url("http://localhost:5173/", timeout=5000)
                await asyncio.sleep(2)
            except Exception as e:
                print("Could not login:", e)

        # 3. Dashboard
        print("Capturing Dashboard...")
        try:
            await page.goto("http://localhost:5173/")
            await asyncio.sleep(2)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_dashboard.png"))
        except Exception as e:
            print("Error capturing Dashboard:", e)
        
        # 4. Crop Planning
        print("Capturing Crop Planning...")
        try:
            await page.goto("http://localhost:5173/crop-planning")
            await asyncio.sleep(2)
            try:
                # Assuming standard inputs, I will check if they exist, otherwise skip filling
                inputs = await page.query_selector_all("input")
                if len(inputs) >= 4:
                    await inputs[0].fill("40")
                    await inputs[1].fill("50")
                    await inputs[2].fill("40")
                    await inputs[3].fill("6.5")
                    await page.click("button[type='submit']")
                    await asyncio.sleep(4)
            except Exception as e:
                print("Error filling crop planning:", e)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_crop_planning.png"))
        except Exception as e:
            print("Error capturing Crop Planning:", e)
        
        # 5. Weather Risk
        print("Capturing Weather Risk...")
        try:
            await page.goto("http://localhost:5173/weather-risk")
            await asyncio.sleep(4)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_weather_risk.png"))
        except Exception as e:
            print("Error capturing Weather Risk:", e)
        
        # 6. Disease Detection
        print("Capturing Vision...")
        try:
            await page.goto("http://localhost:5173/disease-detection")
            await asyncio.sleep(2)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_vision.png"))
        except Exception as e:
            print("Error capturing Vision:", e)
        
        # 7. Market Intelligence
        print("Capturing Market...")
        try:
            await page.goto("http://localhost:5173/market-intelligence")
            await asyncio.sleep(3)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_market.png"))
        except Exception as e:
            print("Error capturing Market:", e)
        
        # 8. Strategist
        print("Capturing Strategist...")
        try:
            await page.goto("http://localhost:5173/strategist")
            await asyncio.sleep(4)
            await page.screenshot(path=os.path.join(OUT_DIR, "ui_strategist.png"))
        except Exception as e:
            print("Error capturing Strategist:", e)
        
        await browser.close()
        print("Screenshots captured successfully.")

if __name__ == "__main__":
    asyncio.run(main())
