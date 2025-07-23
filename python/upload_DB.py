import csv
import datetime
import logging
import os
import re

import mysql.connector
from dotenv import load_dotenv

logging.basicConfig(
    filename=f"/var/www/StaffNet/logs/Registros_{datetime.datetime.now().year}.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

if not os.path.isfile("/var/env/StaffNet.env"):
    logging.critical(f"The env file was not found", exc_info=True)
    raise FileNotFoundError("The env file was not found.")
else:
    load_dotenv("/var/env/StaffNet.env")

info_tables = {
    "personal_information": {
        "cedula": "Cedula",
        "nombres": "Nombre Completo",
        "apellidos": "Apellidos",
        "tipo_documento": "Tipo de documento",
        "fecha_nacimiento": "Fecha de nacimiento",
        "lugar_expedicion": "Lugar Expedición",
        "fecha_expedicion": "Fecha de expedición",
        "genero": "GENERO",
        "rh": "RH",
        "estado_civil": "ESTADO CIVIL",
        "hijos": "Hijos",
        "personas_a_cargo": "Personas a cargo",
        "estrato": "Estrato",
        "celular": "CELULAR",
        "correo": "Correo",
        "correo_corporativo": "Correo corporativo",
        "direccion": "Dirección",
        "barrio": "Barrio",
        "localidad": "Localidad/Region",
        "contacto_emergencia": "Contacto de emergencia",
        "parentesco": "Parentesco",
        "tel_contacto": "Teléfono de contacto",
        "caso_medico": "Caso medico",
    },
    "educational_information": {
        "cedula": "Cedula",
        "nivel_escolaridad": "Nivel de escolaridad",
        "profesion": "Profesión",
        "estudios_en_curso": "Estudios en curso",
    },
    "employment_information": {
        "cedula": "Cedula",
        "fecha_afiliacion_eps": "Fecha de afiliación",
        "eps": "EPS",
        "cambio_eps_legado": "Cambio EPS legado",
        "pension": "Pension",
        "caja_compensacion": "Caja de Compensacion",
        "cesantias": "Cesantias",
        "cuenta_nomina": "Cuenta nomina",
        "banco": "Banco",
        "sede": "Sede",
        "cargo": "Cargo",
        "fecha_nombramiento": "Fecha de nombramiento",
        "fecha_nombramiento_legado": "Fecha de nombramiento legado",
        "gerencia": "Gerencia",
        "campana_general": "Campaña general",
        "area_negocio": "Area de negocio",
        "tipo_contrato": "Tipo de contrato",
        "fecha_ingreso": "Fecha de ingreso",
        "salario": "Salario",
        "valor_subsidio": "Valor del subsidio",
        "tipo_subsidio": "Tipo de subsidio",
        "rodamiento": "Rodamiento",
        "aplica_teletrabajo": "Aplica para teletrabajo",
        "fecha_aplica_teletrabajo": "Fecha de aplicacion de teletrabajo",
        "talla_camisa": "Talla de camisa",
        "talla_pantalon": "Talla de pantalon",
        "talla_zapatos": "Talla de zapatos",
        "observaciones": "Observaciones",
        "usuario_windows": "Usuario de Windows",
    },
    "disciplinary_actions": {
        "cedula": "Cedula",
        "memorando_1": "MEMORANDO 1",
        "memorando_2": "MEMORANDO 2",
        "memorando_3": "MEMORANDO 3",
    },
    "leave_information": {
        "cedula": "Cedula",
        "fecha_retiro": "Fecha de retiro",
        "tipo_retiro": "Tipo de retiro",
        "motivo_retiro": "Motivo del retiro",
        "aplica_recontratacion": "Aplica para recontratacion",
        "estado": "Estado",
    },
}

connection = mysql.connector.connect(
    host="172.16.0.118",
    user="StaffNetuser",
    password=os.environ["StaffNetmysql"],
    # host="172.16.0.115",
    # user="root",
    # password=os.environ["MYSQL_115"],
    database="staffnet",
)

cursor = connection.cursor()

file_path = "/var/www/StaffNet/python/BASE DE DATOS DIAN  CYC SERVICES FINAL STAFF CARGUE MASIVO.csv"


# Function to split last and first names
def split_name(name):
    parts = name.split()
    last_names = " ".join(parts[:-2])  # Everything except the last two parts
    first_names = " ".join(parts[-2:])  # The last two parts
    return last_names, first_names


with open(file_path, "r", encoding="utf-8-sig") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=";")
    for row in csv_reader:
        last_names, first_names = split_name(row["Nombre Completo"])
        row["Nombre Completo"] = first_names
        row["Apellidos"] = last_names
        # Iterate over each table in the JSON object
        for table, column_mapping in info_tables.items():
            column_values = {}
            for column, mapping in column_mapping.items():
                row[mapping] = row[mapping].upper().strip()
                if column in [
                    "",
                    "fecha_nacimiento",
                    "fecha_afiliacion_eps",
                    "fecha_ingreso",
                    "fecha_salida_vacaciones",
                    "fecha_ingreso_vacaciones",
                    "fecha_retiro",
                    "fecha_expedicion",
                    "fecha_aplica_teletrabajo",
                    "fecha_nombramiento",
                ]:
                    date_string = row[mapping]
                    if date_string in ["#N/D", "", " ", "NO", "0/01/1900", "N/A"]:
                        formatted_date = None
                        if column in ["fecha_nacimiento"]:
                            formatted_date = "1000-01-01"
                        parsed_string = None
                    # if parsed_string is list:
                    #     result_string = ", ".join(parsed_string)
                    elif re.search(r"//", date_string):
                        date_string = re.sub(r"/{2,}", "/", date_string)
                        date_object = datetime.datetime.strptime(
                            date_string, "%d/%m/%Y"
                        )
                        formatted_date = date_object.strftime("%Y-%m-%d")
                    elif len(date_string) > 10:
                        formatted_date = date_string
                    else:
                        date_object = datetime.datetime.strptime(
                            date_string, "%d/%m/%Y"
                        )
                        formatted_date = date_object.strftime("%Y-%m-%d")
                    column_values[column] = formatted_date
                elif column in [
                    "fecha_nombramiento",
                    "legado_historico",
                    "cambio_eps_legado",
                ]:
                    column_values[column] = row[mapping]
                elif column in [
                    "salario",
                    "tel_fijo",
                    "valor_subsidio",
                    "dias_utilizados",
                    "personas_a_cargo",
                    "hijos",
                    "estrato",
                    "edad",
                    "cedula",
                ]:
                    integer = row[mapping]
                    integer = re.sub(r"\D", "", integer)
                    if integer in [
                        "",
                        "SIN INFORMACIÓN",
                        "933420000000000",
                        " $ - ",
                    ]:
                        integer = None
                        if column in ["personas_a_cargo", "hijos"]:
                            integer = 0
                        elif column in ["estrato"]:
                            integer = None
                    if column == "dias_utilizados" and integer is not None:
                        integer = int(integer) * 15
                    if integer is not None:
                        try:
                            integer = int(integer)
                        except:
                            integer = None
                    column_values[column] = integer
                elif column in ["lugar_expedicion"]:
                    texto = row[mapping]
                    if texto in ["", "SIN INFORMACIÓN"]:
                        texto = None
                    elif texto == "BOGOTÁ D.C." or texto == "BOGOTA DC":
                        texto = "BOGOTA"
                    column_values[column] = texto
                elif column in ["estado"]:
                    estado = row[mapping]
                    if estado == "ACTIVO":
                        estado = 1
                    elif estado == "RETIRADO":
                        estado = 0
                    column_values[column] = estado
                elif column == "LLAMADO DE ATENCIÓN":
                    query = "INSERT INTO disciplinary_actions (cedula, falta, tipo_sancion, sancion,fecha_faltas) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        query,
                        (
                            row["cedula"],
                            row["LLAMADO DE ATENCIÓN"],
                            None,
                            None,
                            None,
                        ),
                    )
                elif column == "MEMORANDO 1":
                    query = "INSERT INTO disciplinary_actions (cedula, falta, tipo_sancion, sancion,fecha_faltas) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        query, (row["cedula"], row["MEMORANDO 1"], None, None, None)
                    )
                elif column == "MEMORANDO 2":
                    query = "INSERT INTO disciplinary_actions (cedula, falta, tipo_sancion, sancion,fecha_faltas) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        query, (row["cedula"], row["MEMORANDO 2"], None, None, None)
                    )
                elif column == "MEMORANDO 3":
                    query = "INSERT INTO disciplinary_actions (cedula, falta, tipo_sancion, sancion,fecha_faltas) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(
                        query, (row["cedula"], row["MEMORANDO 3"], None, None, None)
                    )
                elif column == "tipo_retiro":
                    texto = row[mapping]
                    if texto in ["", "SIN INFORMACIÓN", "0"]:
                        texto = None
                    column_values[column] = texto
                elif column == "motivo_retiro":
                    texto = row[mapping]
                    if texto.find("-") != -1:
                        texto = texto.split("-")[1].strip()
                    if texto.find(" Y ") != -1:
                        texto = texto.split(" Y ")[0].strip()
                    if texto.find("/") != -1:
                        texto = texto.split("/")[0].strip()
                    if texto.find("–") != -1:
                        texto = texto.split("–")[0].strip()
                    if texto.find(",") != -1:
                        texto = texto.split(",")[0].strip()
                    if texto.startswith("RENUNCIA"):
                        texto = texto.split("RENUNCIA")[1].strip()
                    if texto.find(" E ") != -1:
                        texto = texto.split(" E ")[0].strip()
                    if texto in [
                        "INCOMPATIBIIDAD CON EL JEFE",
                        "MALA RELACION CON EL JEFE",
                        "INCOMPATIBILIDAD CON JEFE",
                        "MOTIVADA MAL RELACIONAMIENTO CON EL JEFE",
                    ]:
                        texto = "INCOMPATIBILIDAD CON EL JEFE"
                    if texto in [
                        "SENA",
                        "REGLAMENTO DE APRENDICES",
                        "TERMINACION CONTRATO DE APRENDIZAJE",
                        "TERMINACIÓN CONTRATO APRENDIZAJE",
                        "TERMINACIÓN CONTRATO DE APRENDIZAJE",
                        "TERMINACIÓN DE CONTRATO APRENDIZAJE",
                        "TERMINACIÓN DE CONTRATO DE APRENDIZAJE",
                        "TERMINACIÓN DE CONTRATO POR PERIODO DE PRUEBA",
                        "TERMINACIÓN UNILATERAL SENA",
                        "REGLAMENTO DE APRENDICES",
                        "TERMINACIÓN DE CONTRATO APRENDIZAJE",
                    ]:
                        texto = "TERMINACIÓN DE CONTRATO SENA"
                    elif texto in ["CAMBIO DE ACTIVIDA"]:
                        texto = "CAMBIO DE ACTIVIDAD"
                    elif texto in [
                        "NO HAY OPORTUNIDADES DE CRECIMIENTO",
                        "NO HAY OPORTUNIDA DE CRECIMIENTO",
                        "NO HAY OPORTUNIDADESS DE CRECIMIENTO",
                        "NO OPORTUNIDAD DE CRECIMIENTO",
                    ]:
                        texto = "NO HAY OPORTUNIDAD DE CRECIMIENTO"
                    elif texto in [
                        "OTRA ODERTA LABORAL",
                        "OTRA OFERTA",
                        "OTRA OFERTA LOBORAL",
                        "OTRA OFERLA LABORAL",
                    ]:
                        texto = "OTRA OFERTA LABORAL"
                    elif texto in [
                        "POR SALUD",
                        "POR VENTAS",
                        "TRATAMIENTO MÉDICO",
                        "QUERIA UN RECESO PARA DESCANSAR",
                        "RECOMENDACION MEDICA",
                        "DEDICARSE A SU SALUD",
                        "POR MOTIVOS DE SALUD",
                        "PROBLEMAS DE SALUD",
                        "SALUD",
                        "DE SALUD",
                    ]:
                        texto = "MOTIVOS DE SALUD"
                    elif texto in [
                        "PROBLEMAS PERSONALES",
                        "PROYECTO PERSONALES",
                        "NEGOCIO PROPIO",
                        "CALAMIDAD DOMÉSTICA",
                        "CALAMIDAD FAMILIAR",
                        "HOSPITALIZACION PADRES",
                        "MOTIVOS PERSONAS",
                        "MOTIVO FAMILAR",
                        "MOTIVOS FAMILIARES",
                        "MOTIVOS PERSONAL",
                        "MOTIVO PERSONAL",
                        ". MOTIVOS PERSONALES",
                        "PROBLEMAS PERSONALES CON CC",
                        "POR MOTIVOS PERSONALES",
                        "PROYECTOS PERSONALES",
                        "POR PROBLEMAS PERSONALES",
                    ]:
                        texto = "MOTIVOS PERSONALES"
                    elif texto in [
                        "VIAJE FAMILIAR",
                        "TRASLADARSE",
                        "SALIDA DEL PAIS",
                        "MOTIVOSDE VIAJE",
                        "MOTIVO DE VIAJE",
                        "VIAJE",
                        "POR MOTIVOS DE VIAJE",
                        "VIAJE PERSONAL",
                        "VIAJE AL EXTERIOR",
                        "MOTIVOS DE VIAJE",
                        "POR MOTIVO DE VIAJE",
                    ]:
                        texto = "SE VA DE LA CIUDAD"
                    elif texto in [
                        "POR DESPLAZAMIENTO",
                        "DESPLAZAMINTO",
                        "DESPLAZAMIENTO",
                    ]:
                        texto = "TRANSPORTE"
                    elif texto in [
                        "HORARIO DE ESTUDIO",
                        "HORARIOS CON SU HIJO",
                        "HORARIO",
                        "HORARIOS LABORALES",
                        "HORARIO LABORAL",
                    ]:
                        texto = "MOTIVOS DE HORARIO"
                    elif texto in ["MAL CLIMA LABORAL", "MAL AMBIENTE"]:
                        texto = "MAL AMBIENTE LABORAL"
                    elif texto in [
                        "NO HAY OPORTUNIDAD DE CRECIMIENTO LABORAL",
                        "NO HAY OPORTUNIDADES DE CRECIMIENTO LABORAL",
                    ]:
                        texto = "NO HAY OPORTUNIDAD DE CRECIMIENTO"
                    elif texto in [
                        "MEJOR OFERTA",
                        "OTRA LABORAL",
                        "MEJOR ORFERTA LABORAL",
                        "MOTIVOS CAMBIO DE LABOR",
                        "OFERTA LABORAL",
                        "OTRA OFERTA LABORAL",
                    ]:
                        texto = "MEJOR OFERTA LABORAL"
                    elif texto in [
                        "ABANDONO",
                        "MANIFESTO NO CONTINUAR",
                        "ABANDONO DE CARGO",
                        "TERMINACIÓN POR ABANDONO DE PUESTO",
                        "TERMINACIÓN ABANDONO DE CARGO",
                        "ABANDONO DE PUESTO",
                        "NO SE VOLVIÓ A REPORTAR A SU LUGAR DE TRABAJO",
                        "NO VOLVIO A SU LUGAR DE TRABAJO",
                        "NO VOLVIO CAMBIO DE CIUDAD",
                        "TERMINACION DE CONTRATO POR ABANDONO DE PUESTO",
                    ]:
                        texto = "TERMINACIÓN DE CONTRATO POR ABANDONO DE PUESTO"
                    elif texto in [
                        "OBRA",
                        "TÉRMINO DEFINIDO",
                        "TERMINACION DE CONTRATO TIEMPO PACTADO",
                        "OBRA O LABOR CONTRATADA",
                        "TERMINACION POR OBRA LABOR CONTRATADA",
                        "TERMINACIÓN DE CONTRATO POR OBRA LABOR",
                        "TERMINACIÓN DE CONTRATO POR OBRA O LABOR",
                        "TERMINACIÓN POR OBRA LABOR CONTRATADA",
                        "TERMINACION POR OBRA LABOR CONTRATADA",
                        "TERMINACION DE CONTRATO POR OBRA O LABOR",
                        "TERMINACION DE OBRA O LABOR CONTRATADA",
                        "OBRA O LABOR",
                        "TERMINACION POR OBRA O LABOR CONTRATADA",
                        "TERMINACIÒN DE CONTRATO POR OBRA O LABOR",
                        "TERMINACIÓN CONTRATO OBRA LABOR",
                        "TERMINACIÓN CONTRATO OBRA O LABOR",
                        "TERMINACIÓN DE CONTRATO OBRA LABOR",
                        "TERMINACIÓN OBRA O LABOR",
                        "TERMINACIÓN DE OBRA O LABOR CONTRATADA",
                        "TERMINACIÓN POR OBRA O LABOR CONTRATADA",
                        "TERMINACION OBRA O LABOR CONTRATADA",
                        "TERMINACION DE CONTRATO DE OBRA LABOR",
                    ]:
                        texto = f"TERMINACIÓN DE CONTRATO DE OBRA O LABOR"
                    elif texto in [
                        "SIN JUSTA CAUSA",
                        "TERMINACION DE CONTRATO SIN JUSTA CAUSA",
                        "TERMINACIÓN SIN JUSTA CAUSA",
                        "TERMINACIÓN CONTRATO SIN JUSTA CAUSA",
                        "TERMINACION SIN JUSTA CAUSA",
                        "TERMINACION DE CONTRATRO SIN JUSTA CAUSA",
                    ]:
                        texto = "TERMINACIÓN DE CONTRATO SIN JUSTA CAUSA"
                    elif texto in [
                        "JUSTA CAUSA",
                        "TERMINACIÓN DE CONTRATO JUSTA CAUSA",
                        "TERMINACIÓN DE CONTRATO DE JUSTA CAUSA",
                        "CON JUSTA CAUSA",
                        "TERMINACIÓN CONTRATO LABORAL CON JUSTA CAUSA",
                        "TERMINACIÓN CONTRATO CON JUSTA CAUSA",
                        "TERMINACIÓN CON JUSTA CAUSA",
                        "TERMINACION DE CONTRATO CON JUSTA CAUSA",
                        "TERMINACION CONTRATO CON JUSTA CAUSA",
                        "TERMINACIO DE CONTRATO CON JUSTA CAUSA",
                    ]:
                        texto = "TERMINACIÓN DE CONTRATO CON JUSTA CAUSA"
                    elif texto in [
                        "POR PERIODO DE PRUEBA",
                        "TERMINACIÓN POR PERIODO DE PRUEBA",
                        "TERMINACIÓN PERIODO DE PRUEBA",
                        "TERMINACIÓN DE CONTRATO PERIODO DE PRUEBA",
                        "TERMINACIÓN DE CONTRARO POR PERIODO DE PRUEBA",
                        "TERMINACIÓN CONTRATO PERIODO DE PRUEBA",
                        "TERMINACIÓN CONTRATO DE TRABAJO DE PERIODO DE PRUEBA",
                        "TERMINACION PERIODO DE PRUEBA",
                        "TERMINACION DE CONTRATO POR PERIODO DE PRUEBA",
                        "TERMINACION DE CONTRATO PERIODO DE PRUEBA",
                        "PERIODO DE PRUEBA",
                    ]:
                        texto = "TERMINACIÓN DE CONTRATO POR PERIODO DE PRUEBA"
                    elif texto in [
                        "NO HAY OPORTUNIDAD DE ESTUDIAR",
                        "FORMACIÓN ACADÉMICA",
                        "PRACTICAS",
                        "PROYECTOS EN LA CARRERA",
                        "POR ESTUDIOS",
                        "OPORTUNIDAD DE ESTUDIO",
                        "NO HAY POSIBILIDADES DE ESTUDIAR",
                        "NO HAY OPORTUNIDADES DE ESTUDIAR",
                        "POR MOTIVOS DE ESTUDIO",
                        "POR ESTUDIO",
                        "ESTUDIOS FUERA DEL PAIS",
                        "ESTUDIOS",
                        "ESTUDIO",
                        "NO HAY OPORTUNIDADES DE ESTUDIAR",
                    ]:
                        texto = "MOTIVOS DE ESTUDIO"
                    elif texto in ["", "SIN INFORMACION", "VOLUNTARIO", "0"]:
                        texto = None
                    column_values[column] = texto
                else:
                    if row[mapping] in [
                        "Gerencia de Recursos fisicos",
                        "Recursos Fisicos",
                    ]:
                        row[mapping] = "Recursos Físicos "
                    elif row[mapping] in ["Analista Gestión Humana"]:
                        row[mapping] = "Analista de Gestión Humana"
                    elif row[mapping] in [
                        "",
                        "",
                        " ",
                        "N/A",
                        0,
                        "0",
                        "SIN INFORMACION",
                        "SIN INFORMACIÓN",
                    ]:
                        row[mapping] = None
                    elif row[mapping] in ["Analista Juridico"]:
                        row[mapping] = "Analista Jurídico"
                    elif row[mapping] in ["Director(a) de Investigación "]:
                        row[mapping] = "Director(a) de Investigaciones"
                    column_values[column] = row[mapping]
            column_names = ", ".join(column_values.keys())
            placeholders = ", ".join(["%s"] * len(column_values))
            update_columns = ", ".join(
                [f"{column} = VALUES({column})" for column in column_values]
            )
            query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_columns}"
            try:
                print(query, tuple(column_values.values()))
                cursor.execute(query, tuple(column_values.values()))
            except Exception as e:
                logging.error(f"Error inserting row into {table} table, error: ", e)
                raise Exception(f"Error inserting row into {table} table, error: ", e)

# Commit the changes and close the cursor and connection
try:
    connection.commit()
    print("Subida exitosa!")
    cursor.close()
    connection.close()
except Exception as e:
    logging.error(
        f"Error committing changes and closing cursor and connection, error: ", e
    )
    print(e)
