#!/usr/bin/env python3


"""
Autor: Marco Heins

Version: 0.1

Lizenz: MIT

Erstellt eine Einnahmeüberschussrechnung zur freiberuflichen Einkommenssteuererklärung
aus einer csv-Datei mit Kontobewegungen der Apobank
und gibt eine csv-Datei mit summierten Einnahmen und Ausgaben aus.
"""


from collections import OrderedDict
import csv
from functools import reduce
import operator
from pprint import pformat
from typing import List


EUES_CSV_SPALTENNAMEN = (
    'einnahmen_text', 'einnahmen_betrag', 'ausgaben_text', 'ausgaben_betrag')


class Konto:
    """Erlaub das summieren und auflisten von Buchungen anhand von
    Suchbegriffen im Buchungstext
    """
    def __init__(self, csv_datei: str) -> None:
        """Erstellt eine Buchungsliste aus csv-Datei

        Args:

            csv_datei: Dateiname der Kontobewegungen bei der Apobank

        Return:

            Kein
        """
        with open(csv_datei, "rt", newline="", encoding="ISO-8859-1") as dateiname:
            csv.register_dialect("semi", delimiter=";")
            csv_dictreader = csv.DictReader(dateiname, dialect='semi')
            self._buchungen = list(csv_dictreader)

        for buchung in self._buchungen:
            if buchung.get('Belastung'):
                buchung['Belastung'] = Konto.usa_format(buchung['Belastung']) * -1
            elif buchung.get('Gutschrift'):
                buchung['Gutschrift'] = Konto.usa_format(buchung['Gutschrift'])
            else:
                del self._buchungen[self._buchungen.index(buchung)]

    def gesamt(self, suchtext: str) -> float:
        """Addiere alle Buchungen in denen der Suchtext vorkommt

        Args:

            suchtext: Alle Buchungen mit suchtext im Buchungstext werden summiert

        Return:

            Gesamtbetrag der gefundenen Buchungen

        Raises:

            Exception: Falls Buchung weder Gutschrift noch Belastung
        """
        try:
            return sum(
                [buchung['Gutschrift'] if buchung['Gutschrift'] else buchung['Belastung']
                 for buchung in self if suchtext in buchung['Buchungstext']]
            )
        except TypeError as type_error:
            raise Exception('Buchung ist weder Gutschrift noch Belastung!') from type_error

    def zeige_buchungen(self, suchtext: str = '', buchungstext: bool = False) -> list:
        """Zeige alle Buchungen an, in denen der Suchtext vorkommt

        Keyword Args:

            suchtext: Text, welcher im Buchungstext enthalten sein soll (default: '')
            buchungstext: Buchungstext auch mit anzeigen (default: False)

        Return:

            Formatierte Buchungsliste
        """

        return [[buchung['Buchungsdatum'],
                 buchung['Gutschrift'] if buchung['Gutschrift'] else buchung['Belastung'],
                 buchung['Buchungstext'] if buchungstext is True else '']
                for buchung in self._buchungen if suchtext in buchung['Buchungstext']]

    @staticmethod
    def usa_format(waehrung: str):
        """Wandelt deutsches Zahlenformat in amerikanisches um

        Args:

            Betrag im deutschen Währungsformat

        Return:

            Betrag im amerikanischen Währungsformat
        """
        return float(waehrung.replace('.', '').replace(',', '.'))

    def __iter__(self):
        return iter(self._buchungen)

    def __getitem__(self, item):  # pragma: no cover
        return self._buchungen[item]


