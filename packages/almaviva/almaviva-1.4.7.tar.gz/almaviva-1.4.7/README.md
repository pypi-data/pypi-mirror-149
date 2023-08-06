# Almaviva | Biblioteca Python
> Biblioteca Python Almaviva com funções personalizadas para uso geral (pip install almaviva)

## Executando o programa

- Para usar esta biblioteca, basta instalar via PIP e posteriormente realizar a importação para dentro do código-fonte do seu projeto.

    ```shell
    pip install almaviva
    ```

- Para instalar a biblioteca na versão anteriormente publicada, acrescente "==1.1.0" na frente do nome do pacote que está instalando, ex.:

    ```shell
    pip install almaviva==1.4.7
    ```

- Para instalar a biblioteca do repositório de testes do PyPI, execute:

    ```shell
    pip install -i https://test.pypi.org/simple/ almaviva
    ```

### Ambiente virtual

- Para criar a máquina virtual, caso não tenha sido criado a pasta ``.venv`` por parte do download do template python (tutorial acima), vá até a pasta que contém os arquivos deste projeto e execute, no PowerShell:

    ```shell
    python -m venv .venv --clear;
    .venv/scripts/activate;
    ```

- Para que os passos acima sejam executados com sucesso, será necessário revisar a política de execução do scripts do PowerShell (no modo de administrador). Então, execute, no PowerShell:

    ```shell
    Get-ExecutionPolicy -List
    ```

- Caso ``Scope ExecutionPolicy`` no item ``LocalMachine`` esteja diferente de ``Remotesigned``, execute, no PowerShell:

    ```shell
    Set-ExecutionPolicy -ExecutionPolicy Remotesigned -Scope LocalMachine
    ```

### Modo de operação do módulo: Database

#### Importação da biblioteca

Realize a importação para dentro do código-fonte do seu projeto

```py
from almaviva.database import Database
```

#### Manipulando banco de dados

1. Crie a conexão com o servidor e informe o nome do banco de dados principal

    Configurando a conexão usando autenticação windows (trusted connection):
    
    ```py
    server = '__servidor__'     # Ex.: r'servidor1\instancia1'
    database = '__banco__'      # Ex.: 'Assets'
    db = Database (
        server
    ,   database
    )
    db.connect()
    ```

    Configurando a conexão usando autenticação de usuário:
    
    ```py
    server = '__servidor__'     # Ex.: r'servidor1\instancia1'
    database = '__banco__'      # Ex.: 'Assets'
    username = '__usuario__'    # Ex.: 'User1'
    password = '__senha__'      # Ex.: 'Senha1'
    db = Database (
        server
    ,   database
    ,   username
    ,   password
    )
    db.connect ()
    ```

    Opcionamente podemos configurar a versão do ``driver`` que está instalado no sistema operacional, adicionando a configuração abaixo. Por padrão, se não informando ``driver=None`` é utilizado ``ODBC Driver 13 for SQL Server``

    ```py
    driver='ODBC Driver 13 for SQL Server'
    db.set_driver (driver)
    ```

    A opção de logging/debug no terminal pode ser ativado simplesmente acrescentando a condição abaixo no seu código:
    
    > Por padrão, esta condição é desabilitada

    ```py
    db.set_debugging (
        activated=True
    )
    ```

2. Exemplos dos métodos SQL para manipulação de dados

    - SELECT:

        ```py
        query = '__select * from [...]__'
        resultado = db.select (query)
        ```

    - INSERT:

        ```py
        query = '__insert [...] (__campos__) values [...] ou select [...]__'
        db.insert (query)
        ```

    - DELETE:

        ```py
        query = '__delete [...] from [...]__'
        db.delete (query)
        ```

    - UPDATE:

        ```py
        query = '__update [...] set [...]__'
        db.update (query)
        ```

    - STORED PROCEDURE:

        ```py
        params = '__parametro1__', '__parametro2__'
        procedure = '[__banco__].[__schema__].[__procedure__]'
        db.execute_sp (
            stored_procedure=procedure
        ,   param=(params)
        )
        ```

### Modo de operação do módulo: File

#### Importação da biblioteca

Realize a importação para dentro do código-fonte do seu projeto

```py
from almaviva.file import Files
```

#### Manipulando pastas e arquivos via Python

