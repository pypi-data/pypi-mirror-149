"""hbase客户端封装.

主要解决易用性问题:
1. 让客户端不需要导入thrift定义的类.
2. 让客户端不用显式的传输bytes类型的参数.
3. 让客户端可以使用事先设定好的编码解码函数直接沟通python和hbase

使用方法:

    with HBaseCli(
                url="http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:9190",
                headers={"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}) as client:
        nsinfo = client.show_namespaces()
    print(nsinfo)

"""
import json
import binascii
import datetime
from typing import Callable, Dict, List, Mapping, Sequence, Optional, Any, List, Dict, Tuple, Union, Tuple
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient

from .hbase import THBaseService
from .hbase.ttypes import (
    TColumn,
    TColumnFamilyDescriptor,
    TColumnValue,
    TGet,
    TDelete,
    TCellVisibility,
    TNamespaceDescriptor,
    TPut,
    TAppend,
    TIncrement,
    TScan,
    TTableDescriptor,
    TTableName,
    TDurability,
    TBloomFilterType,
    TCompressionAlgorithm,
    TDataBlockEncoding,
    TKeepDeletedCells,
    TTimeRange,
    TAuthorization,
    TConsistency,
    TDeleteType,
    TReadType,
    TColumnIncrement
)


def fullcolumn(family: str, column: str) -> str:
    """构造列完整名.

    Args:
        family (str): 列簇名
        column (str): 列名

    Returns:
        str: 列完整名
    """
    return f"{family}:{column}"


def newTColumnValue(column: str, value_bytes: bytes, *, family: Optional[str] = None, timestamp: Optional[datetime.datetime] = None, tags: Optional[str] = None, type_: Optional[str] = None) -> TColumnValue:
    """创建一个可用于代理的TColumnValue对象.

    Args:
        column (str): 列名,列名中如果是"family:column"的形式即为列全名,即已经指定了列簇则可以不填family参数
        family (Optional[str]): 列簇名
        value_bytes (bytes): 列的值
        timestamp (Optional[datetime.datetime], optional): 时间. Defaults to None.
        tags (Optional[str], optional): 标签. Defaults to None.
        type_ (Optional[str], optional): type值. Defaults to None.

    Raises:
        AttributeError: 列名格式不合法

    Returns:
        TColumnValue: 列结果对象
    """
    if family is not None:
        _family = family
        _column = column
    else:
        columninfo = column.split(":")
        if len(columninfo) == 2:
            _family = columninfo[0]
            _column = columninfo[1]
        else:
            raise AttributeError(f"parameter column syntax error: {column}")
    _tags = None
    if tags:
        _tags = tags.encode("utf-8")
    _type = None
    if type_:
        _type = type_.encode("utf-8")

    _timestamp = None
    if timestamp:
        _timestamp = timestamp.timestamp()
        _timestamp = int(_timestamp * 1000)
    return TColumnValue(
        family=_family.encode("utf-8"),
        qualifier=_column.encode("utf-8"),
        value=value_bytes,
        timestamp=_timestamp,
        tags=_tags,
        type=_type)


class ColumnsValue:
    """TColumnValue的代理类."""
    __slots__ = ('instance', "_encoder", "_decoder")
    instance: Optional[TColumnValue]
    _encoder: Optional[Callable[[Any, Optional[str]], bytes]]
    _decoder: Optional[Callable[[bytes, Optional[bytes]], Any]]

    def __getattr__(self, attr: str) -> Any:
        if self.instance is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return getattr(self.instance, attr)

    def __setattr__(self, attr: str, value: Any) -> Any:
        if attr not in self.__slots__:
            raise AttributeError('Cannot set attribute on proxy.')
        return super().__setattr__(attr, value)

    @classmethod
    def from_value(clz,
                   family: str, column: str, value: Any, *, encoder: Callable[[Any, Optional[str]], bytes],
                   timestamp: Optional[datetime.datetime] = None, tags: Optional[str] = None, type_: Optional[str] = None) -> 'ColumnsValue':

        p = clz(encoder=encoder)
        p.initialize_from_value(family=family, column=column, value=value, timestamp=timestamp, tags=tags, type_=type_)
        return p

    def __init__(self, *, encoder: Optional[Callable[[Any, Optional[str]], bytes]] = None, decoder: Optional[Callable[[bytes, Optional[bytes]], Any]] = None) -> None:
        """创建一个TColumnValue的代理对象

        Args:
            encoder (Optional[Callable[[Any, Optional[str]], bytes]]): 将值编码为bytes的函数,可选项str会在调用时传入tags的值,方便一些场景根据tag判断编码方法
            decoder (Optional[Callable[[bytes, Optional[bytes]], Any]]): 将bytes编码为值的函数,可选项str会在调用时传入tags的值,方便一些场景根据tag判断编码方法
        """
        self.instance = None
        if encoder:
            self._encoder = encoder
        else:
            self._encoder = None

        if decoder:
            self._decoder = decoder
        else:
            self._decoder = None

    def regist_decoder(self, decoder: Callable[[bytes, Optional[bytes]], Any]) -> None:
        """为代理对象注册解码器.

        Args:
            decoder (Callable[[bytes, Optional[bytes]], Any]): 将bytes编码为值的函数,可选项str会在调用时传入tags的值,方便一些场景根据tag判断编码方法
        """
        self._decoder = decoder

    def regist_encoder(self, encoder: Callable[[Any, Optional[str]], bytes]) -> None:
        """为代理对象注册编码器.

        Args:
            encoder (Callable[[Any, Optional[str]], bytes]): 将值编码为bytes的函数,可选项str会在调用时传入tags的值,方便一些场景根据tag判断编码方法
        """
        self._encoder = encoder

    def initialize(self, instance: TColumnValue) -> None:
        """将被代理的实例注册到代理上."""
        if isinstance(instance, TColumnValue):
            self.instance = instance
        else:
            raise AttributeError("instance is not TColumnValue")

    def initialize_from_value(self, family: str, column: str, value: Any, *, timestamp: Optional[datetime.datetime] = None, tags: Optional[str] = None, type_: Optional[str] = None) -> None:
        """创建一个新的TColumnValue对象并使用本对象进行代理.

        Args:
            column (str): 列名,列名中如果是"family:column"的形式即为列全名,即已经指定了列簇则可以不填family参数
            family (Optional[str]): 列簇名
            value_bytes (bytes): 列的值
            timestamp (Optional[datetime.datetime], optional): 时间. Defaults to None.
            tags (Optional[str], optional): 标签. Defaults to None.
            type_ (Optional[str], optional): type值. Defaults to None.
        """
        if not self._encoder:
            raise AttributeError("need to set encoder first")
        value_bytes = self._encoder(value, tags)
        instance = newTColumnValue(family=family, column=column, value_bytes=value_bytes, timestamp=timestamp, tags=tags, type_=type_)
        self.initialize(instance)

    def info(self) -> Dict[str, Union[int, str, bytes]]:
        """获取ColumnsValue的信息字典.

        该信息字典可以被`newTColumnValue`函数用于创建一个TColumnValue.

        Returns:
            Dict[str, Union[int, str, bytes]]: 信息字典
        """
        if not self.instance:
            raise AttributeError("not initialize yet")
        result = {
            "column": self.instance.qualifier.decode("utf-8"),
            "family": self.instance.family.decode("utf-8"),
            "value_bytes": self.instance.value
        }
        if self.instance.timestamp:
            result.update({
                "timestamp": datetime.datetime.fromtimestamp(self.instance.timestamp / 1000)
            })
        if self.instance.tags:
            result.update({
                "tags": self.instance.tags.decode("utf-8")
            })
        if self.instance.type:
            result.update({
                "type_": self.instance.type.decode("utf-8")
            })
        return result

    def values(self) -> Tuple[str, Any]:
        """获取python可以直接处理的键值对.

        Returns:
            Tuple[str, Any]: python可以直接处理的键值对,键为列全名,值为列的值.
        """
        if not self.instance:
            raise AttributeError("not initialize yet")
        if not self._decoder:
            raise AttributeError("need to set decoder first")
        key = fullcolumn(self.instance.family.decode("utf-8"), self.instance.qualifier.decode("utf-8"))
        value = self._decoder(self.instance.value, self.instance.tags)
        return key, value

    def as_TColumnValue(self) -> TColumnValue:
        """提取代理的TColumnValue对象.

        Returns:
            TColumnValue: 代理对象内代理的TColumnValue对象
        """
        if not self.instance:
            raise AttributeError("not initialize yet")
        return self.instance


