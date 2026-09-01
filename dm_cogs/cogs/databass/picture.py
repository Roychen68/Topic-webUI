import json, urllib.parse
from datetime import datetime
from .SQL_done import get_weekly_data
async def get_weekly_chart(user_id):
    data = await get_weekly_data(user_id)
    today = datetime.now().isoweekday()  # 今天是星期几
    
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # 今天以前（含今天）有数据，之后填 None（空白）
    counts = []
    for i in range(1, 8):
        if i <= today:
            counts.append(data.get(i, 0))  # 没记录的天补 0
        else:
            counts.append(None)            # 未来的天显示空白

    chart_config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "完成事項",
                "data": counts,
                "spanGaps": False,
                "fill": True,
                "backgroundColor": "rgba(168, 85, 247, 0.25)",
                "borderColor": "rgba(192, 132, 252, 1)",
                "pointBackgroundColor": "rgba(216, 180, 254, 1)",
                "pointBorderColor": "rgba(168, 85, 247, 1)",
                "pointRadius": 6,
                "pointHoverRadius": 8,
                "tension": 1
            }]
        },
        "options": {
            "legend": {
                "labels": {
                    "usePointStyle": True,
                    "pointStyle": "circle",
                    "boxWidth": 10
                }
            },
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True,
                        "min": 0,
                        "stepSize": 1,
                        "precision": 0
                    }
                }]
            }
        }
    }

    encoded = urllib.parse.quote(json.dumps(chart_config))
    
    return f"https://quickchart.io/chart?c={encoded}&backgroundColor=rgb(15,10,30)"