package com.mann.mandir.util;

import com.mann.mandir.client.impl.HanumanChalisaClient;
import com.mann.mandir.dto.domain.ChalisaDto;
import com.mann.mandir.dto.domain.GitaChapterDto;
import com.mann.mandir.dto.domain.MahabharataParvaDto;
import com.mann.mandir.dto.domain.MahabharataVerseDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.RamayanaKandaDto;
import com.mann.mandir.dto.domain.RamayanaVerseDto;
import com.mann.mandir.dto.domain.RigVedaVerseDto;
import com.mann.mandir.dto.domain.StotramDto;
import com.mann.mandir.dto.domain.StotramVerseDto;
import com.mann.mandir.dto.domain.UpanishadDto;
import com.mann.mandir.dto.domain.UpanishadVerseDto;
import com.mann.mandir.dto.domain.VedaDto;
import com.mann.mandir.dto.god.AartiDto;
import org.springframework.stereotype.Component;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Random;
import java.util.stream.Collectors;

@Component
public class StaticContentRegistry {
    public List<HanumanChalisaClient.ChalisaVerseResponse> getHanumanChalisaVerses() {
        return Collections.emptyList();
    }

    public List<RamayanaVerseDto> getRamayanaVerses(String kandaId, int sarga) {
        return Collections.emptyList();
    }

    public List<MahabharataVerseDto> getMahabharataVerses(int parva, int chapter) {
        return Collections.emptyList();
    }

    public List<RigVedaVerseDto> getRigVedaVerses(int mandala) {
        return Collections.emptyList();
    }

    public List<UpanishadVerseDto> getUpanishadVerses(String upanishadId, int chapter) {
        return Collections.emptyList();
    }

    public Optional<ChalisaDto> getChalisaByDeity(String deity) {
        return getAllChalisas().stream()
                .filter(c -> c.getDeity().equalsIgnoreCase(deity))
                .findFirst();
    }

    public MantraDto getRandomMantra() {
        List<MantraDto> all = getVedaMantras(null);
        return all.isEmpty() ? MantraDto.builder()
                .text("ॐ")
                .meaning("The primordial sound, Brahman")
                .build()
                : all.get(new Random().nextInt(all.size()));
    }

    public List<MantraDto> getMantras(String deity, int limit) {
        return getVedaMantras(null).stream()
                .filter(m -> deity == null || deity.equalsIgnoreCase(m.getDeity()))
                .limit(limit)
                .collect(java.util.stream.Collectors.toList());
    }

