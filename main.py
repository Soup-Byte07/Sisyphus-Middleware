from core.sisyphus import Sisyphus

from mods.example_pxy.example_pxy import ExampleMod
from mods.hof.hof import Hof



s = Sisyphus()
_ExampleMod = ExampleMod(s)
_Hof = Hof(s)

s.run()
