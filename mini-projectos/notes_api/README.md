## API para Bloco de Notas

Pequena API criada para criação de anotações, com rotas para **adicionar, modificar, apagar, importar e exportar** notas.

### Rotas

- **/notas** 
  - **GET**: Retorna todas as notas.
  - **POST**: Adiciona uma nova nota.
  
- **/notas/:id**
  - **GET**: Retorna uma nota específica.
  - **PUT**: Modifica uma nota existente.
  - **DELETE**: Apaga uma nota.

- **/notas/:id/export**
  - **GET**: Exporta uma nota específica.

- **/notas/import**
  - **POST**: Importa notas a partir de um arquivo CSV.

### Exemplo de Uso

1. **Adicionar uma nova nota**
   
   ```json
   POST /notas
   
   {
       "note_title": "Título da Nota",
       "note_content": "Conteúdo da Nota"
   }
2. **Ver todas as notas**
    ```json
    GET /notas
3. **Ver uma nota específica**
    ```json
    GET /notas/:id
4. **Modificar uma nota existente**
    ```json
    PUT /notas/:id

    {
        "note_title": "Novo Título",
        "note_content": "Novo Conteúdo"
    }
5. **Apagar uma nota**
    ```json
    DELETE /notas/:id

6. **Exportar uma nota específica**
    ```json
    GET /notas/:id/export

7. **Importar notas a partir de um arquivo CSV**
    ```json
    POST /notas/import

    {
        "file": "nome_do_arquivo.csv"
    }
## Executar o Projeto
1. **Execute o arquivo notes_app.py:**
    ```bash
    python app/notes_app.py

## Teste de API
O arquivo api_endpoints_test.py contém testes para as rotas da API. Execute o arquivo para testar a API:

    ```bash
    python app/tests/api_endpoints_test.py