# Superclass for  Datalakes
class Datalake:
    def __init__(self, datalake_name):
        self._datalake_name = datalake_name
    
    @property
    def datalake_name(self) -> str:
        return self._datalake_name