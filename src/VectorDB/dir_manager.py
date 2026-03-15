"""
Модуль менеджера директория базы данных. Нужен для создания, удаления и проверки сущестовавания файлов. Придерживается такой архитектуры

Структура: 
├────DB
│    ├───dir1VDB
│    │   ├────fileChunks
│    │   │    ├───chunck_1.txt
│    │   │    ├───chunck_2.txt
│    │   │    ├───...
│    │   │    └──chunck_n.txt
│    │   └───fileEmbd.(расширение файла с эмбэддингом, пока не понятно)
│    │   ...
├───another_dir1VDB
│    └─── ...

"""

import os
import asyncio
from chromadb.api.types import Document
from files_splitter import Splitter
from data_operator import Operator
from logger import loginfo, logcritical

import numpy as np


chunk_size = 200 # Размер чанка
chunk_overlap = 50 # Размер перекрытия чанков
dir_of_full_DB = ".\\DB"


class DirManager:
    def __init__(self, base_dir: str, data_path: str, data_name: str) -> None:
        """ Менеджер данными в базе. Првоеряет существоание 
        base_dir - Директория базы данных 
        data_path - путь до папки с данными, которые будут конвертироваться в эмбэддинги. Именно ПАПКИ с файлами, просто файл пока не прокатит 
        name_of_dir - название папки с данными
        Папка с файлами должна находиться в директории RUGPT-RAG-PT/data
        """
        self.base_dir = base_dir # Директория всей базы данных (./DB)
        self.data_path = data_path # Путь к сырым данным (./data
        self.data_name = data_name # Имя папки с данными (./<папка>)
        self.full_data_path = os.path.join(data_path, data_name)
        self.operator = Operator(embd_dir, "cuda") # Оператор над БД
        self.splitter = Splitter(chunk_size, chunk_overlap) # Сплиттер (возможно станет частью оператора)
        self.VDB_dir_path = os.path.join(self.base_dir, self.data_name + "VDB") # Путь к итоговой базе данных
        
    def get_texts_from_dir(self) -> list[str]:
        """ Функция для получения текстов из файлов директории """
        # Перебор папки с сырыми данными
        files_in_dir = os.listdir(self.full_data_path)
        if len(files_in_dir) == 0:
            logcritical(f"No files were found in the {self.full_data_path} directory")
            raise FileNotFoundError("По данному пути не найдено ни одного файла") # Ситуация, когда дана пустая папка

        texts = []
        for file in files_in_dir:
            with open(self.full_data_path + "\\" + file, encoding='utf-8') as opened_file:
                texts.append(" ".join(opened_file.readlines()).replace("\n", " "))
                loginfo(f"Extracted data from the file {file}")

        return texts

    def _check_dir_of_data(self, path: str) -> bool:
        """ Функция проверки существования директории """
        # print(self.base_dir + self.data_path + "VDB")
        return os.path.exists(path)
        # return os.path.exists(self.base_dir + self.data_path + "VDB")

    
    def save_chunk(self, chunk: Document, id: int) -> None:
        """ Функция для сохранения одного чанка по пути
        chunk - Чанк типа Document
        id - айди чанка
        """
        # Путь до файла чанка
        path_of_chunk = self.VDB_dir_path + f"\\{self.data_name}Chunks\\chunk_{id}.txt"
        # Открытие и сохранение чанка
        with open(path_of_chunk, "w", encoding="utf-8") as chunk_file:
            chunk_file.write(chunk.page_content)
        

    def save_chunks(self, chunks: list[Document]) -> None:
        """ Функция для сохранения всех чанков 
        chunks - список чанков типа Document
        """
        loginfo(f"Writing chunks ({len(chunks)}) to files")
        for i, chunk in enumerate(chunks):
            self.save_chunk(chunk, i)
        loginfo(f"All chunks are written to files")

    def save_embeddings(self, embd_list: np.ndarray[np.ndarray[np.float32]]) -> None:
        loginfo("Writing embeddings to file")
        np.save(self.VDB_dir_path + f"{self.data_name}Embeddings.npy", embd_list)
        loginfo("Embeddings are written to files")


    def get_path_to_VBD(self) -> str:
        """ Функция для получения пути, по которому хранится векторная база данных для заданного файла"""
        
        # Проверка на существование уже отвекторизованных чанков
        if self._check_dir_of_data(self.VDB_dir_path):
            loginfo(f"Path already exists")
            return self.VDB_dir_path
        os.makedirs(self.VDB_dir_path)
        os.makedirs(self.VDB_dir_path + f"\\{self.data_name}Chunks\\")
        loginfo(f"The path {self.VDB_dir_path} was created")

        texts = self.get_texts_from_dir()
        chunks = self.splitter.get_chunks_from_texts(texts)
        
        self.save_chunks(chunks)
        embeddings_list = self.operator.get_embd_from_chunks(chunks)
        self.save_embeddings(embeddings_list)
        
        return self.VDB_dir_path
         
