# pages/yeongcheon_page.py
from shiny import ui, render
import pandas as pd

def yeongcheon_dashboard():
    return ui.page_fluid(
        ui.h1("영천시 귀농인 현황 대시보드")
    )

def yeongcheon_dashboard_server(input, output, session):
    @render.text
    def yeongcheon():
        return "반갑고"   