from objects.gardening.gardening_component_crop_fruit import GardeningCropFruitComponent
class TunableGardeningComponentVariant(TunableVariant):

    def __init__(self, **kwargs):
        super().__init__(fruit_component=GardeningFruitComponent.TunableFactory(), plant_component=GardeningPlantComponent.TunableFactory(), crop_fruit_component=GardeningCropFruitComponent.TunableFactory(), crop_plant_component=GardeningCropPlantComponent.TunableFactory(), shoot=GardeningShootComponent.TunableFactory(), locked_args={'disabled': None}, default='disabled', **kwargs)