def StrEncoder(x: Any, y: Optional[str] = None) -> bytes:
    """字符串编码器.

    将python对象的字面量编码为字节流.

    Args:
        x (Any): python对象
        y (Optional[str]): 无用占位

    Returns:
        bytes: 编码后的结果
    """
    return str(x).encode("utf-8")


def StrDecoder(x: bytes, y: Optional[bytes] = None) -> str:
    """字符串解码器.

    将字节流解码为将python字符串.

    Args:
        x (bytes): 待解码字节流
        y (Optional[bytes]): 无用占位

    Returns:
        str: 字符串
    """
    return x.decode("utf-8")


def JsonEncoder(x: Any, y: Optional[str] = None) -> bytes:
    """json编码器.

    将python对象用json编码为字节流.

    Args:
        x (Any): python对象
        y (Optional[str]): 无用占位

    Returns:
        bytes: 编码后的结果
    """
    return json.dumps(x).encode("utf-8")


def JsonDecoder(x: bytes, y: Optional[bytes] = None) -> Any:
    """json解码器.

    将字节流解码为将python字符串.

    Args:
        x (bytes): 待解码字节流
        y (Optional[bytes]): 无用占位

    Returns:
        Any: python对象
    """
    return json.loads(x.decode("utf-8"))


def NumberDecoder(x: bytes, y: Optional[bytes] = None) -> int:
    """将bytes转化为int型数据.

    用于获取incr操作列中的当前值.

    Args:
        x (bytes): 待解码字节流
        y (bytes): 无用占位

    Returns:
        int: 当前值
    """
    return int(str(binascii.b2a_hex(x))[2:-1], 16)


def _createClosestRowAfter(row: bytes) -> bytes:
    """找到比当前row大的最小row.
    方法是在当前row后加入一个0x00的byte,从比当前row大的最小row开始scan.可以保证中间不会漏扫描数据.

    Args:
        row (bytes): 当前row

    Returns:
        bytes: 比当前row大的最小row
    """
    array = bytearray(row)
    array.append(0x00)
    return bytes(array)