    public List<AartiDto> getAllAartis() {
        return List.of(
                AartiDto.builder().id("aarti-ganesh").name("Jai Ganesh Deva").deity("Ganesha")
                        .devanagari("जय गणेश जय गणेश जय गणेश देवा")
                        .transliteration("Jai Ganesh Jai Ganesh Jai Ganesh Deva")
                        .translation("Victory to Lord Ganesha, son of Parvati and Shiva.")
                        .verses(List.of(
                                "जय गणेश जय गणेश जय गणेश देवा माता जाकी पार्वती पिता महादेवा",
                                "एक दन्त दयावन्त चार भुजा धारी माथे पर तिलक सोहे मूसे की सवारी",
                                "पान चढ़े फूल चढ़े और चढ़े मेवा लड्डुअन का भोग लगे संत करें सेवा",
                                "अन्धन को आँख देत कोढ़िन को काया बंझन को पुत्र देत निर्धन को माया",
                                "सूर्य श्याम शरण आए सफल कीजे सेवा माता जाकी पार्वती पिता महादेवा"
                        )).build(),
                AartiDto.builder().id("aarti-lakshmi").name("Jai Lakshmi Mata").deity("Lakshmi")
                        .devanagari("जय लक्ष्मी माता")
                        .transliteration("Jai Lakshmi Mata")
                        .translation("Victory to Mother Lakshmi, goddess of wealth and prosperity.")
                        .verses(List.of(
                                "जय लक्ष्मी माता, मैया जय लक्ष्मी माता। तुमको निसदिन सेवत हर विष्णु विधाता॥",
                                "उमा, रमा, ब्रह्माणी, तुम ही जग-माता। सूर्य-चंद्रमा ध्यावत नारद ऋषि गाता॥",
                                "दुर्गा रूप निरंजन सुख सम्पत्ति दाता। जो कोई तुमको ध्यावत ऋद्धि-सिद्धि धन पाता॥",
                                "तुम ही पाताल निवासिनी, तुम ही शुभदाता। कर्मप्रभाव प्रकाशिनी, भवनिधि की ताता॥",
                                "जिस घर में तुम रहतीं, सब सद्गुण आता। सब सम्भव हो जाता, मन वांछित फल पाता॥"
                        )).build(),
                AartiDto.builder().id("aarti-shiva").name("Om Jai Shiv Omkara").deity("Shiva")
                        .devanagari("ॐ जय शिव ओंकारा")
                        .transliteration("Om Jai Shiv Omkara")
                        .translation("Glory to Lord Shiva, the primordial sound.")
                        .verses(List.of(
                                "ॐ जय शिव ओंकारा, स्वामी जय शिव ओंकारा। ब्रह्मा विष्णु सदाशिव, अर्द्धांगी धारा॥",
                                "एकानन चतुरानन पञ्चानन राजे। हंसासन गरूड़ासन वृषवाहन साजे॥",
                                "दो भुज चार चतुर्भुज, दशभुज अति सोहे। त्रिगुण रूप निरखते, त्रिभुवन जन मोहे॥",
                                "अक्षमाला वनमाला, मुण्डमाला धारी। चन्दन मृगमद सोहे, भाले शशिधारी॥",
                                "श्वेताम्बर पीताम्बर, बाघम्बर अंगे। सनकादिक ब्रह्मादिक, भूतादिक संगे॥",
                                "कर में कमण्डल चक्र त्रिशूल धर्ता। जगकर्ता जगभर्ता, जग पालन कर्ता॥",
                                "ब्रह्मा विष्णु सदाशिव, जानत अविवेका। प्रणवाक्षर के मध्यें, ये तीनों एका॥",
                                "त्रिगुण स्वामी की आरती, जो कोई नर गावे। कहत शिवानंद स्वामी, मनवांछित फल पावे॥"
                        )).build(),
                AartiDto.builder().id("aarti-krishna").name("Jai Jagdish Hare").deity("Vishnu/Krishna")
                        .devanagari("ॐ जय जगदीश हरे")
                        .transliteration("Om Jai Jagdish Hare")
                        .translation("Victory to the Lord of the Universe.")
                        .verses(List.of(
                                "ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे। भक्त जनों के संकट, क्षण में दूर करे॥",
                                "जो ध्यावे फल पावे, दुःख विनसे मन का। सुख सम्पत्ति घर आवे, कष्ट मिटे तन का॥",
                                "मात पिता तुम मेरे, शरण गहूं मैं किसकी। तुम बिन और न दूजा, आस करूँ मैं जिसकी॥",
                                "तुम पूरण परमात्मा, तुम अन्तर्यामी। पारब्रह्म परमेश्वर, तुम सबके स्वामी॥",
                                "तुम करुणा के सागर, तुम पालनकर्ता। मैं मूरख खल कामी, कृपा करो भर्ता॥",
                                "तुम हो एक अगोचर, सबके प्राणपति। किस विधि मिलूं दयामय, तुमको मैं कुमति॥"
                        )).build(),
                AartiDto.builder().id("aarti-durga").name("Jai Ambe Gauri").deity("Durga")
                        .devanagari("जय अम्बे गौरी")
                        .transliteration("Jai Ambe Gauri")
                        .translation("Victory to Mother Durga, the divine feminine power.")
                        .verses(List.of(
                                "जय अम्बे गौरी, मैया जय श्यामा गौरी। तुमको निशिदिन ध्यावत, हरि ब्रह्मा शिवरी॥",
                                "माँग सिन्दूर विराजत, टीको मृगमद को। उज्ज्वल से दोउ नैना, चन्द्रवदन नीको॥",
                                "कनक समान कलेवर, रक्ताम्बर राजे। रक्तपुष्प गल माला, कण्ठन पर साजे॥",
                                "केहरि वाहन राजत, खड्ग खप्पर धारी। सुर-नर-मुनि जन सेवत, तिनके दुखहारी॥",
                                "कानन कुण्डल शोभित, नासाग्रे मोती। कोटिक चन्द्र दिवाकर, सम राजत ज्योती॥",
                                "चण्ड-मुण्ड संहारे, शोणित बीज हरे। मधु-कैटभ दोउ मारे, सुर भयहीन करे॥"
                        )).build(),
                AartiDto.builder().id("aarti-saraswati").name("Jai Saraswati Mata").deity("Saraswati")
                        .devanagari("जय सरस्वती माता")
                        .transliteration("Jai Saraswati Mata")
                        .translation("Victory to Goddess Saraswati, bestower of knowledge.")
                        .verses(List.of(
                                "जय सरस्वती माता, मैया जय सरस्वती माता। सद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥",
                                "चन्द्रवदनि पद्मासिनी, ध्युति मंगलकारी। सोहभा श्वेताम्बर, सुरनर मुनि तारी॥",
                                "कमलपटिका पदवन्दित, मुनि मन हरषाती। ज्ञान, बुद्धि, विद्या दा, वर दे मोहि माता॥",
                                "तुम त्रिभुवन में न्यारी, तुम ही ज्ञानप्रदाता। भक्तों के दुख हरता, सदा सुखदाता॥"
                        )).build()
        );
    }

