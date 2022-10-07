class Alert:
    def __init__(self, _id=None, _priority=None, _doctor=None, _user=None, _createdTime=None, _responseTime=None,
                 _content=None, _response=None):
        self.doctor = _doctor
        self.id = _id
        self.user = _user
        self.createdTime = _createdTime
        self.responseTime = _responseTime
        self.content = _content
        self.response = _response
        self.priority = _priority

    def fromdict(self, d):
        self.doctor = d['doctor']
        self.user = d['user']
        self.id = d['id']
        self.createdTime = d['createdTime']
        self.responseTime = d['responseTime']
        self.content = d['content']
        self.response = d['response']
        self.priority = d['priority']

    def todict(self):
        d = {"responseTime": self.responseTime,
             "createdTime": self.createdTime,
             "user": self.user,
             "id": self.id,
             "priority": self.priority,
             "doctor": self.doctor,
             "content": self.content,
             "response": self.response
             }
        return d