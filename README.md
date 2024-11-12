# Sistema Distribuído com Algoritmo de Exclusão Mútua com Token

## Descrição do Projeto

Este projeto implementa um sistema distribuído utilizando o conceito de Algoritmo de Exclusão Mútua com Token. Nesta técnica, um "token" circula entre os processos, permitindo que apenas o processo que possui o token acesse o recurso crítico. Quando um processo termina sua tarefa, o token é passado para o próximo processo na fila.

## Estrutura do Projeto

O projeto é composto por dois arquivos principais:

- `cliente.py`: Implementa os processos clientes que solicitam acesso ao recurso compartilhado.
- `servidor.py`: Implementa o processo servidor que gerencia todos os tokens.

## Funcionalidades

### Servidor

O servidor é responsável por:

- Gerenciar a fila de processos que solicitam o token.
- Enviar o token para o próximo processo na fila quando o token é liberado.
- Monitorar teclas para fechar conexões ou reiniciar o servidor.

### Cliente

Os clientes são responsáveis por:

- Solicitar o token ao servidor para acessar o recurso compartilhado.
- Atualizar o status do cliente e exibir na tela.
- Liberar o token após o uso do recurso compartilhado.

## Recurso Compartilhado

O recurso compartilhado neste sistema é representado pelo contador e contador de espera, que são atualizados pelos clientes ao receber e liberar o token.

## Como Executar

### Requisitos

- Python 3.x
- Bibliotecas: `socket`, `threading`, `queue`, `keyboard`, `os`, `time`

### Passos para Execução

1. **Iniciar o Servidor:**

   Execute o arquivo `servidor.py`:

   ```sh
   python servidor.py
   ```

2. **Iniciar os Clientes:**

   Execute o arquivo `cliente.py`:

   ```sh
   python cliente.py
   ```

   O script cliente.py iniciará múltiplos clientes que solicitarão o token ao servidor.

## Estrutura do Código

### Servidor

- iniciar_servidor: Inicia o servidor e aceita conexões dos clientes.
- gerenciar_token: Gerencia as solicitações de token dos clientes.
- enviar_token: Envia o token para o próximo cliente na fila.
- monitorar_teclas: Monitora teclas para fechar conexões ou reiniciar o servidor.
- fechar_conexoes: Fecha todas as conexões ativas.
- reiniciar_servidor: Reinicia o servidor.

### Cliente

- solicitar_token: Solicita o token ao servidor.
- atualizar_status: Atualiza o status do cliente.
- atualizar_tela: Atualiza a tela com o status dos clientes.
- iniciar_cliente: Inicia o cliente e cria threads para solicitar token e atualizar status.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções para este projeto. Para isso, faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a MIT License.
