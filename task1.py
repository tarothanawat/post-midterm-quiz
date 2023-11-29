class Candidate:
    def __init__(self, name:str, age:int, followers:int = 0, genre:str = "unknown"):
        if not isinstance(name, str):
            raise TypeError
        if not isinstance(age, int):
            raise TypeError
        if not isinstance(followers, int):
            raise TypeError
        if not isinstance(genre, str):
            raise TypeError
        if not age > 0:
            raise ValueError
        if not followers > 0:
            raise ValueError
        if name == '' or name.isspace():
            raise ValueError
        if genre == '' or genre.isspace():
            raise ValueError
        self.__name = name
        self.__age = age
        self.__followers = followers
        self.__genre = genre
        self.__status = "new"


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status:str):
        statusdefault = ["new", "qualified", "accepted", "rejected"]
        if status == '' or status.isspace():
            raise ValueError
        if not isinstance(status, str):
            raise TypeError
        if status not in statusdefault:
            raise ValueError

        self.__status = status

    def __str__(self):
        return f"Candidate: {self.__name}, {self.__age}, {self.__followers}, {self.__genre} ({self.__status})"


a = Candidate("Kenny", 18, 2000, "dog game")
a.status = "new"
print(a)