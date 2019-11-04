#Este codigo se destina a armazenar uma sequência de strings de entrada em um único arquivo de texto

message = ''
#Aqui entra um processo onde uma sequência de inputs, na forma de strings, é fornecida

message = message + new + '\n'
#Cada novo input recebido deve ser acrescido a uma única string, seguida de uma quebra de linha

log = open('message_log.txt', a+)
#Cria-se um novo arquivo 'message_log.txt', caso ele não exista, e o abre em modo append

log.write(message)
log.close()
#Escrevem-se todas as mensagens e fecha-se o arquivo
