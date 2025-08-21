import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# kumpulan universe
temperatur = ctrl.Antecedent(np.arange(0, 31, 1), 'temperatur')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
smart_ac   = ctrl.Consequent(np.arange(0, 31, 1), 'smart_ac')

# kurva temperatur
temperatur['dingin'] = fuzz.trimf(temperatur.universe, [15, 18, 21])
temperatur['sedang'] = fuzz.trimf(temperatur.universe, [19, 23, 27])
temperatur['panas']  = fuzz.trimf(temperatur.universe, [25, 28, 30])

# kurva kelembapan
kelembapan['sangat_kering']  = fuzz.trimf(kelembapan.universe, [0, 0, 25])
kelembapan['kering']         = fuzz.trimf(kelembapan.universe, [23, 27, 32])
kelembapan['ideal']          = fuzz.trimf(kelembapan.universe, [30, 45, 60])
kelembapan['lembab']         = fuzz.trimf(kelembapan.universe, [58, 65, 72])
kelembapan['sangat_lembab']  = fuzz.trimf(kelembapan.universe, [70, 100, 100])

# kurva smart ac
smart_ac['rendah'] = fuzz.trimf(smart_ac.universe, [15, 15, 20])
smart_ac['sedang'] = fuzz.trimf(smart_ac.universe, [19, 22.5, 26])
smart_ac['tinggi'] = fuzz.trimf(smart_ac.universe, [25, 30, 30])

# rule (3 temperatur × 5 kelembapan = 15 rule)
rules = [
    ctrl.Rule(temperatur['dingin'] & kelembapan['sangat_kering'], smart_ac['rendah']),
    ctrl.Rule(temperatur['dingin'] & kelembapan['kering'],        smart_ac['rendah']),
    ctrl.Rule(temperatur['dingin'] & kelembapan['ideal'],         smart_ac['rendah']),
    ctrl.Rule(temperatur['dingin'] & kelembapan['lembab'],        smart_ac['sedang']),
    ctrl.Rule(temperatur['dingin'] & kelembapan['sangat_lembab'], smart_ac['sedang']),

    ctrl.Rule(temperatur['sedang'] & kelembapan['sangat_kering'], smart_ac['sedang']),
    ctrl.Rule(temperatur['sedang'] & kelembapan['kering'],        smart_ac['sedang']),
    ctrl.Rule(temperatur['sedang'] & kelembapan['ideal'],         smart_ac['sedang']),
    ctrl.Rule(temperatur['sedang'] & kelembapan['lembab'],        smart_ac['tinggi']),
    ctrl.Rule(temperatur['sedang'] & kelembapan['sangat_lembab'], smart_ac['tinggi']),

    ctrl.Rule(temperatur['panas'] & kelembapan['sangat_kering'],  smart_ac['tinggi']),
    ctrl.Rule(temperatur['panas'] & kelembapan['kering'],         smart_ac['tinggi']),
    ctrl.Rule(temperatur['panas'] & kelembapan['ideal'],          smart_ac['tinggi']),
    ctrl.Rule(temperatur['panas'] & kelembapan['lembab'],         smart_ac['tinggi']),
    ctrl.Rule(temperatur['panas'] & kelembapan['sangat_lembab'],  smart_ac['tinggi']),
]

fan_ctrl = ctrl.ControlSystem(rules)
fan_sim  = ctrl.ControlSystemSimulation(fan_ctrl)

# inputan, bawahnya di simpen ke dalam variabel untuk plot saja
temp_in = 27
hum_in  = 80
fan_sim.input['temperatur'] = temp_in
fan_sim.input['kelembapan'] = hum_in

# centroid
fan_sim.compute()
fan_out = fan_sim.output['smart_ac']
print(f"Output smart_ac: {fan_out:.2f}")

# plot lah bahasanya tu
fig, axes = plt.subplots(3, 1, figsize=(9, 10))

axes[0].plot(temperatur.universe, temperatur['dingin'].mf, label='Dingin')
axes[0].plot(temperatur.universe, temperatur['sedang'].mf, label='Sedang')
axes[0].plot(temperatur.universe, temperatur['panas'].mf,  label='Panas')
axes[0].axvline(temp_in, color='k', linestyle='--', label=f'Input = {temp_in}°C')
axes[0].set_title('Temperatur')
axes[0].set_ylabel('Keanggotaan')
axes[0].legend(loc='upper right')

axes[1].plot(kelembapan.universe, kelembapan['sangat_kering'].mf, label='Sangat Kering')
axes[1].plot(kelembapan.universe, kelembapan['kering'].mf,        label='Kering')
axes[1].plot(kelembapan.universe, kelembapan['ideal'].mf,         label='Ideal')
axes[1].plot(kelembapan.universe, kelembapan['lembab'].mf,        label='Lembab')
axes[1].plot(kelembapan.universe, kelembapan['sangat_lembab'].mf, label='Sangat Lembab')
axes[1].axvline(hum_in, color='k', linestyle='--', label=f'Input = {hum_in}%')
axes[1].set_title('Kelembapan')
axes[1].set_ylabel('Keanggotaan')
axes[1].legend(loc='upper right')

axes[2].plot(smart_ac.universe, smart_ac['rendah'].mf, label='Rendah')
axes[2].plot(smart_ac.universe, smart_ac['sedang'].mf, label='Sedang')
axes[2].plot(smart_ac.universe, smart_ac['tinggi'].mf, label='Tinggi')
axes[2].axvline(fan_out, color='orange', linestyle=':', label=f'Output = {fan_out:.2f}')
axes[2].set_title('Smart AC (Keluaran)')
axes[2].set_xlabel('Nilai')
axes[2].set_ylabel('Keanggotaan')
axes[2].legend(loc='upper right')

plt.tight_layout()
plt.show()
