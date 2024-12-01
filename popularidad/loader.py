import pandas as pd
from song import Song
from hash_table import SongHashTable
import asyncio
from PyQt6.QtCore import QObject, pyqtSignal, QThread


class AsyncSongLoader(QThread):
    data_loaded = pyqtSignal(SongHashTable)  # Signal to notify when loading is complete

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    async def load_data(self):
        """
        Carga las canciones de manera asincrónica usando chunks y las inserta en la tabla hash.
        """
        hash_table = SongHashTable()

        try:
            # Leer el archivo CSV en chunks
            chunk_size = 10000  # Puedes ajustar el tamaño del chunk según sea necesario
            chunks = pd.read_csv(
                self.file_path,
                quotechar='"',
                skipinitialspace=True,
                on_bad_lines='skip',
                encoding='utf-8',
                chunksize=chunk_size
            )

            for chunk in chunks:
                # Procesar cada chunk y agregarlo a la tabla hash
                for _, row in chunk.iterrows():
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
                        hash_table.insert(song)
                    except Exception as e:
                        print(f"Error al procesar la fila: {e}")
                await asyncio.sleep(0)  # Permite que el hilo principal se mantenga activo

            self.data_loaded.emit(hash_table)  # Emitir el hash_table cargado
        except Exception as e:
            print(f"Error cargando los datos: {e}")

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.load_data())  # Ejecutar el proceso asíncrono


def load_songs_into_hash_table(file_path):
    """
    Función para iniciar el proceso asincrónico de carga de canciones.
    :param file_path: Ruta al archivo CSV con los datos de las canciones.
    :return: Instancia de SongHashTable con las canciones cargadas.
    """
    loader = AsyncSongLoader(file_path)
    return loader
