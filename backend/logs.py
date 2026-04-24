from backend.database import conectar
from datetime import datetime


def registrar_log(
    registros_lidos,
    registros_validos,
    registros_invalidos,
    inseridos,
    duplicados,
    status
):

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
    INSERT INTO log_carga_pacientes (
        data_execucao,
        registros_lidos,
        registros_validos,
        registros_invalidos,
        inseridos,
        duplicados,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        datetime.now(),
        int(registros_lidos),
        int(registros_validos),
        int(registros_invalidos),
        int(inseridos),
        int(duplicados),
        str(status)
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()