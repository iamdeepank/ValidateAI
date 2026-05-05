import asyncio
from playwright.async_api import async_playwright

from src.schemas import AgentState
from src.tools import TableauScraper


async def run_scraper(parsed_input):
    URL = "https://public.tableau.com/app/profile/harry.richards4213/viz/PositionsDatabaseNER0cs/PositionsDatabaseNER0cs"

    async with async_playwright() as p:
        scraper = TableauScraper(URL)

        await scraper.launch(p)
        await scraper.open_dashboard()
        await scraper.get_frame()

        # 🔥 Use filter from parsed input (no enhancement)
        country = "Canada"
        if parsed_input and parsed_input.filters.country:
            country = parsed_input.filters.country

        await scraper.apply_country_filter(country)

        data = await scraper.extract_data()

        await scraper.close()

        return data


def ui_node(state: AgentState) -> AgentState:
    parsed_input = state.parsed_input

    if parsed_input is None:
        return state.model_copy(update={
            "validation_error": "Parsed input missing for UI node"
        })

    # 🔥 Run async scraper
    data = asyncio.run(run_scraper(parsed_input))

    print("datttttt",data,"--end")
    print("datt--type",type(data),"--end")



    return AgentState(
        user_input=state.user_input,
        parsed_input=state.parsed_input,
        execution_plan=state.execution_plan,
        validation_error=None,
        raw_llm_output=state.raw_llm_output,
        ui_data=data
    )