class Eues:
    """ Erstellung einer Einnahmeüberschussrechnung für Freiberufler
    im Rahmen der Einkommenssteuererklärung
    """
    def __init__(self, konto_csvdatei: str):
        """Liest eine csv-Datei mit Buchungen ein,
        bereinigt diese um leere Buchungen und
        ändert das Währungsformat von Deutsch auf Amerikanisch

        Args:

            konto_csvdatei: csv-Textdatei der Apobank mit Buchungen

        Return:

            Kein
        """
        self.konto = Konto(konto_csvdatei)
        self.eues: List = []

    def neue_einnahme(self, kategorie: str, *, suchtext: str) -> None:
        """Fügt eine neue Einnahmenkategorie und deren Gesamtbetrag zur EÜS hinzu

        Args:

            kategorie: Name der Einnahmenkategorie
            suchtext: Alle Buchungen mit suchtext im Buchungstext werden summiert

        Return:

            Kein
        """

        self._neuer_posten('einnahme', kategorie, self.konto.gesamt(suchtext))

    def neue_ausgabe(self, kategorie: str, *, suchtext: str) -> None:
        """Fügt eine neue Ausgabenkategorie und deren Gesamtbetrag zur EÜS hinzu

        Args:

            kategorie: Name der Ausgabenkategorie
            suchtext: Alle Buchungen mit suchtext im Buchungstext werden summiert

        Return:

            Kein
        """

        self._neuer_posten('ausgabe', kategorie, self.konto.gesamt(suchtext))

    def schreib_csv(self, dateiname: str):
        """Fertige EÜS in csv-datei ausgeben

        Args:

            dateiname: Name der csv-Datei

        Return:

            Kein
        """
        csv_writer = csv.writer(open(dateiname, 'wt', encoding='utf-8'))  # pylint: disable=R1732
        csv_writer.writerow(EUES_CSV_SPALTENNAMEN)
        csv_writer.writerows(self.flache_eues)

    @property
    def flache_eues(self) -> list[list[str]]:
        """Wandelt den eüs-Datentyp um zum einfachen Schreiben in csv-Ausgabedatei

        Return:

            Liste von csv-Zeilen
        """

        return list(reduce(operator.add,
                           list([str(eintrag) for eintrag in text_betrag.values()]
                                for text_betrag in zeile.values()))
                    for zeile in self.eues)

    def _neuer_posten(
            self, einnahme_ausgabe: str, kategorie: str, gesamtbetrag) -> None:
        """Falls passende Spalten in vorhandenen Zeilen frei sind dort eintragen,
        sonst neue Zeile anlegen

        Args:

            einnahme_ausgabe: 'einnahme' oder 'ausgabe'
            kategorie: Name der Kategorie
            gesamtbetrag: Summe der Kategorie

        Return:

            Kein

        Note:

            Fügt neue Einträge in eüs ein oder modifiziert bestehende
        """

        for zeile in self.eues:
            if not zeile[einnahme_ausgabe]['betrag']:
                zeile[einnahme_ausgabe]['text'] = kategorie
                zeile[einnahme_ausgabe]['betrag'] = gesamtbetrag
                return

        neue_zeile = OrderedDict([('einnahme', OrderedDict([('text', ''), ('betrag', '')]),),
                                  ('ausgabe', OrderedDict([('text', ''), ('betrag', '')]),)])
        neue_zeile[einnahme_ausgabe]['text'] = kategorie
        neue_zeile[einnahme_ausgabe]['betrag'] = gesamtbetrag

        self.eues.append(neue_zeile)

    def __repr__(self):  # pragma: no cover
        """"""
        return pformat(self.eues)

    def __weakref__(self):
        """"""


def main():  # pragma: no cover  pylint: disable=C0116
    eues.neue_einnahme('KVH-Honorar', suchtext='KVH')
    eues.neue_einnahme('Untermiete', suchtext='SCHOLZ')

    eues.neue_ausgabe('Strom/Gas', suchtext='PROENGENO')
    eues.neue_ausgabe('Miete', suchtext='Eike Pflüger Info: Miete Praxisräume')
    eues.neue_ausgabe('Praxisreinigung', suchtext='MUENNICH')
    eues.neue_ausgabe('Strom/Gas', suchtext='PROENGENO')
    eues.neue_ausgabe('EDV', suchtext='HASOMED')
    eues.neue_ausgabe('Krankenkasse', suchtext='Techniker Krankenkasse')
    eues.neue_ausgabe('Versorgunswerk', suchtext='Psychotherapeutenversorgungswerk')
    eues.neue_ausgabe('DSL', suchtext='Vodafone')
    eues.neue_ausgabe('Praxishandy', suchtext='Drillisch')
    eues.neue_ausgabe('Steuervorauszahlung', suchtext='Landeshauptkasse')
    eues.neue_ausgabe('GEZ-Praxis', suchtext='Rundfunk')


if __name__ == '__main__':  # pragma: no cover
    eues = Eues('apo.csv')
    main()
    eues.schreib_csv('ausgabe.csv')
