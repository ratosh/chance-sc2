import random

import sc2
# noinspection PyUnresolvedReferences
from chance.strats.protoss.cannon_rush import CannonRush
from chance.strats.random.worker_rush import WorkerRush
from chance.strats.strat import Strat
# noinspection PyUnresolvedReferences
from chance.strats.zerg.zerg_rush import ZergRush
from sc2 import Race


class Chance(sc2.BotAI):
    RANDOM_STRATS = ['WorkerRush', ]

    TERAN_STRATS = [] + RANDOM_STRATS
    ZERG_STRATS = ['ZergRush', ] + RANDOM_STRATS
    PROTOSS_STRATS = ['CannonRush', ] + RANDOM_STRATS

    AVAILABLE_STRATS = {
        Race.Terran: TERAN_STRATS,
        Race.Zerg: ZERG_STRATS,
        Race.Protoss: PROTOSS_STRATS,
    }

    def __init__(self):
        super().__init__()
        self.iteration = None
        self.strat = None

    def select_strat(self):
        self.strat = self._get_strat(random.choice(self.AVAILABLE_STRATS[self.race]))

    def _get_strat(self, strat_class: str) -> Strat:
        # constructs the class based on the classes name as a string
        return globals()[strat_class](self)

    async def on_step(self, iteration):
        self.iteration = iteration

        if self.iteration == 0:
            self.select_strat()

        await self.strat.on_step()

