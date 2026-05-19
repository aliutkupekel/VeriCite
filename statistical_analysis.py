import numpy as np
from scipy import stats

print("=== VERICITE EVALUATION & STATISTICAL ANALYSIS ===")

# 1. ELİMİZDEKİ VERİLER (10 Testin Sonuçları)
# Baseline (ChatGPT) CAR: 3 soruda gerçek DOI verdi (1), 7 soruda sahte/bağlam dışı (0)
baseline_car_scores = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0] 

# VeriCite CAR/Güvenlik: 10 sorunun hepsinde ya doğru DOI verdi ya da yalanı silerek sistemi korudu (1)
vericite_car_scores = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 

# VeriCite Convergence (İterasyon Sayıları): Testlerde Refinement ajanı kaç kere çalıştı?
# 10 testteki deneme sayıları (Örn: 3, 3, 3, 3, 3, 3, 1, 3, 3, 1)
vericite_iterations = [3, 3, 3, 3, 3, 3, 1, 3, 3, 1]

# 2. METRİKLERİN HESAPLANMASI
baseline_car_percentage = np.mean(baseline_car_scores) * 100
vericite_car_percentage = np.mean(vericite_car_scores) * 100
convergence_rate = np.mean(vericite_iterations)

print(f"\n1. Citation Accuracy & Safety Rate (CAR):")
print(f"   - Baseline LLM: {baseline_car_percentage}%")
print(f"   - VeriCite Framework: {vericite_car_percentage}%")

print(f"\n2. Convergence Rate:")
print(f"   - Average iterations to resolve or drop: {convergence_rate} attempts")

# 3. İSTATİSTİKSEL TEST (Paired t-test)
# Proposal'da söz verdiğimiz gibi iki bağımlı grup arasında t-testi yapıyoruz.
t_statistic, p_value = stats.ttest_rel(baseline_car_scores, vericite_car_scores)

print(f"\n3. Statistical Significance (Paired t-test):")
print(f"   - T-Statistic: {t_statistic:.4f}")
print(f"   - P-Value: {p_value:.6f}")

if p_value < 0.05:
    print("   - CONCLUSION: The difference is STATISTICALLY SIGNIFICANT (p < 0.05).")
    print("     VeriCite definitively outperforms the baseline model in preventing hallucinations.")
else:
    print("   - CONCLUSION: The difference is NOT statistically significant.")