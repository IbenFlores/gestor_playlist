import pandas as pd
import re
import random

def conocer_cancion_nueva(df, reproductor_personal):
    """
    Selecciona una canción al azar del DataFrame, muestra información al usuario,
    y permite decidir si guardarla en el reproductor personal.
    """
    while True:
        # Elegir una canción al azar
        cancion_aleatoria = df.sample(1).iloc[0]  # Selecciona una fila aleatoria del DataFrame
        
        # Mostrar información de la canción
        print("\n🎵 ¡Conoce una nueva canción! 🎶")
        print(f"Artista: {cancion_aleatoria['artist_name']}")
        print(f"Canción: {cancion_aleatoria['track_name']}")
        print(f"Género: {cancion_aleatoria['genre']}")
        
        # Opciones del usuario
        print("\n¿Qué deseas hacer con esta canción?")
        print("1. Guardar en mi reproductor personal")
        print("2. Escuchar otra canción aleatoria")
        print("3. Volver al menú principal")
        
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == '1':
            # Guardar canción en el reproductor personal
            reproductor_personal.append({
                'artist_name': cancion_aleatoria['artist_name'],
                'track_name': cancion_aleatoria['track_name'],
                'genre': cancion_aleatoria['genre']
            })
            print(f"✅ Canción '{cancion_aleatoria['track_name']}' de '{cancion_aleatoria['artist_name']}' guardada en tu reproductor personal.")
            break  # Salimos después de guardar
        elif opcion == '2':
            print("\nBuscando otra canción aleatoria... 🎶")
            continue  # Selecciona otra canción
        elif opcion == '3':
            print("Volviendo al menú principal.")
            break  # Salimos al menú principal
        else:
            print("Opción no válida. Por favor, selecciona una opción válida (1-3).")

# Ruta del archivo CSV
file_path = "hash_py/spotify_data.csv"

try:
    df = pd.read_csv(
        file_path,
        quotechar='"',
        skipinitialspace=True,
        on_bad_lines='skip',
        encoding='utf-8'
    )
    print("Archivo CSV cargado con éxito.")
except FileNotFoundError:
    print("Error: El archivo CSV no se encontró. Asegúrate de que el archivo esté en la ubicación correcta.")
    df = None  # Evitamos errores si el archivo no se carga

# Lista para el reproductor personal
reproductor_personal = []

def limpiar_titulo(titulo):
    """
    Limpia los títulos de canciones, conservando solo el texto relevante (hasta el último guion).
    """
    if not isinstance(titulo, str):
        return ""
    return re.sub(r' - [^,]+,.*', '', titulo).strip()

def buscar_canciones_por_artista(df):
    """
    Permite buscar canciones por el nombre del artista y guardar canciones en el reproductor personal.
    """
    while True:
        artista = input("\nIngresa el nombre del artista (o escribe 'salir' para terminar): ").strip()
        if artista.lower() == 'salir':
            print("Volviendo al menú principal.")
            break
        
        # Filtrar canciones por el nombre del artista
        canciones = df[df['artist_name'].str.contains(artista, case=False, na=False)][['artist_name', 'track_name', 'genre']]
        
        if not canciones.empty:
            print(f"\nCanciones de '{artista}':")
            
            # Mostrar canciones bien alineadas
            print(canciones.reset_index(drop=True).to_string(index=True, header=True))
            
            # Solicitar guardar canciones
            seleccion = input("\nIngresa el número de la canción para guardar en tu reproductor (o escribe 'salir' para regresar): ").strip()
            if seleccion.lower() == 'salir':
                continue
            elif seleccion.isdigit() and 0 <= int(seleccion) < len(canciones):
                cancion = canciones.iloc[int(seleccion)]
                
                # Agregar canción al reproductor personal con género incluido
                reproductor_personal.append({
                    'artist_name': cancion['artist_name'],
                    'track_name': cancion['track_name'],
                    'genre': cancion['genre']
                })
                print(f"Canción '{cancion['track_name']}' de '{cancion['artist_name']}' (Género: {cancion['genre']}) guardada en tu reproductor personal.")
            else:
                print("Selección inválida. Intenta de nuevo.")
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

