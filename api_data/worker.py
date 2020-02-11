import luigi
from luigi.contrib.postgres import PostgresTarget

class Worker(luigi.Task):
    
    def requires(self):
        return None
    
    def 