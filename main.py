from core.sisyphus import Sisyphus

from mods.example_pxy.example_pxy import ExampleMod

s = Sisyphus()
_ExampleMod = ExampleMod(s)

s.run()
