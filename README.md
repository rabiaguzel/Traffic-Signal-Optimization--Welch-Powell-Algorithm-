### **Türkçe**

# Trafik Sinyal Optimizasyonu (Welch-Powell Algoritması)

Bu proje, trafik yoğunluğunu azaltmak ve kavşaklar arasında daha verimli sinyalizasyon sağlamak amacıyla Welch-Powell graf boyama algoritmasını kullanmaktadır. 

## 🚦 Proje Hakkında

- Zaman aralığı: 08:00 - 19:00 (11 zaman dilimi)
- Kavşaklar: Endonezya'dan örnek yollar
- Giriş (Entrance) ve çıkış (Exit) verileri sentetik olarak oluşturulmuştur
- Trafik yoğunluğu: Sabah (08–09) ve akşam (17–18) saatlerinde daha yüksek
- Ağırlık: Her kavşak için (giriş - çıkış) farkı
- Amaç: Kavşaklara çakışmayan sinyal fazları atamak

### **English**

# Traffic Signal Optimization (Welch-Powell Algorithm)

This project applies the Welch-Powell graph coloring algorithm to assign non-conflicting traffic signal phases based on traffic intensity.

## 🚦 About the Project

- Time range: 08:00 - 19:00 (11 hourly intervals)
- Intersections: Sample roads from Indonesia
- Entrance and exit data are synthetically generated
- Peak hours: 08–09 and 17–18
- Weight: (Entrance - Exit) for each intersection
- Goal: Assign non-conflicting signal phases to intersections

## 🔍 Technologies Used

- Python
- NetworkX
- Streamlit
- Matplotlib
- NumPy
- Pandas

## 🖼️ Interface

The user selects a time slot to visualize traffic load and signal phases at intersections.

## 🚀 Run the App

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
