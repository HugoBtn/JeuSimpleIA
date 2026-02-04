import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, norm

#  1. LOI BINOMIALE
n, p = 20, 1/3
x = np.arange(0, 16)
prob = binom.pmf(x, n, p)

plt.figure(figsize=(10, 5))
plt.bar(x, prob, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(n*p, color='red', linestyle='--', label=f'Espérance (Moyenne) $\\approx {n*p:.2f}$')
plt.title("Distribution des Probabilités (Loi Binomiale)")
plt.xlabel("Nombre de dés présents")
plt.ylabel("Probabilité")
plt.legend()
plt.savefig('distribution_binomiale.png')

#  2. IMPACT DU RISQUE 
risks = [0.2, 0.5, 0.8]
slacks = np.linspace(-2, 2, 400)

plt.figure(figsize=(10, 5))
for r in risks:
    limit = -0.15 + (0.35 * (1.0 - r))
    decision = np.where(slacks < limit, 0, 1)
    plt.plot(slacks, decision + (r*0.02), label=f'Risque {r}') # Décalage pour lisibilité

plt.title("Décision du Bot selon le Risque et la Marge")
plt.xlabel("Marge (Estimation - Enchère)")
plt.ylabel("Action (0=Dodo, 1=Surenchère)")
plt.legend()
plt.savefig('impact_risque.png')

#  3. MARGE D'ERREUR 
mu = 6.67
x_err = np.linspace(4, 9, 500)
y_err = norm.pdf(x_err, mu, 0.5)

plt.figure(figsize=(10, 5))
plt.plot(x_err, y_err, 'b-', label='Perception du Bot')
plt.fill_between(x_err, y_err, where=((x_err >= mu - 0.75) & (x_err <= mu + 0.75)), 
                 color='orange', alpha=0.3, label='Zone de flou (Incertitude)')
plt.axvline(mu, color='red', label='Espérance Réelle')
plt.title("Simulation de l'erreur d'estimation humaine")
plt.legend()
plt.savefig('marge_erreur.png')