#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from .basics import Basics
import showlog
import time
import envx
default_silence = False
default_env_file_name = 'local.mongo.env'


def make_con_info(
        env_file_name: str = default_env_file_name
):
    # ---------------- 固定设置 ----------------
    inner_env = envx.read(file_name=env_file_name)
    connect_str = inner_env.get('connect_str')
    if connect_str is None:
        host = inner_env.get('host', 'localhost')
        port = int(inner_env.get('port', '27017'))
        username = inner_env.get('username', 'root')
        password = inner_env.get('password', '')
        connect_str = f'mongodb://{username}:{password}@{host}:{port}/'
    else:
        pass
    return connect_str
    # ---------------- 固定设置 ----------------


def safe_get_records(
        query: dict = None,
        db: str = None,
        collection: str = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response = mongo_basics.collection_records(
                query=query,
                db=db,
                collection=collection
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_find(
        query: dict = None,
        db: str = None,
        collection: str = None,
        show_setting: dict = None,
        sort_setting: list = None,  # 注意在python里是list，例如[('aa', 1)]
        limit_num: int = None,
        skip_num: int = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response, response_count = mongo_basics.find(
                query=query,
                db=db,
                collection=collection,
                show_setting=show_setting,
                sort_setting=sort_setting,
                limit_num=limit_num,
                skip_num=skip_num
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_find_page(
        db: str = None,
        collection: str = None,
        query: dict = None,
        previous_tag: str = None,
        previous_value: str = None,
        where_str: str = '$gt',
        show_setting: dict = None,
        sort_setting: list = [('_id', 1)],  # 注意在python里是list，例如[('aa', 1)]
        limit_num: int = 10,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response, response_count = mongo_basics.find_page(
                db=db,
                collection=collection,
                query=query,
                previous_tag=previous_tag,
                previous_value=previous_value,
                where_str=where_str,
                show_setting=show_setting,
                sort_setting=sort_setting,
                limit_num=limit_num
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_find_page_by_num(
        db: str = None,
        collection: str = None,
        query: dict = None,
        show_setting: dict = None,
        sort_setting: list = [('_id', 1)],  # 注意在python里是list，例如[('aa', 1)]
        previous_tag: str = None,
        page_size: int = 20,
        page: int = 1,
        _id: str = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    """
    按页码获取数据
    """
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response, response_count = mongo_basics.get_page_data(
                db=db,
                collection=collection,
                query=query,
                show_setting=show_setting,
                sort_setting=sort_setting,
                previous_tag=previous_tag,
                page_size=page_size,
                page=page,
                _id=_id
            )
            return response, response_count
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_insert(
        values: list,
        db: str = None,
        collection: str = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response = mongo_basics.insert(
                values=values,
                db=db,
                collection=collection
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_upsert(
        values: list,
        db: str = None,
        collection: str = None,
        query_keys: list = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response = mongo_basics.upsert(
                values=values,
                db=db,
                collection=collection,
                query_keys=query_keys
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_delete_one(
        db: str = None,
        collection: str = None,
        query: dict = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    """
    删除一条数据
    """
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response = mongo_basics.delete_one(
                db=db,
                collection=collection,
                query=query
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)


def safe_delete_many(
        db: str = None,
        collection: str = None,
        query: dict = None,
        connect_str: str = None,  # 若指定，将优先使用
        env_file_name: str = default_env_file_name,
        silence: bool = default_silence
):
    """
    删除满足条件的所有数据
    """
    # ---------------- 固定设置 ----------------
    if connect_str is None:
        connect_str = make_con_info(env_file_name=env_file_name)
    # ---------------- 固定设置 ----------------
    while True:
        try:
            mongo_basics = Basics(
                connect_str=connect_str,
                db=db,
                collection=collection,
                silence=silence,
            )
            response = mongo_basics.delete_many(
                db=db,
                collection=collection,
                query=query
            )
            return response
        except ConnectionError:
            if silence is False:
                showlog.warning('连接失败，将重试...')
            time.sleep(1)
        except Exception as ex:
            if silence is False:
                showlog.error('未知错误')
            time.sleep(1)
