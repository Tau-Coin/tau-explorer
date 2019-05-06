import pymysql
from pprint import pprint

class Tx(object):
    def db_connect(self,sql):
        try:
            db = pymysql.connect("host", "user", "password","db")
        except Exception as e:
            print(e)
            db = None
        if db:
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                datas = cursor.fetchall()
            except Exception as e:
                print(e)
                datas = None
            if datas:
                cols = [col[0] for col in cursor.description]
                datas = [dict(zip(cols, list(data))) for data in list(datas)]
                for data in datas:
                    if "txtime" in data:
                        data["txtime"] = data["txtime"].strftime("%Y-%m-%d %H:%M:%S")
            cursor.close()
            db.close()
            return datas

    def lastest_txs_100(self):
        sql = 'select * from tauchain order by txtime desc limit 100;'
        datas = self.db_connect(sql)
        return datas

    def get_height(self, height):
        sql = 'select * from  tauchain where blockheight={};'.format(height)
        datas = self.db_connect(sql)
        if not datas:
            sql = 'select * from taublocks where blockheight={};'.format(height)
            datas = self.db_connect(sql)
        return datas

    def get_block(self, blockhash):
        sql = 'select * from  tauchain where blockhash="{}";'.format(blockhash)
        datas = self.db_connect(sql)
        if not datas:
            sql= 'select * from taublocks where blockhash="{}";'.format(blockhash)
            datas = self.db_connect(sql)
        nextblock_sql = 'select blockhash from taublocks where blockheight={};'.format(int(datas[0]["blockheight"])+1)
        next_blockhash = self.db_connect(nextblock_sql)
        if next_blockhash:
            datas[0]["nextblockhash"] = next_blockhash[0].get("blockhash")
        else:
            datas[0]["nextblockhash"] = None
        return datas

    def get_txid(self, txhash):
        sql = 'select * from tauchain where txhash="{}";'.format(txhash)
        datas = self.db_connect(sql)
        return datas

    def get_address(self, address):
        mining_sql = 'select sum(fee) as miningIncome from tauchain where forger="{}";'.format(address)
        mining_data = self.db_connect(mining_sql)
        minings_sql = 'select *  from tauchain where forger="{}" order by txtime desc limit 100;'.format(address)
        minings_datas = self.db_connect(minings_sql)
        send_sql = 'select * from tauchain where sender="{}" order by txtime desc limit 100;'.format(address)
        send_datas = self.db_connect(send_sql)
        received_sql = 'select * from tauchain where receiver="{}" order by txtime desc limit 100;'.format(address)
        recieved_datas = self.db_connect(received_sql)
        datas = {
            "sent": send_datas,
            "received": recieved_datas,
            "miningIncome": mining_data[0],
            "miningDetail": minings_datas
        }
        return datas

    def total_txs(self):
        txs_sql = 'select count(txhash) as total_txs from tauchain;'
        blocks_sql = 'select max(blockheight) as total_blocks from taublocks;'
        txs_datas = self.db_connect(txs_sql)
        blocks_data = self.db_connect(blocks_sql)
        datas = {
            "total_txs": txs_datas[0]["total_txs"],
            "total_blocks": blocks_data[0]["total_blocks"]
        }
        return datas

    def top_100(self):
        sql = 'select receiver, sum(amount) as total from tauchain group by receiver order by total desc limit 100;'
        datas = self.db_connect(sql)
        return datas
        

if __name__ == "__main__":
    tx = Tx()
    #datas = tx.lastest_txs_100()
    #datas = tx.get_height("163")
    datas = tx.get_block("d0f944f598dc2880de6ede8ca617e5aae59fdb55")
    #datas = tx.get_txid("174c4939f69e93d6faf08750c6216cce9677c0003802bdff60e6af5a683286ad")
    #datas= tx.get_address("TEcy6L8B4Tss5MF13RCzAGHmhfduT1HTyd")
    #datas= tx.get_address("TN3jW3AZq5jD9zpvAeULwT3GYPEi8bo11s")
    #datas = tx.get_heigth("20")
    #datas = tx.total_txs()
    #datas = tx.top_100()
    pprint(datas[0])
