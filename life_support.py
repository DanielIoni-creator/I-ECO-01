import time
import random

class LifeSupportSystem:
    def __init__(self):
        # Parametri iniziali per la Stazione Spaziale
        self.oxygen_level = 21.0  # Range normale: 19.5% - 23.5%
        self.co2_level = 0.04     # Range normale: < 0.1%
        self.water_purity = 98.5  # Percentuale di purezza dell'acqua
        self.temperature = 22.0   # Celsius (Normale: 20-24°C)
        self.humidity = 45.0      # Percentuale (Normale: 30-60%)
        self.system_status = "ONLINE"

    def controllo_ossigeno_co2(self):
        print("[O2/CO2] Monitoraggio dei livelli atmosferici in corso...")
        if self.oxygen_level < 20.0:
            print("[O2/CO2] Attenzione: Livello di ossigeno basso! Avvio generatori di emergenza.")
            self.oxygen_level += 1.5
        elif self.co2_level > 0.1:
            print("[O2/CO2] Attenzione: Concentrazione di CO2 elevata! Attivazione depuratori.")
            self.co2_level -= 0.02
        else:
            print("[O2/CO2] Parametri atmosferici stabili. O2: {:.2f}%, CO2: {:.2f}%".format(self.oxygen_level, self.co2_level))

    def sistema_filtrazione_acqua(self):
        print("[Acqua] Avvio del ciclo di filtrazione dell'acqua...")
        if self.water_purity < 95.0:
            print("[Acqua] Attenzione: Purezza calata! Aumento della potenza di filtrazione.")
            self.water_purity = 99.0
        else:
            print("[Acqua] Sistema di filtrazione ottimale. Livello di purezza: {:.2f}%".format(self.water_purity))

    def controllo_temperatura_umidita(self):
        print("[Clima] Regolazione della temperatura e dell'umidità interna...")
        self.temperature += random.uniform(-0.5, 0.5)
        self.humidity += random.uniform(-1.0, 1.0)
        print("[Clima] Temperatura: {:.2f}°C, Umidità: {:.2f}%".format(self.temperature, self.humidity))

    def allarmi_sicurezza(self):
        print("[Sicurezza] Scansione dei protocolli di sicurezza...")
        if self.oxygen_level < 19.0 or self.temperature > 28.0 or self.water_purity < 90.0:
            self.system_status = "CRITICAL ALARM"
            print(f"[ALLARME DI SICUREZZA] Stato: {self.system_status}! Richiesto intervento immediato dell'equipaggio!")
        else:
            self.system_status = "SECURE"
            print(f"[Sicurezza] Tutti i sistemi operativi sono normali. Stato: {self.system_status}")

    def integrazione_dashboard(self):
        print("--------------------------------------------------")
        print("         PANNELLO DI CONTROLLO - STAZIONE SPAZIALE")
        print("--------------------------------------------------")
        print(f" Stato del Sistema : {self.system_status}")
        print(f" Livello Ossigeno  : {self.oxygen_level:.2f}%")
        print(f" Livello CO2       : {self.co2_level:.2f}%")
        print(f" Purezza Acqua     : {self.water_purity:.2f}%")
        print(f" Temperatura       : {self.temperature:.2f}°C")
        print(f" Umidità           : {self.humidity:.2f}%")
        print("--------------------------------------------------\n")

if __name__ == "__main__":
    station = LifeSupportSystem()
    for ciclo in range(3):
        print(f"--- Ciclo di controllo #{ciclo + 1} ---")
        station.controllo_ossigeno_co2()
        station.sistema_filtrazione_acqua()
        station.controllo_temperatura_umidita()
        station.allarmi_sicurezza()
        station.integrazione_dashboard()
        time.sleep(1)
