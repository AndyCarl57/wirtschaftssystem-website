import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

class WirtschaftsSimulation:
    """
    Eine Simulation, die das Zusammenspiel von Freiwirtschaft (Gesell), 
    Modern Money Theory (MMT) und Bedingungslosem Grundeinkommen (BGE) modelliert.
    """
    
    def __init__(self, 
                 anzahl_haushalte=1000,
                 anzahl_unternehmen=100,
                 simulationsdauer=120,  # Monate
                 umlaufsicherung_rate=0.05,  # 5% pro Jahr
                 bge_betrag_erwachsene=1200,  # Euro pro Monat
                 bge_betrag_kinder=600,  # Euro pro Monat
                 einkommensteuer_rate=0.5,  # 50%
                 co2_steuer=0,  # Euro pro Tonne
                 vermoegensteuer_rate=0,  # Prozent ab 1 Mio
                 bodenreform_aktiv=False,
                 mmt_aktiv=False,
                 bge_aktiv=False):
        """
        Initialisiert die Simulation mit den angegebenen Parametern.
        
        Parameter:
        ----------
        anzahl_haushalte : int
            Anzahl der Haushalte in der Simulation
        anzahl_unternehmen : int
            Anzahl der Unternehmen in der Simulation
        simulationsdauer : int
            Dauer der Simulation in Monaten
        umlaufsicherung_rate : float
            Jährliche Rate der Umlaufsicherung (Demurrage) auf gehaltenes Geld
        bge_betrag_erwachsene : float
            Monatlicher BGE-Betrag für Erwachsene in Euro
        bge_betrag_kinder : float
            Monatlicher BGE-Betrag für Kinder in Euro
        einkommensteuer_rate : float
            Einkommensteuersatz (einheitlich für alle Einkommen)
        co2_steuer : float
            CO2-Steuer in Euro pro Tonne
        vermoegensteuer_rate : float
            Vermögensteuersatz für Vermögen über 1 Mio. Euro
        bodenreform_aktiv : bool
            Ob die Bodenreform nach Gesell aktiv ist
        mmt_aktiv : bool
            Ob die Modern Money Theory aktiv ist
        bge_aktiv : bool
            Ob das Bedingungslose Grundeinkommen aktiv ist
        """
        # Simulationsparameter
        self.anzahl_haushalte = anzahl_haushalte
        self.anzahl_unternehmen = anzahl_unternehmen
        self.simulationsdauer = simulationsdauer
        
        # Parameter für die drei Bausteine
        self.umlaufsicherung_rate = umlaufsicherung_rate
        self.bge_betrag_erwachsene = bge_betrag_erwachsene
        self.bge_betrag_kinder = bge_betrag_kinder
        self.einkommensteuer_rate = einkommensteuer_rate
        self.co2_steuer = co2_steuer
        self.vermoegensteuer_rate = vermoegensteuer_rate
        
        # Aktivierungsstatus der Bausteine
        self.bodenreform_aktiv = bodenreform_aktiv
        self.mmt_aktiv = mmt_aktiv
        self.bge_aktiv = bge_aktiv
        
        # Wirtschaftliche Indikatoren
        self.bip_verlauf = []
        self.gini_verlauf = []
        self.arbeitslosigkeit_verlauf = []
        self.inflation_verlauf = []
        self.geldmenge_verlauf = []
        self.umlaufgeschwindigkeit_verlauf = []
        self.konsum_verlauf = []
        self.investitionen_verlauf = []
        self.staatsverschuldung_verlauf = []
        
        # Initialisierung der Wirtschaftsakteure
        self.haushalte = self._initialisiere_haushalte()
        self.unternehmen = self._initialisiere_unternehmen()
        self.staat = {
            'budget': 0,
            'schulden': 0,
            'steuereinnahmen': 0,
            'ausgaben': 0,
            'geldschoepfung': 0
        }
        self.zentralbank = {
            'geldmenge': sum(haushalt['geldvermoegen'] for haushalt in self.haushalte) + 
                         sum(unternehmen['kapital'] for unternehmen in self.unternehmen),
            'zinssatz': 0.02  # 2% Basiszinssatz
        }
        
        # Gesamtwirtschaftliche Variablen
        self.gesamtkonsum = 0
        self.gesamtinvestitionen = 0
        self.gesamtproduktion = 0
        self.inflation = 0.02  # 2% Ausgangsinflation
        self.arbeitslosigkeit = 0.05  # 5% Ausgangsarbeitslosigkeit
        
    def _initialisiere_haushalte(self):
        """Initialisiert die Haushalte mit unterschiedlichen Eigenschaften."""
        haushalte = []
        
        # Vermögensverteilung nach Pareto-Prinzip
        vermoegen = np.random.pareto(1.5, self.anzahl_haushalte) * 10000
        
        for i in range(self.anzahl_haushalte):
            # Zufällige Anzahl von Erwachsenen (1-2) und Kindern (0-3) pro Haushalt
            erwachsene = np.random.randint(1, 3)
            kinder = np.random.randint(0, 4)
            
            # Einkommen basierend auf Qualifikation und Zufall
            qualifikation = np.random.uniform(0.5, 2.0)
            einkommen_basis = 2000 * qualifikation
            einkommen = np.random.normal(einkommen_basis, einkommen_basis * 0.2)
            
            # Konsumneigung sinkt mit steigendem Vermögen
            konsumneigung = 0.8 - 0.3 * (np.log1p(vermoegen[i]) / 15)
            konsumneigung = max(0.3, min(0.9, konsumneigung))
            
            haushalt = {
                'erwachsene': erwachsene,
                'kinder': kinder,
                'qualifikation': qualifikation,
                'einkommen': max(0, einkommen),
                'geldvermoegen': vermoegen[i],
                'sachvermoegen': vermoegen[i] * np.random.uniform(0.5, 2.0),
                'grundbesitz': np.random.random() < 0.3,  # 30% haben Grundbesitz
                'konsumneigung': konsumneigung,
                'unternehmergeist': np.random.uniform(0, 1),
                'beschaeftigt': np.random.random() < 0.95,  # 95% Beschäftigungsquote
                'co2_fussabdruck': np.random.normal(10, 3) * (1 + np.log1p(vermoegen[i]) / 10)  # Tonnen pro Jahr
            }
            haushalte.append(haushalt)
        
        return haushalte
    
    def _initialisiere_unternehmen(self):
        """Initialisiert die Unternehmen mit unterschiedlichen Eigenschaften."""
        unternehmen = []
        
        # Größenverteilung nach Pareto-Prinzip
        groesse = np.random.pareto(1.2, self.anzahl_unternehmen) * 10
        
        for i in range(self.anzahl_unternehmen):
            mitarbeiter = int(groesse[i] * 10) + 1
            kapital = groesse[i] * 100000
            
            unternehmen_obj = {
                'mitarbeiter': mitarbeiter,
                'kapital': kapital,
                'umsatz': kapital * np.random.uniform(0.5, 1.5),
                'gewinn': kapital * np.random.uniform(0.05, 0.2),
                'investitionsneigung': np.random.uniform(0.1, 0.4),
                'innovationskraft': np.random.uniform(0, 1),
                'co2_intensitaet': np.random.normal(5, 2)  # Tonnen CO2 pro 10.000€ Umsatz
            }
            unternehmen.append(unternehmen_obj)
        
        return unternehmen
    
    def _berechne_gini_koeffizient(self):
        """Berechnet den Gini-Koeffizienten als Maß für die Ungleichheit."""
        vermoegen = np.array([h['geldvermoegen'] + h['sachvermoegen'] for h in self.haushalte])
        vermoegen = np.sort(vermoegen)
        n = len(vermoegen)
        index = np.arange(1, n + 1)
        return (np.sum((2 * index - n - 1) * vermoegen)) / (n * np.sum(vermoegen))
    
    def _wende_umlaufsicherung_an(self):
        """Wendet die Umlaufsicherung (Demurrage) auf gehaltenes Geld an."""
        if not self.bodenreform_aktiv:
            return
        
        # Monatliche Umlaufsicherungsrate
        monatliche_rate = self.umlaufsicherung_rate / 12
        
        # Anwendung auf Haushalte
        for haushalt in self.haushalte:
            umlaufsicherung_betrag = haushalt['geldvermoegen'] * monatliche_rate
            haushalt['geldvermoegen'] -= umlaufsicherung_betrag
            self.staat['steuereinnahmen'] += umlaufsicherung_betrag
        
        # Anwendung auf Unternehmen
        for unternehmen in self.unternehmen:
            umlaufsicherung_betrag = unternehmen['kapital'] * monatliche_rate * 0.2  # Nur auf liquide Mittel
            unternehmen['kapital'] -= umlaufsicherung_betrag
            self.staat['steuereinnahmen'] += umlaufsicherung_betrag
    
    def _erhebe_steuern(self):
        """Erhebt verschiedene Steuern basierend auf den aktiven Bausteinen."""
        self.staat['steuereinnahmen'] = 0
        
        # Einkommensteuer
        for haushalt in self.haushalte:
            if haushalt['beschaeftigt']:
                einkommensteuer = haushalt['einkommen'] * self.einkommensteuer_rate
                haushalt['geldvermoegen'] -= einkommensteuer
                self.staat['steuereinnahmen'] += einkommensteuer
        
        # CO2-Steuer
        if self.co2_steuer > 0:
            for haushalt in self.haushalte:
                co2_steuer = (haushalt['co2_fussabdruck'] / 12) * self.co2_steuer
                haushalt['geldvermoegen'] -= co2_steuer
                self.staat['steuereinnahmen'] += co2_steuer
            
            for unternehmen in self.unternehmen:
                co2_steuer = (unternehmen['co2_intensitaet'] * unternehmen['umsatz'] / 120000) * self.co2_steuer
                unternehmen['kapital'] -= co2_steuer
                self.staat['steuereinnahmen'] += co2_steuer
        
        # Vermögensteuer
        if self.vermoegensteuer_rate > 0:
            for haushalt in self.haushalte:
                gesamtvermoegen = haushalt['geldvermoegen'] + haushalt['sachvermoegen']
                if gesamtvermoegen > 1000000:  # 1 Mio. Schwelle
                    vermoegensteuer = (gesamtvermoegen - 1000000) * (self.vermoegensteuer_rate / 12)
                    haushalt['geldvermoegen'] -= vermoegensteuer
                    self.staat['steuereinnahmen'] += vermoegensteuer
    
    def _zahle_grundeinkommen(self):
        """Zahlt das Bedingungslose Grundeinkommen an alle Haushalte aus."""
        if not self.bge_aktiv:
            return
        
        bge_gesamtkosten = 0
        
        for haushalt in self.haushalte:
            bge_betrag = (haushalt['erwachsene'] * self.bge_betrag_erwachsene + 
                          haushalt['kinder'] * self.bge_betrag_kinder)
            haushalt['geldvermoegen'] += bge_betrag
            bge_gesamtkosten += bge_betrag
        
        self.staat['ausgaben'] += bge_gesamtkosten
        
        # Wenn MMT aktiv ist, wird das BGE teilweise durch Geldschöpfung finanziert
        if self.mmt_aktiv:
            geldschoepfung_anteil = max(0, bge_gesamtkosten - self.staat['steuereinnahmen'])
            self.staat['geldschoepfung'] += geldschoepfung_anteil
            self.zentralbank['geldmenge'] += geldschoepfung_anteil
        else:
            # Ansonsten erhöht sich die Staatsverschuldung
            self.staat['schulden'] += max(0, bge_gesamtkosten - self.staat['steuereinnahmen'])
    
    def _aktualisiere_wirtschaft(self):
        """Aktualisiert die wirtschaftlichen Aktivitäten für einen Simulationsschritt."""
        # Konsum der Haushalte
        self.gesamtkonsum = 0
        for haushalt in self.haushalte:
            verfuegbares_einkommen = haushalt['einkommen']
            if self.bge_aktiv:
                verfuegbares_einkommen += (haushalt['erwachsene'] * self.bge_betrag_erwachsene + 
                                          haushalt['kinder'] * self.bge_betrag_kinder)
            
            konsum = verfuegbares_einkommen * haushalt['konsumneigung']
            
            # Wenn Umlaufsicherung aktiv ist, erhöht sich die Konsumneigung
            if self.bodenreform_aktiv:
                konsum *= (1 + self.umlaufsicherung_rate / 4)
            
            konsum = min(konsum, haushalt['geldvermoegen'])
            haushalt['geldvermoegen'] -= konsum
            self.gesamtkonsum += konsum
        
        # Investitionen der Unternehmen
        self.gesamtinvestitionen = 0
        for unternehmen in self.unternehmen:
            # Umsatz basierend auf Gesamtkonsum
            unternehmen['umsatz'] = (unternehmen['mitarbeiter'] / sum(u['mitarbeiter'] for u in self.unternehmen)) * self.gesamtkonsum * 1.2
            
            # Gewinn
            gewinnmarge = np.random.uniform(0.05, 0.15)
            unternehmen['gewinn'] = unternehmen['umsatz'] * gewinnmarge
            unternehmen['kapital'] += unternehmen['gewinn']
            
            # Investitionen
            investition_basis = unternehmen['gewinn'] * unternehmen['investitionsneigung']
            
            # Wenn Umlaufsicherung aktiv ist, erhöht sich die Investitionsneigung
            if self.bodenreform_aktiv:
                investition_basis *= (1 + self.umlaufsicherung_rate / 3)
            
            investition = min(investition_basis, unternehmen['kapital'] * 0.5)
            unternehmen['kapital'] -= investition
            self.gesamtinvestitionen += investition
        
        # Gesamtproduktion (BIP)
        self.gesamtproduktion = self.gesamtkonsum + self.gesamtinvestitionen + self.staat['ausgaben']
        
        # Arbeitsmarkt
        # Wenn BGE aktiv ist, sinkt die Arbeitslosigkeit langsamer bei Wirtschaftsabschwung
        arbeitsmarkt_faktor = 1.0
        if self.bge_aktiv:
            arbeitsmarkt_faktor = 0.8
        
        # Wenn MMT aktiv ist, gibt es eine Arbeitsgarantie
        if self.mmt_aktiv:
            self.arbeitslosigkeit = max(0.02, self.arbeitslosigkeit * 0.9)
        else:
            # Arbeitslosigkeit basierend auf Wirtschaftswachstum
            bip_wachstum = 0
            if len(self.bip_verlauf) > 1:
                bip_wachstum = (self.gesamtproduktion / self.bip_verlauf[-1]) - 1
            
            self.arbeitslosigkeit = max(0.02, min(0.2, self.arbeitslosigkeit - bip_wachstum * 0.5 * arbeitsmarkt_faktor))
        
        # Aktualisierung der Beschäftigungsstatus
        for haushalt in self.haushalte:
            if not haushalt['beschaeftigt']:
                # Chance auf neue Beschäftigung
                if np.random.random() < (1 - self.arbeitslosigkeit) * 0.2:
                    haushalt['beschaeftigt'] = True
                    haushalt['einkommen'] = 2000 * haushalt['qualifikation'] * np.random.uniform(0.8, 1.2)
            else:
                # Risiko der Arbeitslosigkeit
                if np.random.random() < self.arbeitslosigkeit * 0.1:
                    haushalt['beschaeftigt'] = False
                    haushalt['einkommen'] = 0
        
        # Inflation
        # Basis-Inflationsrate
        ziel_inflation = 0.02  # 2% Zielinflation
        
        # Einfluss der Geldmenge (MMT)
        if self.mmt_aktiv:
            geldmengen_einfluss = self.staat['geldschoepfung'] / self.zentralbank['geldmenge']
            ziel_inflation += geldmengen_einfluss * 2
        
        # Einfluss der Kapazitätsauslastung
        kapazitaetsauslastung = 1 - self.arbeitslosigkeit
        if kapazitaetsauslastung > 0.95:
            ziel_inflation += (kapazitaetsauslastung - 0.95) * 10
        
        # Allmähliche Anpassung der Inflation
        self.inflation = self.inflation * 0.8 + ziel_inflation * 0.2
        
        # Aktualisierung der Staatsfinanzen
        self.staat['budget'] = self.staat['steuereinnahmen'] - self.staat['ausgaben']
        if self.staat['budget'] < 0 and not self.mmt_aktiv:
            self.staat['schulden'] -= self.staat['budget']
    
    def _aktualisiere_indikatoren(self):
        """Aktualisiert die wirtschaftlichen Indikatoren für die Analyse."""
        self.bip_verlauf.append(self.gesamtproduktion)
        self.gini_verlauf.append(self._berechne_gini_koeffizient())
        self.arbeitslosigkeit_verlauf.append(self.arbeitslosigkeit)
        self.inflation_verlauf.append(self.inflation)
        self.geldmenge_verlauf.append(self.zentralbank['geldmenge'])
        
        # Umlaufgeschwindigkeit = BIP / Geldmenge
        umlaufgeschwindigkeit = self.gesamtproduktion / self.zentralbank['geldmenge'] * 12  # Annualisiert
        self.umlaufgeschwindigkeit_verlauf.append(umlaufgeschwindigkeit)
        
        self.konsum_verlauf.append(self.gesamtkonsum)
        self.investitionen_verlauf.append(self.gesamtinvestitionen)
        self.staatsverschuldung_verlauf.append(self.staat['schulden'])
    
    def simuliere(self):
        """Führt die Simulation für die angegebene Dauer durch."""
        for monat in range(self.simulationsdauer):
            # Anwendung der drei Bausteine
            self._wende_umlaufsicherung_an()
            self._erhebe_steuern()
            self._zahle_grundeinkommen()
            
            # Wirtschaftliche Aktivitäten
            self._aktualisiere_wirtschaft()
            
            # Aktualisierung der Indikatoren
            self._aktualisiere_indikatoren()
        
        return {
            'bip': self.bip_verlauf,
            'gini': self.gini_verlauf,
            'arbeitslosigkeit': self.arbeitslosigkeit_verlauf,
            'inflation': self.inflation_verlauf,
            'geldmenge': self.geldmenge_verlauf,
            'umlaufgeschwindigkeit': self.umlaufgeschwindigkeit_verlauf,
            'konsum': self.konsum_verlauf,
            'investitionen': self.investitionen_verlauf,
            'staatsverschuldung': self.staatsverschuldung_verlauf
        }
    
    def visualisiere_ergebnisse(self, ergebnisse=None):
        """Visualisiert die Simulationsergebnisse."""
        if ergebnisse is None:
            ergebnisse = {
                'bip': self.bip_verlauf,
                'gini': self.gini_verlauf,
                'arbeitslosigkeit': self.arbeitslosigkeit_verlauf,
                'inflation': self.inflation_verlauf,
                'geldmenge': self.geldmenge_verlauf,
                'umlaufgeschwindigkeit': self.umlaufgeschwindigkeit_verlauf,
                'konsum': self.konsum_verlauf,
                'investitionen': self.investitionen_verlauf,
                'staatsverschuldung': self.staatsverschuldung_verlauf
            }
        
        # Stil für die Plots
        sns.set(style="whitegrid")
        plt.rcParams.update({'font.size': 12})
        
        # Erstelle eine Figur mit mehreren Subplots
        fig, axs = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Simulationsergebnisse: Wirtschaftssystem mit Freiwirtschaft, MMT und BGE', fontsize=16)
        
        # BIP-Verlauf
        axs[0, 0].plot(ergebnisse['bip'], 'b-', linewidth=2)
        axs[0, 0].set_title('BIP-Verlauf')
        axs[0, 0].set_xlabel('Monate')
        axs[0, 0].set_ylabel('BIP (Euro)')
        
        # Gini-Koeffizient
        axs[0, 1].plot(ergebnisse['gini'], 'r-', linewidth=2)
        axs[0, 1].set_title('Gini-Koeffizient (Ungleichheit)')
        axs[0, 1].set_xlabel('Monate')
        axs[0, 1].set_ylabel('Gini-Koeffizient')
        axs[0, 1].set_ylim(0, 1)
        
        # Arbeitslosigkeit
        axs[0, 2].plot(np.array(ergebnisse['arbeitslosigkeit']) * 100, 'g-', linewidth=2)
        axs[0, 2].set_title('Arbeitslosigkeit')
        axs[0, 2].set_xlabel('Monate')
        axs[0, 2].set_ylabel('Arbeitslosigkeit (%)')
        axs[0, 2].set_ylim(0, 20)
        
        # Inflation
        axs[1, 0].plot(np.array(ergebnisse['inflation']) * 100, 'm-', linewidth=2)
        axs[1, 0].set_title('Inflation')
        axs[1, 0].set_xlabel('Monate')
        axs[1, 0].set_ylabel('Inflation (%)')
        
        # Geldmenge
        axs[1, 1].plot(ergebnisse['geldmenge'], 'c-', linewidth=2)
        axs[1, 1].set_title('Geldmenge')
        axs[1, 1].set_xlabel('Monate')
        axs[1, 1].set_ylabel('Geldmenge (Euro)')
        
        # Umlaufgeschwindigkeit
        axs[1, 2].plot(ergebnisse['umlaufgeschwindigkeit'], 'y-', linewidth=2)
        axs[1, 2].set_title('Geldumlaufgeschwindigkeit')
        axs[1, 2].set_xlabel('Monate')
        axs[1, 2].set_ylabel('Umlaufgeschwindigkeit (pro Jahr)')
        
        # Konsum
        axs[2, 0].plot(ergebnisse['konsum'], 'b--', linewidth=2)
        axs[2, 0].set_title('Konsum')
        axs[2, 0].set_xlabel('Monate')
        axs[2, 0].set_ylabel('Konsum (Euro)')
        
        # Investitionen
        axs[2, 1].plot(ergebnisse['investitionen'], 'r--', linewidth=2)
        axs[2, 1].set_title('Investitionen')
        axs[2, 1].set_xlabel('Monate')
        axs[2, 1].set_ylabel('Investitionen (Euro)')
        
        # Staatsverschuldung
        axs[2, 2].plot(ergebnisse['staatsverschuldung'], 'g--', linewidth=2)
        axs[2, 2].set_title('Staatsverschuldung')
        axs[2, 2].set_xlabel('Monate')
        axs[2, 2].set_ylabel('Staatsverschuldung (Euro)')
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('/home/ubuntu/wirtschaftssystem_projekt/simulation/simulationsergebnisse.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return '/home/ubuntu/wirtschaftssystem_projekt/simulation/simulationsergebnisse.png'
    
    def vergleiche_szenarien(self):
        """Vergleicht verschiedene Szenarien mit unterschiedlichen Kombinationen der Bausteine."""
        # Definiere die Szenarien
        szenarien = [
            {"name": "Basisszenario", "bodenreform": False, "mmt": False, "bge": False},
            {"name": "Nur Freiwirtschaft", "bodenreform": True, "mmt": False, "bge": False},
            {"name": "Nur MMT", "bodenreform": False, "mmt": True, "bge": False},
            {"name": "Nur BGE", "bodenreform": False, "mmt": False, "bge": True},
            {"name": "Freiwirtschaft + MMT", "bodenreform": True, "mmt": True, "bge": False},
            {"name": "Freiwirtschaft + BGE", "bodenreform": True, "mmt": False, "bge": True},
            {"name": "MMT + BGE", "bodenreform": False, "mmt": True, "bge": True},
            {"name": "Alle drei Bausteine", "bodenreform": True, "mmt": True, "bge": True}
        ]
        
        # Speichere die Ergebnisse für jeden Indikator
        ergebnisse = {}
        
        # Führe die Simulationen für jedes Szenario durch
        for szenario in szenarien:
            # Setze die Parameter für dieses Szenario
            self.bodenreform_aktiv = szenario["bodenreform"]
            self.mmt_aktiv = szenario["mmt"]
            self.bge_aktiv = szenario["bge"]
            
            # Zurücksetzen der Simulation
            self.__init__(
                anzahl_haushalte=self.anzahl_haushalte,
                anzahl_unternehmen=self.anzahl_unternehmen,
                simulationsdauer=self.simulationsdauer,
                umlaufsicherung_rate=self.umlaufsicherung_rate,
                bge_betrag_erwachsene=self.bge_betrag_erwachsene,
                bge_betrag_kinder=self.bge_betrag_kinder,
                einkommensteuer_rate=self.einkommensteuer_rate,
                co2_steuer=self.co2_steuer,
                vermoegensteuer_rate=self.vermoegensteuer_rate,
                bodenreform_aktiv=szenario["bodenreform"],
                mmt_aktiv=szenario["mmt"],
                bge_aktiv=szenario["bge"]
            )
            
            # Führe die Simulation durch
            ergebnisse[szenario["name"]] = self.simuliere()
        
        # Visualisiere die Vergleiche
        self._visualisiere_szenario_vergleiche(ergebnisse)
        
        return ergebnisse
    
    def _visualisiere_szenario_vergleiche(self, ergebnisse):
        """Visualisiert den Vergleich verschiedener Szenarien."""
        # Stil für die Plots
        sns.set(style="whitegrid")
        plt.rcParams.update({'font.size': 12})
        
        # Indikatoren für den Vergleich
        indikatoren = [
            {"name": "BIP", "key": "bip", "title": "BIP-Verlauf", "ylabel": "BIP (Euro)"},
            {"name": "Gini", "key": "gini", "title": "Gini-Koeffizient (Ungleichheit)", "ylabel": "Gini-Koeffizient"},
            {"name": "Arbeitslosigkeit", "key": "arbeitslosigkeit", "title": "Arbeitslosigkeit", "ylabel": "Arbeitslosigkeit (%)"},
            {"name": "Inflation", "key": "inflation", "title": "Inflation", "ylabel": "Inflation (%)"}
        ]
        
        # Erstelle für jeden Indikator einen eigenen Plot
        for indikator in indikatoren:
            plt.figure(figsize=(12, 8))
            
            for szenario_name, szenario_ergebnisse in ergebnisse.items():
                daten = szenario_ergebnisse[indikator["key"]]
                
                # Für Prozentangaben
                if indikator["key"] in ["arbeitslosigkeit", "inflation"]:
                    daten = np.array(daten) * 100
                
                plt.plot(daten, linewidth=2, label=szenario_name)
            
            plt.title(indikator["title"], fontsize=16)
            plt.xlabel("Monate", fontsize=14)
            plt.ylabel(indikator["ylabel"], fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True)
            
            # Speichere den Plot
            plt.savefig(f'/home/ubuntu/wirtschaftssystem_projekt/simulation/vergleich_{indikator["name"]}.png', 
                        dpi=300, bbox_inches='tight')
            plt.close()
        
        # Erstelle einen zusammenfassenden Plot für das Ende der Simulation
        self._erstelle_endzustand_vergleich(ergebnisse)
    
    def _erstelle_endzustand_vergleich(self, ergebnisse):
        """Erstellt einen Vergleich der Endzustände aller Szenarien."""
        # Indikatoren für den Vergleich
        indikatoren = [
            {"name": "BIP", "key": "bip", "title": "BIP", "faktor": 1},
            {"name": "Gini", "key": "gini", "title": "Gini-Koeffizient", "faktor": 1},
            {"name": "Arbeitslosigkeit", "key": "arbeitslosigkeit", "title": "Arbeitslosigkeit (%)", "faktor": 100},
            {"name": "Inflation", "key": "inflation", "title": "Inflation (%)", "faktor": 100},
            {"name": "Umlaufgeschwindigkeit", "key": "umlaufgeschwindigkeit", "title": "Geldumlaufgeschwindigkeit", "faktor": 1}
        ]
        
        # Sammle die Endzustände
        endzustaende = {}
        for szenario_name, szenario_ergebnisse in ergebnisse.items():
            endzustaende[szenario_name] = {}
            for indikator in indikatoren:
                endzustaende[szenario_name][indikator["key"]] = szenario_ergebnisse[indikator["key"]][-1] * indikator["faktor"]
        
        # Erstelle einen Dataframe für die Visualisierung
        df_endzustaende = pd.DataFrame(endzustaende).T
        
        # Normalisiere die Werte für bessere Vergleichbarkeit
        df_normalisiert = df_endzustaende.copy()
        for col in df_normalisiert.columns:
            if col in ["gini", "arbeitslosigkeit", "inflation"]:
                # Für diese Indikatoren ist niedriger besser
                max_val = df_normalisiert[col].max()
                df_normalisiert[col] = 1 - (df_normalisiert[col] / max_val)
            else:
                # Für diese Indikatoren ist höher besser
                max_val = df_normalisiert[col].max()
                df_normalisiert[col] = df_normalisiert[col] / max_val
        
        # Erstelle einen Radar-Plot
        categories = [indikator["title"] for indikator in indikatoren]
        N = len(categories)
        
        # Winkel für den Plot
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Schließe den Kreis
        
        # Erstelle die Figur
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
        
        # Zeichne für jedes Szenario
        for szenario_name in df_normalisiert.index:
            values = df_normalisiert.loc[szenario_name].values.flatten().tolist()
            values += values[:1]  # Schließe den Kreis
            
            ax.plot(angles, values, linewidth=2, label=szenario_name)
            ax.fill(angles, values, alpha=0.1)
        
        # Beschrifte den Plot
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        
        ax.set_ylim(0, 1)
        ax.set_rlabel_position(0)
        ax.set_title("Vergleich der Szenarien (normalisiert)", fontsize=16)
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        plt.savefig('/home/ubuntu/wirtschaftssystem_projekt/simulation/radar_vergleich.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
        
        # Erstelle auch einen Balkendiagramm-Vergleich für ausgewählte Indikatoren
        fig, axs = plt.subplots(len(indikatoren), 1, figsize=(12, 15))
        
        for i, indikator in enumerate(indikatoren):
            sns.barplot(x=df_endzustaende.index, y=df_endzustaende[indikator["key"]], ax=axs[i])
            axs[i].set_title(indikator["title"])
            axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=45, ha='right')
            
            # Für Gini und Arbeitslosigkeit: Niedriger ist besser
            if indikator["key"] in ["gini", "arbeitslosigkeit", "inflation"]:
                best_idx = df_endzustaende[indikator["key"]].idxmin()
            else:
                best_idx = df_endzustaende[indikator["key"]].idxmax()
            
            # Markiere das beste Szenario
            best_bar = axs[i].patches[df_endzustaende.index.get_loc(best_idx)]
            best_bar.set_facecolor('green')
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/wirtschaftssystem_projekt/simulation/balken_vergleich.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()


# Hauptfunktion zum Ausführen der Simulation
def main():
    # Erstelle die Simulation
    simulation = WirtschaftsSimulation(
        anzahl_haushalte=1000,
        anzahl_unternehmen=100,
        simulationsdauer=120,  # 10 Jahre (120 Monate)
        umlaufsicherung_rate=0.05,  # 5% pro Jahr
        bge_betrag_erwachsene=1200,  # Euro pro Monat
        bge_betrag_kinder=600,  # Euro pro Monat
        einkommensteuer_rate=0.5,  # 50%
        co2_steuer=0,  # Euro pro Tonne
        vermoegensteuer_rate=0,  # Prozent ab 1 Mio
        bodenreform_aktiv=False,
        mmt_aktiv=False,
        bge_aktiv=False
    )
    
    # Führe die Simulation für das Basisszenario durch
    print("Simuliere Basisszenario...")
    ergebnisse_basis = simulation.simuliere()
    
    # Visualisiere die Ergebnisse
    print("Visualisiere Ergebnisse des Basisszenarios...")
    simulation.visualisiere_ergebnisse(ergebnisse_basis)
    
    # Aktiviere alle drei Bausteine
    simulation = WirtschaftsSimulation(
        anzahl_haushalte=1000,
        anzahl_unternehmen=100,
        simulationsdauer=120,
        umlaufsicherung_rate=0.05,
        bge_betrag_erwachsene=1200,
        bge_betrag_kinder=600,
        einkommensteuer_rate=0.5,
        co2_steuer=0,
        vermoegensteuer_rate=0,
        bodenreform_aktiv=True,
        mmt_aktiv=True,
        bge_aktiv=True
    )
    
    # Führe die Simulation für das kombinierte Szenario durch
    print("Simuliere kombiniertes Szenario mit allen drei Bausteinen...")
    ergebnisse_kombiniert = simulation.simuliere()
    
    # Visualisiere die Ergebnisse
    print("Visualisiere Ergebnisse des kombinierten Szenarios...")
    simulation.visualisiere_ergebnisse(ergebnisse_kombiniert)
    
    # Vergleiche verschiedene Szenarien
    print("Vergleiche verschiedene Szenarien...")
    simulation = WirtschaftsSimulation(
        anzahl_haushalte=1000,
        anzahl_unternehmen=100,
        simulationsdauer=120
    )
    simulation.vergleiche_szenarien()
    
    print("Simulation abgeschlossen. Ergebnisse wurden gespeichert.")

if __name__ == "__main__":
    main()
