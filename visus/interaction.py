from dash import dcc, html

# Dropdown
def build_dropdown_year(item_list):
    # création d'un dictionnaire pour chaque élément
    options = [{"label": x, "value": x} for x in item_list]
    return dcc.Dropdown(id='dropdown',
                        options=options,
                        value=item_list[0],
                        style={'color': 'black'})

def build_dropdown_year_multi(item_list):
    options = [{"label": x, "value": x} for x in item_list]
    return dcc.Dropdown(id='dropdown',
                        options=options,
                        value=item_list, 
                        multi=True, 
                        style={'color': 'black'})


# Range slider
def build_range_slider(min_val, max_val, default_values, marks_list):
    # Crée un dictionnaire de marques pour le curseur de plage
    marks = {str(mark): str(mark) for mark in marks_list}
    return dcc.RangeSlider(
        id='rangeslider',
        min=min_val,
        max=max_val,
        value=default_values,
        marks=marks,
        step=1,
    )


# Radio item
def build_radioitems():
    radioitems = dcc.RadioItems(
        id='origine-radio',
        options=[
            {'label': 'Distinction des origines', 'value': 'distinct'},
            {'label': 'Globale', 'value': 'all'},
        ],
        value='distinct',
        inline=True,
        style={'fontSize': 20, 'textAlign': 'center'}
    )
    cumulative_radioitem = dcc.RadioItems(
        id='cumulative-radio',
        options=[
            {'label': 'Cumulatif', 'value': True},
            {'label': 'Non Cumulatif', 'value': False},
        ],
        value=False,
        inline=True,
        style={'fontSize': 20, 'textAlign': 'center'}
    )
    return html.Div([radioitems, cumulative_radioitem])


# Date picker
def build_radioitems_map(start_date, end_date):
    datepickerrange_props = {
        "start_date": start_date,
        "end_date": end_date,
        "display_format": "YYYY-MM-DD",
        "id": "date-picker-range"
    }
    radioitems_props = {
        "options": [
            {"label": "Nombre d'incidents", "value": "incident_count"},
            {"label": "Moyenne du niveau de gravité", "value": "average_gravity"},
        ],
        "value": "incident_count",
        "inline": True,
        "style": {"fontSize": 20, "textAlign": "center"},
        "id": "map-display-option"
    }
    # tuple donc on doit mettre des étoiles : retourner en tant qu'éléments distincts plutôt que sous la forme d'un tuple
    datepickerrange = dcc.DatePickerRange(**datepickerrange_props)
    radioitems = dcc.RadioItems(**radioitems_props)
    return datepickerrange, radioitems


# Buttons Map
def generate_button_div():
    # Liste de tuples contenant l'ID et le libellé de chaque bouton
    button_info = [
        ('button-no-electric-lines', 'Sans les lignes'),
        ('button-with-electric-lines', 'Lignes électrifiées'),
        ('button-with-lines-types', 'Lignes types'),
    ]
    # Crée une liste de boutons à partir de button_info
    buttons = [html.Button(label, id=button_id, n_clicks=0) for button_id, label in button_info]   
    # Crée une division contenant les boutons, avec une mise en page spécifique
    button_div = html.Div(buttons, style={'textAlign': 'center', 'justify-content': 'space-between'})   
    # Retourne la division contenant les boutons
    return button_div
