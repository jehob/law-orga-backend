#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2020  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

prod_record_tags: [{"name": str, "name_de": str, "name_it": str}] = [
    {
        "name": "Family reunification",
        "name_de": "Familiennachzug",
        "name_it": "Riunificazione familiare",
    },
    {"name": "Dublin IV", "name_de": "Dublin IV", "name_it": "Dublino IV"},
    {
        "name": "Work permit",
        "name_de": "Arbeitserlaubnis",
        "name_it": "Permesso di lavoro",
    },
    {
        "name": "Refugee status",
        "name_de": "Flüchtlingseigenschaft",
        "name_it": "Lo status di rifugiato",
    },
    {
        "name": "subsidiary protection",
        "name_de": "subsidiärer Schutz",
        "name_it": "protezione sussidiaria",
    },
    {"name": "Marriage", "name_de": "Eheschließung", "name_it": "Matrimonio"},
    {"name": "Engagement", "name_de": "Verlobung", "name_it": "Fidanzamento"},
    {
        "name": "illegal departure from the federal territory",
        "name_de": "illegale Ausreise aus dem Bundesgebiet",
        "name_it": "partenza illegale dal territorio federale",
    },
    {"name": "Immersion", "name_de": "Untertauchen", "name_it": "Immersione"},
    {
        "name": "Recognize children",
        "name_de": "Kinder anerkennen",
        "name_it": "Riconosci i bambini",
    },
    {"name": "Training", "name_de": "Ausbildung", "name_it": "Formazione"},
    {"name": "Birth", "name_de": "Geburt", "name_it": "Nascita"},
    {
        "name": "A child in the asylum procedure",
        "name_de": "Eines Kindes im Asylverfahren",
        "name_it": "Un bambino nella procedura di asilo",
    },
    {"name": "Toleration", "name_de": "Duldung", "name_it": "Tolleranza"},
    {"name": "Training tolerance", "name_de": "Ausbildungsduldung", "name_it": "asd"},
    {"name": "Visa", "name_de": "Visum", "name_it": "Visa"},
    {"name": "Hearing", "name_de": "Anhörung", "name_it": "Udito"},
    {
        "name": "Change of Accommodation",
        "name_de": "Wechsel der Unterkunft",
        "name_it": "Cambio di alloggio",
    },
    {
        "name": "Residence requirement",
        "name_de": "Wohnsitzauflage",
        "name_it": "Requisito di residenza",
    },
    {
        "name": "Follow-up application",
        "name_de": "Folgeantrag",
        "name_it": "Domanda di follow-up",
    },
    {
        "name": "Confirmatory application",
        "name_de": "Zweitantrag",
        "name_it": "Domanda di conferma",
    },
    {
        "name": "Accommodation in the asylum procedure",
        "name_de": "Unterbringung im Asylverfahren",
        "name_it": "Sistemazione nella procedura di asilo",
    },
    {
        "name": "Revocation of the right to asylum",
        "name_de": "Widerruf der Asylberechtigung",
        "name_it": "Revoca del diritto di asilo",
    },
    {
        "name": "Withdrawal of asy entitlement",
        "name_de": "Rücknahme der Asyberechtigung",
        "name_it": "Revoca del diritto di asy",
    },
    {
        "name": "Obtaining a passport",
        "name_de": "Passbeschaffung",
        "name_it": "Ottenere un passaporto",
    },
    {
        "name": "Obligations to cooperate",
        "name_de": "Mitwirkungspflichten",
        "name_it": "Obblighi di collaborazione",
    },
    {
        "name": "Failure to conduct the procedure",
        "name_de": "Nichtbetreiben des Verfahrens",
        "name_it": "Mancata esecuzione della procedura",
    },
    {
        "name": "Illness in the asylum procedure",
        "name_de": "Krankheit im Asylverfahren",
        "name_it": "Malattia nella procedura di asilo",
    },
    {"name": "Family asylum", "name_de": "Familienasyl", "name_it": "Asilo familiare"},
    {
        "name": "unaccompanied minor refugee",
        "name_de": "UmF",
        "name_it": "rifugiato minore non accompagnato",
    },
    {
        "name": "Dublin III family reunification",
        "name_de": "Familienzusammenführung nach Dublin III",
        "name_it": "Ricongiungimento familiare Dublino III",
    },
    {
        "name": "Negative response",
        "name_de": "Negativbescheid",
        "name_it": "Risposta negativa",
    },
    {"name": "Relocation", "name_de": "Relocation", "name_it": "Trasferimento"},
    {"name": "Resettlement", "name_de": "Resettlement", "name_it": "Reinsediamento"},
    {
        "name": "Asylum Seekers Benefits Act",
        "name_de": "Asylbewerberleistungsgesetz",
        "name_it": "Asylum Seekers Benefits Act",
    },
    {"name": "Church asylum", "name_de": "Kirchenasyl", "name_it": "Chiesa asilo"},
    {
        "name": "Application for asylum",
        "name_de": "Asylantrag",
        "name_it": "Domanda di asilo",
    },
    {"name": "Deportation", "name_de": "Abschiebung", "name_it": "Deportazione"},
    {
        "name": "Action for failure to act",
        "name_de": "Untätigkeitsklage",
        "name_it": "Azione per inadempienza",
    },
    {"name": "Education", "name_de": "Studium", "name_it": "Formazione scolastica"},
    {"name": "Prosecution", "name_de": "Strafverfolgung", "name_it": "Accusa"},
    {"name": "Other", "name_de": "Sonstiges", "name_it": "Altro"},
    {
        "name": "Residence permit",
        "name_de": "Aufenthaltserlaubnis",
        "name_it": "Permesso di soggiorno",
    },
    {
        "name": "Residence permit 2",
        "name_de": "Aufenthaltsgestattung",
        "name_it": "Permesso di residenza",
    },
    {
        "name": "Permanent residence permit",
        "name_de": "Niederlassungserlaubnis",
        "name_it": "Permesso di soggiorno permanente",
    },
    {
        "name": "Naturalization",
        "name_de": "Einbürgerung",
        "name_it": "Naturalizzazione",
    },
    {"name": "Citizenship", "name_de": "Staatsbürgerschaft", "name_it": "Cittadinanza"},
]
