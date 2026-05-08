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

            lines = [
                l.strip()
                for l in text.split("\n")
                if l.strip()
            ]

            print("\n--- DATA PREVIEW ---\n")
            print("\n".join(lines[:80]))

            # -----------------------------------
            # Find Start
            # -----------------------------------
            start = None

            for idx, line in enumerate(lines):

                if line in [
                    "IGL-Opener",
                    "Support",
                    "AWPer",
                    "Closer",
                    "Opener",
                    "Rifler",
                    "IGL-AWPer",
                    "IGL-Closer",
                    "IGL-Rifler"
                ]:
                    start = idx
                    break

            if start is None:
                print("Could not identify table")

                return []

            # -----------------------------------
            # Detect Row Count
            # -----------------------------------
            roles = []

            role_keywords = [
                "IGL-Opener",
                "Support",
                "AWPer",
                "Closer",
                "Opener",
                "Rifler",
                "IGL-AWPer",
                "IGL-Closer",
                "IGL-Rifler"
            ]

            current = start

            while current < len(lines):

                if lines[current] in role_keywords:
                    roles.append(lines[current])
                    current += 1
                else:
                    break

            row_count = len(roles)

            print(f"Detected Rows: {row_count}")

            # -----------------------------------
            # Dynamic Slicing
            # -----------------------------------
            names = lines[current:current + row_count]
            current += row_count

            teams = lines[current:current + row_count]
            current += row_count

            t_target = lines[current:current + row_count]
            current += row_count

            ct_target = lines[current:current + row_count]
            current += row_count

            # -----------------------------------
            # Build Structured Table
            # -----------------------------------
            result = []

            for i in range(row_count):
                result.append({
                    "role": roles[i],
                    "player_name": names[i],
                    "team": teams[i],
                    "t_target_last12": t_target[i],
                    "ct_target_last12": ct_target[i]
                })

            # -----------------------------------
            # Pretty Print
            # -----------------------------------
            print("\n--- STRUCTURED TABLE ---\n")

            for row in result:
                print(row)

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
