#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import json


def read_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        contenido = file.read()

    return contenido


def main():
    """
    Script de ejemplo para transformar un CSV de métricas individuales (evento a evento)
    a un CSV agregado por jugador y partido, con columnas resumidas y calculadas por 90 minutos.

    Ejecución:
        python transformar.py ruta/entrada.csv ruta/salida.csv
    """

    config = json.loads(read_file("./config.json"))

    if len(sys.argv) < 3:
        print("Uso: python transformar.py <archivo_entrada.csv> <archivo_salida.csv>")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    # -------------------------------------------------------------------------
    # 1. Lectura del CSV de entrada
    # -------------------------------------------------------------------------
    df = pd.read_csv(archivo_entrada, low_memory=False)

    # -------------------------------------------------------------------------
    # 2. Definir las columnas clave para agrupar.
    #    Ajusta según tus datos reales (por ejemplo 'Posición especifica' si es relevante).
    # -------------------------------------------------------------------------
    columnas_agrupacion = config["columnas_agrupacion"]

    # -------------------------------------------------------------------------
    # 3. Definir cuáles columnas se van a sumar directamente y mapearlas
    #    al nombre final que deseas en el CSV de salida.
    #
    #    Por ejemplo, para "1v1D+", en el CSV de entrada puede llamarse igual
    #    y queremos que también se llame igual en el CSV final.
    #
    #    Ajusta según tus columnas reales de tu CSV de origen.
    # -------------------------------------------------------------------------
    # Estas columnas se sumarán en el groupby:
    columnas_a_sumar = config["columnas_a_sumar"]

    # -------------------------------------------------------------------------
    # 4. Crear columna "PERDIDAS" como la suma de las tres sub-columnas.
    #    Ajusta si la lógica es distinta (p.ej. si algunas no se suman).
    # -------------------------------------------------------------------------
    # Para evitar problemas en caso de que no existan las columnas o estén vacías,
    # nos aseguramos de convertirlas a numéricas con fillna(0).
    for col in ["PERDIDAS: xControl", "PERDIDAS: xGambeta", "PERDIDAS: xPase"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["PERDIDAS"] = (
        df["PERDIDAS: xControl"] + df["PERDIDAS: xGambeta"] + df["PERDIDAS: xPase"]
    )

    # También queremos sumar PERDIDAS en el groupby final
    columnas_a_sumar["PERDIDAS"] = "PERDIDAS"

    # -------------------------------------------------------------------------
    # 5. Nos aseguramos de convertir a numérico las columnas que deban sumarse
    #    (a veces vienen como string o floats con comas, etc.).
    # -------------------------------------------------------------------------
    for col_in, col_out in columnas_a_sumar.items():
        df[col_in] = pd.to_numeric(df[col_in], errors="coerce").fillna(0)

    # -------------------------------------------------------------------------
    # 6. Construir el diccionario de agregaciones para el groupby
    # -------------------------------------------------------------------------
    agg_dict = {col_in: "sum" for col_in in columnas_a_sumar.keys()}

    # -------------------------------------------------------------------------
    # 7. Realizar el groupby y la sumatoria de las columnas numéricas.
    #    Esto agrupa por Jugador+Rival+DNI+División+Posición especifica
    # -------------------------------------------------------------------------
    df_grouped = df.groupby(columnas_agrupacion, as_index=False).agg(agg_dict)

    # -------------------------------------------------------------------------
    # 8. Calcular las columnas por 90 minutos para cada métrica que lo requiera.
    #
    #    Ejemplo: "1v1D+ por 90" = (1v1D+ / Minutos Jugados) * 90
    #    Ajusta según tus necesidades reales.
    # -------------------------------------------------------------------------
    # Lista (ordenada) de columnas a las que les calcularemos el "por 90"
    columnas_por_90 = config["columnas_por_90"]

    # Creamos las nuevas columnas "por 90" en el DataFrame resultante
    df_grouped["Minutos Jugados"] = df_grouped["Minutos Jugados"].replace(
        0, 0.00001
    )  # Para evitar dividir por cero

    for col in columnas_por_90:
        col_90 = f"{col} por 90 minutos"
        df_grouped[col_90] = (df_grouped[col] / df_grouped["Minutos Jugados"]) * 90

    # -------------------------------------------------------------------------
    # 9. Opcional: Crear la columna "DNI por 90 minutos"
    #    (Esto es un ejemplo ficticio; normalmente el DNI no se calcula "por 90".)
    #    Si no lo necesitas, quítalo.
    # -------------------------------------------------------------------------
    df_grouped["DNI por 90 minutos"] = (
        df_grouped["DNI"] / df_grouped["Minutos Jugados"]
    ) * 90

    # -------------------------------------------------------------------------
    # 10. Ordenar las columnas en el formato final deseado
    #     (solo un ejemplo de orden; ajústalo a tus requerimientos).
    # -------------------------------------------------------------------------
    columnas_finales = config["columnas_finales"] + [
        f"{c} por 90 minutos" for c in columnas_por_90
    ]

    # Nos aseguramos de que las columnas existan (puede que alguna no exista en el input)
    columnas_finales_presentes = [
        c for c in columnas_finales if c in df_grouped.columns
    ]

    # Reordenamos
    df_final = df_grouped[columnas_finales_presentes].copy()

    # -------------------------------------------------------------------------
    # 11. Guardar el CSV de salida
    # -------------------------------------------------------------------------
    df_final.to_csv(archivo_salida, index=False, encoding="utf-8-sig")
    print(f"Archivo transformado y guardado en: {archivo_salida}")


if __name__ == "__main__":
    main()
