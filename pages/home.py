import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', location="sidebar", external_stylesheets=[
                   dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

card_style = {
    'padding': '20px',
    'border': '2px solid #D3D3D3',
    'border-radius': '10px',
    'margin': '20px',
    'background-color': '#F8F9FA',
}


layout = html.Div(style={'color': 'black', 'min-height': '100vh'}, children=[
    html.Div([
        html.H1('Home', style={'textAlign': 'center',
                'color': '#670907', 'font-size': '2.5em'}),
    ], style=card_style),
    html.Br(),
    html.H2("Bienvenue sur la page d'accueil !",
            style={'textAlign': 'center', 'fontSize': '3.0em'}),
    html.Br(),
    html.Div(style={'color': 'black'}, children=[
        html.H4(
            'Mesdames et Messieurs, bonjour et bienvenue à bord de notre Dashboard en direction notre projet de visualisation qui porte sur les données d’incidents de la SNCF. '
            'Au départ de la page Home, notre Dashboard desservira la page Visualisations et la page About us, son terminus.',
            style={'textAlign': 'center', 'fontSize': '1.75em'}),
        html.H4(
            'Nous vous souhaitons à toutes et à tous une agréable expérience. Attention au départ !',
            style={'textAlign': 'center', 'fontSize': '1.75em'}),

        html.Img(src='/static/IMG/gare.png', style={'width': '20%', 'display': 'block',
                 'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '20px'}),

        html.P("Tout d’abord, pourquoi ces données ? Nous les avons choisies car nous cherchions un thème en rapport avec les déplacements et la sécurité routière en France, "
               "en particulier les incidents de la route, d’avion, ... puis nous avons trouvé une base de données sur les incidents de la SNCF sur laquelle nous nous sommes intéressées. "
               "Par la suite, sur ce même site nous avons trouvé d'autres bases de données sur les lignes que nous avons décidé de récupérer pour notre projet. "
               "À travers ce dashboard, nous allons vous présenter les questions que nous nous sommes posées sur ces données et les visualisations que nous avons réalisé pour y répondre.", style={'fontSize': '1.25em'}),

        html.P("Pour la récupération des données, nous avons mis en place une utilisation de l'outil MongoDB "
               "avec l'API afin d'assurer une mise à jour régulière et une précision maximale. Les données sont extraites "
               "à partir du site officiel de la SNCF et sont traitées de manière à fournir des informations "
               "pertinentes et à jour.", style={'fontSize': '1.25em'}),
        html.P("Les 6 bases de données que nous utilisons sont les suivantes :", style={
            'fontSize': '1.25em'}),
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'fontSize': '1.25em'}, children=[
            html.Li(html.A("Incidents de sécurité (Evénements de sécurité remarquables - ESR) de janvier 2015 à décembre 2022",
                    href='https://data.sncf.com/explore/dataset/incidents-securite/table/?sort=date', target='_blank')),
            html.Li(html.A("Incidents de sécurité (EPSF) depuis janvier 2023", href='https://data.sncf.com/explore/dataset/incidents-de-securite-epsf/table/?sort=date&calendarview=month&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZ3Jhdml0ZV9lcHNmIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ExMDA2QiJ9XSwieEF4aXMiOiJkYXRlIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoibW9udGgiLCJzb3J0IjoiIiwiY29uZmlnIjp7ImRhdGFzZXQiOiJpbmNpZGVudHMtZGUtc2VjdXJpdGUtZXBzZiIsIm9wdGlvbnMiOnsic29ydCI6ImRhdGUifX19XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZSwidGltZXNjYWxlIjoiIn0%3D', target='_blank')),
            html.Li(html.A("Liste des lignes électrifiées",
                    href='https://data.sncf.com/explore/dataset/liste-des-lignes-electrifiees/table/', target='_blank')),
            html.Li(html.A("Lignes par type",
                    href='https://data.sncf.com/explore/dataset/lignes-par-type/table/', target='_blank')),
            html.Li(html.A("Lignes par région administrative",
                    href='https://data.sncf.com/explore/dataset/lignes-par-region-administrative/table/', target='_blank')),
            html.Li(html.A("Météo",
                    href='https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/table/?sort=date&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJ0YyIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiNGRjUxNUEifV0sInhBeGlzIjoiZGF0ZSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6ImRheSIsInNvcnQiOiIiLCJjb25maWciOnsiZGF0YXNldCI6ImRvbm5lZXMtc3lub3AtZXNzZW50aWVsbGVzLW9tbSIsIm9wdGlvbnMiOnt9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D', target='_blank'))
        ]),
        html.Br(),
        html.P("Nos deux premières bases de données concernant les incidents de 2015 à 2022 et de 2023, contiennent des informations sur les incidents : "
               "la date, l'origine, le type d'évènements, la région et le lieu, ainsi que le niveau de gravité.", style={'fontSize': '1.25em'}),
        html.P("Chaque incident est classé selon l'échelle de gravité ci-dessous (de 1 la plus faible, à 6 la plus forte). Comme indiqué, cette échelle a été mise en place en 2016, "
               "cela explique que dans nos bases de données les incidents avant 2016 n'ont pas de gravité associée.", style={'fontSize': '1.25em'}),

        html.Img(src='/static/IMG/gravite.png', style={'width': '40%', 'display': 'block',
                 'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '20px'}),
        html.P("Image issue du site : https://www.cheminots.net/topic/42925-prise-en-écharpe/", style={'width': '30%', 'display': 'block',
                                                                                                       'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '20px', 'fontSize': '0.15em'}),

        html.P("Dans nos 3 bases de données concernant les lignes, nous allons nous intéresser aux colonnes des coordonnées géographiques et des régions, dans le but de construire des cartes pour les visualiser.", style={
               'fontSize': '1.25em'}),

        html.P("Enfin, dans la base de données de la météo, parmis les 82 colonnes, nous allons nous intéresser à la température, la date, la région, les précipitations, et les coordonnées géographiques.", style={
               'fontSize': '1.25em'}),
    ])
])