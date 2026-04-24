from backend.database import conectar
from datetime import datetime


def salvar_historico_paciente(cpf):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    # dados atuais do paciente

    sql_busca = """
    SELECT id, nome, cpf, data_nascimento,
           sexo, telefone, email
    FROM pacientes
    WHERE cpf = %s
    """

    cursor.execute(sql_busca, (cpf,))
    paciente = cursor.fetchone()

    if paciente:

        sql_insert = """
        INSERT INTO pacientes_historico (
            paciente_id,
            nome,
            cpf,
            data_nascimento,
            sexo,
            telefone,
            email,
            data_alteracao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            paciente["id"],
            paciente["nome"],
            paciente["cpf"],
            paciente["data_nascimento"],
            paciente["sexo"],
            paciente["telefone"],
            paciente["email"],
            datetime.now()
        )

        cursor.execute(sql_insert, valores)

        conexao.commit()

    cursor.close()
    conexao.close()