1. Primeiro crie uma instancia do objeto, executando um dos seguintes códigos abaixo:

    Podemos iniciar a instância informando um caminho ao qual os arquivos serão manipulados por esta função:

    ```py
    folder = Files (
        tempfolder=r'C:\_automacao\'
    )
    ```

    Ou, quando não for informado o caminho da pasta que está querendo mapear, o código criará uma pasta com nome randômico nas pastas temporárias do sistema operacioal ``%tmp%``

    ```py
    folder = Files (
        tempfolder=None
    )
    print (
        folder.get_folder_path()
    )
    ```

    Posteriormente podemos configurar outro caminho de pasta, nesta mesma instância, executando:

    ```py
    folder.set_folder_path (
        tempfolder='__outra pasta__'
    )
    ```

2. Procurar e/ou listar arquivos do diretório

    Lista todos os arquivos do diretório mapeado de uma determinada instância é fácil, basta executar o código abaixo:

    ```py
    folder.list_files()
    ```

    Mas, se quiser localizar uma pasta ou arquivo específico podemos usar:

    > Aqui podemos usar caracteres coringas para localizar parte do nome do arquivo ou pasta
    
    ```py
    folder.search_path_or_file (
        name_or_pattern_to_search='*'
    )
    ```

3. Excluir os arquivos da pasta

    Podemos executar o código abaixo para excluir TODOS os arquivos e pastas que existirem na pasta mapeada em uma determinada instância
    
    ```py
    folder.delete_all_files()
    ```

    Também temos a possibilidade de excluir um arquivo específico, executando:

    ```py
    folder.delete_file (
        file_name='__arquivo1.xlsb__'
    )
    ```

4. Mover arquivos de um diretório para outro

    Se quiser mover todos os arquivos de um diretorio, basta executar:

    > Aqui recomenda-se usar a função ``to_folder=folder2.get_folder_path()`` de outra instância para evitar exceções na execução do código

    ```py
    folder.move_all_files (
        to_folder='__nova pasta__'
    )
    ```

    Mover um arquivo específico de um diretório para outro:

    > Aqui recomenda-se usar a função ``file_name=folder.search_path_or_file('__arquivo1__.xls*')[0]`` da mesma instância e também o exemplo ``to_folder=folder2.get_folder_path()`` de outra instância para evitar exceções na execução do código

    ```py
    folder.move_file (
        file_name='__arquivo1.xlsb__'
    ,   to_folder='__nova pasta__'
    )
    ```

5. Copiar arquivos de um diretório para outro

    Se quiser copiar todos os arquivos de um diretorio, basta executar:

    > Aqui recomenda-se usar a função ``to_folder=folder2.get_folder_path()`` de outra instância para evitar exceções na execução do código

    ```py
    folder.copy_all_files (
        to_folder='__nova pasta__'
    )
    ```

    Copiar um arquivo específico de um diretório para outro:

    > Aqui recomenda-se usar a função ``file_name=folder.search_path_or_file('__arquivo1__.xls*')[0]`` da mesma instância e também o exemplo ``to_folder=folder2.get_folder_path()`` de outra instância para evitar exceções na execução do código

    ```py
    folder.copy_file (
        file_name='__arquivo1.xlsb__'
    ,   to_folder='__nova pasta__'
    )
    ```

### Modo de operação do módulo: IHM

#### Importação da biblioteca

Realize a importação para dentro do código-fonte do seu projeto:

```py
from almaviva.ihm import HUNames
```

#### Para obter o nome da máquina e o usuário atualmente conectado

1. Primeiro crie uma instancia do objeto, executando:

    ```py
    huname = HUNames()
    ```

2. Para saber o usuário atualmente conectado ``username``, execute:

    ```py
    print (
        huname.get_username()
    )
    ```

3. Para saber o nome da máquina ``hostname``, execute:

    ```py
    print (
        huname.get_hostname()
    )
    ```

4. Para saber a versão do Python instalado no sistema, execute:

    ```py
    print (
        huname.get_app()
    )
    ```

### Modo de operação do módulo: LOGGING

#### Importação da biblioteca

Realize a importação para dentro do código-fonte do seu projeto

```py
from almaviva.logging import Logging
```

#### Registrando eventos de log

1. Crie uma instancia do objeto antes de iniciar os registros, executando:

    ```py
    log = Logging()
    ```

2. Para registrar um evento de log no nível de segurança ``INFO``, basta executar:

    ```py
    log.info (
        description='__primeiro log__'
    ,   step='__etapa1__'               # Step é opcional
    ,   complete=__True_or_False__      # Complete é opcional
    )
    ```

    > O argumento ``complete`` pode ser informado com ``True`` ou ``False``, porém se não informado, o sistema sempre registrará o status como ``OK``

