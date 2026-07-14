import plotly.io as pio

NIGHT_BLUE = "#1B2A4A"

pio.templates["night_blue"] = pio.templates["plotly"]
pio.templates["night_blue"].layout.font = dict(color=NIGHT_BLUE, family="Inter, sans-serif")
pio.templates["night_blue"].layout.hoverlabel.font = dict(color=NIGHT_BLUE)
pio.templates.default = "night_blue"
