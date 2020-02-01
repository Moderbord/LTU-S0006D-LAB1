class EntityManager:

    def __init__(self):
        self.entityMap = {}
    
    def Register(self, entity):
        self.entityMap[entity.GetID()] = entity

    def GetFromID(self, ID):
        return self.entityMap[ID]