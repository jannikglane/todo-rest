class List:
  def __init__(self, id, name, entries):
    self.id = id
    self.name = name
    self.entries = entries
    
class NewListDto:
  def __init__(self, id, name):
    self.id = id
    self.name = name