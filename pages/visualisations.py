import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, location="sidebar", use_pages=True, external_stylesheets=[
    dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

card_style = {
    'padding': '20px',
    'border': '2px solid #D3D3D3',
    'border-radius': '10px',
    'margin': '20px',
    'background-color': '#F8F9FA', 
}

image_style = {
    'width': '100%',
    'max-width': '700px',
    'height': 'auto',
    'display': 'block',
    'margin': '0 auto',
}

def layout():
    children = []
    children.append(html.Div([
        html.H1('Visualisations', style={'textAlign': 'center',
                'color': '#670907', 'font-size': '2.5em'})
    ], style=card_style))
    children.append(
        html.Img(src='/static/IMG/train.png', style={'width': '10%'}))
    children.append(
        html.P("Nous nous sommes posé plusieurs questions sur les données de la SNCF concernant les incidents, et c'est à travers différentes visualisations que nous avons tenté d'y répondre.", style={'fontSize': '1.25em'}))

    children.append(html.Div([
        dcc.Link(pi['question'], href=pi['path'],
                 style={'fontSize': min(30, max(15, 400 // len(pi['question']))), 
                        'margin': '20px', 'padding': '10px', 'border': '5px double white',
                        'backgroundColor': '#670907', 'color': 'white', 'width': '300px',
                        'height': '300px', 'text-align': 'center', 'horizontalAlign': 'middle',
                        'textDecoration': 'none'})
        for pi in dash.page_registry.values() if 'question' in pi
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-evenly'}))
    children.append(
        html.Img(src='/static/IMG/gif_train.gif', style=image_style))

    return html.Div(children=children)