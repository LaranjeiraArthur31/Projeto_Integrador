# Projeto_Integrador
================================================================================
                          SISTEMA HELP DESK - README
================================================================================

  Versão : 1.0
  Linguagem: Python 3
  Banco de Dados: MySQL

================================================================================
  DESCRIÇÃO DO PROJETO
================================================================================

  Sistema de gerenciamento de chamados (Help Desk) desenvolvido em Python com
  banco de dados MySQL. Permite abrir, acompanhar e encerrar tickets de suporte,
  além de calcular a prioridade do chamado automaticamente com base na urgência
  e no impacto informados pelo usuário.

================================================================================
  ARQUIVOS DO PROJETO
================================================================================

  BancodeDados.sql         → Script SQL para criação e populacao do banco de dados
  Menu.py                  → Arquivo principal com o menu interativo do sistema
  Regra_de_Prioridade.py   → Módulo de abertura de chamado com cálculo automático
                             de prioridade

================================================================================
  ESTRUTURA DO BANCO DE DADOS
================================================================================

  Tabelas:
  --------
  usuarios          → Cadastro de usuários do sistema
                      (id, nome, email, empresa)

  categorias        → Tipos de problema
                      Dados iniciais: TI, RH, Financeiro, Administrativo

  prioridades       → Níveis de prioridade
                      Dados iniciais: Baixa, Média, Alta

  status            → Estados do ticket
                      Dados iniciais: Aberta, Em andamento, Fechada

  tickets           → Registros dos chamados abertos
                      (id, titulo, descricao, categoria, prioridade,
                       status, usuario_abertura, usuario_responsavel,
                       data_abertura, data_atualizacao, data_fechamento)

  ticket_historico  → Histórico de atualizações de cada ticket
                      (id, ticket_id, status, comentario, data)

================================================================================
  REQUISITOS E INSTALAÇÃO
================================================================================

  1. Python 3.8 ou superior instalado
     Download: https://www.python.org/downloads/

  2. Biblioteca mysql-connector-python instalada:
     Execute no terminal:
       pip install mysql-connector-python

  3. Servidor MySQL em execução (local ou remoto)

  4. Configuração da conexão (edite as variáveis no topo dos arquivos .py):
       SERVIDOR = 'endereço_do_servidor'
       USUARIO  = 'seu_usuario_mysql'
       SENHA    = 'sua_senha'
       BD       = 'nome_do_banco'

  5. Execute o script SQL para criar o banco:
       mysql -u seu_usuario -p < BancodeDados.sql

================================================================================
  COMO EXECUTAR O SISTEMA
================================================================================

  Após configurar o banco e instalar as dependências, execute:

    python Menu.py

  O menu principal será exibido no terminal.

================================================================================
                         TUTORIAL DE USO DO SISTEMA
================================================================================

  Ao iniciar o sistema, você verá o menu principal:

    ========================================
             HELP DESK SYSTEM
    ========================================
      1 - Cadastrar usuário
      2 - Abrir ticket
      3 - Listar tickets
      4 - Atualizar status do ticket
      5 - Ver histórico do ticket
      6 - Ver estatísticas
      0 - Sair
    ========================================

--------------------------------------------------------------------------------
  PASSO 1 — CADASTRAR USUÁRIO (Opção 1)
--------------------------------------------------------------------------------

  Antes de abrir qualquer ticket, é necessário cadastrar ao menos um usuário.

  Passos:
    1. No menu, escolha a opção 1
    2. Digite o nome do usuário e pressione Enter
    3. Digite o e-mail do usuário e pressione Enter
    4. Digite a empresa do usuário e pressione Enter
    5. O sistema confirmará o cadastro com o ID gerado

  Exemplo:
    Nome: João Silva
    E-mail: joao@empresa.com
    Empresa: Empresa XPTO
    ✔ Usuário 'João Silva' cadastrado! (ID 1)

--------------------------------------------------------------------------------
  PASSO 2 — ABRIR TICKET (Opção 2)
--------------------------------------------------------------------------------

  Abre um novo chamado de suporte.

  Passos:
    1. No menu, escolha a opção 2
    2. O sistema exibe a lista de usuários cadastrados — informe o ID do usuário
    3. Digite o título do ticket (breve resumo do problema)
    4. Digite a descrição detalhada do problema
    5. O sistema exibe as categorias disponíveis — informe o ID da categoria:
         [1] TI
         [2] RH
         [3] Financeiro
         [4] Administrativo
    6. O sistema exibe as prioridades disponíveis — informe o ID:
         [1] Baixa
         [2] Média
         [3] Alta
    7. O ticket é criado com status "Aberta" automaticamente
    8. O sistema confirma com o número do ticket gerado

  Exemplo:
    ID do usuário: 1
    Título do ticket: Computador não liga
    Descrição do problema: O computador da recepção não está ligando desde hoje.
    ID da categoria: 1   ← TI
    ID da prioridade: 3  ← Alta
    ✔ Ticket #1 criado com sucesso!

  DICA — Cálculo automático de prioridade (Regra_de_Prioridade.py):
    Se utilizar o módulo Regra_de_Prioridade.py, a prioridade é calculada
    automaticamente a partir de dois critérios:

      Urgência (1 a 3): quão rápido o problema precisa ser resolvido
      Impacto  (1 a 3): quantas pessoas ou processos são afetados

      Soma 2 ou menos → Prioridade BAIXA
      Soma 3 ou 4     → Prioridade MÉDIA
      Soma 5 ou 6     → Prioridade ALTA

    Exemplos:
      Urgência 1 + Impacto 1 = 2 → Baixa
      Urgência 2 + Impacto 2 = 4 → Média
      Urgência 3 + Impacto 3 = 6 → Alta

