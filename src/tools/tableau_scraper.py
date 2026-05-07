import asyncio
from playwright.async_api import async_playwright
from src.config import settings


class TableauScraper:

    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless
        self.browser = None
        self.page = None
        self.frame = None

    # -------------------------------
    # Setup Browser
    # -------------------------------
    async def launch(self, playwright):
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        self.page = await self.browser.new_page()

    # -------------------------------
    # Open Dashboard
    # -------------------------------
    async def open_dashboard(self):
        print("Opening dashboard...")
        await self.page.goto(self.url, timeout=settings.tableau.INITIAL_WAIT)
        await self.page.wait_for_timeout(settings.tableau.PAGE_LOAD_TIMEOUT)

    # -------------------------------
    #  Get Tableau Frame
    # -------------------------------
    async def get_frame(self):
        for f in self.page.frames:
            if "/views/" in f.url:
                self.frame = f
                print("Frame found:", f.url)
                return

        raise Exception("Tableau frame not found")

    # -------------------------------
    # Apply Filter
    # -------------------------------
    """for specific country """
    async def apply_country_filter(self, country="Canada"):
        print(f"Applying Country filter: {country}")

        dropdowns = self.frame.locator("text=(All)")
        count = await dropdowns.count()
        print("Dropdowns found:", count)

        try:
            await dropdowns.nth(3).click()
            await self.page.wait_for_timeout(settings.tableau.FILTER_WAIT)

            await self.frame.locator(f"text={country}").first.click()
            await self.page.wait_for_timeout(settings.tableau.POST_FILTER_WAIT)

            print("Filter applied successfully")

        except Exception as e:
            print("Filter apply failed:", e)

    # async def apply_filters(self, filters):
    #     print(f"Applying filters: {filters}")
    #     print("filters--type", type(filters))
    #
    #     # Normalize input (CRITICAL FIX)
    #     if hasattr(filters, "model_dump"):
    #         filters = filters.model_dump()
    #
    #     if not isinstance(filters, dict):
    #         print(f"Invalid filters input: {filters}")
    #         return
    #
    #     dropdowns = self.frame.locator("text=(All)")
    #     count = await dropdowns.count()
    #     print("Dropdowns found:", count)
    #
    #     dropdown_order = ["name", "role", "team", "country"]
    #
    #     try:
    #         for idx, field in enumerate(dropdown_order):
    #             print("fields--:", field)
    #             print("fields--type--:", type(field))
    #
    #             value = filters.get(field)
    #
    #             if not value:
    #                 print(f"Skipping {field}")
    #                 continue
    #
    #             print(f"Applying {field}: {value}")
    #
    #             try:
    #                 await dropdowns.nth(idx).click()
    #                 await self.page.wait_for_timeout(settings.tableau.FILTER_WAIT)
    #
    #                 await self.frame.locator(f"text={value}").first.click()
    #                 await self.page.wait_for_timeout(settings.tableau.POST_FILTER_WAIT)
    #
    #                 print(f"{field} applied successfully")
    #
    #             except Exception as e:
    #                 print(f"{field} filter failed:", e)
    #
    #         print("All filters applied (AND condition)")
    #
    #     except Exception as e:
    #         print("Filter application failed:", e)
    # -------------------------------
    # Extract & Structure Data
    # -------------------------------
    async def extract_data(self):
        print("Extracting visible data...")

        try:
            text = await self.frame.inner_text("body")

            lines = [l.strip() for l in text.split("\n") if l.strip()]

            if "IGL-Opener" not in lines:
                print("Target data not found")
                return []

            start = lines.index("IGL-Opener")

            print("start:---", start)

            roles = lines[start:start+2]
            names = lines[start+2:start+4]
            teams = lines[start+4:start+6]
            t_last = lines[start+6:start+10]
            ct_last = lines[start+10:start+12]

            result = []

            for i in range(len(roles)):
                result.append({
                    "role": roles[i],
                    "player_name": names[i],
                    "team": teams[i],
                    "t_target_last12": t_last[i],
                    "ct_target_last12": ct_last[i]
                })

            print("\n--- STRUCTURED DATA ---\n")
            for r in result:
                print(r, "\n")

            return result

        except Exception as e:
            print("Extraction failed:", e)
            return []

    # -------------------------------
    #  Close Browser
    # -------------------------------
    async def close(self):
        if self.browser:
            await self.browser.close()


# -------------------------------
#  Runner (optional - keep for local testing)
# -------------------------------
# async def run():
#
#     async with async_playwright() as p:
#         scraper = TableauScraper(settings.tableau.URL,settings.tableau.HEADLESS)
#
#         await scraper.launch(p)
#         await scraper.open_dashboard()
#         await scraper.get_frame()
#         await scraper.apply_country_filter("Canada")
#
#         data = await scraper.extract_data()
#
#         await scraper.close()
#
#         return data
