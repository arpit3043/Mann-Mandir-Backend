from __future__ import annotations

IST_TIMEZONE = "Asia/Kolkata"

TITHI_NAMES = (
    "Pratipada",
    "Dwitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dwadashi",
    "Trayodashi",
    "Chaturdashi",
    "Purnima",
)
KRISHNA_AMAVASYA = "Amavasya"
NAKSHATRAS = (
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashirsha",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
)
YOGA_NAMES = (
    "Vishkambha",
    "Priti",
    "Ayushman",
    "Saubhagya",
    "Shobhana",
    "Atiganda",
    "Sukarma",
    "Dhriti",
    "Shoola",
    "Ganda",
    "Vriddhi",
    "Dhruva",
    "Vyaghata",
    "Harshana",
    "Vajra",
    "Siddhi",
    "Vyatipata",
    "Variyan",
    "Parigha",
    "Shiva",
    "Siddha",
    "Sadhya",
    "Shubha",
    "Shukla",
    "Brahma",
    "Indra",
    "Vaidhriti",
)
WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)
WEEKDAYS_HI = (
    "सोमवार",
    "मंगलवार",
    "बुधवार",
    "गुरुवार",
    "शुक्रवार",
    "शनिवार",
    "रविवार",
)
RITU_BY_MONTH = {
    1: "Hemanta",
    2: "Shishira",
    3: "Shishira",
    4: "Vasanta",
    5: "Vasanta",
    6: "Grishma",
    7: "Grishma",
    8: "Varsha",
    9: "Varsha",
    10: "Sharad",
    11: "Sharad",
    12: "Hemanta",
}
UTTARAYANA_START_MONTH = 3
UTTARAYANA_END_MONTH = 9
AYANA_UTTARAYANA = "Uttarayana"
AYANA_DAKSHINAYANA = "Dakshinayana"
PAKSHA_KRISHNA = "Krishna"
PAKSHA_SHUKLA = "Shukla"

WEEKDAY_MANTRA_IDS = {
    0: "m3",
    1: "m7",
    2: "m8",
    3: "m4",
    4: "m9",
    5: "m10",
    6: "m1",
}
WEEKDAY_DEITIES = {
    0: ("Monday", "सोमवार", "Shiva"),
    1: ("Tuesday", "मंगलवार", "Hanuman"),
    2: ("Wednesday", "बुधवार", "Ganesha"),
    3: ("Thursday", "गुरुवार", "Vishnu"),
    4: ("Friday", "शुक्रवार", "Lakshmi"),
    5: ("Saturday", "शनिवार", "Shani"),
    6: ("Sunday", "रविवार", "Surya"),
}

VEDA_STANZA_SPLIT_PATTERN = r"॥\s*[0-9०-९]+\s*॥"
YAJUR_SPLIT_PATTERN = r"।{2}\s*\d+\s*।{2}"
