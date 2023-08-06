# coding: utf-8

#
# Dependences
# 
import os, os.path, tempfile, shutil
import fnmatch      # fassad, 2020-06-30: adicionado biblioteca para busca de arquivos e diretorios
import string, random   # fassad, 2020-06-30: adicionado biblioteca para criação de diretórios com nomes randômicos

"""
Descrição:
    Gerenciador de pastas e arquivos
funções disponíveis:
    Files().set_folder_path(folder_path=None)
    Files().get_folder_path() -> str
    Files().list_files() -> list
    Files().search_path_or_file(name_or_pattern_to_search='*') -> list
    Files().delete_all_files()
    Files().delete_file(file_name)
    Files().move_all_files(to_folder)
    Files().move_file(file_name, to_folder)
    Files().copy_all_files(to_folder)
    Files().copy_file(file_name, to_folder)
"""
class Files():
    
    def __init__ (
        self
    ,   folder_path=None
    ):
        self.set_folder_path (
            folder_path
        )
    
    """
    Procedimento para verificar a existência da pasta e set_up
    """
    def set_folder_path (
        self
    ,   folder_path=None
    ):

        if (
            'folder_path' in locals()
        and folder_path!=None
        ):
            folder = folder_path

        else:
            # fassad, 2020-06-30: adicionado _random_path_name para criação de diretórios com nomes randômicos
            _random_path_name = ''.join(
                random.choice (
                    string.ascii_lowercase + string.digits
                ) for _ in range(6)
            )
            folder = str (
                tempfile.gettempdir()
            ) + '\\' + _random_path_name + '\\'

        # Caso seja caminho de rede, iniciar a verificação depois do `hostname` e o `shared_name`
        # Caso seja caminho da máquina local, iniciar a verificação depois da `unidade de disco`
        if (
            folder[:2] == r'\\'
        ):
            startWith = r'\\' + '\\'.join(folder.split('\\')[2:][0:2]) + '\\'
            offset = 4
        else:
            startWith = '\\'.join(folder.split('\\')[0:][0:1]) + '\\'
            offset = 1

        # Cria a pasta e sub-pastas caso não encontre
        path = folder.split('\\')[offset:]
        for pos in range(len(path)):
            test = startWith + '\\'.join(path[0:pos+1])
            if not os.path.isdir (test):
                os.mkdir (test)

        # Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path
        self.folder_path = os.path.realpath (
            folder
        )
    
    """
    Retorna a pasta verificada
    """
    def get_folder_path (
        self
    ):
        return self.folder_path
    
    """
    Excluir todos os arquivos da pasta
    """
    def delete_all_files (
        self
    ):
        for file in os.listdir (
            self.folder_path
        ):
            os.remove (
                str (
                    self.folder_path
                ) + '\\' + str (
                    file
                )
            )

    """
    Excluir um arquivo temporário
    """
    def delete_file (
        self
    ,   file_name
    ):
        os.remove (
            str (
                self.folder_path
            ) + '\\' + str (
                file_name
            )
        )

    """
    Listar arquivos do diretório
    """
    def list_files (
        self
    ):
        return os.listdir (
            self.folder_path
        )

    """
    Mover todos os arquivos de um diretório para outro
    """
    def move_all_files (
        self
    ,   to_folder
    ):
        
        to_folder_valid = os.path.realpath (
            to_folder
        )

        for file in os.listdir (
            self.folder_path
        ):
            _old = self.folder_path + '\\' + str (file)
            _new = str (to_folder_valid) + '\\' + str (file)
            shutil.move (_old, _new)

    """
    Mover um arquivo específico de um diretório para outro
    """
    def move_file (
        self
    ,   file_name
    ,   to_folder
    ):
        
        to_folder_valid = os.path.realpath (
            to_folder
        )

        _old = self.folder_path + '\\' + str (file_name)
        _new = str(to_folder_valid) + '\\' + str (file_name)
        shutil.move (_old, _new)

    """
    Copiar todos os arquivos de um diretório para outro
    """
    def copy_all_files (
        self
    ,   to_folder
    ):
        
        to_folder_valid = os.path.realpath (
            to_folder
        )

        for file in os.listdir (
            self.folder_path
        ):
            _old = self.folder_path + '\\' + str (file)
            _new = str (to_folder_valid) + '\\' + str (file)
            shutil.copy (_old, _new)

    """
    Copiar um arquivo específico de um diretório para outro
    """
    def copy_file (
        self
    ,   file_name
    ,   to_folder
    ):
        
        to_folder_valid = os.path.realpath (
            to_folder
        )

        _old = self.folder_path + '\\' + str (file_name)
        _new = str(to_folder_valid) + '\\' + str (file_name)
        shutil.copy (_old, _new)


    """
    Buscar arquivos neste diretório
    fassad, 2020-06-30: adicionado biblioteca para busca de arquivos e diretorios
    """
    def search_path_or_file (
        self
    ,   name_or_pattern_to_search='*'
    ):
        
        result = []
        
        for root, dirs, files in os.walk (
            self.folder_path
        ):
            for file in files:
                if fnmatch.fnmatch (
                    file
                ,   name_or_pattern_to_search
                ):
                    result.append (
                        os.path.join (
                            root
                        ,   file
                        )
                    )
        
        return result