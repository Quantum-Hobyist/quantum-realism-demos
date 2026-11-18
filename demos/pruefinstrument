# Das Prüfinstrument

Vier Fragen, mit denen sich eine öffentliche Behauptung zu
Quantencomputing in der Chemie prüfen lässt. Sie folgen aus den
Messungen in `demos/02_wo_es_bricht.ipynb` und brauchen keine
Spezialkenntnisse, nur die Bereitschaft, nach Zahlen zu fragen.

## 1. Lief es auf Hardware oder im Simulator?

Die billigste und schärfste Frage. Ein Simulator rechnet die
Wellenfunktion exakt aus und kennt kein Rauschen, solange man ihm
keines einbaut. Ergebnisse von dort sagen nichts darüber, ob dieselbe
Rechnung auf einer Maschine funktionieren würde.

Auch die Demos in diesem Repo laufen auf einem Simulator. Der
Unterschied ist, dass es hier dabeisteht.

## 2. Gatterzahl mal Fehlerrate, liegt das über 1?

Jede Operation an einem Qubit geht mit einer gewissen
Wahrscheinlichkeit schief, und die Fehler summieren sich über die
Länge des Schaltkreises. Multipliziert man die Zahl der Operationen mit
der Fehlerrate pro Operation, bekommt man ein Fehlerbudget. Liegt es
über etwa 1, ist das Ergebnis Rauschen.

Gemessene Werte aus Demo 2, bei einer Fehlerrate von 10⁻³:

| Molekül | Gatter | Fehlerbudget |
|---|---|---|
| H₂ | 21 | 0.02 |
| LiH | 1137 | 1.14 |
| BeH₂ | 5719 | 5.72 |
| H₂O | 5778 | 5.78 |

Die Regel überschätzt um rund Faktor zwei und taugt deswegen als
konservative Obergrenze.

Wichtig dabei: Die Fehlerrate ist eine Eingabe und keine Konstante. Man
muss die tatsächliche Rate der konkreten Plattform einsetzen und keine
Hausnummer. Bei 3 mal 10⁻⁴ statt 10⁻³ fällt das LiH-Budget von 1.14 auf
0.34, und damit kippt das Urteil ins Gegenteil. Wer eine pauschale Rate
einsetzt, prüft in Wirklichkeit nichts.

## 3. Welcher Basissatz, und reicht der für chemische Genauigkeit?

Der Basissatz legt fest, aus wie vielen Bausteinen die Elektronenwolke
nachgebaut wird. Je gröber er ist, desto weniger kostet die Rechnung
und desto weiter liegt das Ergebnis daneben, und zwar unabhängig von
jeder Hardware.

Gemessen an H₂, gegen den experimentellen Wert von 458.0 kJ/mol:

| Basissatz | Qubits | Bindung in kJ/mol | Abweichung |
|---|---|---|---|
| sto3g | 4 | 360.5 | 97.5 |
| cc-pVDZ | 20 | 428.5 | 29.5 |
| cc-pVTZ | 56 | 452.4 | 5.6 |
| cc-pVQZ | 120 | 456.2 | 1.8 |

Die chemische Genauigkeit liegt bei 1 kcal/mol, also rund 4.2 kJ/mol.
Erst cc-pVQZ liegt darunter, und das bedeutet 120 Qubits für zwei
Wasserstoffatome. Wer mit sto3g rechnet und das Ergebnis chemisch
belastbar nennt, hat einen Fehler von 21 Prozent im Resultat, bevor
überhaupt ein Qubit beteiligt war.

## 4. Ganzes Molekül oder nur ein Aktivraum?

Ein echtes Wirkstoffmolekül hat mehrere hundert Orbitale. Niemand
rechnet das vollständig quantenmechanisch, und niemand will das. Üblich
und legitim ist, nur den kleinen Teil quantenmechanisch zu behandeln,
an dem klassische Verfahren tatsächlich scheitern, und den Rest
klassisch zu rechnen.

Legitim ist das, solange es dabeisteht. Eine Rechnung über zehn bis
fünfzig Orbitale eines Reaktionszentrums ist kein "Grundzustand eines
Wirkstoffmoleküls".

## Was nach diesen vier Fragen übrig bleibt

Wer heute ein ganzes Wirkstoffmolekül auf einem Quantencomputer
rechnet, rechnet keine Chemie. Entweder lief es auf einem Simulator,
oder es war nur ein Ausschnitt, oder das Ergebnis liegt ausserhalb der
chemischen Genauigkeit.

Das ist eine engere Aussage als "Quanten helfen der Pharmaforschung
nicht". Der strukturelle Grund, warum sich der Aufwand lohnt, bleibt
gültig: Ein Fragment mit 100 Spinorbitalen und 50 Elektronen hat
1.0 mal 10²⁹ mögliche Elektronenanordnungen, viel zu viele für eine
exakte klassische Rechnung, und ein Quantencomputer braucht dafür 100
Qubits. Exponentieller Zustandsraum gegen linear wachsende Qubitzahl,
bei Messkosten mit der vierten Potenz. Dieser Handel ist der Kern des
Arguments und er ist nicht widerlegt.

Er greift nur noch nicht.
