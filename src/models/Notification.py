from datetime import *
from src.db.MyDBConnection import MyDBConnection
from src.models.User import User


class Notification:

    """
    This class represents the notification that the user receive when the date of one of his favorite show next episode
    is getting close.
    """

    def __init__(self, id_user: int, id_show: int, num_season: int, num_ep: int, date_ep: datetime=None,
                 new_id: int=None, seen_flag: bool=False):
                self.__set_id(new_id)
                self.__set_id_show(id_show)
                self.__set_id_user(id_user)
                self.__set_seen_flag(seen_flag)
                self.__set_num_ep(num_ep)
                self.__set_num_season(num_season)
                self.__set_date_ep(date_ep)

    @property
    def id(self):
        return self.__id

    def __set_id(self, new_id: int):
        if type(new_id) is not int and new_id is not None:
            raise TypeError("Id should be an integer")
        else:
            self.__id = new_id

    @property
    def id_show(self):
        return self.__id_show

    def __set_id_show(self, id_show: int):
        if type(id_show) is not int:
            raise TypeError("Show id should be an integer")
        else:
            self.__id_show = id_show

    @property
    def id_user(self):
        return self.__id_user

    def __set_id_user(self, id_user: int):
        if type(id_user) is not int:
            raise TypeError("User id should be an integer")
        else:
            self.__id_user = id_user
            
    @property
    def seen_flag(self):
        return self.__seen_flag

    def __set_seen_flag(self, seen_flag: bool):
        if type(seen_flag) is not bool:
            raise TypeError("Seen flag should be a boolean")
        else:
            self.__seen_flag = seen_flag

    @property
    def num_ep(self):
        return self.__num_ep

    def __set_num_ep(self, num_ep: int):
        if type(num_ep) is not int:
            raise TypeError("Episode number should be an integer")
        else:
            self.__num_ep = num_ep

    @property
    def num_season(self):
        return self.__num_season

    def __set_num_season(self, num_season: int):
        if type(num_season) is not int:
            raise TypeError("Episode number should be an integer")
        else:
            self.__num_season = num_season

    @property
    def date_ep(self):
        return self.__date_ep

    def __set_date_ep(self, date_ep: datetime):
        if type(date_ep) is not datetime and date_ep is not None:
            raise TypeError("Date of episode should be a datetime")
        else:
            self.__date_ep = date_ep

    def set_as_seen(self):
        if self.seen_flag == False:
            self.__set_seen_flag(True)

    def set_as_not_seen(self):
        if self.seen_flag == True:
            self.__set_seen_flag(False)

    def create_notification_in_bdd(self, my_db: MyDBConnection):
        my_db.exec_one("""
                INSERT INTO notification (id_user, id_show, seen_flag) VALUES 
                ((?), (?), (?))""", (
            self.id_user, self.id_show, self.seen_flag
        ))
        new_notif = Notification.retrieve_notification_from_bdd(self.id_user, self.id_show, my_db)
        self.__set_id(new_notif.id)

    @classmethod
    def retrieve_notification_from_bdd(cls, id_user: int, id_show: int, my_db: MyDBConnection):
        notification_res = my_db.exec_one("SELECT * from `notification` WHERE id_user = (?) AND id_show = (?)",
                                          (id_user, id_show))
        if not notification_res:
            return None
        id_user, id_show, seen_flag, new_id = notification_res[0]
        return Notification(id_user, id_show, id=new_id)

    def update_notification_in_bdd(self, my_db: MyDBConnection, num_season: int = None, num_ep: int = None,
                                   date_ep: datetime=None, seen_flag: bool=None):
        if num_season is not None:
            self.__set_num_season(num_season)
        if num_ep is not None:
            self.__set_num_ep(num_ep)
        if date_ep is not None:
            self.__set_date_ep(date_ep)
        if seen_flag is not None:
            self.__set_seen_flag(seen_flag)
        my_db.exec_one("UPDATE NOTIFICATION SET id_user=(?), id_show=(?), seen_flag=(?), WHERE id=(?)",
                       (self.id_user, self.id_show, self.seen_flag, self.id)
                       )

    def delete_notification_in_bdd(self, my_db: MyDBConnection):
        my_db.exec_one("DELETE from `notification` WHERE `notification`.id = (?)", (self.id))
        del self

    @classmethod
    def get_notification_from_user(cls, user: User, my_db: MyDBConnection):
        if User is None:
            raise TypeError("The user from which we want to get notifications is not valid")
        else:
            list_notifications = my_db.exec_one("SELECT * from `notification` WHERE id_user = (?)", (user.id))
            return list_notifications