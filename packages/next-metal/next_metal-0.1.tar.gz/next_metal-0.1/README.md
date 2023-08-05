# Repository Patten for Python

## How to use

Init callback
```py
import metal

def call_back(query:str, args, context:str):
    return 200

metal.init(call_back)
```
Declare the query by decortor
```py
import metal

class FooDao():
    @metal.query(query = "select * from test where id = ?")
    def find_by_id(self, p1):
        return
```
Once DAO is called, callback will fired
```py
daoFoo = FooDao()
rt = self.daoFoo.find_by_id_2(123)
```
