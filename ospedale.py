import json
import os


class Persona:
    def __init__(self, nome, cognome, cf):
        self.nome = nome
        self.cognome = cognome
        self.cf = cf


class Paziente(Persona):
    def __init__(self, id_paziente, nome, cognome, cf, medico_assegnato):
        super().__init__(nome, cognome, cf)
        self.id_paziente = id_paziente
        self.medico_assegnato = medico_assegnato


class Medico(Persona):
    def __init__(self, matricola, nome, cognome):
        super().__init__(nome, cognome, None)
        self.matricola = matricola
        self.num_pazienti = 0
        self.pazienti = []


FILE_DATI = "dati_ospedale.json"


def salva_dati(id_pazienti):
    dati = {
        "id_pazienti": id_pazienti,
        "medici": [vars(m) for m in medici],
        "pazienti": [vars(p) for p in pazienti],
    }
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4, ensure_ascii=False)


def carica_dati():
    if not os.path.exists(FILE_DATI):
        return 1
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        try:
            dati = json.load(f)
        except json.JSONDecodeError:
            return 1
        for dato in dati["medici"]:
            medico = Medico(dato["matricola"], dato["nome"], dato["cognome"])
            medico.num_pazienti = dato["num_pazienti"]
            medico.pazienti = dato["pazienti"]
            medici.append(medico)
        for dato in dati["pazienti"]:
            paziente = Paziente(
                dato["id_paziente"],
                dato["nome"],
                dato["cognome"],
                dato["cf"],
                dato["medico_assegnato"],
            )
            pazienti.append(paziente)
        return dati["id_pazienti"]


pazienti = []
medici = []
id_pazienti = carica_dati()


def nuovo_paziente(id_persone):
    nome = input("Inserisci nome: ")
    cognome = input("Inserisci cognome: ")
    cf = input("Inserici codice fiscale: ")
    esito_paziente = scheda_paziente(cf)
    if esito_paziente != None:
        print("IL PAZIENTE E GIA STATO INSERITO")
    else:
        paziente = Paziente(id_persone, nome, cognome, cf, None)
        pazienti.append(paziente)


def nuovo_medico():
    matricola = int(input("Inserisci matricola: "))
    nome = input("Inserisci nome: ")
    cognome = input("Inserisci cognome: ")
    medico = Medico(matricola, nome, cognome)
    medici.append(medico)


def visualizza_medici(medici):
    for medico in medici:
        print(f"Nome: {medico.nome} Cognome: {medico.cognome}")


def scheda_paziente(cf):
    for paziente in pazienti:
        if cf == paziente.cf:
            return paziente
    return None


def cerca_medico(matricola):
    for medico in medici:
        if matricola == medico.matricola:
            return medico
    return None


run = True
while run:
    print("------OSPEDALE------")
    print("1: Nuovo medico")
    print("2: Nuovo paziente")
    print("3: Assegna medico a paziente")
    print("4: Visualizza medici")
    print("5: Scheda paziente")
    print("6: Scheda medico")
    print("0: Esci")
    scelta = int(input("Scelta: "))
    if scelta == 0:
        run = False
        salva_dati(id_pazienti)
        print("------A PRESTO------")
        break
    elif scelta == 1:
        nuovo_medico()
        salva_dati(id_pazienti)
    elif scelta == 2:
        nuovo_paziente(id_pazienti)
        id_pazienti += 1
        salva_dati(id_pazienti)
    elif scelta == 3:
        matricola = int(input("Inserisci la matricola del medico: "))
        esito_medico = cerca_medico(matricola)
        if esito_medico == None:
            print("Medico non trovato!")
        elif esito_medico.num_pazienti >= 500:
            print("NON PUOI ASSEGNARE PIU DI 500 PAZIENTI AL MEDICO")
        else:
            cf = input("Inserisci codice fiscale: ")
            esito_paziente = scheda_paziente(cf)
            if esito_paziente == None:
                print("Paziente non trovato!")
            elif esito_paziente.medico_assegnato != None:
                print("IL PAZIENTE GIA E ASSEGNATO AL MEDICO")
            else:
                print(
                    f"MEDICO: Nome: {esito_medico.nome} | Cognome: {esito_medico.cognome}"
                )
                print(
                    f"PAZIENTE: Nome: {esito_paziente.nome} | Cognome: {esito_paziente.cognome}"
                )
                risposta = input("VUOI ASSEGNARE MEDICO AL PAZIENTE (s/n):").lower()
                if risposta == "n":
                    print("MEDICO NON ASSEGNATO!")
                elif risposta == "s":
                    esito_paziente.medico_assegnato = esito_medico.matricola
                    esito_medico.pazienti.append(esito_paziente.cf)
                    esito_medico.num_pazienti += 1
                    salva_dati(id_pazienti)
                    print("PAZIENTE ASSEGNATO")
                else:
                    print("RISPOSTA NON VALIDA")

    elif scelta == 4:
        visualizza_medici(medici)
    elif scelta == 5:
        cf = input("Inserisci il codice fiscale: ")
        esito_paziente = scheda_paziente(cf)
        if esito_paziente == None:
            print("Paziente non trovato!")
        else:
            print(
                f"Nome: {esito_paziente.nome} | Cognome: {esito_paziente.cognome} | Medico Assegnato: {esito_paziente.medico_assegnato}"
            )
            if esito_paziente.medico_assegnato == None:
                pass
            else:
                esito_medico = cerca_medico(esito_paziente.medico_assegnato)
                print(f"Medico Assegnato: {esito_medico.nome} {esito_medico.cognome}")
    elif scelta == 6:
        matricola = int(input("Inserisci la matricola del medico: "))
        esito_medico = cerca_medico(matricola)
        if esito_medico == None:
            print("Il medico non trovato!")
        else:
            print(f"MEDICO: Nome: {esito_medico.nome} | Cognome:{esito_medico.cognome}")
            for paziente in esito_medico.pazienti:
                esito_paziente = scheda_paziente(paziente)
                print(
                    f"-------------Nome: {esito_paziente.nome} | Cognome: {esito_paziente.cognome}"
                )
