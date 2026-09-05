# Quantum Realism Demos

Eine nüchterne Sammlung lauffähiger Demos zur Frage: Wo hilft
Quantencomputing bei Optimierungs- und Chemieproblemen heute wirklich –
und wo nicht? Kein Hype, sondern ehrliche Einordnung mit Code, den man
selbst laufen lassen kann.

## Die These

Bei Optimierungsproblemen wie Routenplanung schlägt ein klassischer
Solver aktuelle Quantenverfahren – und zwar aus strukturellen, nicht nur
aus hardwarebedingten Gründen. Bei der Simulation von Molekülen dagegen
passt Quantencomputing strukturell zum Problem; hier fehlt heute vor
allem die nötige Hardware-Reife. Der Unterschied zwischen diesen beiden
Formen von "funktioniert heute noch nicht" ist der Kern dieser Sammlung.

## Die Demos

| Datei | Was sie zeigt |
|---|---|
| `demos/01_routing_qaoa.py` | QAOA mit geratenen Parametern – scheitert, liefert Zufallsniveau |
| `demos/02_routing_qaoa_optimiert.py` | QAOA mit klassischer Optimierung – hilft, bleibt aber unzuverlässig |
| `demos/03_annealing.py` | Simulated Annealing – gültige Lösungen, aber ohne Optimalitätsgarantie |
| `demos/04_klassischer_solver.py` | Klassischer Solver – optimal, beweisbar, in Millisekunden |
| `demos/05_chemie_vqe_h2.py` | VQE für das H₂-Molekül – wo Quantum strukturell passt |

## Ausführen

Python 3.12 empfohlen. Abhängigkeiten installieren:

    pip install -r requirements.txt

Dann eine Demo starten, z.B.:

    python demos/04_klassischer_solver.py

Die Skripte sind eigenständig und ohne Reihenfolge-Abhängigkeit; jedes
gibt sein Ergebnis direkt auf der Konsole aus.

## Wichtiger Hinweis

Dies sind bewusst kleine Modellprobleme. Sie belegen die *Mechanismen*
(warum ein Verfahren gelingt oder scheitert), nicht die absolute Grenze
realer Anwendungen. Die verwendeten Chemie-Koeffizienten sind
publizierte Standardwerte und für ernsthafte Nutzung an einer Fachquelle
zu prüfen.

## Über dieses Projekt

Entstanden im Rahmen meines selbstgesteuerten Einarbeitens in
Quantencomputing, mit dem Ziel, seriös beurteilen zu können, wo die
Technik echten Nutzen bringt und wo nicht.
