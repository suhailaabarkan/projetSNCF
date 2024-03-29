import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from visus.builder import barplot_1522
from visus.interaction import build_range_slider
from data.get_data import get_data_barplot_1522, get_years_range_slider
from story_telling.barplot_story import get_text_below_barplot

question = "Est-ce que les régions les plus fréquentées sont celles où se produisent le plus d’incidents ? Pour chaque région, quelle est la cause d’incidents qui atteint le plus grand niveau de gravité ?"

dash.register_page(__name__, question=question, external_stylesheets=[
    dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


def layout():
    rangeslider = build_range_slider(*get_years_range_slider())
    graph = dcc.Graph(id='barplot')
    apres = dbc.Button(
        "Après", id="btn-apres1", color="primary", className="mr-1", style={'float': 'right', 'background-color': '#670907'})
    return [html.Div(children=[
        html.Div([
            apres,
            dbc.Button("Retour", id="btn-retour1", color="primary",
                       className="mr-1", style={'float': 'right', 'background-color': '#670907'}),
            html.H3(question, style={'textAlign': 'center'})
        ]),
        html.Div([html.P("Sélectionner un interval d'années :"),
                  rangeslider,
                  graph
                  ]),
        get_text_below_barplot(),
    ]), dcc.Location(id='url-redirect1')]


@callback(Output('barplot','figure'),
          [Input('rangeslider','value')])
def graph_update(rangeslider_value):
    if rangeslider_value is None:
        rangeslider_value = get_years_range_slider() 
    data = get_data_barplot_1522(rangeslider_value)
    return barplot_1522(data)


@callback(
    Output("url-redirect1", "pathname"),
    [Input("btn-retour1", "n_clicks"),
     Input("btn-apres1", "n_clicks")]
)
def button_callback(n_clicks_retour, n_clicks_apres):
    if n_clicks_retour:
        return '/visualisations'
    elif n_clicks_apres:
        return '/boxplot'