--------------------------------------------------------------------------------
  PASSO 3 — LISTAR TICKETS (Opção 3)
--------------------------------------------------------------------------------

  Exibe todos os tickets cadastrados no sistema em formato de tabela.

  Informações exibidas por ticket:
    - ID
    - Título
    - Usuário que abriu
    - Categoria
    - Prioridade
    - Status atual
    - Data de abertura

  Passos:
    1. No menu, escolha a opção 3
    2. A tabela com todos os tickets é exibida automaticamente

  Os tickets são ordenados do mais recente para o mais antigo (ID decrescente).

--------------------------------------------------------------------------------
  PASSO 4 — ATUALIZAR STATUS DO TICKET (Opção 4)
--------------------------------------------------------------------------------

  Altera o status de um ticket existente e registra um comentário no histórico.

  Passos:
    1. No menu, escolha a opção 4
    2. Informe o ID do ticket que deseja atualizar
    3. O sistema exibe os status disponíveis:
         [1] Aberta
         [2] Em andamento
         [3] Fechada
    4. Informe o ID do novo status
    5. Digite um comentário explicando a atualização (ou pressione Enter para
       usar a mensagem padrão "Status atualizado.")
    6. O sistema confirma a atualização

  Observação: ao selecionar um status do tipo "Fechada", "Resolvida" ou
  "Encerrada", o sistema registra automaticamente a data de fechamento
  do ticket.

  Exemplo:
    ID do ticket: 1
    ID do novo status: 2   ← Em andamento
    Comentário: Técnico acionado, aguardando peça de reposição.
    ✔ Status do ticket #1 atualizado para 'Em andamento'.

--------------------------------------------------------------------------------
  PASSO 5 — VER HISTÓRICO DO TICKET (Opção 5)
--------------------------------------------------------------------------------

  Exibe todas as movimentações e comentários registrados em um ticket.

  Passos:
    1. No menu, escolha a opção 5
    2. Informe o ID do ticket
    3. O histórico completo é exibido em ordem cronológica

  Exemplo de saída:
    ===== Histórico — Ticket #1 =====
      01/06/2025 09:00 | [Aberta] Ticket aberto.
      01/06/2025 14:30 | [Em andamento] Técnico acionado, aguardando peça.
      02/06/2025 10:00 | [Fechada] Problema resolvido com sucesso.
    ========================================

--------------------------------------------------------------------------------
  PASSO 6 — VER ESTATÍSTICAS (Opção 6)
--------------------------------------------------------------------------------

  Exibe um resumo geral dos tickets por status, prioridade e categoria.

  Passos:
    1. No menu, escolha a opção 6
    2. As estatísticas são exibidas automaticamente

  Exemplo de saída:
    ========================================
             ESTATÍSTICAS
    ========================================
      Total de tickets: 10

      Por Status:
        Em andamento         4
        Aberta               4
        Fechada              2

      Por Prioridade:
        Alta                 5
        Média                3
        Baixa                2

      Por Categoria:
        TI                   6
        Financeiro           2
        RH                   1
        Administrativo       1
    ========================================

--------------------------------------------------------------------------------
  OPÇÃO 0 — SAIR
--------------------------------------------------------------------------------

  Encerra o sistema com segurança, fechando a conexão com o banco de dados.

================================================================================
  FLUXO RECOMENDADO DE USO
================================================================================

  1. Execute o script SQL para criar o banco de dados
  2. Inicie o sistema com: python Menu.py
  3. Cadastre os usuários (opção 1)
  4. Abra tickets conforme necessário (opção 2)
  5. Acompanhe e atualize os tickets (opções 3 e 4)
  6. Consulte o histórico para rastreabilidade (opção 5)
  7. Monitore as estatísticas periodicamente (opção 6)

================================================================================
  OBSERVAÇÕES IMPORTANTES
================================================================================

  - O sistema roda inteiramente no terminal (interface de linha de comando)
  - Certifique-se de que o servidor MySQL está acessível antes de iniciar
  - As credenciais de banco de dados ficam nos arquivos .py — recomenda-se
    movê-las para variáveis de ambiente em ambientes de produção
  - O arquivo Regra_de_Prioridade.py pode ser executado de forma independente
    para abrir chamados com cálculo automático de prioridade

================================================================================
