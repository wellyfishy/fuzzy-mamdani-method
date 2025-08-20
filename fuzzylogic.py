import numpy as np
import matplotlib.pyplot as plt

# (x - a) / (b - a) mencari value membership "lebih kecil dari" misal pada low adalah 15, 20, 25 maka yang dicari adalah value membership di antara 15 sampai 20
# misal perulangan x adalah 15, maka (15 - 15) / (20 - 15) = 0 / 5 = 0
# sedangkan (c - x) / (c - b) mencari value membership pada sebelah kanan
# (25 - 15) / (25 - 20) = 10 / 5 = 2
# karena kita mencari minimum (untuk menghindari membership diatas 1.0) maka yang dipilih adalah 0 karena
# setelah mencari minimum, kita mencari maximum, menggunakan minimum terlebih dahulu mempreventasi nilai membership diatas 1.0
# maka jika array minimum adalah 0.123456, 0.234567, 0.34567 dan seterusnya sampai 1.0+, yang dipilih adalah 0.123456
def segitiga(x, a, b, c):
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)

# fungsi linspace essentially membuat array 15 sampai 40 memiliki space sebanyak 500x. 15.05, 15.10, 15.15, dan seterusnya
x = np.linspace(15, 40, 500)

# ini variabel untuk membuat segitiga pada nantinya
# ini juga array variabel untuk mencari value yang pas untuk di cocokkan dengan value membership yang kita cari berdasarkan temperatur nanti
low = segitiga(x, 15, 17.5, 20)    
medium = segitiga(x, 18, 21.5, 25)    
high = segitiga(x, 23, 26.5, 30) 

# temperatur sekarang
temp = 27

# mencari value membership pada segitiga low, pada perulangan jika x nya adalah 25.5 dan seterusnya, value membership akan stay 0 yang menjelaskan bahwa garis membership
# tidak berada di low (bisa saja di med atau high)
# hal ini berlaku juga pada medium dan high
# maka jika 0.2 pada low, 0.4 pada med dan 0 pada high, maka garis akan muncul di sekitar pertengahan segitiga low dan med yang kena overlap
low_val = segitiga(temp, 15, 17.5, 20)
print(low_val)
med_val = segitiga(temp, 18, 21.5, 25)
print(med_val)
high_val = segitiga(temp, 23, 26.5, 30)
print(high_val) 
# print hanya untuk melihat membership pada terminal saja

low_output = np.minimum(low, low_val)
med_output = np.minimum(medium, med_val)
high_output = np.minimum(high, high_val)

# aggregasi semua output sebelumnya (Mamdani aggregation: max)
combined = np.maximum(np.maximum(low_output, med_output), high_output)

# defuzzification centroid
mamdani_temp = np.sum(x * combined) / np.sum(combined)

# grafik
fig, axes = plt.subplots(3, 1, figsize=(6, 8), sharex=True)

def plot_set(ax, x, y, label, color):
    ax.plot(x, y, color, label=label)
    ax.axvline(temp, color="k", linestyle="--", label="Temperatur")
    ax.axvline(mamdani_temp, color="orange", linestyle=":", label="Temperatur Centroid")
    ax.set_ylabel("Membership")
    ax.legend()

plot_set(axes[0], x, low, "Low", "b")
plot_set(axes[1], x, medium, "Medium", "g")
plot_set(axes[2], x, high, "High", "r")

axes[2].set_xlabel("Temperatur")

plt.suptitle(f"Temp = {temp}°C\nKoreksi Centroid → {mamdani_temp}°C")
plt.tight_layout()
plt.show()
