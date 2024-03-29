import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import concurrent.futures


# Boxplot
def build_boxplot(data):
    fig = px.box(data, x='year', y=data.groupby('year').cumcount(),
                 title='Nombre d\'incidents par année',
                 category_orders={'year': sorted(data['year'].unique())})
    fig.add_trace(go.Scatter(
        x=['2020', '2020'],
        y=[0, data.groupby('year').cumcount().max() + 1],
        mode="lines",
        line=dict(color="red", width=2, dash='dash'),
        showlegend=True,  # Afficher la légende pour cette trace
        name='Début de la crise du COVID-19'
    ))
    fig.update_layout(
        title_font=dict(size=24),
        xaxis=dict(
            title=dict(text='Années', font=dict(size=18)),
            tickfont=dict(size=18),
        ),
        yaxis=dict(title=dict(text='Nombre d\'incidents', font=dict(size=22)),
                   tickfont=dict(size=18),),
        legend=dict(
            x=1.02,
            y=0.5,
            traceorder='normal',
            font=dict(size=16),
            bgcolor='rgba(255, 255, 255, 0.5)',
        )
    )
    return fig


# Scatter
def build_scatter(df, year):
    if year == '2023':
        gravite = 'gravite_epsf'
    else:
        gravite = 'niveau_gravite'
    df['Mois'] = df['Mois'].dt.strftime('%Y-%m')
    fig = px.scatter(df, x='Mois', y=gravite,
                     title=f'Gravité moyenne par mois', color=gravite)
    fig.update_traces(marker=dict(size=25), selector=dict(mode='markers'))
    #mode de sélection et de clic sur le graphique. Avec cette configuration, 
    #le graphique peut être interagi en cliquant et en sélectionnant des éléments
    fig.update_layout(clickmode='event+select', yaxis_title="Gravité")
    return fig


# Lineplot
def build_lineplot(df, selected_option, cumulative_mode):
    # Groupe les données par année et origine, puis compte le nombre d'incidents par groupe
    incidents_par_annee = df.groupby(['year', 'origine']).size().reset_index(name='nombre_incidents')   
    # Vérifie si le mode cumulatif est activé
    if cumulative_mode:
        # Calcule le nombre cumulatif d'incidents par origine au fil des années
        incidents_par_annee['cumulative_incidents'] = incidents_par_annee.groupby('origine')['nombre_incidents'].cumsum()
        y_column = 'cumulative_incidents'
        title = 'Nombre cumulatif d\'incidents au cours des années'
    else:
        y_column = 'nombre_incidents'
        title = 'Nombre d\'incidents au cours des années'
    # Vérifie l'option sélectionnée ('all' ou une origine spécifique)
    if selected_option == 'all':
        # Agrège les données pour toutes les origines
        aggregated_df = incidents_par_annee.groupby('year')[y_column].sum().reset_index()       
        # Crée un graphique de ligne pour l'agrégation
        fig_line = px.line(aggregated_df, x='year', y=y_column, title=title,
                           labels={'nombre_incidents': 'Nombre d\'incidents', 'year': 'Années'})
    else:
        # Filtre les données pour inclure uniquement l'origine spécifiée dans 'selected_option'
        filtered_df_line = incidents_par_annee[incidents_par_annee['origine'].isin(df['origine'].unique())]       
        # Crée un graphique de ligne pour les données filtrées par origine
        fig_line = px.line(filtered_df_line, x='year', y=y_column, color='origine',
                           title=title, labels={'nombre_incidents': 'Nombre d\'incidents', 'year': 'Années'}) 
    # Retourne le graphique de ligne résultant
    return fig_line



# Heapmap
def build_heapmap(df, selected_option, click_data):
    # Groupe les données par année, origine et région, puis compte le nombre d'incidents par groupe
    incidents_par_region_annee = df.groupby(
        ['year', 'origine', 'region']).size().reset_index(name='nombre_incidents')
    # Vérifie s'il y a des données de clic et si l'option 'all' est sélectionnée
    if click_data and 'points' in click_data and click_data['points']:
        if selected_option == 'all':  # version globale du heapmap quand on passe de distinction à all -> all=globale
            # Crée un heatmap pour toutes les origines confondues
            fig_heatmap = px.imshow(incidents_par_region_annee.pivot_table(index='year', columns='region', values='nombre_incidents'),
                                    labels=dict(x="Régions", y="Années",
                                                color="Nombre d'incidents"),
                                    title='Heatmap du nombre d\'incidents par région au cours des années pour toutes les origines confondues')
        else:
            # Obtient l'origine sur laquelle l'utilisateur a cliqué
            clicked_origine = click_data['points'][0]['curveNumber']
            # Filtre les données pour inclure uniquement l'origine spécifiée par le clic
            filtered_df = incidents_par_region_annee[incidents_par_region_annee['origine'] == df['origine'].unique()[
                clicked_origine]]
            clicked_origine_label = incidents_par_region_annee['origine'].unique()[
                clicked_origine]
            # Crée un heatmap pour l'origine spécifique sélectionnée
            fig_heatmap = px.imshow(filtered_df.pivot_table(index='year', columns='region', values='nombre_incidents'),
                                    labels=dict(x="Régions", y="Années",
                                                color="Nombre d'incidents"),
                                    title=f'Heatmap du nombre d\'incidents causés par {clicked_origine_label} par région au cours des années')
    else:
        # Crée un heatmap pour toutes les origines confondues (option par défaut) -> au tout début quand on ouvre la page
        fig_heatmap = px.imshow(incidents_par_region_annee.pivot_table(index='year', columns='region', values='nombre_incidents'),
                                labels=dict(x="Régions", y="Années",
                                            color="Nombre d'incidents"),
                                title='Heatmap du nombre d\'incidents par région au cours des années pour toutes les origines confondues')

    fig_heatmap.update_layout(xaxis=dict(tickangle=45))
    return fig_heatmap


