from src.Model import Subject


class Schedule:
    def __init__(self,
                 groupName: str,
                 numberOfWeek: int,
                 subject: Subject,
                 day: str,
                 numberOfSubject: int):
        self.groupName = groupName
        self.numberOfWeek = numberOfWeek
        self.subject = subject
        self.day = day
        self.numberOfSubject = numberOfSubject
