import plotly.graph_objects as go


template = dict(
    layout=go.Layout(
        dict(
            height=200,
            margin=dict(l=20, r=20, b=20, t=40),
            dragmode=False,
            hovermode='closest',
            bargap=0.25,
            plot_bgcolor='#F9F9F9',
            paper_bgcolor='#F9F9F9',
            title=dict(
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            xaxis=dict(
                zeroline=False,
                automargin=True,
                showgrid=False,
                showline=True,
                linewidth=1,
                linecolor='black',
                dtick='D1',
                tickformat='%m/%d'
            ),
            yaxis=dict(
                zeroline=False,
                showline=False,
                automargin=True,
                gridcolor='#e9e9e9'
            )
        )
    )
)