    public List<ChalisaDto> getAllChalisas() {
        return List.of(
                ChalisaDto.builder().id("chalisa-hanuman").deity("Hanuman")
                        .title("Hanuman Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-ganesh").deity("Ganesh")
                        .title("Ganesh Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-durga").deity("Durga")
                        .title("Durga Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-lakshmi").deity("Lakshmi")
                        .title("Lakshmi Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-shiva").deity("Shiva")
                        .title("Shiv Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-saraswati").deity("Saraswati")
                        .title("Saraswati Chalisa").totalVerses(40).build(),
                ChalisaDto.builder().id("chalisa-ram").deity("Ram")
                        .title("Ram Chalisa").totalVerses(40).build()
        );
    }

    public List<StotramDto> getAllStotrams() {
        List<StotramVerseDto> shivaTandavaVerses = List.of(
                StotramVerseDto.builder().verseNumber(1)
                        .sanskrit("जटा टवी गलज्जलप्रवाह पावितस्थले गलेऽव लम्ब्यलम्बितां भुजंगतुंग मालिकाम्‌")
                        .transliteration("Jata tavi galaj jal pravah pavit sthale gale av lambya lambitam bhujang tung malikam")
                        .meaning("His neck is purified by the flowing waters from his matted hair, a serpent hangs like a garland").build(),
                StotramVerseDto.builder().verseNumber(2)
                        .sanskrit("जटाकटा हसंभ्रम भ्रमन्निलिंपनिर्झरी विलोलवीचिवल्लरी विराजमानमूर्धनि")
                        .transliteration("Jata kata hasambhram bhraman nilimpanirjhari vilol vichi vallari virajmaan moordhani")
                        .meaning("My devotion lies in Shiva whose head is adorned by the flowing Ganga").build(),
                StotramVerseDto.builder().verseNumber(3)
                        .sanskrit("धराधरेंद्रनंदिनी विलासबन्धुबन्धुर स्फुरद्दिगंतसंतति प्रमोद मानमानसे")
                        .transliteration("Dharadharendra nandini vilas bandhu bandhura sphurad digant santati pramod man manase")
                        .meaning("May my mind find joy in Shiva, beloved of Parvati, who spreads bliss everywhere").build(),
                StotramVerseDto.builder().verseNumber(11)
                        .sanskrit("जयत्वदभ्रविभ्रम भ्रमद्भुजंगमस्फुरद्ध गद्धगद्विनिर्गमत्कराल भाल हव्यवाट्")
                        .transliteration("Jayatvad abhravibhram bhramad bhujangam sphurad dhagad dhagad vinirgamat karal bhaal")
                        .meaning("Victory to Shiva, whose fierce cosmic dance resounds with powerful drumbeats").build(),
                StotramVerseDto.builder().verseNumber(16)
                        .sanskrit("इमं हि नित्यमेव मुक्तमुक्तमोत्तम स्तवं पठन्स्मरन्‌ ब्रुवन्नरो विशुद्धमेति संततम्‌")
                        .transliteration("Imam hi nityameva muktamuktamottam stavam pathan smaran bruvannaro vishuddhameti santatam")
                        .meaning("Whoever recites this hymn becomes pure, gains devotion to Shiva").build()
        );

        return List.of(
                StotramDto.builder().id("stotram-vishnu-sahasranama").name("Vishnu Sahasranama")
                        .deity("Vishnu").author("Vyasa").description("The thousand names of Lord Vishnu")
                        .verseCount(107).verses(Collections.emptyList()).build(),
                StotramDto.builder().id("stotram-shiva-tandava").name("Shiva Tandava Stotram")
                        .deity("Shiva").author("Ravana").description("The cosmic dance of Lord Shiva described by Ravana")
                        .verseCount(17).verses(shivaTandavaVerses).build(),
                StotramDto.builder().id("stotram-mahishasura-mardini").name("Mahishasura Mardini Stotram")
                        .deity("Durga").author("Adi Shankaracharya")
                        .description("Hymn to Goddess Durga, the slayer of Mahishasura")
                        .verseCount(21).verses(Collections.emptyList()).build(),
                StotramDto.builder().id("stotram-aditya-hridayam").name("Aditya Hridayam")
                        .deity("Surya").author("Agastya").description("Hymn to the Sun God, from Valmiki Ramayana")
                        .verseCount(30).verses(Collections.emptyList()).build(),
                StotramDto.builder().id("stotram-soundarya-lahari").name("Soundarya Lahari")
                        .deity("Parvati").author("Adi Shankaracharya")
                        .description("Waves of beauty — 100 verses to Goddess Parvati")
                        .verseCount(100).verses(Collections.emptyList()).build(),
                StotramDto.builder().id("stotram-ganesh-atharvashirsha").name("Ganesh Atharvashirsha")
                        .deity("Ganesh").author("Atharva Veda")
                        .description("Upanishad dedicated to Lord Ganesha")
                        .verseCount(14).verses(Collections.emptyList()).build()
        );
    }

