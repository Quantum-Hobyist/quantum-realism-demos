
# Quantum Realism Demos

In diesem Repo werden Nachrechnungen zum Thema Quantencomputing in der
Wirkstoffforschung durchgeführt. Damit soll insbesondere Unternehmen
dabei geholfen werden, die Behauptungen von Anbietern realistisch
einordnen zu können.

## Die Demos

Das absolute Herzstück sind die beiden Demos zur Wirkstoffforschung.

**Demo 1: Grundzustandsenergien von H₂ und LiH**
[`demos/01_grundzustaende_Li_und_H2.ipynb`](demos/01_grundzustaende_Li_und_H2.ipynb)

Die erste Demo zeigt die Rechenfähigkeit des VQE-Verfahrens am Beispiel
eines H₂- und eines LiH-Moleküls. Dabei wird auch die enorme
Komplexität schon leicht grösserer Moleküle sichtbar. Beim LiH musste
ein Aktivraum aus zwei Elektronen und zwei Orbitalen gewählt werden,
ohne den der VQE-Ansatz sehr lange gebraucht hätte. Friert man nur den
Atomrumpf ein, bleiben 8 Qubits und die Rechnung dauert bereits 160
Sekunden; ohne jede Reduktion läuft sie über zehn Minuten ohne
Ergebnis. Mit dem Aktivraum sind es 2 Qubits und knapp eine halbe
Sekunde.

**Demo 2: Grundzustandsenergie mit Gattern, Messbudget und Basissatz**
[`demos/02_messbudget_gatter_basissatz.ipynb`](demos/02_messbudget_gatter_basissatz.ipynb)

In der zweiten Demo werden dann verschiedene Bruchstellen vorgestellt,
die auf echter Hardware auf einen zukämen. Dennoch wurde auch hier, wie
schon in der ersten Demo, ein Simulator verwendet. Dabei wird deutlich,
dass die Grenze bereits innerhalb der Spielzeugmoleküle verläuft. H₂
hält mit einem Fehlerbudget von 0.02 noch stand, LiH liegt im
einfachsten Basissatz sto3g bereits bei 1.14, und ab einem Wert von
etwa 1 ist das Ergebnis Rauschen.

## Der Gegenfall: Routing

Allerdings gibt es auch eine ganze Reihe an Codeversuchen, die belegen,
dass Quantum bei Routingproblemen dem klassischen Solver unterliegt.
Das gehört dazu, damit auch die Schwächen von Quantum deutlich
aufgezeigt werden.

| Datei | Was sie zeigt |
|---|---|
| `demos/optimierung/01_routing_qaoa.py` | QAOA mit geratenen Parametern, scheitert, liefert Zufallsniveau |
| `demos/optimierung/02_routing_qaoa_optimiert.py` | QAOA mit klassischer Optimierung, hilft, bleibt aber unzuverlässig |
| `demos/optimierung/03_annealing.py` | Simulated Annealing, gültige Lösungen, aber ohne Optimalitätsgarantie |
| `demos/optimierung/04_klassischer_solver.py` | Klassischer Solver, optimal, beweisbar, in Millisekunden |

## Das Prüfinstrument

Aus Demo 2 folgen vier Fragen, mit denen sich eine Anbieterbehauptung
prüfen lässt. Ausführlich mit den zugehörigen Zahlen stehen sie in
[`pruefinstrument.md`](pruefinstrument.md):

1. Lief es auf Hardware oder im Simulator?
2. Gatterzahl mal Fehlerrate, liegt das über 1?
3. Welcher Basissatz, und reicht der für chemische Genauigkeit?
4. Ganzes Molekül oder nur ein Aktivraum?

## Selbst gerechnet und zitiert

Bei den Wirkstoffversuchen waren natürlich nicht alle Daten selbst
errechnet, sondern manche auch zitiert. Hierzu die Aufteilung:

**Selbst gerechnet:** alle Energien, Gatterzahlen, Termzahlen,
Rauschergebnisse, die Basissatz-Reihe und die Anordnungszahlen. Wer das
Notebook laufen lässt, bekommt dieselben Zahlen.

**Zitiert:** die chemische Genauigkeit von 1 kcal/mol als Konvention
des Fachgebiets, die Hartree-Umrechnung, der experimentelle
Bindungswert von H₂, der exponentielle Zusammenhang zwischen Energie
und Bindungsstärke, die heutigen Fehlerraten, das Verhältnis physischer
zu logischen Qubits sowie Embedding.

## Ausführen

Die beiden Notebooks laufen in Google Colab ohne lokale Installation.
Die Installationszelle steht jeweils zuoberst und muss vor den
Code-Zellen ausgeführt werden.

Lokal, Python 3.12 empfohlen:

    pip install -r requirements.txt

Die Skripte im Optimierungsordner sind eigenständig und ohne
Reihenfolge-Abhängigkeit; jedes gibt sein Ergebnis direkt auf der
Konsole aus:

    python demos/optimierung/04_klassischer_solver.py

## Über dieses Projekt

Dieses Repository wurde von einem 18-jährigen Gymnasialschüler nach
autodidaktischer Erarbeitung erstellt. Für den Code wurde teilweise
künstliche Intelligenz zu Hilfe genommen.
