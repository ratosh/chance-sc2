from chance.strats.strat import Strat
from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sharpy.general.extended_power import ExtendedPower
from sharpy.managers.core.roles import UnitTask
from sharpy.plans import BuildOrder, SequentialList
from sharpy.plans.acts import *
from sharpy.plans.acts.terran import AutoDepot
from sharpy.plans.tactics import *
from sharpy.plans.tactics.terran import LowerDepots, ManTheBunkers, Repair, ContinueBuilding, PlanZoneGatherTerran


class AllInPlanZoneAttack(PlanZoneAttack):

    def _start_attack(self, power: ExtendedPower, attackers: Units):
        self.retreat_multiplier = 0  # never retreat, never surrender

        for unit in self.cache.own(UnitTypeId.SCV).closest_n_units(self.knowledge.zone_manager.enemy_start_location, 5):
            self.knowledge.roles.set_task(UnitTask.Attacking, unit)

        return super()._start_attack(power, attackers)


class FiveRax(Strat):
    async def create_plan(self) -> BuildOrder:
        return BuildOrder([
            SequentialList([
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 15),
                GridBuilding(UnitTypeId.SUPPLYDEPOT, 1),
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 17),
                GridBuilding(UnitTypeId.BARRACKS, 1),
                GridBuilding(UnitTypeId.SUPPLYDEPOT, 2),
                GridBuilding(UnitTypeId.BARRACKS, 5),
                GridBuilding(UnitTypeId.SUPPLYDEPOT, 3),
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 18),
                BuildOrder([
                    AutoDepot(),
                    ActUnit(UnitTypeId.MARINE, UnitTypeId.BARRACKS, 200),
                ])

            ]),
            SequentialList(
                [
                    PlanCancelBuilding(),
                    LowerDepots(),
                    PlanZoneDefense(),
                    DistributeWorkers(),
                    ManTheBunkers(),
                    Repair(),
                    ContinueBuilding(),
                    PlanZoneGatherTerran(),
                    AllInPlanZoneAttack(10),
                    PlanFinishEnemy(),
                ])
        ])
