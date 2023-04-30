import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `meusboletos`;")

cursor.execute("CREATE DATABASE `meusboletos`;")

cursor.execute("USE `meusboletos`;")

# criando tabelas
TABLES = {}
TABLES['Boletos'] = ('''
      CREATE TABLE `boletos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `descricao` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `valor` decimal(8,2) NOT NULL,
      `data_vencimento` date NOT NULL,
      `data_pagamento` date,
      `situacao` varchar(20) NOT NULL,
      `codigo_boleto` varchar(48) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
