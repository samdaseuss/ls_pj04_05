# shiny_dashboard/styles/styles.py

# CSS 스타일 정의
custom_css = """
.region-card {
    height: 100%;
    transition: transform 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
}
.region-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}
.best-choice {
    background: linear-gradient(135deg, #4CAF50, #8BC34A);
    color: white;
    box-shadow: 0 10px 20px rgba(76, 175, 80, 0.2);
}
.second-choice {
    background: linear-gradient(135deg, #2196F3, #03A9F4);
    color: white;
}
.third-choice {
    background: linear-gradient(135deg, #9C27B0, #673AB7);
    color: white;
}
.ribbon {
    position: absolute;
    top: 20px;
    right: -30px;
    transform: rotate(45deg);
    background-color: #FF5722;
    color: white;
    padding: 5px 40px;
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.feature-item {
    padding: 10px;
    margin: 5px 0;
    border-radius: 4px;
    background-color: rgba(255,255,255,0.1);
}
.feature-star {
    color: #FFD700;
    margin-right: 5px;
}
.stats-box {
    background-color: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    text-align: center;
}
.score-display {
    font-size: 24px;
    font-weight: bold;
    color: #FFEB3B;
}
.chart-container {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
}
.section-title {
    font-size: 24px;
    font-weight: bold;
    margin: 20px 0;
    text-align: center;
    color: #333;
}
.header-section {
    background: linear-gradient(135deg, #1A237E, #283593);
    color: white;
    padding: 30px 0;
    border-radius: 8px;
    margin-bottom: 30px;
}
"""

def get_custom_css():
    return custom_css