# app.py
from shiny import App, ui
import os
from shiny_dashboard.pages.farming_population import farming_population_dashboard, farming_population_dashboard_server
from shiny_dashboard.pages.yeongcheon_page import yeongcheon_dashboard, yeongcheon_dashboard_server
from shiny_dashboard.pages.region_comparison_pages import region_comparison_ui, region_comparison_server


app_ui = ui.page_navbar(
    ui.nav_panel("전국 귀농 현황", farming_population_dashboard()),
    ui.nav_panel("영천 귀농 현황", yeongcheon_dashboard()),
    ui.nav_panel("경북지역 귀농 혜택", region_comparison_ui()),
    title="영천시 귀농 분석",
    id="navbar",
)

def server(input, output, session):
    farming_population_dashboard_server(input, output, session)
    yeongcheon_dashboard_server(input, output, session)
    region_comparison_server(input, output, session)

app = App(app_ui, server, static_assets=os.path.join(os.path.dirname(__file__), "www"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)