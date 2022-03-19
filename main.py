from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def main():
    return 'Usa /suggestions para desplegar info'

@app.route('/suggestions', methods=['GET'])
def suggestions():
    print (request.args)
    if len(request.args) > 0:
        params = request.args.to_dict()
        if params['q'] != '':
            ciudad_l = params['q']
            latitud = float(params['latitude']) if 'latitude' in params.keys() else 0
            longitud = float(params['longitude']) if 'longitude' in params.keys() else 0
            ciudades_gen = load_city(ciudad_l,latitud,longitud)
            ciudades_gen = ciudades_gen.reindex(columns=['name','latitude','longtitude','score'])
            print(ciudades_gen)
            despliegue={'suggestion':ciudades_gen.to_dict('records')}
            print(despliegue)            
        else:
            despliegue = 'No hay un Ciudad'
    else:
        despliegue = 'Ingresa los parametros'
    return despliegue, 200

def load_city(ciudad_func,latitud_func,longitud_func):
    datos_ciudad = pd.read_csv('cities_canada-usa.tsv', sep='\t')
    columnas_tabla = ['lat','long','name']
    ciudades_correspondientes = datos_ciudad[datos_ciudad['name'].str.contains(ciudad_func)][columnas_tabla]
    if latitud_func != 0 and longitud_func != 0:
        columnas_latylong = ['lat', 'long']
        ciudades_correspondientes[columnas_latylong] = ciudades_correspondientes[columnas_latylong].astype(float) 
        ciudades_correspondientes['score']=ciudades_correspondientes.apply(lambda d: calculodescore(d["long"],d['lat'],  longitud_func, latitud_func ), axis=1)        
        ciudades_correspondientes.rename(columns={'lat':'latitude', 'long':'longtitude'}, inplace=True)
        ciudades_correspondientes['name']=ciudades_correspondientes.apply(lambda d: ''+d['name'], axis=1)        
        ciudades_correspondientes.sort_values(by='score', ascending=False, inplace=True) 
        ciudades_correspondientes.reset_index(drop=True, inplace=True)        
    return ciudades_correspondientes

def calculodescore(longitud1, latitud1, longitud2, latitud2):
    latitudG = abs(latitud2 - latitud1)
    longitudG = abs(longitud2 - longitud1)
    score = 10 - (latitudG + longitudG) / 2
    score = round(score,0) / 10 if score > 0 else 0
    return score

if __name__ == '__main__':
    app.run()
