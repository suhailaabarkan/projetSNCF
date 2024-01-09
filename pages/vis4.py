import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from visus.visualisation import build_sunburst
from visus.interaction import build_dropdown_year_multi
from data.get_data import get_data_sunburst, get_years_dropdown

question = "Quelles sont les causes des accidents les plus récurrentes ?"

dash.register_page(__name__, question=question, external_stylesheets=[
    dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


def layout():
    return [html.Div(children=[
        html.Div([
            dbc.Button("Retour", id="btn-retour4", color="primary",
                       className="mr-1", style={'float': 'right', 'background-color': '#670907'}),
            html.H3(question, style={'textAlign': 'center'}),
        ]),
        html.Div([
            html.P("Sélectionner une ou plusieurs années à afficher (par défaut toutes les années de 2016 à 2023 sont affichées) :"),
            build_dropdown_year_multi(get_years_dropdown()),
            html.Div(id='sunburst-container', children=[])
        ])
    ]), dcc.Location(id='url-redirect4')]


@callback(Output(component_id='sunburst-container', component_property='children'),
          [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values is None or len(dropdown_values) == 0:
        return html.Div(children=[
            html.H1("Veuillez selectionner au moins une année")])
    graphs = []
    for year in dropdown_values:
        data = get_data_sunburst(year)
        fig = build_sunburst(data)
        graph = dcc.Graph(figure=fig)
        graph_with_title = html.Div([
            html.H3(f"Année {year}", style={'textAlign': 'center'}),
            graph
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '1%', 'verticalAlign': 'top'})
        graphs.append(graph_with_title)
    return graphs


@callback(
    Output("url-redirect4", "pathname"),
    [Input("btn-retour4", "n_clicks")]
)
def retour_button_callback(n_clicks):
    if n_clicks:
        return '/visualisations'
    raise dash.exceptions.PreventUpdate
