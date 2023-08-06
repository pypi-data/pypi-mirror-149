class BaseSeeding:

    def __init__(self, rollback: bool = False):
        if rollback:
            self.rollback()
        else:
            self.seeding()

    def seeding(self):
        """ Seeding data in project """
        pass

    def rollback(self):
        """ Remove seeded data from project  """
        pass

    def batch_handle(self):
        """ TODO: handling of big count of item from DB """
        pass