    public List<MantraDto> getVedaMantras(String veda) {
        List<MantraDto> all = List.of(
                MantraDto.builder().id("m1").name("Gayatri Mantra")
                        .devanagari("ॐ भूर् भुवः स्वः। तत् सवितुर् वरेण्यम्। भर्गो देवस्य धीमहि। धियो यो नः प्रचोदयात्॥")
                        .transliteration("Om bhur bhuvah svah, tat savitur varenyam, bhargo devasya dhimahi, dhiyo yo nah prachodayat")
                        .meaning("We meditate on the divine light of the sun god Savitri. May he illuminate our intellect.")
                        .deity("Surya").veda("Rig").tags(List.of("gayatri", "surya", "morning")).build(),
                MantraDto.builder().id("m2").name("Maha Mrityunjaya Mantra")
                        .devanagari("ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय माऽमृतात्॥")
                        .transliteration("Om tryambakam yajamahe sugandhim pushtivardhanam, urvarukamiva bandhanat mrityor mukshiya mamritat")
                        .meaning("We worship the three-eyed Shiva who nourishes all. May he free us from death like a cucumber from its vine, towards immortality.")
                        .deity("Shiva").veda("Yajur").tags(List.of("shiva", "healing", "longevity")).build(),
                MantraDto.builder().id("m3").name("Om Namah Shivaya")
                        .devanagari("ॐ नमः शिवाय")
                        .transliteration("Om Namah Shivaya")
                        .meaning("I bow to Lord Shiva — the inner Self")
                        .deity("Shiva").veda("Yajur").tags(List.of("shiva", "panchakshara")).build(),
                MantraDto.builder().id("m4").name("Om Namo Bhagavate Vasudevaya")
                        .devanagari("ॐ नमो भगवते वासुदेवाय")
                        .transliteration("Om Namo Bhagavate Vasudevaya")
                        .meaning("I bow to Lord Vishnu/Krishna, the son of Vasudeva")
                        .deity("Vishnu").veda("Atharva").tags(List.of("vishnu", "krishna", "dvadashakshara")).build(),
                MantraDto.builder().id("m5").name("Saraswati Vandana")
                        .devanagari("या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता")
                        .transliteration("Ya Kundendu tusharahara dhavala ya shubhravastravrita")
                        .meaning("She who is as pure as jasmine, the moon, and the snow — Goddess Saraswati")
                        .deity("Saraswati").veda("Rig").tags(List.of("saraswati", "knowledge")).build()
        );
        if (veda == null) return all;
        return all.stream()
                .filter(m -> veda.equalsIgnoreCase(m.getVeda()))
                .collect(Collectors.toList());
    }

