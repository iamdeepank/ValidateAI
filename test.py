# import logging
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# llm = ChatOpenAI(
#     base_url="",
#     api_key="",
#     model="gpt-5.4",
#     temperature=0.0001,
#     timeout=120,
#     max_retries=5,
# )
#
# messages = [
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="What is the capital of France? Tell me more about it"),
# ]
#
# try:
#     response = llm.invoke(messages)
#     logger.info("LLM call successful")
#     print(response.content)
# except Exception as e:
#     logger.error("LLM call failed: %s", repr(e))
#


# import asyncio
# from playwright.async_api import async_playwright
#
# class TableauScraper:
#
#     def __init__(self, url: str, headless: bool = True):
#         self.url = url
#         self.headless = headless
#         self.browser = None
#         self.page = None
#         self.frame = None
#
#     # -------------------------------
#     # Setup Browser
#     # -------------------------------
#     async def launch(self, playwright):
#         self.browser = await playwright.chromium.launch(
#             headless=self.headless,
#             args=["--no-sandbox", "--disable-dev-shm-usage"]
#         )
#         self.page = await self.browser.new_page()
#
#     # -------------------------------
#     # Open Dashboard
#     # -------------------------------
#     async def open_dashboard(self):
#         print("Opening dashboard...")
#         await self.page.goto(self.url, timeout=120000)
#         await self.page.wait_for_timeout(10000)
#
#     # -------------------------------
#     #  Get Tableau Frame
#     # -------------------------------
#     async def get_frame(self):
#         for f in self.page.frames:
#             if "/views/" in f.url:
#                 self.frame = f
#                 print("Frame found:", f.url)
#                 return
#
#         raise Exception("Tableau frame not found")
#
#     # -------------------------------
#     # Apply Country Filter
#     # -------------------------------
#     async def apply_country_filter(self, country="Canada"):
#         print(f"Applying Country filter: {country}")
#
#         dropdowns = self.frame.locator("text=(All)")
#         count = await dropdowns.count()
#         print("Dropdowns found:", count)
#
#         try:
#             await dropdowns.nth(3).click()
#             await self.page.wait_for_timeout(2000)
#
#             await self.frame.locator(f"text={country}").first.click()
#
#             await dropdowns.nth(1).click()
#             await self.page.wait_for_timeout(2000)
#             await self.frame.locator(f"text=AWPer").first.click()
#
#
#             await self.page.wait_for_timeout(5000)
#
#             print("Filter applied successfully")
#
#         except Exception as e:
#             print("Filter apply failed:", e)
#
#     # -------------------------------
#     # Extract & Structure Data
#     # -------------------------------
#     async def extract_data(self):
#
#       print("Extracting visible data...")
#
#       try:
#
#           text = await self.frame.inner_text("body")
#
#           lines = [
#               l.strip()
#               for l in text.split("\n")
#               if l.strip()
#           ]
#
#           print("\n--- DATA PREVIEW ---\n")
#           print("\n".join(lines[:80]))
#
#           # -----------------------------------
#           # Find Start
#           # -----------------------------------
#           start = None
#
#           for idx, line in enumerate(lines):
#
#               if line in [
#                   "IGL-Opener",
#                   "Support",
#                   "AWPer",
#                   "Closer",
#                   "Opener",
#                   "Rifler",
#                   "IGL-AWPer",
#                   "IGL-Closer",
#                   "IGL-Rifler"
#               ]:
#                   start = idx
#                   break
#
#           if start is None:
#
#               print("Could not identify table")
#
#               return []
#
#           # -----------------------------------
#           # Detect Row Count
#           # -----------------------------------
#           roles = []
#
#           role_keywords = [
#               "IGL-Opener",
#               "Support",
#               "AWPer",
#               "Closer",
#               "Opener",
#               "Rifler",
#               "IGL-AWPer",
#               "IGL-Closer",
#               "IGL-Rifler"
#           ]
#
#           current = start
#
#           while current < len(lines):
#
#               if lines[current] in role_keywords:
#                   roles.append(lines[current])
#                   current += 1
#               else:
#                   break
#
#           row_count = len(roles)
#
#           print(f"Detected Rows: {row_count}")
#
#           # -----------------------------------
#           # Dynamic Slicing
#           # -----------------------------------
#           names = lines[current:current + row_count]
#           current += row_count
#
#           teams = lines[current:current + row_count]
#           current += row_count
#
#           t_target = lines[current:current + row_count]
#           current += row_count
#
#           ct_target = lines[current:current + row_count]
#           current += row_count
#
#           # -----------------------------------
#           # Build Structured Table
#           # -----------------------------------
#           result = []
#
#           for i in range(row_count):
#
#               result.append({
#                   "role": roles[i],
#                   "player_name": names[i],
#                   "team": teams[i],
#                   "t_target_last12": t_target[i],
#                   "ct_target_last12": ct_target[i]
#               })
#
#           # -----------------------------------
#           # Pretty Print
#           # -----------------------------------
#           print("\n--- STRUCTURED TABLE ---\n")
#
#           for row in result:
#               print(row)
#
#           return result
#
#       except Exception as e:
#
#           print("Extraction failed:", e)
#
#           return []
#     # -------------------------------
#     #  Close Browser
#     # -------------------------------
#     async def close(self):
#         if self.browser:
#             await self.browser.close()
#
#
# # -------------------------------
# #  Runner
# # -------------------------------
# async def run():
#     URL = "https://public.tableau.com/app/profile/harry.richards4213/viz/PositionsDatabaseNER0cs/PositionsDatabaseNER0cs"
#
#     async with async_playwright() as p:
#         scraper = TableauScraper(URL)
#
#         await scraper.launch(p)
#         await scraper.open_dashboard()
#         await scraper.get_frame()
#         await scraper.apply_country_filter("Argentina")
#
#         data = await scraper.extract_data()
#
#         await scraper.close()
#
#         return data
#
#
# if __name__ == "__main__":
#     asyncio.run(run())