3. Para registrar um evento de log no nível de segurança ``WARN``, basta executar:

    ```py
    log.warn (
        description='__segundo log__'
    ,   step='__etapa1__'               # Step é opcional
    ,   complete=__True_or_False__      # Complete é opcional
    )
    ```
    
    > O argumento ``complete`` pode ser informado com ``True`` ou ``False``, porém se não informado, o sistema sempre registrará o status como ``OK``

4. Para registrar um evento de log no nível de segurança ``ERROR``, basta executar:

    ```py
    log.error (
        description='__terceiro log__'
    ,   step='__etapa1__'               # Step é opcional
    )
    ```
    
    > O status desta função sempre retornará como ``OK``, porém com a sinalização ``ERROR``.

5. Opções avançadas:

    > A opção ``logging_in_db`` foi substituída na versão 1.2.1 para ``logging_in_server`` carregando o registro de log em texto para o servidor de processamento de log do NOC Central

    ```py
    log.set_options (           # Configurações padrão
        logging_in_file=True
    ,   debug_in_terminal=False
    ,   logging_in_server=False
    )
    ```
    
    > Por padrão o sistema cria um arquivo de log na mesma pasta em que a aplicação está executando, para desativar isto, desabilite a opção:

    ```py
    logging_in_file=False
    ```

    > Podemos exibir todos os registros de logs de ``INFO`` até ``ERROR`` no terminal. Para fazer isto, habilite a seguinte opção:

    ```py
    debug_in_terminal=True
    ```

    > Todo registro de atividade da aplicação pode ser enviada para o servidor de processamento de log central localizado no NOC Central por padrão. Para fazer isto, habilite a opção:

    ```py
    logging_in_server=True
    ```

### Modo de operação do módulo: WEBDRIVER

#### Importação da biblioteca

Realize a importação para dentro do código-fonte do seu projeto

```py
from almaviva.webdriver import WebDriverChrome
from selenium.webdriver.common.by import By
```

#### Executando o Google Chrome no modo automatizado

> Aviso Importante! Para usar esta biblioteca, é necessário a instalação do [Navegador Chrome](https://www.google.pt/intl/pt-BR/chrome/) e [Chrome Driver](https://chromedriver.chromium.org/downloads)

1. Inicialização do WebDriver com perfil para permitir restaurar ultima sessão

    ```py
    driver = WebDriverChrome (
        profile_location=r'profiles\profile1'    # profile_location: Parâmetro opcional
    ,   executable_path=r'drivers\chromedriver.exe'
    )
    ```
    
2. Opções adicionais de configuração das preferências do navegador:
    
    ```py
    download_dir = r'download_folder\'     # Importante encerrar com 2 barras no final
    preferences = {
        "profile.default_content_settings.popups": 0
    ,   "download.default_directory": str(download_dir)
    ,   "download.prompt_for_download": False
    ,   "directory_upgrade": True
    }
    driver.add_experimental_option (prefs=preferences)          # Adicionar preferencias personalizadas.
    ```

3. Opções adicionais avançadas que podem ser configurados no navegador:

    ```py
    driver.set_options (new_argument='--disable-dev-shm-usage') # Opção para desabilitar recursos de desenvolvedor - economiza custo da memória
    driver.set_options (new_argument='--disable-gpu')           # Opção para economizar processamento de vídeo
    driver.set_options (new_argument='--no-sandbox')            # Opção para teste de versões Beta da aplicação
    driver.set_options (new_argument='--start-maximized')       # Opção para maximizar a janela no start do browser
    driver.set_options (new_argument='--window-size=960,1080')  # Opção para modificar largura x altura em pixel no start do browser
    driver.set_options (new_argument='--headless')              # Opção para não rendenizar a janela do Google Chrome
    ```

4. Agora basta inicializar o navegador e obter os objeto de localização e controle dos elementos da página passando a função instanciada ``driver.set_browser(url)`` previamente configurado:
    
    ```py
    browser=driver.set_browser (
        url=r'https://portaldocolaborador.almavivadobrasil.com.br'
    )
    ```

5. Use comandos, como no exemplo abaixo para localizar os elementos e controlar a página web, para mais informaçoes busque as palavras ``selenium browser find_elements`` na web.

    #  | BY_CHOISES
    -- | ------------------------
    1  | ``By.ID``               
    2  | ``By.XPATH``            
    3  | ``By.LINK_TEXT``        
    4  | ``By.PARTIAL_LINK_TEXT``
    5  | ``By.NAME``             
    6  | ``By.TAG_NAME``         
    7  | ``By.CLASS_NAME``       
    8  | ``By.CSS_SELECTOR``     
    
    ```py
    browser.find_element (
        by=By.XPATH,
        value='__x_path__'
    )
    ```