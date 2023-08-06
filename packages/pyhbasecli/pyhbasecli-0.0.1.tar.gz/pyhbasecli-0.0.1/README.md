# pyhbasecli

基于thrift2的hbase客户端

+ author: hsz

keywords: hbase,thrift

## 特性

+ 可以连接处理阿里云hbase
+ 使用的是[thrift2版本](https://github.com/apache/hbase/blob/master/hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift2/hbase.thrift?spm=a2c6h.12873639.article-detail.6.216d35d1BSozCF&file=hbase.thrift)
+ 支持http方式连接
+ python友好的接口设计

## 安装

```bash
pip install pyhbasecli
```

## 例子

```python
with HBaseCli(
                url=URL,
                headers={"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}) as client:
    nsinfo = client.show_namespaces()
    print(nsinfo)

```

## todo

+ 增加socket方式连接
+ 增加对Mutation的支持
