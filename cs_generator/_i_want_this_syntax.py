

class Resolver():
    slots = []
    

class slot():
    ...
    

class SomeBuilder():
    def pass_to_one():
        ...
        
    def to_many():
        ...

class Router():
    def by(self, path: str):
        return Router()

    def send_to(self, type: type[SomeBuilder]):
        return Router()
    
class DiskFileInstr(SomeBuilder):
    def pass_to_one(b: SomeBuilder):
        pass
    
    def to_many(b: SomeBuilder):
        pass



class SomeOtherInstr(SomeBuilder):
    def pass_to_one(b: SomeBuilder):
        pass
    
    def to_many(b: SomeBuilder):
        pass



####### SOME SAMPLE CODE HERE --- just sketching #######


# Router().by("/somepath").send_to(DiskFileInstr)