# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class TencentMysqlPipeline(object):
    # 初始化
    def __init__(self):
        try:
            self.conn = MySQLdb.connect('192.168.2.102', 'lx', '123456', 'pachong', charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception, e:
            print '数据库连接失败'
            print str(e)

    def process_item(self, item, spider):
        print dict(item)
        sql = 'insert into tencent(name,type,location,num,zhize,yaoqiu,url) values(%s,%s,%s,%s,%s,%s,%s) on duplicate key update name=values(name),type=values(type),location=values(location),num=values(num), zhize=values(zhize),yaoqiu=values(yaoqiu)'
        # print sql
        try:
            self.cursor.execute(sql, (item['name'], item['type'], item['location'], item['num'], item['zhize'], item['yaoqiu'],item['url'],))
            self.conn.commit()
        except Exception, e:
            print '插入失败',str(e)
        return item

    # 最后调用
    def close_spider(self):
        self.cursor.close()
        self.conn.close()

class ZhaopinPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        print '''

        进入pipeline

        '''
    # 方法名是固定的
    @classmethod  # 类方法 静态方法 先加载类静态方法，优先__init__执行
    def from_settings(cls, settings):
        db_config = dict(
            host=settings['MYHOST'],
            user=settings['MYUSER'],
            passwd=settings['MYPASSWORD'],
            db=settings['MYDB'],
            charset='utf8',
            #cursorclass=MySQLdb.cursors.DictCursor,
            #use_unicode = True,
        )
        # 数据库连接池
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_config)
        adbapi.Connection(dbpool)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 异步插入操作
        print '进入 process item'
        print dict(item)
        try:
            query = self.dbpool.runInteraction(self.insert, item)
            #query = self.dbpool._runOperation(self.insert, item)
        except Exception ,e:
            print e
        print '退出 process item'
        query.addErrback(self.handle_error)
        return item

    # 插入操作
    def insert(self, cursor, item):
        print '进入 insert'
        sql = 'insert into tencent(name,type,location,num,zhize,yaoqiu,url) values(%s,%s,%s,%s,%s,%s,%s) on duplicate key update name=values(name),type=values(type),location=values(location),num=values(num), zhize=values(zhize),yaoqiu=values(yaoqiu)'
        print sql
        cursor.execute(sql, (item['name'], item['type'], item['location'], item['num'], item['zhize'], item['yaoqiu'],item['url'],))
    # 错误处理函数
    def handle_error(self, error):
        print '进入错误处理'
        print str(error)
