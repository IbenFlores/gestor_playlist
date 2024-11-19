import pandas as pd
import re

# Ruta del archivo CSV
file_path = "spotify_data.csv"

def limpiar_titulo(titulo):
    """
    Limpia los títulos de canciones, conservando solo el texto relevante (hasta el último guion).
    """
    if not isinstance(titulo, str):
        return ""
    return re.sub(r' - [^,]+,.*', '', titulo).strip()

def buscar_canciones_por_artista(df):
    """
    Permite buscar canciones por el nombre del artista.
    """
    while True:
        artista = input("\nIngresa el nombre del artista (o escribe 'salir' para terminar): ").strip()
        if artista.lower() == 'salir':
            print("Volviendo al menú principal.")
            break
        canciones = df[df['artist_name'].str.contains(artista, case=False, na=False)][['track_name']]
        if not canciones.empty:
            print(f"\nCanciones de '{artista}':")
            print(canciones.to_string(index=False, header=False))
        else:
            print(f"\nNo se encontraron canciones para el artista '{artista}'.")

def mostrar_todas_las_canciones(df):
    """
    Muestra todas las canciones y artistas disponibles en bloques de 100 filas.
    Permite ordenar los datos por diferentes criterios.
    """
    while True:
        print("\nOpciones de ordenamiento:")
        print("1. Ordenar por nombre del artista")
        print("2. Ordenar por nombre de la canción")
        
        # Generar dinámicamente las opciones para columnas adicionales
        columnas_adicionales = {
            '3': 'year',
            '4': 'popularity',
            '5': 'danceability',
            '6': 'energy',
            '7': 'key',
            '8': 'loudness',
            '9': 'mode',
            '10': 'speechiness',
            '11': 'acousticness',
            '12': 'instrumentalness',
            '13': 'liveness',
            '14': 'valence',
            '15': 'tempo',
            '16': 'time_signature',
            '17': 'duration_ms'
        }
        
        for clave, columna in columnas_adicionales.items():
            if columna in df.columns:
                print(f"{clave}. Ordenar por {columna}")
        
        print("18. Volver al menú principal")
        opcion_orden = input("Selecciona una opción: ").strip()
        
        if opcion_orden == '18':
            print("Volviendo al menú principal.")
            break
        elif opcion_orden not in columnas_adicionales.keys() and opcion_orden not in ['1', '2']:
            print("Opción no válida. Intenta de nuevo.")
            continue
        
        # Elegir la dirección de ordenamiento
        print("\nOpciones de dirección:")
        print("1. Ascendente")
        print("2. Descendente")
        direccion = input("Selecciona una dirección (1-2): ").strip()
        ascendente = direccion == '1'
        
        if direccion not in ['1', '2']:
            print("Dirección no válida. Intenta de nuevo.")
            continue
        
        # Aplicar el criterio de ordenamiento
        columna_orden = {
            '1': 'artist_name',
            '2': 'track_name',
            **columnas_adicionales
        }[opcion_orden]
        
        df_sorted = df.sort_values(by=columna_orden, ascending=ascendente)
        
        # Dividir los datos en bloques de 100 filas
        num_filas = 100
        total_filas = len(df_sorted)
        total_bloques = (total_filas // num_filas) + (1 if total_filas % num_filas != 0 else 0)
        
        while True:
            print(f"\nTotal de bloques disponibles: {total_bloques}")
            print("Introduce el número del bloque que deseas ver (o escribe 'salir' para regresar):")
            bloque = input(f"Selecciona un bloque (1-{total_bloques}): ").strip()
            
            if bloque.lower() == 'salir':
                print("Saliendo del modo de visualización.")
                break
            elif not bloque.isdigit() or int(bloque) < 1 or int(bloque) > total_bloques:
                print(f"Opción no válida. Introduce un número entre 1 y {total_bloques}.")
                continue
            
            # Mostrar el bloque seleccionado
            bloque = int(bloque)
            inicio = (bloque - 1) * num_filas
            fin = min(inicio + num_filas, total_filas)
            print(f"\nMostrando bloque {bloque} (filas {inicio + 1}-{fin}):")
            
            # Mostrar solo las columnas relevantes: criterio de orden, artista y canción
            print(df_sorted.iloc[inicio:fin][[columna_orden, 'artist_name', 'track_name']].to_string(index=False))

try:
    # Leer el archivo CSV ignorando líneas mal formateadas
    df = pd.read_csv(
        file_path,
        quotechar='"',
        skipinitialspace=True,
        on_bad_lines='skip',
        encoding='utf-8'
    )

    # Verificar si las columnas necesarias existen
    if 'artist_name' in df.columns and 'track_name' in df.columns:
        df['artist_name'] = df['artist_name'].astype(str).str.strip()
        df['track_name'] = df['track_name'].apply(limpiar_titulo)

        while True:
            print("\nMenú de opciones:")
            print("1. Buscar canciones por artista")
            print("2. Mostrar todas las canciones")
            print("3. Salir")
            
            opcion = input("Selecciona una opción (1-3): ").strip()
            
            if opcion == '1':
                buscar_canciones_por_artista(df)
            elif opcion == '2':
                mostrar_todas_las_canciones(df)
            elif opcion == '3':
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, selecciona una opción válida (1-3).")
    else:
        print("El archivo no contiene las columnas 'artist_name' o 'track_name'. Verifica el formato del archivo.")

except FileNotFoundError:
    print("El archivo no se encontró. Asegúrate de que el archivo esté en la ubicación correcta.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
