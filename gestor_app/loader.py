import pandas as pd
from song import Song
from hash_table import SongHashTable


def load_songs_into_hash_table(file_path):
    """
    Carga canciones desde un archivo CSV y las inserta en una instancia de SongHashTable.
    :param file_path: Ruta al archivo CSV con los datos de las canciones.
    :return: Instancia de SongHashTable con las canciones cargadas.
    """
    hash_table = SongHashTable()

    try:
        # Cargar datos del archivo CSV usando pandas
        df = pd.read_csv(
            file_path,
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines='skip',
            encoding='utf-8'
        )

        # Validar si las columnas requeridas están presentes en el CSV
        required_columns = [
            'artist_name', 'track_name', 'track_id', 'popularity', 'year', 'genre',
            'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature'
        ]
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"La columna '{column}' no se encontró en el archivo CSV.")

        # Convertir cada fila en una instancia de Song e insertarla en el hash table
        for idx, row in df.iterrows():
            try:
                song = Song(
                    song_id=int(row['song_id']),  # Usamos el índice como song_id si no está en el CSV
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
                hash_table.insert(song)
            except Exception as e:
                print(f"Error al procesar la fila {idx}: {e}")

    except FileNotFoundError:
        print("El archivo CSV no fue encontrado. Verifica la ruta proporcionada.")
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

    return hash_table