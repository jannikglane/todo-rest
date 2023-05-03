class Entry:
  def __init__(self, id, name, description, user_id, list_id):
    self.id = id
    self.name = name
    self.description = description
    self.user_id = user_id
    self.list_id = list_id
    
class NewEntryDto:
  def __init__(self, name, description):
    self.name = name
    self.description = description