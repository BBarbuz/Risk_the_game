class Territories:
    def __init__(self, id_terr, name_terr, force, terr_own):
        self.id_terr = id_terr          # territory id
        self.name_terr = name_terr      # name of territory
        self.force = force              # force count in this territory
        self.terr_own = terr_own

    def set_force(self, force):
        self.force = self.force + force

    def set_terr_own(self, terr_own):
        self.terr_own = terr_own

    def get_terr_own(self):
        return self.terr_own
