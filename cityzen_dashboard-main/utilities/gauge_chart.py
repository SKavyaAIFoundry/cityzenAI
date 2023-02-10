import plotly.graph_objects as go

def gauge_chart(value, title):

    '''
    Generates a minimal gauge plot displaying the value and title.
    Axis range and color change limits can be edited as desired.
    '''

    gauge_max = 100

    if value <= gauge_max * 0.3:
        color = 'Crimson'
    elif value <= gauge_max * 0.5:
        color = 'Orange'
    elif value <= gauge_max * 0.7:
        color = 'Gold'
    elif value > gauge_max * 0.7:
        color = 'ForestGreen'

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {"suffix" : " %"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, gauge_max], 'ticks': "", 'visible': False},
            'bar': {'color': color},
            'bgcolor': "lightgray",
            'borderwidth': 0.5
        }))

    return fig