# playlist_loader.py
import os
import pandas as pd
from song import Song

def load_playlists_from_folder(folder_path):
    """
    Carga todas las playlists desde los archivos CSV en una carpeta.
    :param folder_path: Ruta a la carpeta que contiene los archivos CSV.
    :return: Diccionario donde las llaves son los nombres de las playlists y los valores son listas de instancias de Song.
    """
    playlists = {}

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"La carpeta '{folder_path}' no existe.")

    # Iterar sobre todos los archivos en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            playlist_name = os.path.splitext(file_name)[0]  # Nombre del archivo sin extensión
            file_path = os.path.join(folder_path, file_name)

            try:
                # Cargar el archivo CSV
                df = pd.read_csv(
                    file_path,
                    quotechar='"',
                    skipinitialspace=True,
                    on_bad_lines='skip',
                    encoding='utf-8'
                )

                # Verificar si las columnas necesarias existen
                required_columns = [
                    'artist_name', 'track_name', 'track_id', 'popularity', 'year', 'genre',
                    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                    'duration_ms', 'time_signature'
                ]

                if not all(column in df.columns for column in required_columns):
                    print(f"El archivo '{file_name}' no tiene todas las columnas requeridas. Se omitirá.")
                    continue

                # Crear instancias de Song
                songs = []
                for _, row in df.iterrows():
                    try:
                        song = Song(
                            song_id=int(row['song_id']),
                            artist_name=row['artist_name'],
                            track_name=row['track_name'],
                            track_id=row['track_id'],
                            popularity=int(row['popularity']),
                            year=int(row['year']),
                            genre=row['genre'],
                            danceability=float(row['danceability']),
                            energy=float(row['energy']),
                            key=int(row['key']),
                            loudness=float(row['loudness']),
                            mode=int(row['mode']),
                            speechiness=float(row['speechiness']),
                            acousticness=float(row['acousticness']),
                            instrumentalness=float(row['instrumentalness']),
                            liveness=float(row['liveness']),
                            valence=float(row['valence']),
                            tempo=float(row['tempo']),
                            duration_ms=int(row['duration_ms']),
                            time_signature=int(row['time_signature'])
                        )
                        songs.append(song)
                    except Exception as e:
                        print(f"Error al crear la canción en '{file_name}': {e}")
                        continue

                # Guardar la playlist en el diccionario
                playlists[playlist_name] = songs

            except Exception as e:
                print(f"Error al leer el archivo '{file_name}': {e}")
    
    return playlists