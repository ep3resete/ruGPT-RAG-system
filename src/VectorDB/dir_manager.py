"""
Модуль менеджера директория базы данных. Нужен для создания, удаления и проверки сущестовавания файлов. Придерживается такой архитектуры

Структура: 
├────DB
│    ├───dir1VDB
│    │    ├───fileVDB
│    │    │   ├────fileChunks
│    │    │   │    ├───chunck_1.txt
│    │    │   │    ├───chunck_2.txt
│    │    │   │    ├───...
│    │    │   │    └──chunck_n.txt
│    │    │   └───fileEmbd.(расширение файла с эмбэддингом, пока не понятно)
│    │    ├───another_fileVDB
│    │    │   ...
│    ├───another_dir1VDB
│    │    └─── ...
...
"""

import os
import asyncio
from chromadb import Client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.api.types import Document
from files_splitter import Splitter
# from config import chunk_size, chunk_overlap, dir_of_full_DB


chunk_size = 200 # Размер чанка
chunk_overlap = 50 # Размер перекрытия чанков
dir_of_full_DB = "./DB"

path_of_dir = "./data/docs_samgtu"
dir_of_file_DB = "./fileDB"

class DirManager:
    def __init__(self, base_dir: str, data_path: str) -> None:
        """ Менеджер данными в базе. Првоеряет существоание 
        base_dir - Директория базы данных 
        data_path - название папки с файлами, которые будут конвертироваться в эмбэддинги. Именно ПАПКИ с файлами, просто файл пока не прокатит 
        Папка с файлами должна находиться в директории RUGPT-RAG-PT/data
        """
        self.base_dir = base_dir
        self.data_path = data_path
        
    def get_texts_from_dir(self) -> list[str]:
        """ Функция для получения текстов из файлов директории """
        # Перебор папки с сырыми данными
        files_in_dir = os.listdir(self.data_path)
        if len(files_in_dir) == 0:
            raise FileNotFoundError("По данному пути не найдено ни одного файла") # Ситуация, когда дана пустая папка

        texts = []
        for file in files_in_dir:
            with open(self.data_path + "/" + file, encoding='utf-8') as opened_file:
                texts.append(" ".join(opened_file.readlines()).replace("\n", " "))

        return texts


    def get_embd_from_chunks(chunks: list[Document]):

        pass

    def get_path_to_VBD(self) -> str:
        """ Функция для получения пути, по которому хранится векторная база данных для заданного файла"""
        # Проверка на существование уже отвекторизованных чанков
        if self._check_dir_of_data():
            return 

        # print(chuns)

    def _check_dir_of_data(self) -> bool:
        """ Функция проверки существования директории """
        # print(self.base_dir + self.data_path + "VDB")
        return os.path.exists(self.base_dir + self.data_path + "VDB")
         

DM = DirManager(dir_of_full_DB, path_of_dir)
DM.get_path_to_VBD()
print(DM._check_dir_of_data())
print(os.listdir(path_of_dir))
