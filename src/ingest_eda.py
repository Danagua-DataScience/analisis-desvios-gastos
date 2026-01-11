import pandas as pd
from pathlib import Path
import tkinter as tk                  


mes = input("\nEscriba el mes de los mayores a analizar (MM): ")
anio = input("\nEscriba el año de los mayores a analizar (AAAA): ")
columnas_obligatorias = ["fecha", "debe", "haber", "cuenta"]
columnas_faltantes = []
df_raw: pd.DataFrame | None = None
df_mayor: pd.DataFrame | None = None
cuentas_ingreso = [
    6157, 6159, 6160, 6162, 6194, 6206, 6164, 6168,
    6183, 6213, 6165, 6214, 6220, 6166, 6179, 6180, 6218
]


ROOT = Path.cwd().parent

mayores = ROOT / "Analisis_gastos" / "data" / "raw" / anio / mes

dfs = []



def validacion_co (df: pd.DataFrame, dfs: list, archivo):
    for o in columnas_obligatorias:
        if not o in df.columns:
            columnas_faltantes.append(o)
    if len(columnas_faltantes) == 0:
        df["archivo_origen"] = archivo.name
        dfs.append(df)
    else:
        print(f"Las siguientes columnas {columnas_faltantes} no se encuentran en el sigueinte csv: {archivo.name} ")
        exit()


def lectura_csv():
    for archivo in mayores.iterdir():     # Itera cada archivo dentro de la carpeta
        if archivo.suffix == '.CSV' or archivo.suffix == '.csv':   # Solo procesa archivos csv
            df = pd.read_csv(
                archivo,
                sep=",",
                encoding="latin1",
                engine="python",          # CLAVE
                quotechar='"',
                skipinitialspace=True,
                on_bad_lines="warn"
                )
            validacion_co(df, dfs, archivo)

    if len(dfs) > 0:
        df_raw = pd.concat(dfs)

        df_raw_ruta = ROOT / "Analisis_gastos" / "data" / "processed" / f"mayor_unificado_{mes}_{anio}.csv"

        df_raw.to_csv(
        df_raw_ruta,
        index=False
        )
        return df_raw, df_raw_ruta
    else:
        print("\nNo se leyeron los csv correctamente.")
        exit()



# LIMPIEZA DEL MAYOR UNIFICADO 

def limpieza_csv(df_raw: pd.DataFrame):
    
    df_clean: pd.DataFrame = df_raw.copy()
    df_dim = pd.read_excel(ROOT / "Analisis_gastos" / "data" / "mapping" / "clasificacion_cuentas.xlsx")
    df_cc = pd.read_excel(ROOT / "Analisis_gastos" / "data" / "mapping" / "centros_costos.xlsx")

    #Eliminar las filas de saldos acumulados inciales (sin datos)
    if len(df_clean[df_clean["det1"] == "SALDO INICIAL"].index) > 0:
       df_clean = df_clean.drop(df_clean[df_clean["det1"] == "SALDO INICIAL"].index, axis=0) 

    #Fechas
    df_clean["fecha"] = pd.to_datetime(df_clean["fecha"], dayfirst=True,)

    #Columnas sin valor
    df_clean = df_clean.drop(["apenom", "dominio", "nomdom"], axis=1)

    #Columnas con valor cero
    df_clean = df_clean.drop(["letra", "terminal", "importe", "legajo", "neto", "saldoini", "salfin"], axis=1)

    #Columnas no nocesarias
    df_clean = df_clean.drop(["cta", "saldo", "det1", "concepto", "detalle"], axis=1)

    #Columnas calculadas
    df_clean["importe"] = df_clean["debe"] - df_clean["haber"]

    #Rename de columnas
    df_clean = df_clean.rename(columns={"cuenta" : "cod_cuenta", 
                                "desccta" : "nombre_cuenta", 
                                "scosto" : "sucursal", 
                                "ccosto" : "centro_costo",
                                "descneg" : "nombre_negocio", 
                                "idsector" : "id_sector", 
                                "codsect" : "cod_sector",
                                "descset" : "nombre_sector",
                                "Mes" : "mes",
                                "Año" : "año",
                                "Archivo Origen" : "archivo_origen"})
    
    #Agregar columnas del archivo que clasifica las cuentas contables
    df_clean = df_clean.merge(
    df_dim,
    on="cod_cuenta",
    how="left",
    )

    #Agregar nombre de los centros de costos
    df_clean = df_clean.merge(
    df_cc,
    on="centro_costo",
    how="left",
    )

    #Validacion de cuentas sin clasificacion
    if df_clean["Clasif"].isna().sum() > 0:
        print(f"El archivo que clasifica las cuentas debe ser actualizado. Cuentas sin clasificar: {df_clean.loc[df_clean["Clasif"].isna(), "cod_cuenta"].unique()}")
        exit()

    #Validacion de cuentas sin clasificacion por cc
    if df_clean["nombre_cc"].isna().sum() > 0:
        print(f"El archivo que clasifica el centro de costo debe ser actualizado. Cuentas sin clasificar: {df_clean.loc[df_clean["nombre_cc"].isna(), "centro_costo"].unique()}")
        #exit()

    #Se excluyen cuentas de ingreso para evitar distorsión en el análisis de gastos (Pareto, desvíos, outliers)
    df_clean = df_clean[~df_clean["cod_cuenta"].isin(cuentas_ingreso)].copy()
    

    df_clean_ruta = ROOT / "Analisis_gastos" / "data" / "processed" / "mayor_analisis.csv"

    if df_clean_ruta.exists():
        df_mayor = pd.read_csv(df_clean_ruta)
        df_mayor = pd.concat([df_mayor, df_clean])
        df_mayor.to_csv(
        df_clean_ruta,
        index=False
        )
    else:
        df_clean.to_csv(
        df_clean_ruta,
        index=False
        )

if mayores.exists():
    df_raw, df_raw_ruta = lectura_csv()
    if not df_raw.empty:
        limpieza_csv(df_raw)
else:
    print(f"\nLos datos ingresados son incorrectos | Mes: {mes} | Año: {anio}. O la carpeta mensual de csv, no existe")
    exit()



