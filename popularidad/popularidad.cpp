#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

using namespace std;

struct Cancion {
    string nombre;
    int populary;
};

bool compararPopularidad(const Cancion& a, const Cancion& b) {
    return a.populary > b.populary;
}

vector<Cancion> leerCancionesDesdeCSV(const string& nombreArchivo, const string& logArchivo) {
    vector<Cancion> canciones;
    ifstream archivo(nombreArchivo);
    ofstream log(logArchivo);
    string linea;
    int lineCount = 0, errorCount = 0;

    if (!archivo.is_open()) {
        cerr << "Error al abrir el archivo CSV." << endl;
        return canciones;
    }

    getline(archivo, linea);  // Omitir la primera línea (encabezado)

    // Leer y procesar en bloques
    const int bloqueTamano = 100000;  // Procesar en bloques de 100,000 canciones
    int cancionesProcesadas = 0;

    while (getline(archivo, linea)) {
        lineCount++;
        stringstream ss(linea);
        string temp, nombreCancion, popularidadStr;

        getline(ss, temp, ',');               // Ignora la primera columna (numeración)
        getline(ss, temp, ',');               // Nombre del artista (no necesario aquí)
        getline(ss, nombreCancion, ',');      // Nombre de la canción
        getline(ss, temp, ',');               // ID de la canción (no necesario aquí)
        getline(ss, popularidadStr, ',');     // Popularidad

        if (!popularidadStr.empty()) {
            try {
                int popularidad = stoi(popularidadStr);

                // Guardar la canción sin filtro de popularidad
                Cancion cancion;
                cancion.nombre = nombreCancion;
                cancion.populary = popularidad;
                canciones.push_back(cancion);
                cancionesProcesadas++;
            } catch (const invalid_argument& e) {
                log << "Línea " << lineCount << ": popularidad inválida para la canción '" 
                    << nombreCancion << "'. Valor: " << popularidadStr << endl;
                errorCount++;
            }
        } else {
            log << "Línea " << lineCount << ": popularidad vacía para la canción '" << nombreCancion << "'" << endl;
            errorCount++;
        }

        // Procesa el bloque y limpia memoria si llega al tamaño máximo
        if (cancionesProcesadas >= bloqueTamano) {
            canciones.clear();  // Liberar memoria después de cada bloque
            cancionesProcesadas = 0;  // Reiniciar el contador de canciones procesadas
        }
    }

    archivo.close();
    cout << "Total de errores encontrados: " << errorCount << endl;
    log.close();
    return canciones;
}


vector<Cancion> filtrarPorPopularidad(const vector<Cancion>& canciones, int popularidadMinima) {
    vector<Cancion> cancionesFiltradas;

    for (const Cancion& cancion : canciones) {
        if (cancion.populary >= popularidadMinima) {
            cancionesFiltradas.push_back(cancion);
        }
    }

    return cancionesFiltradas;
}

int main() {
vector<Cancion> canciones = leerCancionesDesdeCSV("../spotify_data.csv", "log_errores.txt");

    // Ordenar las canciones por popularidad
    sort(canciones.begin(), canciones.end(), compararPopularidad);

    // Filtrar las canciones que tengan una popularidad mayor o igual a un valor dado
    int popularidadMinima;
    cout << "Ingrese la popularidad mínima: ";
    cin >> popularidadMinima;

    vector<Cancion> cancionesFiltradas = filtrarPorPopularidad(canciones, popularidadMinima);

    // Imprimir las canciones filtradas
    cout << "Canciones con popularidad mayor o igual a " << popularidadMinima << ":\n";
    for (const Cancion& cancion : cancionesFiltradas) {
        cout << "Nombre: " << cancion.nombre << ", Popularidad: " << cancion.populary << endl;
    }

    return 0;
}
