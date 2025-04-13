# Konzept für die wirtschaftliche Simulation

## Einführung

Diese Simulation soll das Zusammenspiel der drei theoretischen Bausteine demonstrieren:
1. Freiwirtschaftsidee nach Silvio Gesell (Umlaufsicherung und Bodenreform)
2. Modern Money Theory (MMT) mit zweckgebundener Geldschöpfung
3. Bedingungsloses Grundeinkommen (BGE)

Ziel ist es, zu zeigen, wie diese drei Elemente in einem kohärenten Wirtschaftssystem zusammenwirken können und welche Auswirkungen sie auf verschiedene wirtschaftliche und soziale Indikatoren haben.

## Simulationsansatz

Die Simulation wird als agentenbasiertes Modell konzipiert, das die Interaktionen zwischen verschiedenen Wirtschaftsakteuren (Haushalte, Unternehmen, Staat, Zentralbank) abbildet. Wir werden Python mit den Bibliotheken NumPy, Pandas und Matplotlib für die Implementierung und Visualisierung verwenden.

## Schlüsselkomponenten der Simulation

### 1. Wirtschaftsakteure

- **Haushalte**: Verschiedene Einkommens- und Vermögensgruppen mit unterschiedlichen Konsum- und Sparverhalten
- **Unternehmen**: Produzenten von Gütern und Dienstleistungen, die Arbeitskräfte beschäftigen
- **Staat**: Verantwortlich für Geldschöpfung (gemäß MMT), Auszahlung des BGE und Erhebung von Steuern
- **Zentralbank**: Implementiert die Umlaufsicherung und arbeitet mit dem Staat zusammen

### 2. Implementierung der drei Bausteine

#### Freiwirtschaft (Gesell)
- **Umlaufsicherung**: Implementierung einer Gebühr auf gehaltenes Geld (Demurrage)
- **Bodenreform**: Modellierung von Bodennutzungsgebühren anstelle von privatem Bodeneigentum

#### Modern Money Theory (MMT)
- **Staatliche Geldschöpfung**: Der Staat schafft Geld für öffentliche Ausgaben
- **Steuererhebung**: Steuern dienen zur Regulierung der Geldmenge und Inflationskontrolle
- **Arbeitsgarantie**: Implementierung eines staatlichen Beschäftigungsprogramms

#### Bedingungsloses Grundeinkommen (BGE)
- **Universelle Auszahlung**: Jeder Haushalt erhält regelmäßig einen festen Betrag
- **Finanzierung**: Kombination aus MMT-basierter Geldschöpfung und Steuereinnahmen

### 3. Wirtschaftliche Indikatoren

Die Simulation wird folgende Indikatoren verfolgen:
- Wirtschaftswachstum (BIP)
- Einkommens- und Vermögensverteilung (Gini-Koeffizient)
- Arbeitslosigkeit und Beschäftigungsquote
- Inflation
- Geldmenge und Umlaufgeschwindigkeit
- Konsum und Investitionen
- Staatsverschuldung

## Simulationsszenarien

Wir werden verschiedene Szenarien simulieren, um die Auswirkungen der drei Bausteine zu untersuchen:

1. **Basisszenario**: Konventionelles Wirtschaftssystem ohne die drei Bausteine
2. **Einzelbausteine**: Separate Implementierung jedes Bausteins
3. **Kombinierte Implementierung**: Vollständige Integration aller drei Bausteine
4. **Übergangsszenarien**: Schrittweise Einführung der Bausteine über einen Zeitraum

## Annahmen und Parameter

Die Simulation wird auf folgenden Annahmen basieren:

- **Umlaufsicherungsrate**: 5% pro Jahr auf gehaltenes Geld
- **BGE-Höhe**: 1.200 € pro Monat für Erwachsene, 600 € für Kinder
- **Steuersätze**: Anpassbar je nach Szenario
- **Geldschöpfungsrate**: Abhängig von wirtschaftlichen Bedingungen und Inflationsrate

## Erwartete Ergebnisse

Basierend auf den theoretischen Grundlagen erwarten wir folgende Ergebnisse:

1. **Umlaufsicherung**: Erhöhte Geldumlaufgeschwindigkeit, reduzierte Spekulation
2. **Bodenreform**: Geringere Immobilienpreise, gerechtere Verteilung von Bodenrenten
3. **MMT**: Niedrigere Arbeitslosigkeit, höhere öffentliche Investitionen
4. **BGE**: Reduzierte Armut, erhöhte soziale Mobilität, mehr Unternehmertum

Im kombinierten System erwarten wir Synergieeffekte, wie:
- Stabilere Wirtschaft mit geringeren Konjunkturschwankungen
- Gerechtere Einkommens- und Vermögensverteilung
- Höhere soziale Sicherheit bei gleichzeitiger wirtschaftlicher Dynamik
- Nachhaltigeres Wirtschaftswachstum

## Implementierungsplan

1. Entwicklung des Basismodells mit den wichtigsten Wirtschaftsakteuren
2. Integration der drei Bausteine in das Modell
3. Kalibrierung des Modells mit realistischen Parametern
4. Durchführung der Simulationsszenarien
5. Analyse und Visualisierung der Ergebnisse
6. Ableitung von Handlungsempfehlungen für die praktische Umsetzung