# Sunburst
def build_sunburst(df_all_trees):
    colors = {
        1: 'purple',
        2: 'blue',
        3: 'green',
        4: 'yellow',
        5: 'orange',
        6: 'red',
        'Réseau': 'pink', 'Mobilités': 'olive',
        'Voyageur': 'grey',
        'Cause Tiers Réseau': 'brown',
        'Cause Tiers Mobilités': 'cyan',
        'Cause Tiers Voyageur': 'magenta',
        'Indéterminé': 'lime',
        'CT': 'teal',
        'Accident de personne': 'maroon',
        'Collision passage à niveau': 'aliceblue',
        'Voyageurs': 'lightcoral',
        'Electrisation tiers': 'mediumseagreen',
        'Collision hors passage à niveau': 'slategray',
        'FRET': 'wheat',
        'EF CAP TRAIN': 'tomato',
        'EF Ext': 'navy',
        'Externe': 'orchid',
        'Heurt installation par tiers': 'aquamarine',
        'ACCIDENTS SNCF': 'white'
    }
    # on ajoute d'une colonne 'color' basée sur la correspondance avec les couleurs définies
    df_all_trees['color'] = df_all_trees['id'].map(colors)

    fig = go.Figure(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        hovertemplate='<b>%{label} </b> <br> Count: %{value}',
        maxdepth=2,
        marker=dict(
            colors=df_all_trees['color'],
            line=dict(color='black', width=1)
        ),
    ))
    fig.update_layout(margin=dict(t=15, b=15, r=15, l=15))
    return fig


# Barplot
def barplot_1522(data):
    fig = px.bar(data, barmode='group')
    fig.update_layout(
        xaxis={'title': 'Région'},
        yaxis={'title': 'Gravité Moyenne'},
        title='Gravité Moyenne des 5 Principaux Types d\'Incidents dans les 5 Principales Régions'
    )
    return fig


# Map
def build_map(lines_layer, start_date, end_date, fig_fetch_and_process_lines, regions, df_combined, display_option, n_clicks_no_lines, n_clicks_with_lines, n_clicks_with_lines_types):
    if n_clicks_no_lines > 0:
        lines_layer = None
    elif n_clicks_with_lines > 0:
        lines_layer = fig_fetch_and_process_lines
    elif n_clicks_with_lines_types > 0:
        lines_layer = fig_fetch_and_process_lines
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_data = df_combined[(df_combined['date'] >= start_date) & (
        df_combined['date'] <= end_date)]
    if display_option == 'incident_count':
        display_data = filtered_data.groupby(
            'region').size().reset_index(name='display_value')
    elif display_option == 'average_gravity':
        display_data = filtered_data.groupby(
            'region')['niveau_gravite'].mean().reset_index(name='display_value')
    merged_data = pd.merge(regions, display_data,
                           left_on='nom', right_on='region', how='left')
    updated_fig = px.choropleth_mapbox(merged_data,
                                       geojson=merged_data.geometry,
                                       locations=merged_data.index,
                                       color='display_value',
                                       hover_name='nom',
                                       title=f'Carte des incidents SNCF par région - {display_option}',
                                       mapbox_style="carto-positron",
                                       center={"lat": 46.6035, "lon": 1.8888},
                                       zoom=4)
    if lines_layer:
        for trace in lines_layer:
            updated_fig.add_trace(trace)
    return updated_fig


def fetch_and_process_lines(data_lines):
    # Liste qui stocke les traces pour les lignes géographiques
    traces_lines = []
    # Fonction interne pour traiter chaque élément (item) des données
    def process_item(item):
        # Vérifie si les clés nécessaires sont présentes dans l'élément
        if 'geo_shape' in item and 'geometry' in item['geo_shape'] and 'coordinates' in item['geo_shape']['geometry']:
            # Récupère les coordonnées de l'élément
            coordinates = item['geo_shape']['geometry']['coordinates']          
            # Crée une trace pour la ligne géographique
            trace_line = go.Scattermapbox(
                lat=[coord[1] for coord in coordinates],
                lon=[coord[0] for coord in coordinates],
                mode='lines',
                line=dict(color='black', width=2),
                hoverinfo='none',
                showlegend=False,
            )
            # Ajoute la trace à la liste des traces_lines
            traces_lines.append(trace_line)
    # Utilise un ThreadPoolExecutor pour traiter les éléments en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_item, data_lines)
    # Retourne la liste des traces_lines résultantes
    return traces_lines

