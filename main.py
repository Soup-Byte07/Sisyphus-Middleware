from core.sisyphus import Sisyphus
from mods.example_pxy.example_pxy import ExampleMod



if __name__ == "__main__":
    s = Sisyphus(8000)

    _ExampleMod = ExampleMod()
    s.register(_ExampleMod.get_factory().router)

    s.run()
