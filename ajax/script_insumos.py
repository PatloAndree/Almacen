import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import locale

#df = pd.read_csv('c:/xampp/htdocs/almacen/ajax/mesproductos_test.csv')
df = pd.read_csv('c:/xampp2/htdocs/almacen2/ajax/am_confecciones.csv')


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Convierto fecha a datatime para hacer los calculos (La fecha realmente se convierte a 
# numeros para calcular, una fecha tal como esta no se puede calcular )
df['fecha'] = pd.to_datetime(df['fecha'])


idinsumo_dict = {1: "Telas", 2: "Botones", 3: "Etiquetas"}

# Renombra los idinsumos
df['idinsumo'] = df['idinsumo'].replace(idinsumo_dict)


for insumo in df['idinsumo'].unique():
  
    df_insumo = df[df['idinsumo'] == insumo]

   
    df_insumo = df_insumo.sort_values('fecha')

    # Configuro 'Fecha' como el índice
    df_insumo.set_index('fecha', inplace=True)


    df_insumo_mes = df_insumo.resample('M').sum()


    modelo = SARIMAX(df_insumo_mes['cantidad'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    resultado = modelo.fit(disp=False)

    # predict próximos 12 meses
    prediccion = resultado.predict(start=61, end=72)

    # Redondeamos
    prediccion = prediccion.round()


    plt.figure(figsize=(10,6))
    plt.plot(prediccion.index.strftime('%B'), prediccion, marker='o')
    plt.title(f'Predicción del año 2024 para {insumo}')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Muestra las cantidades exactas
    for i, v in enumerate(prediccion):
        plt.text(i, v, int(v), ha='center', va='bottom')

    # Guarda la imagen
    plt.savefig(f'c:/xampp2/htdocs/almacen2/files/reportes_ml/prediccion_{insumo}_2024.png')    
    #guardarmos las imagenes
    # Crea un gráfico de líneas con las predicciones
    """ plt.figure(figsize=(10,6))
    plt.plot(prediccion.index.strftime('%B'), prediccion, marker='o')
    plt.title(f'Predicción del año 2024 para {insumo}')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.grid(True) """

    # Muestra las cantidades exactas en el gráfico
"""     for i, v in enumerate(prediccion):
        plt.text(i, v, int(v), ha='center', va='bottom') """

"""     plt.show() """