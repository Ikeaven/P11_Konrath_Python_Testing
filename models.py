class Booking:

    booking_list = []

    def __init__(self, club_name, competition_name, nb_places_booked):
        self.club_name: str = str(club_name)
        self.competition_name: str = str(competition_name)
        self.nb_places_booked: int = int(nb_places_booked)
        Booking.booking_list.append(self)

    @classmethod
    def already_booked(cls, club, competition):
        for booked in cls.booking_list:
            if (booked.club_name == club) and (booked.competition_name == competition):
                return booked
        return None

    # @already_booked.setter
    # def foo(self, value):
    #     self._foo = value
