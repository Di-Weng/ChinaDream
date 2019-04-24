import matplotlib.pyplot as plt

ch_list = [8.850667987835307, 10.028913054517485, 7.962514345099895, 7.249675951720091, 4.863299197943491, 4.794612050653081, 4.510778340574141, 5.260466198918825, 4.334545053549238, 3.7465131650407337, 2.820168104177157, 5.538336704403297, 5.245274531652314, 13.214834687888471]
x_list = []

xticks_list = []
temp_n = 1
for i in range(2, 16):
    print(i)
    # imple_kmeans(dreamvector_dataframe,i+1)
    x_list.append(i + 1)
    xticks_list.append(temp_n)
    temp_n += 1

plt.plot(xticks_list, ch_list)
plt.xticks(xticks_list, x_list)
print(len(ch_list))
plt.show()