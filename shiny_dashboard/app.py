# app.py
from shiny import App, ui
import os
from shiny_dashboard.pages.comparison_page import page_a_ui, page_a_server
from shiny_dashboard.pages.yeongcheon_page import yeongcheon_dashboard, yeongcheon_dashboard_server
from shiny_dashboard.pages.region_comparison_pages import region_comparison_ui, region_comparison_server


app_ui = ui.page_navbar(
    ui.nav_panel("귀촌인 대시보드", page_a_ui()),
    ui.nav_panel("영천만 분석해 놓은 대시보드", yeongcheon_dashboard()),
    ui.nav_panel("데이터 시각화", region_comparison_ui()),
    title="영천시 귀촌 분석 시스템",
    id="navbar",
)

def server(input, output, session):
    page_a_server(input, output, session)
    yeongcheon_dashboard_server(input, output, session)
    region_comparison_server(input, output, session)

app = App(app_ui, server, static_assets=os.path.join(os.path.dirname(__file__), "www"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)