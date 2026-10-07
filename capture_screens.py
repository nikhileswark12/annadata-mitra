import asyncio
from playwright.async_api import async_playwright
import os

OUT_DIR = r"F:\Annadata Mitra\Annadata_Mitra_Report\images_new"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        # 1. Login
        print("Capturing Login...")
        await page.goto("http://localhost:5173/login")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_login.png"))
        
        # 2. Register
        print("Capturing Register...")
        await page.goto("http://localhost:5173/register")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_register.png"))
        
        print("Filling register form...")
        # Fill register
        try:
            await page.fill("input[name='name']", "Test Farmer")
            await page.fill("input[name='email']", "farmer@example.com")
            await page.fill("input[name='password']", "password123")
            
            # Sometimes there's phone or location
            try:
                await page.fill("input[name='phone']", "9876543210")
            except:
                pass
                
            await page.click("button[type='submit']")
            print("Waiting for dashboard redirect...")
            await asyncio.sleep(4)
        except Exception as e:
            print("Could not register:", e)
            print("Trying to login instead...")
            await page.goto("http://localhost:5173/login")
            await asyncio.sleep(2)
            await page.fill("input[name='email']", "farmer@example.com")
            await page.fill("input[name='password']", "password123")
            await page.click("button[type='submit']")
            await asyncio.sleep(4)

        # 3. Dashboard
        print("Capturing Dashboard...")
        await page.goto("http://localhost:5173/")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_dashboard.png"))
        
        # 4. Crop Planning
        print("Capturing Crop Planning...")
        await page.goto("http://localhost:5173/crop-planning")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        try:
            await page.fill("input[name='nitrogen']", "40")
            await page.fill("input[name='phosphorus']", "50")
            await page.fill("input[name='potassium']", "40")
            await page.fill("input[name='ph']", "6.5")
            await page.click("button[type='submit']")
            await asyncio.sleep(4) # wait for prediction
        except Exception as e:
            print("Error filling crop planning:", e)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_crop_planning.png"))
        
        # 5. Weather Risk
        print("Capturing Weather Risk...")
        await page.goto("http://localhost:5173/weather-risk")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(4)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_weather_risk.png"))
        
        # 6. Disease Detection
        print("Capturing Vision...")
        await page.goto("http://localhost:5173/disease-detection")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_vision.png"))
        
        # 7. Market Intelligence
        print("Capturing Market...")
        await page.goto("http://localhost:5173/market-intelligence")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_market.png"))
        
        # 8. Strategist
        print("Capturing Strategist...")
        await page.goto("http://localhost:5173/strategist")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(4)
        await page.screenshot(path=os.path.join(OUT_DIR, "ui_strategist.png"))
        
        await browser.close()
        print("Screenshots captured successfully.")

if __name__ == "__main__":
    asyncio.run(main())