#
# import asyncio
# from playwright.async_api import async_playwright
#
#
# URL = "https://mstr-prod.bayer.com/MicroStrategy/servlet/mstrWeb"
#
#
# class MicroStrategyPOC:
#
#     def __init__(self):
#         self.browser = None
#         self.page = None
#
#     # -----------------------------------
#     # Launch Browser
#     # -----------------------------------
#     async def launch(self, playwright):
#
#         self.browser = await playwright.chromium.launch(
#             headless=False,   # keep visible for debugging
#             args=[
#                 "--start-maximized"
#             ]
#         )
#
#         context = await self.browser.new_context(
#             viewport={"width": 1920, "height": 1080}
#         )
#
#         self.page = await context.new_page()
#
#     # -----------------------------------
#     # Open MSTR
#     # -----------------------------------
#     async def open_dashboard(self):
#
#         print("Opening MicroStrategy...")
#
#         await self.page.goto(URL, timeout=120000)
#
#         await self.page.wait_for_timeout(5000)
#
#     # -----------------------------------
#     # Navigate to Kerendia Dashboard
#     # -----------------------------------
#     async def navigate_to_kerendia(self):
#
#         print("Navigating to Kerendia...")
#
#         # STEP 1
#         await self.page.locator("text=Kerendia").click()
#
#         await self.page.wait_for_timeout(5000)
#
#         # STEP 2
#         await self.page.locator("text=Overview").click()
#
#         await self.page.wait_for_timeout(10000)
#
#         print("Kerendia Overview Opened")
#
#     # -----------------------------------
#     # Extract KPI Values
#     # -----------------------------------
#     async def extract_kpis(self):
#
#         print("Extracting KPI values...")
#
#         result = {}
#
#         try:
#
#             body_text = await self.page.locator("body").inner_text()
#
#             lines = [
#                 line.strip()
#                 for line in body_text.split("\n")
#                 if line.strip()
#             ]
#
#             # DEBUG
#             print("\n--- PAGE PREVIEW ---\n")
#             print("\n".join(lines[:80]))
#
#             # -----------------------------------
#             # Extract KPI values dynamically
#             # -----------------------------------
#
#             for idx, line in enumerate(lines):
#
#                 # NBRx Total
#                 if line == "NBRx Total":
#                     result["nbrx_total"] = float(lines[idx + 2])
#
#                 # TRx Total
#                 elif line == "TRx Total":
#                     result["trx_total"] = float(lines[idx + 2])
#
#                 # Blink TRx
#                 elif line == "Blink TRx":
#                     blink_value = lines[idx + 2]
#
#                     if blink_value == "(4)":
#                         result["blink_trx"] = -4.0
#                     else:
#                         result["blink_trx"] = float(
#                             blink_value.replace("(", "-").replace(")", "")
#                         )
#
#                 # NRx Total
#                 elif line == "NRx Total":
#                     result["nrx_total"] = float(lines[idx + 2])
#
#             print("\n--- KPI OUTPUT ---\n")
#
#             for k, v in result.items():
#                 print(f"{k}: {v}")
#
#             return result
#
#         except Exception as e:
#
#             print("KPI extraction failed:", e)
#
#             return {}
#
#     # -----------------------------------
#     # Close Browser
#     # -----------------------------------
#     async def close(self):
#
#         if self.browser:
#             await self.browser.close()
#
#
# # -----------------------------------
# # Runner
# # -----------------------------------
# async def run():
#
#     async with async_playwright() as p:
#
#         scraper = MicroStrategyPOC()
#
#         await scraper.launch(p)
#
#         await scraper.open_dashboard()
#
#         await scraper.navigate_to_kerendia()
#
#         kpis = await scraper.extract_kpis()
#
#         print("\nFINAL JSON:\n")
#         print(kpis)
#
#         await scraper.close()
#
#
# if __name__ == "__main__":
#     asyncio.run(run())