def gestionar_reproductor_personal():
    """
    Permite al usuario ver, ordenar, escuchar, agregar o eliminar canciones de su reproductor personal.
    """
    while True:
        print("\nGestión de reproductor personal:")
        print("1. Ver canciones guardadas")
        print("2. Ordenar canciones guardadas")
        print("3. Eliminar una canción")
        print("4. Reproducir canción aleatoria")  # Nueva opción
        print("5. Volver al menú principal")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == '1':
            if reproductor_personal:
                print("\nCanciones en tu reproductor personal:")
                for idx, cancion in enumerate(reproductor_personal, start=1):
                    print(f"{idx}. {cancion['artist_name']} - {cancion['track_name']} (Género: {cancion['genre']})")
                
                # Preguntar si se quiere escuchar una canción
                while True:
                    seleccion = input("\nIngresa el número de la canción que deseas escuchar (o escribe 'salir' para regresar): ").strip()
                    if seleccion.lower() == 'salir':
                        break
                    elif seleccion.isdigit() and 1 <= int(seleccion) <= len(reproductor_personal):
                        cancion_a_reproducir = reproductor_personal[int(seleccion) - 1]
                        print(f"\n🎵 Reproduciendo: '{cancion_a_reproducir['track_name']}' de '{cancion_a_reproducir['artist_name']}' (Género: {cancion_a_reproducir['genre']}) 🎶")
                    else:
                        print("Selección inválida. Por favor, elige un número válido o escribe 'salir'.")
            else:
                print("\nTu reproductor personal está vacío.")
        
        elif opcion == '2':
            if reproductor_personal:
                print("\nOpciones para ordenar canciones:")
                print("1. Ordenar por género")
                print("2. Ordenar por nombre de la canción")
                print("3. Ordenar por artista")
                print("4. Cancelar y volver")
                
                criterio = input("Selecciona un criterio de ordenamiento: ").strip()
                
                if criterio == '1':
                    reproductor_personal.sort(key=lambda x: x['genre'])
                    print("\nCanciones ordenadas por género.")
                elif criterio == '2':
                    reproductor_personal.sort(key=lambda x: x['track_name'])
                    print("\nCanciones ordenadas por nombre.")
                elif criterio == '3':
                    reproductor_personal.sort(key=lambda x: x['artist_name'])
                    print("\nCanciones ordenadas por artista.")
                elif criterio == '4':
                    print("Cancelando ordenamiento.")
                else:
                    print("Opción no válida. Intenta de nuevo.")
            else:
                print("\nTu reproductor personal está vacío, no hay canciones para ordenar.")
        
        elif opcion == '3':
            if not reproductor_personal:
                print("\nTu reproductor personal está vacío.")
                continue
            
            print("\nCanciones en tu reproductor personal:")
            for idx, cancion in enumerate(reproductor_personal, start=1):
                print(f"{idx}. {cancion['artist_name']} - {cancion['track_name']} (Género: {cancion['genre']})")
            
            seleccion = input("\nIngresa el número de la canción que deseas eliminar (o escribe 'salir' para regresar): ").strip()
            if seleccion.lower() == 'salir':
                continue
            elif seleccion.isdigit() and 1 <= int(seleccion) <= len(reproductor_personal):
                cancion_eliminada = reproductor_personal.pop(int(seleccion) - 1)
                print(f"\nCanción '{cancion_eliminada['track_name']}' de '{cancion_eliminada['artist_name']}' eliminada de tu reproductor personal.")
            else:
                print("Selección inválida. Intenta de nuevo.")

        elif opcion == '4':
            if reproductor_personal:
                import random  # Importamos el módulo para generar aleatoriedad
                random.shuffle(reproductor_personal)  # Reorganizamos la lista de forma aleatoria
                
                # Reproducir la primera canción de la lista aleatoria
                primera_cancion = reproductor_personal[0]
                print("\n🔀 ¡Tu playlist ha sido mezclada de forma aleatoria! 🎶")
                print(f"🎵 Reproduciendo: '{primera_cancion['track_name']}' de '{primera_cancion['artist_name']}' (Género: {primera_cancion['genre']}) 🎶")
            else:
                print("\nTu reproductor personal está vacío. Agrega canciones primero.")
        
        elif opcion == '5':
            print("Volviendo al menú principal.")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

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
            print("3. Gestionar reproductor personal")
            print("4. Conocer canción nueva")  # Nueva opción
            print("5. Salir")
            
            opcion = input("Selecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                buscar_canciones_por_artista(df)
            elif opcion == '2':
                mostrar_todas_las_canciones(df)
            elif opcion == '3':
                gestionar_reproductor_personal()
            elif opcion == '4':
                conocer_cancion_nueva(df, reproductor_personal)
            elif opcion == '5':
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, selecciona una opción válida (1-5).")
    else:
        print("El archivo no contiene las columnas 'artist_name' o 'track_name'. Verifica el formato del archivo.")

except FileNotFoundError:
    print("El archivo no se encontró. Asegúrate de que el archivo esté en la ubicación correcta.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
