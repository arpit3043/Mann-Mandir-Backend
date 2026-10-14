"""Bundled fallback content (replacements when upstream APIs fail)."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

ALL_AARTIS: List[Dict[str, Any]] = [
    {
        "id": "aarti-ganesh",
        "name": "Jai Ganesh Deva",
        "deity": "Ganesha",
        "devanagari": "जय गणेश जय गणेश जय गणेश देवा",
        "transliteration": "Jai Ganesh Jai Ganesh Jai Ganesh Deva",
        "translation": "Victory to Lord Ganesha, son of Parvati and Shiva.",
        "verses": [
            "जय गणेश जय गणेश जय गणेश देवा माता जाकी पार्वती पिता महादेवा",
            "एक दन्त दयावन्त चार भुजा धारी माथे पर तिलक सोहे मूसे की सवारी",
        ],
    },
    {
        "id": "aarti-lakshmi",
        "name": "Jai Lakshmi Mata",
        "deity": "Lakshmi",
        "devanagari": "जय लक्ष्मी माता",
        "transliteration": "Jai Lakshmi Mata",
        "translation": "Victory to Mother Lakshmi, goddess of wealth and prosperity.",
        "verses": [
            "जय लक्ष्मी माता, मैया जय लक्ष्मी माता। तुमको निसदिन सेवत हर विष्णु विधाता॥",
            "उमा, रमा, ब्रह्माणी, तुम ही जग-माता। सूर्य-चंद्रमा ध्यावत नारद ऋषि गाता॥",
        ],
    },
    {
        "id": "aarti-shiva",
        "name": "Om Jai Shiv Omkara",
        "deity": "Shiva",
        "devanagari": "ॐ जय शिव ओंकारा",
        "transliteration": "Om Jai Shiv Omkara",
        "translation": "Glory to Lord Shiva, the primordial sound.",
        "verses": [
            "ॐ जय शिव ओंकारा, स्वामी जय शिव ओंकारा। ब्रह्मा विष्णु सदाशिव, अर्द्धांगी धारा॥",
            "एकानन चतुरानन पञ्चानन राजे। हंसासन गरूड़ासन वृषवाहन साजे॥",
        ],
    },
    {
        "id": "aarti-krishna",
        "name": "Jai Jagdish Hare",
        "deity": "Vishnu/Krishna",
        "devanagari": "ॐ जय जगदीश हरे",
        "transliteration": "Om Jai Jagdish Hare",
        "translation": "Victory to the Lord of the Universe.",
        "verses": [
            "ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे। भक्त जनों के संकट, क्षण में दूर करे॥",
            "जो ध्यावे फल पावे, दुःख विनसे मन का। सुख सम्पत्ति घर आवे, कष्ट मिटे तन का॥",
        ],
    },
    {
        "id": "aarti-durga",
        "name": "Jai Ambe Gauri",
        "deity": "Durga",
        "devanagari": "जय अम्बे गौरी",
        "transliteration": "Jai Ambe Gauri",
        "translation": "Victory to Mother Durga, the divine feminine power.",
        "verses": [
            "जय अम्बे गौरी, मैया जय श्यामा गौरी। तुमको निशिदिन ध्यावत, हरि ब्रह्मा शिवरी॥",
            "माँग सिन्दूर विराजत, टीको मृगमद को। उज्ज्वल से दोउ नैना, चन्द्रवदन नीको॥",
        ],
    },
    {
        "id": "aarti-saraswati",
        "name": "Jai Saraswati Mata",
        "deity": "Saraswati",
        "devanagari": "जय सरस्वती माता",
        "transliteration": "Jai Saraswati Mata",
        "translation": "Victory to Goddess Saraswati, bestower of knowledge.",
        "verses": [
            "जय सरस्वती माता, मैया जय सरस्वती माता। सद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥",
            "चन्द्रवदनि पद्मासिनी, ध्युति मंगलकारी। सोहभा श्वेताम्बर, सुरनर मुनि तारी॥",
        ],
    },
]

ALL_CHALISAS: List[Dict[str, Any]] = [
    {"id": "chalisa-hanuman", "deity": "Hanuman", "title": "Hanuman Chalisa", "totalVerses": 40},
    {"id": "chalisa-ganesh", "deity": "Ganesh", "title": "Ganesh Chalisa", "totalVerses": 40},
    {"id": "chalisa-durga", "deity": "Durga", "title": "Durga Chalisa", "totalVerses": 40},
    {"id": "chalisa-lakshmi", "deity": "Lakshmi", "title": "Lakshmi Chalisa", "totalVerses": 40},
    {"id": "chalisa-shiva", "deity": "Shiva", "title": "Shiv Chalisa", "totalVerses": 40},
    {"id": "chalisa-saraswati", "deity": "Saraswati", "title": "Saraswati Chalisa", "totalVerses": 40},
    {"id": "chalisa-ram", "deity": "Ram", "title": "Ram Chalisa", "totalVerses": 40},
]

_SHIVA_TANDAVA_VERSES: List[Dict[str, Any]] = [
    {
        "verseNumber": 1,
        "sanskrit": "जटा टवी गलज्जलप्रवाह पावितस्थले गलेऽव लम्ब्यलम्बितां भुजंगतुंग मालिकाम्‌",
        "transliteration": "Jata tavi galaj jal pravah pavit sthale gale av lambya lambitam bhujang tung malikam",
        "meaning": "His neck is purified by the flowing waters from his matted hair, a serpent hangs like a garland",
    },
    {
        "verseNumber": 2,
        "sanskrit": "जटाकटा हसंभ्रम भ्रमन्निलिंपनिर्झरी विलोलवीचिवल्लरी विराजमानमूर्धनि",
        "transliteration": "Jata kata hasambhram bhraman nilimpanirjhari vilol vichi vallari virajmaan moordhani",
        "meaning": "My devotion lies in Shiva whose head is adorned by the flowing Ganga",
    },
    {
        "verseNumber": 16,
        "sanskrit": "इमं हि नित्यमेव मुक्तमुक्तमोत्तम स्तवं पठन्स्मरन्‌ ब्रुवन्नरो विशुद्धमेति संततम्‌",
        "transliteration": "Imam hi nityameva muktamuktamottam stavam pathan smaran bruvannaro vishuddhameti santatam",
        "meaning": "Whoever recites this hymn becomes pure, gains devotion to Shiva",
    },
]

ALL_STOTRAMS: List[Dict[str, Any]] = [
    {
        "id": "stotram-vishnu-sahasranama",
        "name": "Vishnu Sahasranama",
        "deity": "Vishnu",
        "author": "Vyasa",
        "description": "The thousand names of Lord Vishnu",
        "verseCount": 107,
        "verses": [],
    },
    {
        "id": "stotram-shiva-tandava",
        "name": "Shiva Tandava Stotram",
        "deity": "Shiva",
        "author": "Ravana",
        "description": "The cosmic dance of Lord Shiva described by Ravana",
        "verseCount": 17,
        "verses": _SHIVA_TANDAVA_VERSES,
    },
    {
        "id": "stotram-mahishasura-mardini",
        "name": "Mahishasura Mardini Stotram",
        "deity": "Durga",
        "author": "Adi Shankaracharya",
        "description": "Hymn to Goddess Durga, the slayer of Mahishasura",
        "verseCount": 21,
        "verses": [],
    },
    {
        "id": "stotram-aditya-hridayam",
        "name": "Aditya Hridayam",
        "deity": "Surya",
        "author": "Agastya",
        "description": "Hymn to the Sun God, from Valmiki Ramayana",
        "verseCount": 30,
        "verses": [],
    },
    {
        "id": "stotram-soundarya-lahari",
        "name": "Soundarya Lahari",
        "deity": "Parvati",
        "author": "Adi Shankaracharya",
        "description": "Waves of beauty — 100 verses to Goddess Parvati",
        "verseCount": 100,
        "verses": [],
    },
    {
        "id": "stotram-ganesh-atharvashirsha",
        "name": "Ganesh Atharvashirsha",
        "deity": "Ganesh",
        "author": "Atharva Veda",
        "description": "Upanishad dedicated to Lord Ganesha",
        "verseCount": 14,
        "verses": [],
    },
]

VEDA_MANTRA_POOL: List[Dict[str, Any]] = [
    {
        "id": "m1",
        "name": "Gayatri Mantra",
        "devanagari": "ॐ भूर् भुवः स्वः। तत् सवितुर् वरेण्यम्। भर्गो देवस्य धीमहि। धियो यो नः प्रचोदयात्॥",
        "transliteration": "Om bhur bhuvah svah, tat savitur varenyam, bhargo devasya dhimahi, dhiyo yo nah prachodayat",
        "meaning": "We meditate on the divine light of the sun god Savitri. May he illuminate our intellect.",
        "deity": "Surya",
        "veda": "Rig",
        "tags": ["gayatri", "surya", "morning"],
    },
    {
        "id": "m2",
        "name": "Maha Mrityunjaya Mantra",
        "devanagari": "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय माऽमृतात्॥",
        "transliteration": "Om tryambakam yajamahe sugandhim pushtivardhanam, urvarukamiva bandhanat mrityor mukshiya mamritat",
        "meaning": "We worship the three-eyed Shiva who nourishes all.",
        "deity": "Shiva",
        "veda": "Yajur",
        "tags": ["shiva", "healing", "longevity"],
    },
    {
        "id": "m3",
        "name": "Om Namah Shivaya",
        "devanagari": "ॐ नमः शिवाय",
        "transliteration": "Om Namah Shivaya",
        "meaning": "I bow to Lord Shiva — the inner Self",
        "deity": "Shiva",
        "veda": "Yajur",
        "tags": ["shiva", "panchakshara"],
    },
    {
        "id": "m4",
        "name": "Om Namo Bhagavate Vasudevaya",
        "devanagari": "ॐ नमो भगवते वासुदेवाय",
        "transliteration": "Om Namo Bhagavate Vasudevaya",
        "meaning": "I bow to Lord Vishnu/Krishna, the son of Vasudeva",
        "deity": "Vishnu",
        "veda": "Atharva",
        "tags": ["vishnu", "krishna", "dvadashakshara"],
    },
    {
        "id": "m5",
        "name": "Saraswati Vandana",
        "devanagari": "या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता",
        "transliteration": "Ya Kundendu tusharahara dhavala ya shubhravastravrita",
        "meaning": "She who is as pure as jasmine, the moon, and the snow — Goddess Saraswati",
        "deity": "Saraswati",
        "veda": "Rig",
        "tags": ["saraswati", "knowledge"],
    },
    {
        "id": "m6",
        "name": "Sama Veda Opening",
        "devanagari": "अग्न आयाहि वीतये गृणानो हव्यदातये। नि होता सत्सि बर्हिषि॥",
        "transliteration": "Agna ayahi vitaye grnano havyadataye ni hota satsi barhishi",
        "meaning": "Come, Agni, to the feast, praised as the giver of offerings; sit as the Hotr on the sacred grass.",
        "deity": "Agni",
        "veda": "Sama",
        "tags": ["agni", "sama"],
    },
]

GITA_CHAPTERS: List[Dict[str, Any]] = [
    {"number": 1, "name": "अर्जुन विषाद योग", "translation": "Arjuna Vishada Yoga", "transliteration": "Arjuna Vishada Yoga", "versesCount": 47, "summary": "Arjuna's grief on Kurukshetra"},
    {"number": 2, "name": "सांख्य योग", "translation": "Sankhya Yoga", "transliteration": "Sankhya Yoga", "versesCount": 72, "summary": "The immortal soul and knowledge"},
    {"number": 3, "name": "कर्म योग", "translation": "Karma Yoga", "transliteration": "Karma Yoga", "versesCount": 43, "summary": "Selfless action"},
    {"number": 4, "name": "ज्ञान कर्म संन्यास योग", "translation": "Jnana Karma Sanyasa Yoga", "transliteration": "Jnana Karma Sanyasa Yoga", "versesCount": 42, "summary": "Knowledge and renunciation"},
    {"number": 5, "name": "कर्म संन्यास योग", "translation": "Karma Sanyasa Yoga", "transliteration": "Karma Sanyasa Yoga", "versesCount": 29, "summary": "Renunciation of action"},
    {"number": 6, "name": "ध्यान योग", "translation": "Dhyana Yoga", "transliteration": "Dhyana Yoga", "versesCount": 47, "summary": "Meditation"},
    {"number": 7, "name": "ज्ञान विज्ञान योग", "translation": "Jnana Vijnana Yoga", "transliteration": "Jnana Vijnana Yoga", "versesCount": 30, "summary": "Knowledge of the Absolute"},
    {"number": 8, "name": "अक्षर ब्रह्म योग", "translation": "Aksara Brahma Yoga", "transliteration": "Aksara Brahma Yoga", "versesCount": 28, "summary": "Imperishable Brahman"},
    {"number": 9, "name": "राज विद्या राज गुह्य योग", "translation": "Raja Vidya Raja Guhya Yoga", "transliteration": "Raja Vidya Raja Guhya Yoga", "versesCount": 34, "summary": "Royal knowledge"},
    {"number": 10, "name": "विभूति योग", "translation": "Vibhuti Yoga", "transliteration": "Vibhuti Yoga", "versesCount": 42, "summary": "Divine manifestations"},
    {"number": 11, "name": "विश्वरूप दर्शन योग", "translation": "Vishvarupa Darshana Yoga", "transliteration": "Vishvarupa Darshana Yoga", "versesCount": 55, "summary": "Universal form"},
    {"number": 12, "name": "भक्ति योग", "translation": "Bhakti Yoga", "transliteration": "Bhakti Yoga", "versesCount": 20, "summary": "Devotion"},
    {"number": 13, "name": "क्षेत्र क्षेत्रज्ञ विभाग योग", "translation": "Kshetra Kshetrajna Vibhaga Yoga", "transliteration": "Kshetra Kshetrajna Vibhaga Yoga", "versesCount": 34, "summary": "Field and knower"},
    {"number": 14, "name": "गुणत्रय विभाग योग", "translation": "Gunatraya Vibhaga Yoga", "transliteration": "Gunatraya Vibhaga Yoga", "versesCount": 27, "summary": "Three gunas"},
    {"number": 15, "name": "पुरुषोत्तम योग", "translation": "Purushottama Yoga", "transliteration": "Purushottama Yoga", "versesCount": 20, "summary": "Supreme person"},
    {"number": 16, "name": "दैवासुर सम्पद् विभाग योग", "translation": "Daivasura Sampad Vibhaga Yoga", "transliteration": "Daivasura Sampad Vibhaga Yoga", "versesCount": 24, "summary": "Divine and demoniac natures"},
    {"number": 17, "name": "श्रद्धात्रय विभाग योग", "translation": "Shraddhatraya Vibhaga Yoga", "transliteration": "Shraddhatraya Vibhaga Yoga", "versesCount": 28, "summary": "Threefold faith"},
    {"number": 18, "name": "मोक्ष संन्यास योग", "translation": "Moksha Sanyasa Yoga", "transliteration": "Moksha Sanyasa Yoga", "versesCount": 78, "summary": "Liberation"},
]

RAMAYANA_KANDAS: List[Dict[str, Any]] = [
    {"kandaId": "bala", "name": "Bala Kanda", "description": "Childhood of Rama", "sargas": 77},
    {"kandaId": "ayodhya", "name": "Ayodhya Kanda", "description": "Events at Ayodhya", "sargas": 119},
    {"kandaId": "aranya", "name": "Aranya Kanda", "description": "Forest life", "sargas": 75},
    {"kandaId": "kishkindha", "name": "Kishkindha Kanda", "description": "Alliance with Sugriva", "sargas": 67},
    {"kandaId": "sundara", "name": "Sundara Kanda", "description": "Hanuman's journey", "sargas": 68},
    {"kandaId": "yuddha", "name": "Yuddha Kanda", "description": "War with Ravana", "sargas": 128},
    {"kandaId": "uttara", "name": "Uttara Kanda", "description": "Later life of Rama", "sargas": 111},
]

MAHABHARATA_PARVAS: List[Dict[str, Any]] = [
    {"parvaNumber": 1, "name": "Adi Parva", "description": "The beginning — lineage and early life", "chapters": 225, "verses": 7984},
    {"parvaNumber": 2, "name": "Sabha Parva", "description": "Dice game and exile", "chapters": 72, "verses": 2511},
    {"parvaNumber": 3, "name": "Vana Parva", "description": "Forest exile", "chapters": 299, "verses": 11664},
    {"parvaNumber": 4, "name": "Virata Parva", "description": "Incognito year", "chapters": 67, "verses": 2050},
    {"parvaNumber": 5, "name": "Udyoga Parva", "description": "War preparations", "chapters": 186, "verses": 6698},
    {"parvaNumber": 6, "name": "Bhishma Parva", "description": "Includes Bhagavad Gita", "chapters": 117, "verses": 5884},
    {"parvaNumber": 7, "name": "Drona Parva", "description": "Drona's command", "chapters": 173, "verses": 8909},
    {"parvaNumber": 8, "name": "Karna Parva", "description": "Karna as commander", "chapters": 69, "verses": 4964},
    {"parvaNumber": 9, "name": "Shalya Parva", "description": "Shalya as commander", "chapters": 59, "verses": 3220},
    {"parvaNumber": 10, "name": "Sauptika Parva", "description": "Night raid", "chapters": 18, "verses": 870},
    {"parvaNumber": 11, "name": "Stri Parva", "description": "Women's lament", "chapters": 27, "verses": 775},
    {"parvaNumber": 12, "name": "Shanti Parva", "description": "Peace instructions", "chapters": 353, "verses": 14732},
    {"parvaNumber": 13, "name": "Anushasana Parva", "description": "Further instructions", "chapters": 154, "verses": 8000},
    {"parvaNumber": 14, "name": "Ashvamedhika Parva", "description": "Horse sacrifice", "chapters": 96, "verses": 3320},
    {"parvaNumber": 15, "name": "Ashramavasika Parva", "description": "Forest retreat", "chapters": 42, "verses": 1506},
    {"parvaNumber": 16, "name": "Mausala Parva", "description": "Destruction of Yadavas", "chapters": 8, "verses": 320},
    {"parvaNumber": 17, "name": "Mahaprasthanika Parva", "description": "Final journey", "chapters": 3, "verses": 120},
    {"parvaNumber": 18, "name": "Svargarohana Parva", "description": "Ascent to heaven", "chapters": 5, "verses": 209},
]

ALL_VEDAS: List[Dict[str, Any]] = [
    {"vedaId": "rig", "name": "Rig Veda", "mandalas": 10, "hymns": 1028, "verses": 10552, "description": "Oldest Veda — hymns to the gods."},
    {"vedaId": "yajur", "name": "Yajur Veda", "mandalas": 40, "hymns": 1875, "verses": 1975, "description": "Ritual formulas."},
    {"vedaId": "sama", "name": "Sama Veda", "mandalas": 2, "hymns": 1875, "verses": 1875, "description": "Melodies and chants."},
    {"vedaId": "atharva", "name": "Atharva Veda", "mandalas": 20, "hymns": 730, "verses": 5987, "description": "Practical hymns and formulas."},
]

HANUMAN_CHALISA_VERSES: List[Dict[str, Any]] = [
    {
        "verseNumber": 1,
        "type": "Doha",
        "devanagari": "श्रीगुरु चरन सरोज रज, निज मनु मुकुरु सुधारि। बरनउँ रघुबर बिमल जसु, जो दायकु फल चारि॥",
        "transliteration": "Shree Guru Charan Saroj Raj, Nij manu Mukuru Sudhari. Baranau Raghuvar Bimal Jasu, Jo Dayaku Phala Chari.",
        "englishTranslation": "With the dust of the Guru's lotus feet, I cleanse the mirror of my mind and narrate the pure glory of Shri Raghuvar.",
        "tags": ["Introductory", "Doha", "Prayer"],
    },
    {
        "verseNumber": 2,
        "type": "Doha",
        "devanagari": "बुद्धिहीन तनु जानिके, सुमिरौं पवन-कुमार। बल बुद्धि बिद्या देहु मोहिं, हरहु कलेश बिकार॥",
        "transliteration": "Buddhiheen Tanu Jaanike, Sumirau Pavan Kumar. Bal Buddhi Vidya Dehu Mohin, Harahu Kalesh Vikaar.",
        "englishTranslation": "Considering myself ignorant, I remember the Son of the Wind-God. Grant me strength, wisdom, and knowledge.",
        "tags": ["Introductory", "Doha", "Prayer"],
    },
    {
        "verseNumber": 3,
        "type": "Chaupai",
        "devanagari": "जय हनुमान ज्ञान गुन सागर। जय कपीस तिहुँ लोक उजागर॥",
        "transliteration": "Jai Hanuman Gyan Gun Sagar. Jai Kapeesh Tihun Lok Ujaagar.",
        "englishTranslation": "Victory to Hanuman, the ocean of wisdom and virtue.",
        "tags": ["Chaupai", "Praise"],
    },
]

GANESH_CHALISA_VERSES: List[Dict[str, Any]] = [
    {
        "verseNumber": 1,
        "type": "Doha",
        "devanagari": "जय गणपति सद्गुण सदन, कविवर बदन कृपाल। विघ्न हरण मंगल करण, जय जय गिरिजा लाल॥",
        "transliteration": "Jai Ganapati sadgun sadan, kavivar badan kripal. Vighna haran mangal karan, jai jai Girija lal.",
        "englishTranslation": "Victory to Ganapati, abode of virtues, gracious to poets, remover of obstacles.",
        "tags": ["Doha"],
    }
]

GITA_VERSES: Dict[int, List[Dict[str, Any]]] = {
    1: [
        {
            "bgId": "BG1.1",
            "chapter": 1,
            "verse": 1,
            "shloka": "धृतराष्ट्र उवाच | धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः | मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ||1-1||",
            "transliteration": "dhritarashtra uvacha dharmakshetre kurukshetre samaveta yuyutsavah mamakah pandavaschaiva kimakurvata sanjaya",
            "translations": {"en": "Dhritarashtra said: O Sanjaya, what did my sons and the sons of Pandu do when they assembled on the holy field of Kurukshetra, eager for battle?"},
        },
        {
            "bgId": "BG1.2",
            "chapter": 1,
            "verse": 2,
            "shloka": "सञ्जय उवाच | दृष्ट्वा तु पाण्डवानीकं व्यूढं दुर्योधनस्तदा | आचार्यमुपसङ्गम्य राजा वचनमब्रवीत् ||1-2||",
            "transliteration": "sanjaya uvacha drishtva tu pandavanikam vyudham duryodhanastada acharyamupasangamya raja vachanamabravit",
            "translations": {"en": "Sanjaya said: Seeing the Pandava army arrayed, King Duryodhana approached his teacher and spoke these words."},
        },
    ],
    2: [
        {
            "bgId": "BG2.47",
            "chapter": 2,
            "verse": 47,
            "shloka": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन | मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ||२-४७||",
            "transliteration": "karmanye vadhikaraste ma phaleshu kadachana ma karmaphalaheturbhur ma te sango 'stv akarmani",
            "translations": {
                "en": "Your right is to work only, never to its fruits. Let not the fruits of action be your motive, nor let your attachment be to inaction."
            },
        }
    ],
}

RAMAYANA_VERSES: List[Dict[str, Any]] = [
    {
        "kandaId": "bala",
        "sarga": 1,
        "verse": 1,
        "original": "तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम्। नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम्॥",
        "transliteration": "tapah svadhyaya niratam tapasvi vagvidam varam naradam paripapraccha valmikir munipungavam",
        "translation": "The ascetic Valmiki asked Narada, the foremost of sages, who was ever engaged in austerity and study of the Veda.",
    },
    {
        "kandaId": "bala",
        "sarga": 1,
        "verse": 2,
        "original": "को न्वस्मिन् साम्प्रतं लोके गुणवान् कश्च वीर्यवान्। धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः॥",
        "transliteration": "ko nvasmin sampratam loke gunavan kasca viryavan dharmajnasca krtajnasca satyavakyo drdhavratah",
        "translation": "Who in this world now is endowed with virtues and prowess, who knows dharma, is grateful, truthful, and firm in vows?",
    },
    {
        "kandaId": "bala",
        "sarga": 1,
        "verse": 3,
        "original": "चारित्रेण च को युक्तः सर्वभूतेषु को हितः। विद्वान् कः कः समर्थश्च कश्चैकप्रियदर्शनः॥",
        "transliteration": "caritrena ca ko yuktah sarvabhutesu ko hitah vidvan kah kah samarthasca kascaikapriyadarsanah",
        "translation": "Who is of excellent conduct, who is a well-wisher of all beings, who is learned, capable, and pleasing to behold?",
    },
    {
        "kandaId": "bala",
        "sarga": 1,
        "verse": 4,
        "original": "आत्मवान् को जितक्रोधो द्युतिमान् कोऽनसूयकः। कस्य बिभ्यति देवाश्च जातरोषस्य संयुगे॥",
        "transliteration": "atmavan ko jitakrodho dyutiman ko 'nasuyakah kasya bibhyati devasca jatarosasya samyuge",
        "translation": "Who is self-possessed, who has conquered anger, who is radiant and free from envy? Whom do even the gods fear when he is angry in battle?",
    },
    {
        "kandaId": "bala",
        "sarga": 1,
        "verse": 5,
        "original": "एतदिच्छाम्यहं श्रोतुं परं कौतूहलं हि मे। महर्षे त्वं समर्थोऽसि ज्ञातुमेवंविधं नरम्॥",
        "transliteration": "etad icchamy aham srotum param kautuhalam hi me maharse tvam samartho 'si jnatum evamvidham naram",
        "translation": "This I wish to hear, for my curiosity is great. O great sage, you are able to know such a man.",
    },
]

MAHABHARATA_VERSES: List[Dict[str, Any]] = [
    {
        "parva": 1,
        "chapter": 1,
        "verse": 1,
        "text": "नारायणं नमस्कृत्य नरं चैव नरोत्तमम्। देवीं सरस्वतीं चैव ततो जयमुदीरयेत्॥",
        "translation": "Having bowed to Narayana and Nara, the most exalted of men, and to goddess Saraswati, one should then utter Jaya.",
    },
    {
        "parva": 1,
        "chapter": 1,
        "verse": 2,
        "text": "लोमहर्षणपुत्र उग्रश्रवाः सूतः पौराणिको नैमिषारण्ये शौनकस्य कुलपतेर्द्वादशवार्षिके सत्रे॥",
        "translation": "Ugrashrava, the son of Lomaharshana, a suta well-versed in the Puranas, came to Naimisha forest during Shaunaka's twelve-year sacrifice.",
    },
    {
        "parva": 1,
        "chapter": 1,
        "verse": 3,
        "text": "समासीनानभ्यगच्छद् ब्रह्मर्षीन् संशितव्रतान्। विनयावनतो भूत्वा कदाचित्सूतनन्दनः॥",
        "translation": "Once the son of the suta approached those Brahmarishis of austere vows who were seated there, bowing with humility.",
    },
    {
        "parva": 1,
        "chapter": 1,
        "verse": 4,
        "text": "तमश्रौषीत्कुलपतिः सूतपुत्रं समागतम्। कस्येदानीं स कथयेत्कथां तां पाण्डुनन्दन॥",
        "translation": "The head of the clan heard that the suta's son had arrived, and asked whose tale he would now recount.",
    },
    {
        "parva": 1,
        "chapter": 1,
        "verse": 5,
        "text": "कथयिष्यामि विप्रेन्द्रा यदि वो रोचते कथा। पुराणं परमं पुण्यं महाभारतमद्भुतम्॥",
        "translation": "I shall narrate, O foremost of Brahmins, if the story pleases you — the supreme, sacred, and wondrous Mahabharata.",
    },
]

RIG_VEDA_VERSES: List[Dict[str, Any]] = [
    {
        "mandala": 1,
        "sukta": 1,
        "stanza": 1,
        "text": "अग्निमीळे पुरोहितं यज्ञस्य देवमृत्विजम्। होतारं रत्नधातमम्॥",
        "poet": "Madhuchchhanda Vaishvamitra",
        "deity": "Agni",
        "meter": "Gayatri",
        "poetCategory": "human male",
        "deityCategory": "divine male",
    },
    {
        "mandala": 1,
        "sukta": 1,
        "stanza": 2,
        "text": "अग्निः पूर्वेभिरृषिभिरीड्यो नूतनैरुत। स देवाँ एह वक्षति॥",
        "poet": "Madhuchchhanda Vaishvamitra",
        "deity": "Agni",
        "meter": "Gayatri",
    },
    {
        "mandala": 1,
        "sukta": 1,
        "stanza": 3,
        "text": "अग्निना रयिमश्नवत्पोषमेव दिवेदिवे। यशसं वीरवत्तमम्॥",
        "poet": "Madhuchchhanda Vaishvamitra",
        "deity": "Agni",
        "meter": "Gayatri",
    },
]

UPANISHAD_VERSES: List[Dict[str, Any]] = [
    {
        "upanishadId": "isha",
        "chapter": 1,
        "verse": 1,
        "sanskrit": "ईशावास्यमिदं सर्वं यत्किञ्च जगत्यां जगत्। तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम्॥",
        "transliteration": "ishavasyam idam sarvam yat kincha jagatyam jagat tena tyaktena bhunjitha ma gridhah kasyasvid dhanam",
        "translation": "All this, whatever moves in this moving world, is enveloped by the Lord. Enjoy by renunciation; do not covet anyone's wealth.",
        "commentary": "The Isha Upanishad begins by affirming the divine presence in all that exists.",
    },
    {
        "upanishadId": "isha",
        "chapter": 1,
        "verse": 2,
        "sanskrit": "कुर्वन्नेवेह कर्माणि जिजीविषेच्छतं समाः। एवं त्वयि नान्यथेतोऽस्ति न कर्म लिप्यते नरे॥",
        "transliteration": "kurvanneveha karmani jijivisec chatam samah evam tvayi nanyatheto 'sti na karma lipyate nare",
        "translation": "Performing works here, one should wish to live a hundred years. Thus, and not otherwise, karma does not cling to a person.",
    },
]

ALL_UPANISHADS: List[Dict[str, Any]] = [
    {"id": "isha", "name": "Isha Upanishad", "associatedVeda": "Yajur", "chapters": 1, "description": "Divine in all things."},
    {"id": "kena", "name": "Kena Upanishad", "associatedVeda": "Sama", "chapters": 4, "description": "Nature of Brahman."},
    {"id": "katha", "name": "Katha Upanishad", "associatedVeda": "Yajur", "chapters": 6, "description": "Nachiketa and Yama."},
    {"id": "mundaka", "name": "Mundaka Upanishad", "associatedVeda": "Atharva", "chapters": 3, "description": "Higher and lower knowledge."},
    {"id": "chandogya", "name": "Chandogya Upanishad", "associatedVeda": "Sama", "chapters": 8, "description": "Tat tvam asi."},
    {"id": "brihadaranyaka", "name": "Brihadaranyaka Upanishad", "associatedVeda": "Yajur", "chapters": 6, "description": "Largest Upanishad."},
]


class StaticContentRegistry:
    def get_all_aartis(self) -> List[Dict[str, Any]]:
        return [dict(a) for a in ALL_AARTIS]

    def get_all_chalisas(self) -> List[Dict[str, Any]]:
        return [dict(c) for c in ALL_CHALISAS]

    def get_all_stotrams(self) -> List[Dict[str, Any]]:
        return copy.deepcopy(ALL_STOTRAMS)

    def get_gita_chapters(self) -> List[Dict[str, Any]]:
        return [dict(c) for c in GITA_CHAPTERS]

    def get_gita_verses(self, chapter_number: int) -> List[Dict[str, Any]]:
        return [dict(v) for v in GITA_VERSES.get(chapter_number, [])]

    def get_ramayana_kandas(self) -> List[Dict[str, Any]]:
        return [dict(k) for k in RAMAYANA_KANDAS]

    def get_mahabharata_parvas(self) -> List[Dict[str, Any]]:
        return [dict(p) for p in MAHABHARATA_PARVAS]

    def get_all_vedas(self) -> List[Dict[str, Any]]:
        return [dict(v) for v in ALL_VEDAS]

    def get_all_upanishads(self) -> List[Dict[str, Any]]:
        return [dict(u) for u in ALL_UPANISHADS]

    def get_hanuman_chalisa_verses(self) -> List[Dict[str, Any]]:
        return [dict(v) for v in HANUMAN_CHALISA_VERSES]

    def get_chalisa_verses(self, chalisa_id: str) -> List[Dict[str, Any]]:
        cid = chalisa_id.strip().lower()
        if cid in {"hanuman", "chalisa-hanuman"}:
            return [dict(v) for v in HANUMAN_CHALISA_VERSES]
        if cid in {"ganesh", "chalisa-ganesh"}:
            return [dict(v) for v in GANESH_CHALISA_VERSES]
        return []

    def get_ramayana_verses(self, kanda_id: str, sarga: int) -> List[Dict[str, Any]]:
        wanted = kanda_id.strip().lower()
        return [
            dict(v)
            for v in RAMAYANA_VERSES
            if str(v.get("kandaId", "")).lower() == wanted and int(v.get("sarga") or 0) == sarga
        ]

    def get_mahabharata_verses(self, parva: int, chapter: int) -> List[Dict[str, Any]]:
        return [
            dict(v)
            for v in MAHABHARATA_VERSES
            if int(v.get("parva") or 0) == parva and int(v.get("chapter") or 0) == chapter
        ]

    def get_rig_veda_verses(self, mandala: Optional[int]) -> List[Dict[str, Any]]:
        if mandala is None:
            return [dict(v) for v in RIG_VEDA_VERSES]
        return [dict(v) for v in RIG_VEDA_VERSES if int(v.get("mandala") or 0) == mandala]

    def get_upanishad_verses(self, upanishad_id: str, chapter: int) -> List[Dict[str, Any]]:
        wanted = upanishad_id.strip().lower()
        return [
            dict(v)
            for v in UPANISHAD_VERSES
            if str(v.get("upanishadId", "")).lower() == wanted and int(v.get("chapter") or 0) == chapter
        ]

    def get_chalisa_by_deity(self, deity: str) -> Optional[Dict[str, Any]]:
        d = deity.strip().lower()
        for c in ALL_CHALISAS:
            if str(c["deity"]).lower() == d:
                return dict(c)
        return None

    def get_random_mantra(self) -> Dict[str, Any]:
        import random

        pool = list(VEDA_MANTRA_POOL)
        return dict(random.choice(pool)) if pool else {"text": "ॐ", "meaning": "The primordial sound, Brahman"}

    def get_mantras(self, deity: Optional[str], limit: int) -> List[Dict[str, Any]]:
        out = []
        for m in VEDA_MANTRA_POOL:
            if deity is None or str(m.get("deity", "")).lower() == deity.lower():
                out.append(dict(m))
            if len(out) >= limit:
                break
        return out

    def get_veda_mantras(self, veda: Optional[str]) -> List[Dict[str, Any]]:
        if veda is None:
            return [dict(m) for m in VEDA_MANTRA_POOL]
        v = veda.lower()
        return [dict(m) for m in VEDA_MANTRA_POOL if str(m.get("veda", "")).lower() == v]
