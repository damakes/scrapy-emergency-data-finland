import pandas as pd
import folium
import branca.colormap as cm

def generate_map(csv_file, output_html='index.html'):
    dx = pd.read_csv('emersnow.csv')
    dy = pd.read_csv('latlong.csv')

    df = pd.merge(dx, dy, on="location", how="left")

    df.to_csv("emersnow&latlong.csv", index=False)

    df['incident_detail'] = df.apply(
        lambda row: f"{row['type']} ({row['date']} {row['time']})",
        axis=1
    )
    df.dropna(inplace=True)

    df = df.drop_duplicates()

    max_date = df.date.max()
    min_date = df.date.min()

    title = f'{min_date} / {max_date}'

    title_html = f'<h1 style="position:absolute;z-index:100000;left:40vw" >{title}</h1>'


    all_locations = df.groupby('location').agg(
    latitude=('latitude', 'first'),
    longitude=('longitude', 'first'),
    incidents=('type', 'count'),
    incident_details=('incident_detail', lambda x: '<br>'.join(x))
    ).reset_index()

    colormap = cm.LinearColormap(
        colors=['#00FFFF','#FFD700','#FF4500','#FF0000'],
        vmin=all_locations['incidents'].min(),
        vmax=all_locations['incidents'].max()
    )


    incident_counts = df.groupby(['location', 'type']).size().unstack(fill_value=0).reset_index()

    map = folium.Map(
        location=[64.9146659, 26.0672554],
        tiles='cartodbdark_matter',
        zoom_start=5
    )
    for i, row in all_locations.iterrows():
        location = [row['latitude'], row['longitude']]

        hover_text = (
            f"<h1 style='color:#696969'><u>{row['location']}</u></h1>"
            f"<i><small style='color:#696969'>Hälytykset: {row['incidents']}</small></i><br>"
            )

        incident_info = incident_counts[incident_counts['location'] == row['location']].iloc[:, 1:]

        for incident_type, count in incident_info.items():
            if count.values[0] > 0:
                hover_text += f"<strong style='color:#FF4500'>{incident_type}:</strong> {count.values[0]}<br>"

        color = colormap(row['incidents'])

        popup_text = folium.Popup(f"<u>{row['incident_details']}</u>",
                                max_width=800
                                )

        folium.CircleMarker(
            location=location,
            radius=5,
            tooltip=hover_text + f"<small style='color:#696969'><b><i>lisätietoja...</b></i></small>",
            popup=popup_text,
            color=None,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(map)

    map.get_root().html.add_child(folium.Element(title_html))

    colormap.add_to(map)

    map.save(output_html)

if __name__ == '__main__':
    generate_map('emerscraper\emerscraper\emersnow.csv')