class HBaseCli:

    def __init__(self, url: str, *, headers: Optional[Mapping[str, str]] = None) -> None:
        """连接hbase.

        Example:
            client = HBaseCli(
                url="http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:9190",
                headers={"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"})

        Args:
            url (string): 连接的路径
            headers (Optional[Mapping[str, str]]): 设置请求头,有验证的话用户名设置ACCESSKEYID,密码设置ACCESSSIGNATURE
        """
        try:
            self.transport = THttpClient.THttpClient(url)
            self.transport.setCustomHeaders(headers)
            protocol = TBinaryProtocol.TBinaryProtocolAccelerated(
                self.transport)
            self.client = THBaseService.Client(protocol)
        except Exception as e:
            raise e

    def open(self) -> None:
        self.transport.open()

    def close(self) -> None:
        self.transport.close()

    def __enter__(self) -> 'HBaseCli':
        self.open()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()
        return None

    # 命名空间操作
    def create_namespace(self, ns: str, **configs: str) -> None:
        """ 创建命名空间.

        Args:
            ns (string): 命名空间名称
        """
        self.client.createNamespace(TNamespaceDescriptor(name=ns, configuration=configs))

    def delete_namespace(self, ns: str) -> None:
        """删除命名空间.

        Args:
            ns (str): 命名空间名
        """
        self.client.deleteNamespace(ns)

    def desc_namespace(self, ns: str) -> Dict[str, str]:
        """查看指定命名空间的信息.

        Args:
            ns (str): 命名空间名

        Returns:
            Dict[str, str]: 命名空间信息
        """
        Descriptor = self.client.getNamespaceDescriptor(ns)
        temp = {"name": Descriptor.name}
        if Descriptor.configuration:
            temp.update(Descriptor.configuration)
        return temp

    def show_namespaces(self) -> List[Dict[str, str]]:
        """列出已有的命名空间.

        Returns:
            List[Dict[str, str]]: 命名空间列表
        """
        Descriptors = self.client.listNamespaceDescriptors()
        result = []
        for Descriptor in Descriptors:
            temp = {"name": Descriptor.name}
            if Descriptor.configuration:
                temp.update(Descriptor.configuration)
            result.append(temp)
        return result

    def show_tables(self, ns: str) -> List[Dict[str, str]]:
        """查看指定namespace下的表信息.

        Args:
            ns (str): 命名空间名称

        Returns:
            List[Dict[str, str]]: _description_
        """
        result = []
        TableDescriptors = self.client.getTableDescriptorsByNamespace(ns)
        for TableDescriptor in TableDescriptors:
            if TableDescriptor.durability:
                durability = TableDescriptor.durability
            else:
                durability = 0
            name = ""
            if TableDescriptor.tableName:
                tn = TableDescriptor.tableName
                nsn = tn.ns.decode("utf - 8")
                t = tn.qualifier.decode("utf - 8")
                name = f"{nsn}:{t}"
            meta = {
                "name": name,
                "durability": TDurability._VALUES_TO_NAMES.get(durability, "")
            }
            if TableDescriptor.attributes:
                meta.update({k.decode("utf-8"): v for k, v in TableDescriptor.attributes.items()})
            result.append(meta)
        return result

    # 表操作
    def create_table(self, table: str, families: List[Dict[str, Any]], *,
                     ns: Optional[str] = None,
                     attributes: Optional[Dict[str, bytes]] = None,
                     durability: Optional[str] = None,
                     splitKeys: Optional[str] = None) -> None:
        """创建表.

        必须要先创建namespace.

        Args:
            table (string): 表名,表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            families (List[Dict[str, Any]]): 列簇信息字典
            ns (Optional[str]): 命名空间名称
            attributes (Optional[Dict[str, bytes]]): 表属性设置
            durability  (Optional[str]): 表耐久方式设置,可选的有USE_DEFAULT,SKIP_WAL,ASYNC_WAL,SYNC_WAL,FSYNC_WAL
            splitKeys (Optional[str]): 表初始区域键过滤设置

        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        sk = None
        if splitKeys is not None and len(splitKeys) > 0:
            sk = [i.encode("utf8") for i in splitKeys]
        d = None
        if durability is not None:
            d = TDurability._NAMES_TO_VALUES.get(durability)
        a = None
        if attributes is not None:
            a = {k.encode("utf8"): v for k, v in attributes.items()}
        self.client.createTable(
            desc=TTableDescriptor(
                tableName=tableName,
                columns=[TColumnFamilyDescriptor(**i) for i in families],
                attributes=a,
                durability=d),
            splitKeys=sk
        )

    def table_exists(self, table: str, *, ns: Optional[str] = None) -> bool:
        """检查表是否存在

        Args:
            table (str): 表名,表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns (Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            bool: 是否存在
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        flg = self.client.tableExists(tableName)
        return flg

    def desc_table(self, table: str, *, ns: Optional[str] = None) -> Dict[str, str]:
        """查看指定表的基本信息.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            Dict[str, str]: 描述表基础信息
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")

        TableDescriptor = self.client.getTableDescriptor(tableName)
        if TableDescriptor.durability:
            durability = TableDescriptor.durability
        else:
            durability = 0
        families = []
        if TableDescriptor.columns:
            for family in TableDescriptor.columns:
                families.append(family.name.decode("utf-8"))
        name = ""
        if TableDescriptor.tableName:
            tn = TableDescriptor.tableName
            nsn = tn.ns.decode("utf - 8")
            t = tn.qualifier.decode("utf - 8")
            name = f"{nsn}:{t}"

        meta = {
            "name": name,
            "durability": TDurability._VALUES_TO_NAMES.get(durability, ""),
            "families": ",".join(families)
        }
        if TableDescriptor.attributes:
            meta.update({k.decode("utf-8"): v for k, v in TableDescriptor.attributes.items()})

        return meta

    def show_families(self, table: str, *, ns: Optional[str] = None) -> List[Dict[str, Any]]:
        """查看指定表中包含的列簇信息.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            List[Dict[str, Any]]: 列簇信息
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")

        TableDescriptor = self.client.getTableDescriptor(tableName)
        families = []
        if TableDescriptor.columns:
            for family in TableDescriptor.columns:
                temp = {
                    "name": family.name.decode("utf-8")
                }
                if family.attributes:
                    temp.update({"attributes": {k.decode("utf-8"): v for k, v in family.attributes.items()}})
                if family.configuration:
                    temp.update({"configuration": family.configuration})
                if family.dfsReplication:
                    temp.update({"dfsReplication": family.dfsReplication})
                if family.blockSize:
                    temp.update({"blockSize": family.blockSize})
                if family.maxVersions:
                    temp.update({"maxVersions": family.maxVersions})
                if family.minVersions:
                    temp.update({"minVersions": family.minVersions})
                if family.scope:
                    temp.update({"scope": family.scope})
                if family.timeToLive:
                    temp.update({"timeToLive": family.timeToLive})
                if family.blockCacheEnabled:
                    temp.update({"blockCacheEnabled": family.blockCacheEnabled})
                if family.cacheBloomsOnWrite:
                    temp.update({"cacheBloomsOnWrite": family.cacheBloomsOnWrite})
                if family.cacheDataOnWrite:
                    temp.update({"cacheDataOnWrite": family.cacheDataOnWrite})
                if family.cacheIndexesOnWrite:
                    temp.update({"cacheIndexesOnWrite": family.cacheIndexesOnWrite})
                if family.compressTags:
                    temp.update({"compressTags": family.compressTags})
                if family.evictBlocksOnClose:
                    temp.update({"evictBlocksOnClose": family.evictBlocksOnClose})
                if family.inMemory:
                    temp.update({"inMemory": family.inMemory})

                bloomnFilterType = 0
                if family.bloomnFilterType:
                    bloomnFilterType = family.bloomnFilterType
                    temp.update({"bloomnFilterType": TBloomFilterType._VALUES_TO_NAMES.get(bloomnFilterType)})

                compressionType = 0
                if family.compressionType:
                    compressionType = family.compressionType
                    temp.update({"compressionType": TCompressionAlgorithm._VALUES_TO_NAMES.get(compressionType)})

                dataBlockEncoding = 0
                if family.dataBlockEncoding:
                    dataBlockEncoding = family.dataBlockEncoding
                    temp.update({"dataBlockEncoding": TDataBlockEncoding._VALUES_TO_NAMES.get(dataBlockEncoding)})

                keepDeletedCells = 0
                if family.keepDeletedCells:
                    keepDeletedCells = family.keepDeletedCells
                    temp.update({"keepDeletedCells": TKeepDeletedCells._VALUES_TO_NAMES.get(keepDeletedCells)})

                families.append(temp)
        return families

    def delete_table(self, table: str, *, ns: Optional[str] = None) -> None:
        """删除表.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        self.client.deleteTable(tableName)

    def truncate_table(self, table: str, *, ns: Optional[str] = None, preserveSplits: bool = False) -> None:
        """清空表.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
            preserveSplits (bool): 是否保留以前的拆分,默认False
        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        self.client.truncateTable(tableName, preserveSplits)

    def enable_table(self, table: str, *, ns: Optional[str] = None) -> None:
        """激活表.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        self.client.enableTable(tableName)

    def disable_table(self, table: str, *, ns: Optional[str] = None) -> None:
        """取消激活表.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        self.client.disableTable(tableName)

    def is_table_enabled(self, table: str, *, ns: Optional[str] = None) -> bool:
        """确认表是否已经激活.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
        Raises:
            AttributeError: 表名格式不合法

        Returns:
            bool: 是否已激活
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        return self.client.isTableEnabled(tableName)

    def is_table_disabled(self, table: str, *, ns: Optional[str] = None) -> bool:
        """确认表是否已经取消激活.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
        Raises:
            AttributeError: 表名格式不合法

        Returns:
            bool: 是否已取消激活
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        return self.client.isTableDisabled(tableName)

    def is_table_available(self, table: str, *, ns: Optional[str] = None) -> bool:
        """确认表是否可用.

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns(Optional[str], optional): 命名空间名称
        Raises:
            AttributeError: 表名格式不合法

        Returns:
            bool: 是否可用
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        return self.client.isTableAvailable(tableName)

    # 列簇操作
    def create_family(self, family: str, table: str, *,
                      ns: Optional[str] = None,
                      attributes: Optional[Dict[str, bytes]] = None,
                      configuration: Optional[Dict[str, str]] = None,
                      blockSize: Optional[int] = None,
                      bloomnFilterType: Optional[str] = None,
                      compressionType: Optional[str] = None,
                      dfsReplication: Optional[int] = None,
                      dataBlockEncoding: Optional[str] = None,
                      keepDeletedCells: Optional[str] = None,
                      maxVersions: Optional[int] = None,
                      minVersions: Optional[int] = None,
                      scope: Optional[int] = None,
                      timeToLive: Optional[int] = None,
                      blockCacheEnabled: Optional[bool] = None,
                      cacheBloomsOnWrite: Optional[bool] = None,
                      cacheDataOnWrite: Optional[bool] = None,
                      cacheIndexesOnWrite: Optional[bool] = None,
                      compressTags: Optional[bool] = None,
                      evictBlocksOnClose: Optional[bool] = None,
                      inMemory: Optional[bool] = None) -> None:
        """创建列簇.

        Args:
            table (str):  表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            family (str): 列簇名
            ns(Optional[str], optional): 命名空间名称
            attributes (Optional[Dict[str, bytes]], optional): 列簇属性设置. Defaults to None.
            configuration (Optional[Dict[str, str]], optional): 列簇设置项. Defaults to None.
            blockSize (Optional[int], optional): 块大小设置. Defaults to None.
            bloomnFilterType (str, optional): 布隆过滤器类型.可选NONE,ROW,ROWCOL,ROWPREFIX_FIXED_LENGTH
            compressionType (str, optional): 存储压缩类型.可选LZO,GZ,NONE,SNAPPY,LZ4,BZIP2,ZSTD
            dfsReplication (Optional[int], optional): dfs复制类型. Defaults to None.
            dataBlockEncoding (str, optional): 数据块编码类型. 可选NONE,PREFIX,DIFF,FAST_DIFF,ROW_INDEX_V1
            keepDeletedCells (str, optional): 删除cell策略类型. 可选FALSE,TRUE,TTL
            maxVersions (Optional[int], optional): 数据最大版本. Defaults to None.
            minVersions (Optional[int], optional): 数据最小版本. Defaults to None.
            scope (Optional[int], optional): 范围. Defaults to None.
            timeToLive (Optional[int], optional): 数据过期时间. Defaults to None.
            blockCacheEnabled (bool, optional): 是否开启块缓存. Defaults to False.
            cacheBloomsOnWrite (bool, optional): 是否在写入时缓存布隆过滤器的结果. Defaults to False.
            cacheDataOnWrite (bool, optional): 是否在写入数据时缓存数据. Defaults to False.
            cacheIndexesOnWrite (bool, optional): 是否在写入数据时缓存index. Defaults to False.
            compressTags (bool, optional): 是否压缩tag. Defaults to False.
            evictBlocksOnClose (bool, optional): 是否关闭时驱逐块. Defaults to False.
            inMemory (bool, optional): 是否保存在内存中. Defaults to False.

        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        _bloomnFilterType = None
        if bloomnFilterType:
            _bloomnFilterType = TBloomFilterType._NAMES_TO_VALUES.get(bloomnFilterType)

        _compressionType = None
        if compressionType:
            _compressionType = TCompressionAlgorithm._NAMES_TO_VALUES.get(compressionType)
        _dataBlockEncoding = None
        if dataBlockEncoding:
            _dataBlockEncoding = TDataBlockEncoding._NAMES_TO_VALUES.get(dataBlockEncoding)

        _keepDeletedCells = None
        if keepDeletedCells:
            _keepDeletedCells = TKeepDeletedCells._NAMES_TO_VALUES.get(keepDeletedCells)

        self.client.addColumnFamily(
            tableName,
            TColumnFamilyDescriptor(
                name=family,
                attributes=attributes,
                configuration=configuration,
                blockSize=blockSize,
                bloomnFilterType=_bloomnFilterType,
                compressionType=_compressionType,
                dfsReplication=dfsReplication,
                dataBlockEncoding=_dataBlockEncoding,
                keepDeletedCells=_keepDeletedCells,
                maxVersions=maxVersions,
                minVersions=minVersions,
                scope=scope,
                timeToLive=timeToLive,
                blockCacheEnabled=blockCacheEnabled,
                cacheBloomsOnWrite=cacheBloomsOnWrite,
                cacheDataOnWrite=cacheDataOnWrite,
                cacheIndexesOnWrite=cacheIndexesOnWrite,
                compressTags=compressTags,
                evictBlocksOnClose=evictBlocksOnClose,
                inMemory=inMemory))

    def delete_family(self, family: str, table: str, *, ns: Optional[str] = None) -> None:
        """删除指定列簇.

        Args:
            table (str):  表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            family (str): 列簇名
            ns(Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: _description_
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        self.client.deleteColumnFamily(tableName, family.encode("utf-8"))

    def modify_family(self, family: str, table: str, *,
                      ns: Optional[str] = None,
                      attributes: Optional[Dict[str, bytes]] = None,
                      configuration: Optional[Dict[str, str]] = None,
                      blockSize: Optional[int] = None,
                      bloomnFilterType: Optional[str] = None,
                      compressionType: Optional[str] = None,
                      dfsReplication: Optional[int] = None,
                      dataBlockEncoding: Optional[str] = None,
                      keepDeletedCells: Optional[str] = None,
                      maxVersions: Optional[int] = None,
                      minVersions: Optional[int] = None,
                      scope: Optional[int] = None,
                      timeToLive: Optional[int] = None,
                      blockCacheEnabled: Optional[bool] = None,
                      cacheBloomsOnWrite: Optional[bool] = None,
                      cacheDataOnWrite: Optional[bool] = None,
                      cacheIndexesOnWrite: Optional[bool] = None,
                      compressTags: Optional[bool] = None,
                      evictBlocksOnClose: Optional[bool] = None,
                      inMemory: Optional[bool] = None) -> None:
        """修改已存在列簇.

        不和创建列簇合并是因为担心会有误操作.

        Args:
            table (str):  表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            family (str): 列簇名
            ns(Optional[str], optional): 命名空间名称
            attributes (Optional[Dict[str, bytes]], optional): 列簇属性设置. Defaults to None.
            configuration (Optional[Dict[str, str]], optional): 列簇设置项. Defaults to None.
            blockSize (Optional[int], optional): 块大小设置. Defaults to None.
            bloomnFilterType (str, optional): 布隆过滤器类型.可选NONE,ROW,ROWCOL,ROWPREFIX_FIXED_LENGTH
            compressionType (str, optional): 存储压缩类型.可选LZO,GZ,NONE,SNAPPY,LZ4,BZIP2,ZSTD
            dfsReplication (Optional[int], optional): dfs复制类型. Defaults to None.
            dataBlockEncoding (str, optional): 数据块编码类型. 可选NONE,PREFIX,DIFF,FAST_DIFF,ROW_INDEX_V1
            keepDeletedCells (str, optional): 删除cell策略类型. 可选FALSE,TRUE,TTL
            maxVersions (Optional[int], optional): 数据最大版本. Defaults to None.
            minVersions (Optional[int], optional): 数据最小版本. Defaults to None.
            scope (Optional[int], optional): 范围. Defaults to None.
            timeToLive (Optional[int], optional): 数据过期时间. Defaults to None.
            blockCacheEnabled (bool, optional): 是否开启块缓存. Defaults to False.
            cacheBloomsOnWrite (bool, optional): 是否在写入时缓存布隆过滤器的结果. Defaults to False.
            cacheDataOnWrite (bool, optional): 是否在写入数据时缓存数据. Defaults to False.
            cacheIndexesOnWrite (bool, optional): 是否在写入数据时缓存index. Defaults to False.
            compressTags (bool, optional): 是否压缩tag. Defaults to False.
            evictBlocksOnClose (bool, optional): 是否关闭时驱逐块. Defaults to False.
            inMemory (bool, optional): 是否保存在内存中. Defaults to False.

        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableName = TTableName(qualifier=table, ns=ns)
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 1:
                tableName = TTableName(qualifier=table)
            elif len(tabelinfo) == 2:
                tableName = TTableName(qualifier=tabelinfo[1], ns=tabelinfo[0])
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        _bloomnFilterType = None
        if bloomnFilterType:
            _bloomnFilterType = TBloomFilterType._NAMES_TO_VALUES.get(bloomnFilterType)

        _compressionType = None
        if compressionType:
            _compressionType = TCompressionAlgorithm._NAMES_TO_VALUES.get(compressionType)
        _dataBlockEncoding = None
        if dataBlockEncoding:
            _dataBlockEncoding = TDataBlockEncoding._NAMES_TO_VALUES.get(dataBlockEncoding)

        _keepDeletedCells = None
        if keepDeletedCells:
            _keepDeletedCells = TKeepDeletedCells._NAMES_TO_VALUES.get(keepDeletedCells)

        self.client.modifyColumnFamily(
            tableName,
            TColumnFamilyDescriptor(
                name=family,
                attributes=attributes,
                configuration=configuration,
                blockSize=blockSize,
                bloomnFilterType=_bloomnFilterType,
                compressionType=_compressionType,
                dfsReplication=dfsReplication,
                dataBlockEncoding=_dataBlockEncoding,
                keepDeletedCells=_keepDeletedCells,
                maxVersions=maxVersions,
                minVersions=minVersions,
                scope=scope,
                timeToLive=timeToLive,
                blockCacheEnabled=blockCacheEnabled,
                cacheBloomsOnWrite=cacheBloomsOnWrite,
                cacheDataOnWrite=cacheDataOnWrite,
                cacheIndexesOnWrite=cacheIndexesOnWrite,
                compressTags=compressTags,
                evictBlocksOnClose=evictBlocksOnClose,
                inMemory=inMemory))

    # 写操作
    def put(self, table: str, row: str, kvs: List[ColumnsValue], *,
            ns: Optional[str] = None,
            check_row: Optional[str] = None,
            check_column_full_name: Optional[str] = None,
            check_column_value: Optional[bytes] = None) -> bool:
        """插入一行数据.

        如果有设置check_row和check_column_full_name则执行checkAndPut方法,即只有当检查通过时才插入

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行名
            kvs (List[ColumnsValue]): 传入的值序列
            ns(Optional[str], optional): 命名空间名称
            check_row (Optional[str], optional): 待监测行名
            check_column_full_name (Optional[str], optional): 待检查的列,以`列簇:列名`形式表示,如果有指定`column_value`则检查指定列的值是否和`column_value`指定的相同,否则检查指定列是否存在.
            check_column_value (Optional[bytes], optional): 指定检查列应该满足的值.

        Raises:
            AttributeError: 表名格式不合法

        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        if check_row and check_column_full_name:
            check_row_bytes = check_row.encode("utf8")
            family, cloumn = check_column_full_name.split(":")
            return self.client.checkAndPut(
                table=tableNameInbytes,
                row=check_row_bytes,
                family=family.encode("utf8"),
                qualifier=cloumn.encode("utf8"),
                value=check_column_value,
                tput=TPut(row=row_bytes, columnValues=[kv.as_TColumnValue() for kv in kvs]))
        else:
            self.client.put(
                table=tableNameInbytes,
                tput=TPut(row=row_bytes, columnValues=[kv.as_TColumnValue() for kv in kvs]))
            return True

    def delete(self, table: str, row: str, *,
               ns: Optional[str] = None,
               columns: Optional[Sequence[str]] = None,
               timestamp: Optional[datetime.datetime] = None,
               deleteType: Optional[str] = None,
               attributes: Optional[Dict[str, bytes]] = None,
               durability: Optional[str] = None,
               check_row: Optional[str] = None,
               check_column_full_name: Optional[str] = None,
               check_column_value: Optional[bytes] = None) -> bool:
        """删除指定行的数据.

        如果有设置check_row和check_column_full_name则执行checkAndDelete方法,即只有当检查通过时才删除.

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行号
            ns (Optional[str], optional): 命名空间. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要删除值的列,以"列簇:列名"的形式表达. Defaults to None.
            timestamp (Optional[datetime.datetime], optional): 指定时间戳. Defaults to None.
            deleteType (Optional[str], optional): 指定删除类型,可选为DELETE_COLUMN-删除指定列,DELETE_COLUMNS-删除所有列,DELETE_FAMILY-删除指定列簇,DELETE_FAMILY_VERSION-删除指定列簇的指定版本. Defaults to DELETE_COLUMNS.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            durability (Optional[str], optional): 指定耐久方式设置,可选的有USE_DEFAULT,SKIP_WAL,ASYNC_WAL,SYNC_WAL,FSYNC_WAL.Defaults to None.
            check_row (Optional[str], optional): 待监测行名
            check_column_full_name (Optional[str], optional): 待检查的列,以`列簇:列名`形式表示,如果有指定`column_value`则检查指定列的值是否和`column_value`指定的相同,否则检查指定列是否存在.
            check_column_value (Optional[bytes], optional): 指定检查列应该满足的值.


        Raises:
            AttributeError: 表名格式不合法
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        _columns = None
        if columns:
            _columns = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]

        _timestamp = None
        if timestamp:
            _timestamp = int(timestamp.timestamp() * 1000)
        _deleteType = 1
        if deleteType:
            _deleteType = TDeleteType._NAMES_TO_VALUES.get(deleteType, 1)
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}
        _durability = None
        if durability:
            _durability = TDurability._NAMES_TO_VALUES.get(durability)

        if check_row and check_column_full_name:
            check_row_bytes = check_row.encode("utf8")
            family, cloumn = check_column_full_name.split(":")
            return self.client.checkAndDelete(
                table=tableNameInbytes,
                row=check_row_bytes,
                family=family.encode("utf8"),
                qualifier=cloumn.encode("utf8"),
                value=check_column_value,
                tdelete=TDelete(
                    row=row_bytes,
                    columns=_columns,
                    timestamp=_timestamp,
                    deleteType=_deleteType,
                    attributes=_attributes,
                    durability=_durability
                )
            )
        else:
            self.client.deleteSingle(
                table=tableNameInbytes,
                tdelete=TDelete(
                    row=row_bytes,
                    columns=_columns,
                    timestamp=_timestamp,
                    deleteType=_deleteType,
                    attributes=_attributes,
                    durability=_durability
                )
            )
            return True

    def batch_put(self, table: str, rkvs: Dict[str, List[ColumnsValue]], *, ns: Optional[str] = None) -> None:
        """批量插入

        Args:
            table(str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            rkvs (Dict[str, List[ColumnsValue]]): 行名与传入的值序列构成的字典
            ns(Optional[str], optional): 命名空间名称

        Raises:
            AttributeError: 表名格式不合法

        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")

        puts = [TPut(row=row.encode("utf-8"), columnValues=[kv.as_TColumnValue() for kv in kvs]) for row, kvs in rkvs.items()]
        self.client.putMultiple(table=tableNameInbytes, tputs=puts)

    def batch_delete(self, table: str, rows: List[str], *,
                     ns: Optional[str] = None,
                     columns: Optional[Sequence[str]] = None,
                     timestamp: Optional[datetime.datetime] = None,
                     deleteType: Optional[str] = None,
                     attributes: Optional[Dict[str, bytes]] = None,
                     durability: Optional[str] = None) -> None:
        """批量删除.

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            rows (List[str]): 要删除数据的行.
            ns (Optional[str], optional): 命名空间. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要删除值的列,以"列簇:列名"的形式表达. Defaults to None.
            timestamp (Optional[datetime.datetime], optional): 指定时间戳. Defaults to None.
            deleteType (Optional[str], optional): 指定删除类型,可选为DELETE_COLUMN-删除指定列,DELETE_COLUMNS-删除所有列,DELETE_FAMILY-删除指定列簇,DELETE_FAMILY_VERSION-删除指定列簇的指定版本. Defaults to DELETE_COLUMNS.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            durability (Optional[str], optional): 指定耐久方式设置,可选的有USE_DEFAULT,SKIP_WAL,ASYNC_WAL,SYNC_WAL,FSYNC_WAL.Defaults to None.

        Raises:
            AttributeError: _description_
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        _columns = None
        if columns:
            _columns = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]

        _timestamp = None
        if timestamp:
            _timestamp = int(timestamp.timestamp() * 1000)
        _deleteType = 1
        if deleteType:
            _deleteType = TDeleteType._NAMES_TO_VALUES.get(deleteType, 1)
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}
        _durability = None
        if durability:
            _durability = TDurability._NAMES_TO_VALUES.get(durability)
        self.client.deleteMultiple(
            table=tableNameInbytes,
            tdeletes=[TDelete(
                row=row.encode("utf8"),
                columns=_columns,
                timestamp=_timestamp,
                deleteType=_deleteType,
                attributes=_attributes,
                durability=_durability
            ) for row in rows]
        )

    def append(self, table: str, row: str, kvs: List[ColumnsValue], *,
               ns: Optional[str] = None,
               attributes: Optional[Dict[str, bytes]] = None,
               durability: Optional[str] = None,
               cellVisibility: Optional[str] = None,
               returnResults: bool = False,
               columns_decoder: Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]] = None,
               ) -> Optional[List[ColumnsValue]]:
        """追加列数据.

        在不改变原有数据的情况下追加数据,相当于get->put的原子操作.

        注意追加的是bytes,比如原本数据是`3`,追加`2`后会变成`32`

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行名
            kvs (List[ColumnsValue]): 传入的值序列
            ns (Optional[str], optional): 命名空间名称. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            durability (Optional[str], optional): 指定耐久方式设置,可选的有USE_DEFAULT,SKIP_WAL,ASYNC_WAL,SYNC_WAL,FSYNC_WAL.Defaults to None.
            cellVisibility (Optional[str], optional): cell的可视性设置. Defaults to None.
            returnResults (bool): 是否返回结果. Defaults to False.
            columns_decoder (Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]], optional): _description_. Defaults to None.

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            Optional[List[ColumnsValue]]: 结果序列
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        _columns = None
        if kvs:
            _columns = [kv.as_TColumnValue() for kv in kvs]
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}
        _durability = None
        if durability is not None:
            _durability = TDurability._NAMES_TO_VALUES.get(durability)
        _cellVisibility = None
        if cellVisibility:
            _cellVisibility = TCellVisibility(expression=cellVisibility)

        result = self.client.append(
            table=tableNameInbytes,
            tappend=TAppend(
                row=row_bytes,
                columns=_columns,
                attributes=_attributes,
                durability=_durability,
                cellVisibility=_cellVisibility,
                returnResults=returnResults)
        )
        res = []
        if result.row is not None:
            for tcv in result.columnValues:
                if columns_decoder is not None:
                    family = tcv.family.decode("utf-8")
                    col = tcv.qualifier.decode("utf-8")
                    col_name = fullcolumn(family, col)
                    decoder = columns_decoder[col_name]
                    cv = ColumnsValue(decoder=decoder)
                else:
                    cv = ColumnsValue()
                cv.initialize(tcv)
                res.append(cv)
            return res
        else:
            return None

    def increment(self, table: str, row: str, kvs: Optional[Dict[str, int]] = None, *,
                  ns: Optional[str] = None,
                  attributes: Optional[Dict[str, bytes]] = None,
                  durability: Optional[str] = None,
                  cellVisibility: Optional[str] = None
                  ) -> Dict[str, int]:
        """原子性的自增.

        相当于get->+n->put的原子操作.注意自增存储依然是在bytes上,因此并不能直接获得整型数,需要将bytes转为16进制字符串再转为10进制数据

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行名
            kvs (Optional[Dict[str, int]], optional): 列名与增量的映射关系,当增量设置为0或者为空时使用默认的1作为增量. Defaults to None.
            ns (Optional[str], optional): 命名空间名称. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            durability (Optional[str], optional): 指定耐久方式设置,可选的有USE_DEFAULT,SKIP_WAL,ASYNC_WAL,SYNC_WAL,FSYNC_WAL.Defaults to None.
            cellVisibility (Optional[str], optional): cell的可视性设置. Defaults to None.

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            Optional[List[ColumnsValue]]: 结果序列
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        _columns = None
        if kvs:
            _columns = []
            for k, v in kvs.items():
                f, c = k.split(":")
                if v:
                    _columns.append(TColumnIncrement(family=f.encode("utf-8"), qualifier=c.encode("utf-8"), amount=v))
                else:
                    _columns.append(TColumnIncrement(family=f.encode("utf-8"), qualifier=c.encode("utf-8")))
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}
        _durability = None
        if durability is not None:
            _durability = TDurability._NAMES_TO_VALUES.get(durability)
        _cellVisibility = None
        if cellVisibility:
            _cellVisibility = TCellVisibility(expression=cellVisibility)

        result = self.client.increment(
            table=tableNameInbytes,
            tincrement=TIncrement(
                row=row_bytes,
                columns=_columns,
                attributes=_attributes,
                durability=_durability,
                cellVisibility=_cellVisibility)
        )
        res = {}
        for tcv in result.columnValues:
            family = tcv.family.decode("utf-8")
            col = tcv.qualifier.decode("utf-8")
            col_name = fullcolumn(family, col)
            value = NumberDecoder(tcv.value)
            res[col_name] = value
        return res

    # 读操作
    def exists(self, table: str, row: str, *,
               ns: Optional[str] = None,
               columns: Optional[Sequence[str]] = None,
               timestamp: Optional[datetime.datetime] = None,
               timeRange: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
               maxVersions: Optional[int] = None,
               filterString: Optional[str] = None,
               attributes: Optional[Dict[str, bytes]] = None,
               authorizations: Optional[List[str]] = None,
               consistency: Optional[str] = None,
               targetReplicaId: Optional[int] = None,
               cacheBlocks: Optional[bool] = None,
               storeLimit: Optional[int] = None,
               storeOffset: Optional[int] = None,
               existence_only: Optional[bool] = None,
               filterBytes: Optional[bytes] = None
               ) -> bool:
        """查看指定行是否存在.

        Example:

            isin = cli.exists(tablefullname, row)

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行号
            ns (Optional[str], optional):命名空间. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要获取的列,以"列簇:列名"的形式表达. Defaults to None.
            timestamp (Optional[datetime.datetime], optional): 指定时间戳. Defaults to None.
            timeRange (Optional[Tuple[datetime.datetime, datetime.datetime]], optional): 指定时间范围. Defaults to None.
            maxVersions (Optional[int], optional): 指定最大版本号. Defaults to None.
            filterString (Optional[str], optional): 指定过滤字符串. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            authorizations (Optional[List[str]], optional): 指定认证信息. Defaults to None.
            consistency (Optional[str], optional): 指定一致性,可选的有STRONG,TIMELINE. Defaults to None.
            targetReplicaId (Optional[int], optional): 指定副本丢失修复方法. Defaults to None.
            cacheBlocks (Optional[bool], optional): 指定缓存块. Defaults to None.
            storeLimit (Optional[int], optional): 指定存储限制. Defaults to None.
            storeOffset (Optional[int], optional): 指定存储偏移量. Defaults to None.
            existence_only (Optional[bool], optional): 指定是否只或许已经存在的. Defaults to None.
            filterBytes (Optional[bytes], optional): 过滤字节流. Defaults to None.

        Raises:
            AttributeError: 表名格式错误

        Returns:
            List[ColumnsValue]: 结果列表
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        _columns = None
        if columns:
            _columns = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]

        _timestamp = None
        if timestamp:
            _timestamp = int(timestamp.timestamp() * 1000)
        _timeRange = None
        if timeRange:
            _timeRange = TTimeRange(minStamp=int(timeRange[0].timestamp() * 1000),
                                    maxStamp=int(timeRange[1].timestamp() * 1000))

        _filterString = None
        if filterString:
            _filterString = filterString.encode("utf-8")
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}

        _authorizations = None
        if authorizations:
            _authorizations = TAuthorization(labels=authorizations)

        _consistency = None
        if consistency:
            _consistency = TConsistency._NAMES_TO_VALUES.get(consistency)
        result = self.client.exists(
            table=tableNameInbytes,
            tget=TGet(
                row=row_bytes,
                columns=_columns,
                timestamp=_timestamp,
                timeRange=_timeRange,
                maxVersions=maxVersions,
                filterString=_filterString,
                attributes=_attributes,
                authorizations=_authorizations,
                consistency=_consistency,
                targetReplicaId=targetReplicaId,
                cacheBlocks=cacheBlocks,
                storeLimit=storeLimit,
                storeOffset=storeOffset,
                existence_only=existence_only,
                filterBytes=filterBytes
            ),
        )
        return result

    def get(self, table: str, row: str, *,
            ns: Optional[str] = None,
            columns: Optional[Sequence[str]] = None,
            timestamp: Optional[datetime.datetime] = None,
            timeRange: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
            maxVersions: Optional[int] = None,
            filterString: Optional[str] = None,
            attributes: Optional[Dict[str, bytes]] = None,
            authorizations: Optional[List[str]] = None,
            consistency: Optional[str] = None,
            targetReplicaId: Optional[int] = None,
            cacheBlocks: Optional[bool] = None,
            storeLimit: Optional[int] = None,
            storeOffset: Optional[int] = None,
            existence_only: Optional[bool] = None,
            filterBytes: Optional[bytes] = None,
            columns_decoder: Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]] = None,
            ) -> Optional[List[ColumnsValue]]:
        """获取单条数据.

        Example:

            rowcolumns = cli.get(tablefullname, row, columns_decoder=defaultdict(lambda: lambda x, y: int(x.decode("utf-8"))))

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            row (str): 行号
            ns (Optional[str], optional):命名空间. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要获取的列,以"列簇:列名"的形式表达. Defaults to None.
            timestamp (Optional[datetime.datetime], optional): 指定时间戳. Defaults to None.
            timeRange (Optional[Tuple[datetime.datetime, datetime.datetime]], optional): 指定时间范围. Defaults to None.
            maxVersions (Optional[int], optional): 指定最大版本号. Defaults to None.
            filterString (Optional[str], optional): 指定过滤字符串. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            authorizations (Optional[List[str]], optional): 指定认证信息. Defaults to None.
            consistency (Optional[str], optional): 指定一致性,可选的有STRONG,TIMELINE. Defaults to None.
            targetReplicaId (Optional[int], optional): 指定副本丢失修复方法. Defaults to None.
            cacheBlocks (Optional[bool], optional): 指定缓存块. Defaults to None.
            storeLimit (Optional[int], optional): 指定存储限制. Defaults to None.
            storeOffset (Optional[int], optional): 指定存储偏移量. Defaults to None.
            existence_only (Optional[bool], optional): 指定是否只或许已经存在的. Defaults to None.
            filterBytes (Optional[bytes], optional): 过滤字节流. Defaults to None.
            columns_decoder (Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]], optional): 列的解码器设置,可以使用defaultdict赋值一个默认解码器. Defaults to None.

        Raises:
            AttributeError: 表名格式错误

        Returns:
            List[ColumnsValue]: 结果列表
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        row_bytes = row.encode("utf8")
        _columns = None
        if columns:
            _columns = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]

        _timestamp = None
        if timestamp:
            _timestamp = int(timestamp.timestamp() * 1000)
        _timeRange = None
        if timeRange:
            _timeRange = TTimeRange(minStamp=int(timeRange[0].timestamp() * 1000),
                                    maxStamp=int(timeRange[1].timestamp() * 1000))

        _filterString = None
        if filterString:
            _filterString = filterString.encode("utf-8")
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}

        _authorizations = None
        if authorizations:
            _authorizations = TAuthorization(labels=authorizations)

        _consistency = None
        if consistency:
            _consistency = TConsistency._NAMES_TO_VALUES.get(consistency)
        result = self.client.get(
            table=tableNameInbytes,
            tget=TGet(
                row=row_bytes,
                columns=_columns,
                timestamp=_timestamp,
                timeRange=_timeRange,
                maxVersions=maxVersions,
                filterString=_filterString,
                attributes=_attributes,
                authorizations=_authorizations,
                consistency=_consistency,
                targetReplicaId=targetReplicaId,
                cacheBlocks=cacheBlocks,
                storeLimit=storeLimit,
                storeOffset=storeOffset,
                existence_only=existence_only,
                filterBytes=filterBytes
            ),
        )
        res = []
        if result.row is not None:
            for tcv in result.columnValues:
                if columns_decoder is not None:
                    family = tcv.family.decode("utf-8")
                    col = tcv.qualifier.decode("utf-8")
                    col_name = fullcolumn(family, col)
                    decoder = columns_decoder[col_name]
                    # cv.regist_decoder(decoder)
                    cv = ColumnsValue(decoder=decoder)
                else:
                    cv = ColumnsValue()
                cv.initialize(tcv)
                res.append(cv)
            return res
        else:
            return None

    def batch_get(self, table: str, rows: List[str], *,
                  ns: Optional[str] = None,
                  columns: Optional[Sequence[str]] = None,
                  timestamp: Optional[datetime.datetime] = None,
                  timeRange: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
                  maxVersions: Optional[int] = None,
                  filterString: Optional[str] = None,
                  attributes: Optional[Dict[str, bytes]] = None,
                  authorizations: Optional[List[str]] = None,
                  consistency: Optional[str] = None,
                  targetReplicaId: Optional[int] = None,
                  cacheBlocks: Optional[bool] = None,
                  storeLimit: Optional[int] = None,
                  storeOffset: Optional[int] = None,
                  existence_only: Optional[bool] = None,
                  filterBytes: Optional[bytes] = None,
                  columns_decoder: Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]] = None,
                  ) -> Dict[str, List[ColumnsValue]]:
        """获取单条数据.

        Example:

            rowcolumns = cli.get(tablefullname, row, columns_decoder=defaultdict(lambda: lambda x, y: int(x.decode("utf-8"))))

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            rows (str): 行号列表
            ns (Optional[str], optional):命名空间. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要获取的列,以"列簇:列名"的形式表达. Defaults to None.
            timestamp (Optional[datetime.datetime], optional): 指定时间戳. Defaults to None.
            timeRange (Optional[Tuple[datetime.datetime, datetime.datetime]], optional): 指定时间范围. Defaults to None.
            maxVersions (Optional[int], optional): 指定最大版本号. Defaults to None.
            filterString (Optional[str], optional): 指定过滤字符串. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 指定属性. Defaults to None.
            authorizations (Optional[List[str]], optional): 指定认证信息. Defaults to None.
            consistency (Optional[str], optional): 指定一致性,可选的有STRONG,TIMELINE. Defaults to None.
            targetReplicaId (Optional[int], optional): 指定副本丢失修复方法. Defaults to None.
            cacheBlocks (Optional[bool], optional): 指定缓存块. Defaults to None.
            storeLimit (Optional[int], optional): 指定存储限制. Defaults to None.
            storeOffset (Optional[int], optional): 指定存储偏移量. Defaults to None.
            existence_only (Optional[bool], optional): 指定是否只或许已经存在的. Defaults to None.
            filterBytes (Optional[bytes], optional): 过滤字节流. Defaults to None.
            columns_decoder (Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]], optional): 列的解码器设置,可以使用defaultdict赋值一个默认解码器. Defaults to None.

        Raises:
            AttributeError: 表名格式错误

        Returns:
            Dict[str, List[ColumnsValue]]: 结果列表
        """
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        rows_bytes = [row.encode("utf8") for row in rows]
        _columns = None
        if columns:
            _columns = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]

        _timestamp = None
        if timestamp:
            _timestamp = int(timestamp.timestamp() * 1000)
        _timeRange = None
        if timeRange:
            _timeRange = TTimeRange(minStamp=int(timeRange[0].timestamp() * 1000),
                                    maxStamp=int(timeRange[1].timestamp() * 1000))

        _filterString = None
        if filterString:
            _filterString = filterString.encode("utf-8")
        _attributes = None
        if attributes:
            _attributes = {k.encode("utf-8"): v for k, v in attributes.items()}

        _authorizations = None
        if authorizations:
            _authorizations = TAuthorization(labels=authorizations)

        _consistency = None
        if consistency:
            _consistency = TConsistency._NAMES_TO_VALUES.get(consistency)

        results = self.client.getMultiple(
            table=tableNameInbytes,
            tgets=[TGet(
                row=row_bytes,
                columns=_columns,
                timestamp=_timestamp,
                timeRange=_timeRange,
                maxVersions=maxVersions,
                filterString=_filterString,
                attributes=_attributes,
                authorizations=_authorizations,
                consistency=_consistency,
                targetReplicaId=targetReplicaId,
                cacheBlocks=cacheBlocks,
                storeLimit=storeLimit,
                storeOffset=storeOffset,
                existence_only=existence_only,
                filterBytes=filterBytes
            ) for row_bytes in rows_bytes]
        )
        res = {}
        for result in results:
            if result.row is not None:
                row_key = result.row.decode("utf-8")
                temp = []
                for tcv in result.columnValues:
                    if columns_decoder is not None:
                        family = tcv.family.decode("utf-8")
                        col = tcv.qualifier.decode("utf-8")
                        col_name = fullcolumn(family, col)
                        decoder = columns_decoder[col_name]
                        # cv.regist_decoder(decoder)
                        cv = ColumnsValue(decoder=decoder)
                    else:
                        cv = ColumnsValue()
                    cv.initialize(tcv)
                    temp.append(cv)
                res[row_key] = temp
        return res

    def scan(self, table: str, *,
             ns: Optional[str] = None,
             startRow: Optional[str] = None,
             stopRow: Optional[str] = None,
             columns: Optional[Sequence[str]] = None,
             caching: Optional[int] = None,
             maxVersions: Optional[int] = 1,
             timeRange: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
             filterString: Optional[str] = None,
             batchSize: Optional[int] = None,
             attributes: Optional[Dict[str, bytes]] = None,
             authorizations: Optional[List[str]] = None,
             reversed: Optional[bool] = None,
             cacheBlocks: Optional[bool] = None,
             colFamTimeRangeMap: Optional[Dict[str, Tuple[datetime.datetime, datetime.datetime]]] = None,
             readType: Optional[str] = None,
             limit: Optional[int] = None,
             consistency: Optional[str] = None,
             targetReplicaId: Optional[int] = None,
             filterBytes: Optional[bytes] = None,
             rowNum: Optional[int] = 20,
             columns_decoder: Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]] = None) -> Dict[str, List[ColumnsValue]]:
        """查询符合要求的行数据.

        Args:
            table (str): 表名, 表名中如果是"ns:table"的形式已经指定了命名空间则可以不填ns参数
            ns (Optional[str], optional): 命名空间. Defaults to None.
            startRow (Optional[str], optional): 起始行. Defaults to None.
            stopRow (Optional[str], optional): 结束行. Defaults to None.
            columns (Optional[Sequence[str]], optional): 想要获取的列,以"列簇:列名"的形式表达. Defaults to None.
            caching (Optional[int], optional): 缓存大小. Defaults to None.
            maxVersions (Optional[int], optional): 数据最大版本. Defaults to 1.
            timeRange (Optional[Tuple[datetime.datetime, datetime.datetime]], optional): 查找时间范围. Defaults to None.
            filterString (Optional[str], optional): 查询字符串. Defaults to None.
            batchSize (Optional[int], optional): 批大小. Defaults to None.
            attributes (Optional[Dict[str, bytes]], optional): 属性字典. Defaults to None.
            authorizations (Optional[List[str]], optional): 验证信息. Defaults to None.
            reversed (Optional[bool], optional): 排序反转. Defaults to None.
            cacheBlocks (Optional[bool], optional): 缓存块. Defaults to None.
            colFamTimeRangeMap (Optional[Dict[str, Tuple[datetime.datetime, datetime.datetime]]], optional): 列簇查找时间范围. Defaults to None.
            readType (Optional[str], optional): 阅读类型,可选DEFAULT,STREAM,PREAD. Defaults to None.
            limit (Optional[int], optional): 长度限制. Defaults to None.
            consistency (Optional[str], optional): 指定一致性,可选的有STRONG,TIMELINE. Defaults to None.
            targetReplicaId (Optional[int], optional): 指定副本丢失修复方法.. Defaults to None.
            filterBytes (Optional[bytes], optional): 过滤字节流. Defaults to None.
            rowNum (Optional[int], optional): 一次获取的行数量. Defaults to 20.
            columns_decoder (Optional[Mapping[str, Callable[[bytes, Optional[bytes]], Any]]], optional): _description_. Defaults to None.

        Raises:
            AttributeError: 表名格式不合法

        Returns:
            Dict[str, List[ColumnsValue]]: 结果字典
        """

        # TScan
        if ns is not None:
            tableNameInbytes = f"{ns}:{table}".encode("utf8")
        else:
            tabelinfo = table.split(":")
            if len(tabelinfo) == 2:
                tableNameInbytes = table.encode("utf8")
            else:
                raise AttributeError(f"parameter table syntax error: {table}")
        scan_dict: Dict[str, Any] = {}
        if columns:
            scan_dict["columns"] = [TColumn(family=c.split(":")[0], qualifier=c.split(":")[1]) if len(c.split(":")) == 2 else TColumn(family=c) for c in columns]
        if caching:
            scan_dict["caching"] = caching
        if maxVersions:
            scan_dict["maxVersions"] = maxVersions
        if timeRange:
            scan_dict["timeRange"] = TTimeRange(
                minStamp=int(timeRange[0].timestamp() * 1000),
                maxStamp=int(timeRange[1].timestamp() * 1000))
        if filterString:
            scan_dict["filterString"] = filterString.encode("utf8")
        if attributes:
            scan_dict["attributes"] = {k.encode("utf8"): v for k, v in attributes.items()}
        if authorizations:
            scan_dict["authorizations"] = TAuthorization(labels=authorizations)
        if reversed is not None:
            scan_dict["reversed"] = reversed
        if cacheBlocks is not None:
            scan_dict["cacheBlocks"] = cacheBlocks
        if colFamTimeRangeMap:
            scan_dict["colFamTimeRangeMap"] = {k.encode("utf-8"): TTimeRange(
                minStamp=int(v[0].timestamp() * 1000),
                maxStamp=int(v[1].timestamp() * 1000)) for k, v in colFamTimeRangeMap.items()}
        if readType:
            scan_dict["readType"] = TReadType._NAMES_TO_VALUES.get(readType)
        if consistency:
            scan_dict["consistency"] = TConsistency._NAMES_TO_VALUES.get(consistency)
        if targetReplicaId:
            scan_dict["targetReplicaId"] = targetReplicaId
        if filterBytes:
            scan_dict["filterBytes"] = filterBytes
        if batchSize:
            scan_dict["batchSize"] = batchSize
        if limit:
            scan_dict["limit"] = limit
        if startRow:
            scan_dict["startRow"] = startRow.encode("utf8")
        if stopRow:
            scan_dict["stopRow"] = stopRow.encode("utf8")
        results = []
        while True:
            lastResult = None
            # getScannerResults会自动完成open,close 等scanner操作，HBase增强版必须使用此方法进行范围扫描
            currentResults = self.client.getScannerResults(
                table=tableNameInbytes,
                tscan=TScan(**scan_dict),
                numRows=rowNum,
            )
            for result in currentResults:
                results.append(result)
                lastResult = result
            # 如果一行都没有扫描出来，说明扫描已经结束，我们已经获得startRow和stopRow之间所有的result
            if lastResult is None:
                break
            # 如果此次扫描是有结果的，我们必须构造一个比当前最后一个result的行大的最小row，继续进行扫描，以便返回所有结果
            else:
                nextStartRow = _createClosestRowAfter(lastResult.row)
                scan_dict["startRow"] = nextStartRow
        res = {}
        for result in results:
            row_key = result.row.decode("utf-8")
            temp = []
            for tcv in result.columnValues:
                if columns_decoder is not None:
                    family = tcv.family.decode("utf-8")
                    col = tcv.qualifier.decode("utf-8")
                    col_name = fullcolumn(family, col)
                    decoder = columns_decoder[col_name]
                    # cv.regist_decoder(decoder)
                    cv = ColumnsValue(decoder=decoder)
                else:
                    cv = ColumnsValue()
                cv.initialize(tcv)
                temp.append(cv)
            res[row_key] = temp
        return res
