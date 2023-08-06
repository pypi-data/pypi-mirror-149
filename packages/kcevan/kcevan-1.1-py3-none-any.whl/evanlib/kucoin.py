# _*_ coding: UTF-8 _*_ 
from hdfs import InsecureClient
import pandas as pd
from livy import LivySession, SessionKind
from requests.auth import HTTPBasicAuth
import random

class kcspark():
    def __init__(self,host,user,password,**kw):
        self.host=host
        self.user=user
        self.password=password
        self.client = InsecureClient(f'http://{host}:50070', user='livy')
        for k,w in kw.items():
            setattr(self,k,w)
            
    def hdfs2df(self,path):
        fname=None
        df=pd.DataFrame()
        for f in self.client.list(path):
            if f.split('.')[-1]=='csv':
                fname=f
        if fname is not None:
            with self.client.read(f'{path}/{fname}', encoding = 'utf-8') as reader:
                try:
                    df = pd.read_csv(reader)
                except pd.errors.EmptyDataError:
                    print('查询结果为空！')
        return df            
    def sql2df(self,sql):
        seq=''.join(random.choices(list('ABCDEFGHJKLMNPQRSTUVWXYZ12345678901234567890'), k=5))
        livyname=f"""{self.user}川A{seq}"""   
        LIVY_SERVER = f"http://{self.host}:8998"
        auth = HTTPBasicAuth(self.user,self.password)
        path=f'hdfs:///user/{self.user}/{seq}'
        df_=pd.DataFrame()
        try:
            with LivySession.create(LIVY_SERVER,
                                    auth=auth,
                                    verify=False,
                                    name=livyname,
                                    driver_memory="10g"
                                   ) as session:
                    session.run(f"""df=spark.sql('''{sql}''')""")
                    session.run(f"""df.repartition(1).write.format('com.databricks.spark.csv').mode('overwrite').save('{path}',header = 'true',emptyValue='')""")
                    df_=self.hdfs2df(path[7:])
        except:
            print('查询失败')
            df_='查询失败'
        self.client.delete(path[7:],recursive=True)
        return df_
if __name__ == '__main__':
    pass
