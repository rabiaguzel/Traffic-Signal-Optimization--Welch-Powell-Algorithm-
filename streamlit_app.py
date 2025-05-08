import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


st.title("Trafik Sinyal Optimizasyonu (Welch-Powell Algoritması)")

# Zaman dilimleri ve yolları 
time_range = [f"{h:02d}:00-{h+1:02d}:00" for h in range(8, 19)]
roads = [
    "Mastrip", "Kalimantan", "PB_Sudirman", "Danau_Toba",
    "Jendral_Ahmad_Yani", "Jl_Semeru", "Jl_Hasanuddin", "Jl_Rajawali",
    "Jl_Gatot_Subroto", "Jl_Pahlawan", "Jl_Kartini", "Jl_Diponegoro"
]

# Gerçekçi rastgele veri
np.random.seed(42)
data = {"Time": time_range}
for road in roads:
    entrance = []
    exit = []
    for hour in range(8, 19):
        if hour in [8, 9, 17, 18]:  # yoğun saatler
            e_in = np.random.randint(180, 250)
        else:
            e_in = np.random.randint(80, 140)
        
        e_out = np.random.randint(70, e_in + 1)
        
        entrance.append(e_in)
        exit.append(e_out)

    data[f"{road}_Entrance"] = entrance
    data[f"{road}_Exit"] = exit


df = pd.DataFrame(data)

# Ulaşım ağı çizgesi 
G = nx.Graph()
G.add_nodes_from(roads)
G.add_edges_from([
    ("Mastrip", "Kalimantan"),
    ("Mastrip", "PB_Sudirman"),
    ("Mastrip", "Danau_Toba"),
    ("Kalimantan", "PB_Sudirman"),
    ("PB_Sudirman", "Danau_Toba"),
    ("Danau_Toba", "Jendral_Ahmad_Yani"),
    ("Jendral_Ahmad_Yani", "Jl_Semeru"),
    ("Jl_Semeru", "Jl_Hasanuddin"),
    ("Jl_Hasanuddin", "Jl_Rajawali"),
    ("Jl_Rajawali", "Kalimantan"),
    ("Jl_Rajawali", "Danau_Toba"),
    ("Jl_Gatot_Subroto", "Jl_Semeru"),
    ("Jl_Gatot_Subroto", "Jl_Hasanuddin"),
    ("Jl_Pahlawan", "Jl_Gatot_Subroto"),
    ("Jl_Pahlawan", "Jl_Kartini"),
    ("Jl_Kartini", "Jl_Diponegoro"),
    ("Jl_Diponegoro", "Danau_Toba"),
    ("Jl_Diponegoro", "PB_Sudirman"),
])

# Welch-Powell algoritması 
def welch_powell(graph, weights):
    sorted_nodes = sorted(graph.nodes, key=lambda x: weights[x], reverse=True)
    color_map = {}
    current_color = 0

    for node in sorted_nodes:
        if node not in color_map:
            color_map[node] = current_color
            for other_node in sorted_nodes:
                if other_node not in color_map:
                    if all(color_map.get(neigh) != current_color for neigh in graph.neighbors(other_node)):
                        color_map[other_node] = current_color
            current_color += 1

    return color_map

# Renk listesi
colors_list = [
    'purple', 'blue', 'yellow', 'red', 'green', 'orange',
    'pink', 'brown', 'gray', 'cyan', 'olive', 'lightcoral'
]

# Saat seçimi
selected_time = st.selectbox("Zaman Dilimi Seçin", df["Time"])
frame_index = df.index[df["Time"] == selected_time][0]

# Ağırlıklar (giriş sayısı) ve renk atama
weights = {
    road: df[f"{road}_Entrance"][frame_index] - df[f"{road}_Exit"][frame_index]
    for road in roads
}
color_map = welch_powell(G, weights)
node_colors = [colors_list[color_map[node]] for node in G.nodes]

# Graf çizimi
fig, ax = plt.subplots(figsize=(9, 7))
pos = nx.kamada_kawai_layout(G, scale=2)
nx.draw_networkx(G, pos, node_color=node_colors, with_labels=True, node_size=1200, font_size=9, ax=ax)
ax.set_title(f"Trafik Sinyal Renklemesi - {selected_time}")
ax.axis('off')
st.pyplot(fig)

# Faz + Giriş/Çıkış Tablosu
phase_info = pd.DataFrame.from_dict(color_map, orient='index', columns=["Phase"]).reset_index()
phase_info.columns = ["Intersection", "Phase"]
phase_info["Entrance"] = phase_info["Intersection"].apply(lambda x: df[f"{x}_Entrance"][frame_index])
phase_info["Exit"] = phase_info["Intersection"].apply(lambda x: df[f"{x}_Exit"][frame_index])
phase_info = phase_info.sort_values(by="Phase")

st.subheader("Faz Atamaları ve Giriş/Çıkış Bilgileri")
st.dataframe(phase_info)