    public List<GitaChapterDto> getGitaChapters() {
        return List.of(
                GitaChapterDto.builder().number(1).name("अर्जुन विषाद योग").translation("Arjuna Vishada Yoga")
                        .transliteration("Arjuna Vishada Yoga").versesCount(47)
                        .summary("Arjuna's grief and moral dilemma on the battlefield of Kurukshetra").build(),
                GitaChapterDto.builder().number(2).name("सांख्य योग").translation("Sankhya Yoga")
                        .transliteration("Sankhya Yoga").versesCount(72)
                        .summary("Krishna's teachings on the immortal soul and the path of knowledge").build(),
                GitaChapterDto.builder().number(3).name("कर्म योग").translation("Karma Yoga")
                        .transliteration("Karma Yoga").versesCount(43)
                        .summary("The yoga of selfless action — performing duty without attachment to results").build(),
                GitaChapterDto.builder().number(4).name("ज्ञान कर्म संन्यास योग").translation("Jnana Karma Sanyasa Yoga")
                        .transliteration("Jnana Karma Sanyasa Yoga").versesCount(42)
                        .summary("The yoga of knowledge, action, and renunciation").build(),
                GitaChapterDto.builder().number(5).name("कर्म संन्यास योग").translation("Karma Sanyasa Yoga")
                        .transliteration("Karma Sanyasa Yoga").versesCount(29)
                        .summary("Renunciation of action and its relationship to knowledge").build(),
                GitaChapterDto.builder().number(6).name("ध्यान योग").translation("Dhyana Yoga")
                        .transliteration("Dhyana Yoga").versesCount(47)
                        .summary("The yoga of meditation and self-discipline").build(),
                GitaChapterDto.builder().number(7).name("ज्ञान विज्ञान योग").translation("Jnana Vijnana Yoga")
                        .transliteration("Jnana Vijnana Yoga").versesCount(30)
                        .summary("Knowledge of the Absolute — the divine and material nature").build(),
                GitaChapterDto.builder().number(8).name("अक्षर ब्रह्म योग").translation("Aksara Brahma Yoga")
                        .transliteration("Aksara Brahma Yoga").versesCount(28)
                        .summary("The imperishable Brahman and the path of departure from this world").build(),
                GitaChapterDto.builder().number(9).name("राज विद्या राज गुह्य योग").translation("Raja Vidya Raja Guhya Yoga")
                        .transliteration("Raja Vidya Raja Guhya Yoga").versesCount(34)
                        .summary("The royal knowledge and royal secret of devotion to God").build(),
                GitaChapterDto.builder().number(10).name("विभूति योग").translation("Vibhuti Yoga")
                        .transliteration("Vibhuti Yoga").versesCount(42)
                        .summary("The divine manifestations and opulences of God").build(),
                GitaChapterDto.builder().number(11).name("विश्वरूप दर्शन योग").translation("Vishvarupa Darshana Yoga")
                        .transliteration("Vishvarupa Darshana Yoga").versesCount(55)
                        .summary("The vision of the universal cosmic form of Krishna").build(),
                GitaChapterDto.builder().number(12).name("भक्ति योग").translation("Bhakti Yoga")
                        .transliteration("Bhakti Yoga").versesCount(20)
                        .summary("The yoga of devotion — qualities of the true devotee").build(),
                GitaChapterDto.builder().number(13).name("क्षेत्र क्षेत्रज्ञ विभाग योग").translation("Kshetra Kshetrajna Vibhaga Yoga")
                        .transliteration("Kshetra Kshetrajna Vibhaga Yoga").versesCount(34)
                        .summary("Distinction between the field (body) and the knower of the field (soul)").build(),
                GitaChapterDto.builder().number(14).name("गुणत्रय विभाग योग").translation("Gunatraya Vibhaga Yoga")
                        .transliteration("Gunatraya Vibhaga Yoga").versesCount(27)
                        .summary("The three modes of material nature: Sattva, Rajas, Tamas").build(),
                GitaChapterDto.builder().number(15).name("पुरुषोत्तम योग").translation("Purushottama Yoga")
                        .transliteration("Purushottama Yoga").versesCount(20)
                        .summary("The supreme person — the eternal Ashvattha tree of existence").build(),
                GitaChapterDto.builder().number(16).name("दैवासुर सम्पद् विभाग योग").translation("Daivasura Sampad Vibhaga Yoga")
                        .transliteration("Daivasura Sampad Vibhaga Yoga").versesCount(24)
                        .summary("The divine and demoniac natures distinguished").build(),
                GitaChapterDto.builder().number(17).name("श्रद्धात्रय विभाग योग").translation("Shraddhatraya Vibhaga Yoga")
                        .transliteration("Shraddhatraya Vibhaga Yoga").versesCount(28)
                        .summary("The threefold division of faith according to the three gunas").build(),
                GitaChapterDto.builder().number(18).name("मोक्ष संन्यास योग").translation("Moksha Sanyasa Yoga")
                        .transliteration("Moksha Sanyasa Yoga").versesCount(78)
                        .summary("Liberation through renunciation — the conclusion of all teachings").build()
        );
    }

