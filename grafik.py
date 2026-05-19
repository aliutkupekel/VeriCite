import matplotlib.pyplot as plt
import numpy as np

# Grafikteki Kategoriler (İngilizce ve Akademik)
labels = ['Severe Hallucinations\n(Type I & IV Errors)', 'Verified or Safely Dropped\n(Successful Handling)']

# Excel'den çıkardığımız sonuçlar
baseline_scores = [70, 30] 
vericite_scores = [0, 100]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))
rects1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline LLM', color='#e74c3c')
rects2 = ax.bar(x + width/2, vericite_scores, width, label='VeriCite Framework', color='#2ecc71')

# Eksenler ve Başlık (İngilizce)
ax.set_ylabel('Percentage of Outcomes (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparison of Hallucination Rates: Baseline vs. VeriCite', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
ax.legend()

# Çubukların üzerine İngilizce formatta (70%) yazıları ekleme
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

# Resmi aynı isimle üzerine yazdırarak kaydet
plt.savefig('evaluation_results.png', dpi=300)
print("Graphic has been created succesfully")