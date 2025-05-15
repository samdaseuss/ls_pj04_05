# app.py
from shiny import App, ui
import os
from shiny_dashboard.pages.comparison_page import page_a_ui, page_a_server
from shiny_dashboard.pages.yeongcheon import page_b_ui, page_b_server
# from pages.page_c import page_c_ui, page_c_server

# 네비게이션 UI 생성
app_ui = ui.page_navbar(
    ui.nav_panel("귀촌인 대시보드", page_a_ui()),
    # ui.nav_panel("페이지 B", page_b_ui()),
    # ui.nav_panel("데이터 시각화", page_c_ui()),
    title="영천시 귀촌 분석 시스템",
    id="navbar",
)

def server(input, output, session):
    page_a_server(input, output, session)
    # page_b_server(input, output, session)
    # page_c_server(input, output, session)

app = App(app_ui, server, static_assets=os.path.join(os.path.dirname(__file__), "www"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)