

# Esta clase va a sacar lo peor de nosotros mismos, me temo
class AI():
    def __init__(self, artificialPlayer):
        self.data = artificialPlayer

    def make_commands(self):
        units, structures, resources = self.data.get_info()

        