    public List<RamayanaKandaDto> getRamayanaKandas() {
        return List.of(
                RamayanaKandaDto.builder().kandaId("bala").name("Bala Kanda")
                        .description("Childhood of Rama — birth, education, marriage to Sita").sargas(77).build(),
                RamayanaKandaDto.builder().kandaId("ayodhya").name("Ayodhya Kanda")
                        .description("Events at Ayodhya — exile of Rama, Bharata's grief").sargas(119).build(),
                RamayanaKandaDto.builder().kandaId("aranya").name("Aranya Kanda")
                        .description("Forest life — sages, demons, and abduction of Sita by Ravana").sargas(75).build(),
                RamayanaKandaDto.builder().kandaId("kishkindha").name("Kishkindha Kanda")
                        .description("Alliance with Sugriva and Hanuman — search for Sita").sargas(67).build(),
                RamayanaKandaDto.builder().kandaId("sundara").name("Sundara Kanda")
                        .description("Hanuman's journey to Lanka — finding and comforting Sita").sargas(68).build(),
                RamayanaKandaDto.builder().kandaId("yuddha").name("Yuddha Kanda")
                        .description("The great war with Ravana — victory of Rama and return to Ayodhya").sargas(128).build(),
                RamayanaKandaDto.builder().kandaId("uttara").name("Uttara Kanda")
                        .description("Later life of Rama — Sita's exile and final liberation").sargas(111).build()
        );
    }

    public List<MahabharataParvaDto> getMahabharataParvas() {
        return List.of(
                MahabharataParvaDto
                        .builder()
                        .parvaNumber(1)
                        .name("Adi Parva")
                        .description("The beginning — lineage, birth, and early life of Pandavas and Kauravas")
                        .chapters(225)
                        .verses(7984)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(2)
                        .name("Sabha Parva")
                        .description("The assembly hall — dice game and exile of Pandavas")
                        .chapters(72)
                        .verses(2511)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(3)
                        .name("Vana Parva")
                        .description("Forest life — 12 years of exile, stories and pilgrimages")
                        .chapters(299)
                        .verses(11664)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(4)
                        .name("Virata Parva")
                        .description("Life incognito at King Virata's court")
                        .chapters(67)
                        .verses(2050)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(5)
                        .name("Udyoga Parva")
                        .description("Preparations for war — failed peace negotiations")
                        .chapters(186)
                        .verses(6698)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(6)
                        .name("Bhishma Parva")
                        .description("Bhishma's command — includes Bhagavad Gita")
                        .chapters(117)
                        .verses(5884)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(7)
                        .name("Drona Parva")
                        .description("Drona's command — death of Abhimanyu")
                        .chapters(173)
                        .verses(8909)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(8)
                        .name("Karna Parva")
                        .description("Karna as commander — his death by Arjuna")
                        .chapters(69)
                        .verses(4964)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(9)
                        .name("Shalya Parva")
                        .description("Shalya as commander — death of Duryodhana")
                        .chapters(59)
                        .verses(3220)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(10)
                        .name("Sauptika Parva")
                        .description("Night raid — Ashwatthama's revenge")
                        .chapters(18)
                        .verses(870)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(11)
                        .name("Stri Parva")
                        .description("Women's grief — lament of the widows")
                        .chapters(27)
                        .verses(775)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(12)
                        .name("Shanti Parva")
                        .description("Peace — Yudhishthira's questions to Bhishma")
                        .chapters(353)
                        .verses(14732)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(13)
                        .name("Anushasana Parva")
                        .description("Instructions — duties of kings and people")
                        .chapters(154)
                        .verses(8000)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(14)
                        .name("Ashvamedhika Parva")
                        .description("Horse sacrifice — Arjuna's conquests")
                        .chapters(96)
                        .verses(3320)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(15)
                        .name("Ashramavasika Parva")
                        .description("Forest retreat — last days of Dhritarashtra and Gandhari")
                        .chapters(42)
                        .verses(1506)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(16)
                        .name("Mausala Parva")
                        .description("Club fight — destruction of the Yadavas")
                        .chapters(8)
                        .verses(320)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(17)
                        .name("Mahaprasthanika Parva")
                        .description("Great journey — Pandavas' final journey to the Himalayas")
                        .chapters(3)
                        .verses(120)
                        .build(),

                MahabharataParvaDto
                        .builder()
                        .parvaNumber(18)
                        .name("Svargarohana Parva")
                        .description("Ascent to heaven — final liberation of the Pandavas")
                        .chapters(5)
                        .verses(209)
                        .build()
        );
    }