# import os
# import asyncio
# from playwright.async_api import async_playwright


# URL = "https://mstr-prod.bayer.com/MicroStrategy/servlet/mstrWeb"


# class MicroStrategyPOC:

#     def __init__(self):
#         self.browser = None
#         self.page = None

#     # -----------------------------------
#     # Launch Browser
#     # -----------------------------------

#     async def launch(self, playwright):

#         self.context = await playwright.chromium.launch_persistent_context(

#             user_data_dir=r"C:\playwright-edge-profile",

#             channel="msedge",

#             headless=False,

#             viewport={"width": 1920, "height": 1080},

#             args=[
#                 "--start-maximized"
#             ]
#         )

#         self.page = await self.context.new_page()

#     # -----------------------------------
#     # Open Dashboard
#     # -----------------------------------
#     async def open_dashboard(self):

#         print("Opening MicroStrategy...")

#         await self.page.goto(URL, timeout=120000)

#         await self.page.wait_for_timeout(5000)



#     async def navigate_to_overview(self):

#         print("STEP 1 → Clicking Bayer US DayLight")

#         daylight = self.page.locator(
#             "#projects_ProjectsStyle .mstrLargeIconViewItemLink"
#         ).first

#         await daylight.wait_for(timeout=60000)

#         await daylight.click(force=True)

#         await self.page.wait_for_timeout(8000)

#         print("STEP 2 → Clicking Kerendia")

#         kerendia = self.page.locator(
#             ".mstrWeb .r-cssDefault_K1426347B4345CB4C4081EB838A0ED98B A",
#         ).first

#         await kerendia.wait_for(timeout=60000)

#         await kerendia.click()

#         await self.page.wait_for_timeout(8000)

#         print("STEP 3 → Clicking Overview")

#         overview = self.page.locator(
#     "div.mstrmojo-DocImage.hasLink[title='Overview']"
# ).first

#         await overview.wait_for(timeout=60000)

#         await overview.click()

#         await self.page.wait_for_timeout(12000)

#         print("Overview Dashboard Opened")

#     # -----------------------------------
#     # Extract KPI Values
#     # -----------------------------------
#     async def extract_kpis(self):

#         print("Extracting KPI values...")

#         result = {}

#         try:

#             body_text = await self.page.locator("body").inner_text()

#             lines = [
#                 line.strip()
#                 for line in body_text.split("\n")
#                 if line.strip()
#             ]

#             print("\n--- PAGE PREVIEW ---\n")
#             print("\n".join(lines[:80]))

#             # -----------------------------------
#             # KPI Mapping
#             # -----------------------------------

#             kpi_labels = {
#                 "NBRx Total": "nbrx_total",
#                 "TRx Total": "trx_total",
#                 "Blink TRx": "blink_trx",
#                 "NRx Total": "nrx_total"
#             }

#             # -----------------------------------
#             # Helper Function
#             # -----------------------------------

#             def get_next_numeric(start_index):

#                 for j in range(start_index + 1, len(lines)):

#                     value = lines[j]

#                     cleaned = (
#                         value
#                         .replace("▲", "")
#                         .replace("▼", "")
#                         .replace("(", "-")
#                         .replace(")", "")
#                         .replace("%", "")
#                         .strip()
#                     )

#                     try:
#                         return float(cleaned)
#                     except:
#                         continue

#                 return None

#         # -----------------------------------
#         # Extract KPIs
#         # -----------------------------------

#         for idx, line in enumerate(lines):

#             if line in kpi_labels:

#                 value = get_next_numeric(idx)

#                 result[kpi_labels[line]] = value

#         # -----------------------------------
#         # Final JSON
#         # -----------------------------------

#         print("\n--- KPI JSON ---\n")

#         print(result)

#         return result

#     except Exception as e:

#         print("KPI extraction failed:", e)

#         return {}

#     # -----------------------------------
#     # Close Browser
#     # -----------------------------------
#     async def close(self):

#         if self.browser:
#             await self.browser.close()


# # -----------------------------------
# # Runner
# # -----------------------------------
# async def run():

#     async with async_playwright() as p:

#         scraper = MicroStrategyPOC()

#         await scraper.launch(p)

#         await scraper.open_dashboard()

#         # await scraper.login()

#         await scraper.navigate_to_overview()

#         kpis = await scraper.extract_kpis()

#         print("\nFINAL JSON:\n")
#         print(kpis)

#         await scraper.close()


# if __name__ == "__main__":
#     asyncio.run(run())



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
async def run():

    async with async_playwright() as p:
        scraper = TableauScraper(settings.tableau.URL,settings.tableau.HEADLESS)

        await scraper.launch(p)
        await scraper.open_dashboard()
        await scraper.get_frame()
        await scraper.apply_country_filter("Argentina")

        data = await scraper.extract_data()

        await scraper.close()

        return data
