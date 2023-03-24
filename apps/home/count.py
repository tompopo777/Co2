import pandas as pd
from IPython.core.display import display
from django.db.models import Sum, F, Value, CharField
from django.db.models.functions import Cast
from decimal import *
from .models import *

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)

getcontext().prec = 4

# 發電機
generators = pd.DataFrame(list(emergency_generators.objects.values('did').annotate(
    device_name=Value('柴油發電機', output_field=CharField(max_length=20)),
    fuel_type=Value('柴油', output_field=CharField(max_length=20)),
    sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                       F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4)),
)))
generators = generators.drop(columns=['did'])
display(generators.to_string(index=False))

# 燃燒設備
combustion = pd.DataFrame(list(combustion_equipment.objects.values('device_name', 'fuel_type').annotate(
    process_area=Value('固定式燃燒', output_field=models.CharField(max_length=50)),
    sum_count=Cast(Sum(F('fuel_january') + F('fuel_february') + F('fuel_march') + F('fuel_april') + F('fuel_may') + F('fuel_june') + F('fuel_july') + F('fuel_august') + F('fuel_september') + F('fuel_october') + F('fuel_november') + F('fuel_december')) * 1.818 / 1000,
                   output_field=models.DecimalField(max_digits=20, decimal_places=4)),
).order_by('device_name', 'fuel_type')))
display(combustion.to_string(index=False))

# 公務車
official_car = pd.DataFrame(list(official_car.objects.values('vehicle_type', 'fuel_type').annotate(
    sum_count=Cast(Sum(F('january') + F('february') + F('march') + F('april') + F('may') + F('june') +
                       F('july') + F('august') + F('september') + F('october') + F('november') + F('december')) / 1000, output_field=models.DecimalField(max_digits=20, decimal_places=4))
).order_by('vehicle_type', 'fuel_type')))
display(official_car.to_string(index=False))

# 逸散(冰箱~其他設備)
refrigerator = pd.DataFrame(list(refrigerator.objects.values("device_name", "refrigerant_type", "filling_volume")))
airconditioner = pd.DataFrame(list(airconditioner.objects.values("device_name", "refrigerant_type", "filling_volume")))
vehicle = pd.DataFrame(list(vehicle.objects.values("device_name", "refrigerant_type", "filling_volume")))
water_dispenser = pd.DataFrame(list(water_dispenser.objects.values("device_name", "refrigerant_type", "filling_volume")))
ice_water_dispenser = pd.DataFrame(list(ice_water_dispenser.objects.values("device_name", "refrigerant_type", "filling_volume")))
ice_maker = pd.DataFrame(list(ice_maker.objects.values("device_name", "refrigerant_type", "filling_volume")))
other_device = pd.DataFrame(list(other_device.objects.values("device_name", "refrigerant_type", "filling_volume")))
refrigerant = pd.concat([refrigerator, airconditioner, vehicle, water_dispenser, ice_water_dispenser, ice_maker, other_device])
calculate = refrigerant.groupby(["device_name", "refrigerant_type"]).agg({'filling_volume': 'sum'}).apply(lambda x: x / 1000)
refrigerant = refrigerant.drop(columns=['filling_volume'])
final = refrigerant.merge(calculate, on=["device_name", 'refrigerant_type'], how='left').drop_duplicates()
display(final.reset_index().to_string(index=False))

