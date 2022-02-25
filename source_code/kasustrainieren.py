import os
import subprocess
import sys
import bs4
import spacy
from menudownload import *
import de_dep_news_trf
satzanalyse_werkzeug = de_dep_news_trf.load()
import regex
import pickle
from satzmetzger.satzmetzger import Satzmetzger
import numpy as np
from einfuehrung import einfuehrung

linebreaknach = 70
allekasus = ["Nominativ", "Akkusativ", "Dativ", "Genitiv"]


def read_pkl(filename):
    with open(filename, "rb") as f:
        data_pickle = pickle.load(f)
    return data_pickle


def transpose_list_of_lists(listexxx):
    try:
        return [list(xaaa) for xaaa in zip(*listexxx)]
    except Exception as Fehler:
        print(Fehler)
        try:
            return np.array(listexxx).T.tolist()
        except Exception as Fehler:
            print(Fehler)
            return listexxx


def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
                b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = bs4.BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)


def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))


def get_text():
    p = subprocess.run(get_file_path(r"Everything2TXT.exe")[0], capture_output=True)
    ganzertext = txtdateien_lesen(p.stdout)
    return ganzertext




einfuehrung('Kasustrainer')
satzmetzgerle = Satzmetzger()
ganzertext = get_text()
einzelnesaetze = satzmetzgerle.zerhack_den_text(ganzertext)
allesaetzefertigfueraufgabe = []
verbendeenpt = read_pkl(
    r"verbendept.pkl"
)
alleexistierendenverben = transpose_list_of_lists(verbendeenpt)[0]
allemoeglichenpunkte = 0
punktevomuser = 0
for satzindex, einzelnersatz in enumerate(einzelnesaetze):
    analysierter_text = satzanalyse_werkzeug(einzelnersatz)
    dokument_als_json = analysierter_text.doc.to_json()
    alleverbenimsatz = []
    schongedruckt = False
    for token in dokument_als_json["tokens"]:
        anfangwort = token["start"]
        endewort = token["end"]
        aktuelleswort = dokument_als_json["text"][anfangwort:endewort]
        leerzeichenplatz = len(dokument_als_json["text"][anfangwort:endewort]) * "_"
        platzhalter = (
                dokument_als_json["text"][:anfangwort]
                + leerzeichenplatz
                + dokument_als_json["text"][endewort:]
        )
        satzschongemacht = dokument_als_json["text"][:anfangwort]
        satzdrucken = drucker.f.black.white.italic('Wir sind hier:   ') + drucker.f.white.black.normal(satzschongemacht) + drucker.f.brightyellow.black.italic(aktuelleswort)

        if 'Case=' in token["morph"]:
            allemoeglichenpunkte = allemoeglichenpunkte+1
            print(drucker.f.black.white.italic('Kompletter Satz: ') + drucker.f.white.black.normal(dokument_als_json["text"]))

            print(satzdrucken)
            richtigeantwort = regex.findall('Case=([^\|]+)', token["morph"])[0]
            if richtigeantwort == 'Nom':
                richtigeantwort = 'Nominativ'
            if richtigeantwort == 'Acc':
                richtigeantwort = 'Akkusativ'
            if richtigeantwort == 'Dat':
                richtigeantwort = 'Dativ'
            if richtigeantwort == 'Gen':
                richtigeantwort = 'Genitiv'
            anwortchecken = create_color_menu(allekasus)
            if anwortchecken ==  richtigeantwort:
                punktevomuser = punktevomuser+1
                print(drucker.f.brightwhite.green.bold(f'\n       Die Antwort: "{richtigeantwort}" war richtig!\n'))
            elif anwortchecken !=  richtigeantwort:
                print(drucker.f.brightwhite.red.bold(f'\n        Die Antwort "{anwortchecken}" war falsch! "{richtigeantwort}" ist richtig!\n'))
            print(drucker.f.brightyellow.black.italic(f'\nPunktestand: Du hast  ') + drucker.f.brightyellow.black.negative(f'{punktevomuser} von {allemoeglichenpunkte}') + drucker.f.brightyellow.black.italic(' möglichen Punkten erreicht!\n'))
            print('\n' * 10)

ende = input(drucker.f.brightyellow.black.italic(f'\nPunktestand: Du hast insgesamt  ') + drucker.f.brightyellow.black.negative(
    f'{punktevomuser} von {allemoeglichenpunkte}') + drucker.f.brightyellow.black.italic(
    ' möglichen Punkten erreicht!\n'))
