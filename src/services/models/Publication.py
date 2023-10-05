from datetime import datetime
class Publication():
  def __init__(self, id, title, description, img_url, id_org, id_user) -> None:
    self.id = id
    self.title = title
    self.description = description
    self.img_url = img_url
    self.id_org = id_org
    self.id_user = id_user
    self.likes = 0
    self.comments = 0
    self.date = datetime.now()

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "img_url": self.img_url,
      "id_org": self.id_org,
      "id_user": self.id_user,
      "likes": self.likes,
      "comments": self.comments,
      "date": self.date
    }
