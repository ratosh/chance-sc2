import random

from chance.strats.strat import Strat


class CannonRush(Strat):
    async def on_step(self):
        if not self._bot.townhalls:
            # Attack with all workers if we don't have any nexuses left, attack-move on enemy spawn (doesn't work on 4 player map) so that probes auto attack on the way
            for worker in self._bot.workers:
                self._bot.do(worker.attack(self._bot.enemy_start_locations[0]))
            return
        else:
            nexus = self._bot.townhalls.random

        # Make probes until we have 16 total
        if self._bot.workers.amount < 16 and nexus.is_idle:
            if self._bot.can_afford(PROBE):
                self._bot.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)

        # If we have no pylon, build one near starting nexus
        elif not self._bot.structures(PYLON) and self._bot.already_pending(PYLON) == 0:
            if self._bot.can_afford(PYLON):
                await self._bot.build(PYLON, near=nexus)

        # If we have no forge, build one near the pylon that is closest to our starting nexus
        elif not self._bot.structures(FORGE):
            pylon_ready = self._bot.structures(PYLON).ready
            if pylon_ready:
                if self._bot.can_afford(FORGE):
                    await self._bot.build(FORGE, near=pylon_ready.closest_to(nexus))

        # If we have less than 2 pylons, build one at the enemy base
        elif self._bot.structures(PYLON).amount < 2:
            if self._bot.can_afford(PYLON):
                pos = self._bot.enemy_start_locations[0].towards(self._bot.game_info.map_center,
                                                                 random.randrange(8, 15))
                await self._bot.build(PYLON, near=pos)

        # If we have no cannons but at least 2 completed pylons, automatically find a placement location and build them near enemy start location
        elif not self._bot.structures(PHOTONCANNON):
            if self._bot.structures(PYLON).ready.amount >= 2 and self._bot.can_afford(PHOTONCANNON):
                pylon = self._bot.structures(PYLON).closer_than(20, self._bot.enemy_start_locations[0]).random
                await self._bot.build(PHOTONCANNON, near=pylon)

        # Decide if we should make pylon or cannons, then build them at random location near enemy spawn
        elif self._bot.can_afford(PYLON) and self._bot.can_afford(PHOTONCANNON):
            # Ensure "fair" decision
            for _ in range(20):
                pos = self._bot.enemy_start_locations[0].random_on_distance(random.randrange(5, 12))
                building = PHOTONCANNON if self._bot.state.psionic_matrix.covers(pos) else PYLON
                await self._bot.build(building, near=pos)