    public List<VedaDto> getAllVedas() {
        return List.of(
                VedaDto.builder()
                        .vedaId("rig")
                        .name("Rig Veda")
                        .mandalas(10)
                        .hymns(1028)
                        .verses(10552)
                        .description("The oldest of the four Vedas — a collection of 1,028 Vedic Sanskrit hymns dedicated to the gods, especially Agni and Indra. The foundation of Vedic religion.").build(),

                VedaDto
                        .builder()
                        .vedaId("yajur")
                        .name("Yajur Veda")
                        .mandalas(40)
                        .hymns(1875)
                        .verses(1975)
                        .description("The Veda of ritual formulas — contains prose and verse mantras used in sacrificial ceremonies and Vedic rituals.").build(),

                VedaDto
                        .builder()
                        .vedaId("sama")
                        .name("Sama Veda")
                        .mandalas(2)
                        .hymns(1875)
                        .verses(1875)
                        .description("The Veda of melodies and chants — almost entirely derived from the Rig Veda, set to musical notes for liturgical chanting.").build(),

                VedaDto
                        .builder()
                        .vedaId("atharva")
                        .name("Atharva Veda")
                        .mandalas(20)
                        .hymns(730)
                        .verses(5987)
                        .description("The Veda of magical formulas — contains hymns, mantras, and spells for healing, daily life, and protection. More earthy and practical in nature.").build()
        );
    }

    public List<UpanishadDto> getAllUpanishads() {
        return List.of(
                UpanishadDto.builder().id("isha").name("Isha Upanishad").associatedVeda("Yajur").chapters(1)
                        .description("The shortest Upanishad — 18 verses on the divine in all things and the path of knowledge vs action.").build(),
                UpanishadDto.builder().id("kena").name("Kena Upanishad").associatedVeda("Sama").chapters(4)
                        .description("'By whom?' — explores the nature of Brahman as the ultimate knower behind all senses and mind.").build(),
                UpanishadDto.builder().id("katha").name("Katha Upanishad").associatedVeda("Yajur").chapters(6)
                        .description("Nachiketa's dialogue with Yama (Death) — reveals the secret of the immortal Self.").build(),
                UpanishadDto.builder().id("prashna").name("Prashna Upanishad").associatedVeda("Atharva").chapters(6)
                        .description("Six questions and answers about life, prana, Om, and Brahman.").build(),
                UpanishadDto.builder().id("mundaka").name("Mundaka Upanishad").associatedVeda("Atharva").chapters(3)
                        .description("Two kinds of knowledge — lower (worldly) and higher (knowledge of Brahman).").build(),
                UpanishadDto.builder().id("mandukya").name("Mandukya Upanishad").associatedVeda("Atharva").chapters(1)
                        .description("Twelve verses on Om and the four states of consciousness.").build(),
                UpanishadDto.builder().id("taittiriya").name("Taittiriya Upanishad").associatedVeda("Yajur").chapters(3)
                        .description("Three chapters: Shiksha Valli, Brahmananda Valli, Bhrigu Valli — on education, Brahman, and bliss.").build(),
                UpanishadDto.builder().id("aitareya").name("Aitareya Upanishad").associatedVeda("Rig").chapters(3)
                        .description("Creation of the universe and the nature of Atman — consciousness as Brahman.").build(),
                UpanishadDto.builder().id("chandogya").name("Chandogya Upanishad").associatedVeda("Sama").chapters(8)
                        .description("One of the largest Upanishads — includes 'Tat tvam asi' (That thou art) and the story of Shvetaketu.").build(),
                UpanishadDto.builder().id("brihadaranyaka").name("Brihadaranyaka Upanishad").associatedVeda("Yajur").chapters(6)
                        .description("The largest Upanishad — Yajnavalkya's dialogues on the nature of Brahman, Atman, and liberation.").build()
        );
    }
}
