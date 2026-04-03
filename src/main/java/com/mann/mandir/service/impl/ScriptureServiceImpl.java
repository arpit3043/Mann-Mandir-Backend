package com.mann.mandir.service.impl;

import com.mann.mandir.client.impl.DharmicDataClient;
import com.mann.mandir.client.impl.GitaTheAumClient;
import com.mann.mandir.client.impl.GitaVedicClient;
import com.mann.mandir.constants.CacheNames;
import com.mann.mandir.dto.domain.GitaChapterDto;
import com.mann.mandir.dto.domain.GitaVerseDto;
import com.mann.mandir.dto.domain.MahabharataParvaDto;
import com.mann.mandir.dto.domain.MahabharataVerseDto;
import com.mann.mandir.dto.domain.RamayanaKandaDto;
import com.mann.mandir.dto.domain.RamayanaVerseDto;
import com.mann.mandir.exception.ResourceNotFoundException;
import com.mann.mandir.service.ScriptureService;
import com.mann.mandir.util.PaginationUtils;
import com.mann.mandir.util.StaticContentRegistry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class ScriptureServiceImpl implements ScriptureService {

    private final GitaTheAumClient gitaTheAumClient;
    private final GitaVedicClient gitaVedicClient;
    private final DharmicDataClient dharmicDataClient;
    private final StaticContentRegistry staticRegistry;

    @Override
    @Cacheable(value = CacheNames.GITA, key = "'chapters'")
    public List<GitaChapterDto> getGitaChapters() {
        Optional<List<GitaTheAumClient.TheAumChapterResponse>> response =
                gitaTheAumClient.getAllChapters();

        if (response.isPresent()) {
            return response.get().stream()
                    .map(this::mapGitaChapter)
                    .collect(Collectors.toList());
        }

        log.warn("TheAum chapters API unavailable, trying VedicScriptures fallback");
        return gitaVedicClient.getAllChapters()
                .map(list -> list.stream()
                        .map(c -> GitaChapterDto.builder()
                                .number(c.getChapter_number())
                                .name(c.getName())
                                .translation(c.getTranslation())
                                .versesCount(c.getVerses_count())
                                .build())
                        .collect(Collectors.toList()))
                .orElseGet(staticRegistry::getGitaChapters);
    }

    @Override
    @Cacheable(value = CacheNames.GITA, key = "'chapter_' + #chapterNumber")
    public GitaChapterDto getGitaChapter(int chapterNumber) {
        return gitaTheAumClient.getChapter(chapterNumber)
                .map(this::mapGitaChapter)
                .orElseGet(() -> getGitaChapters().stream()
                        .filter(c -> c.getNumber() == chapterNumber)
                        .findFirst()
                        .orElseThrow(() -> new ResourceNotFoundException("Gita chapter", String.valueOf(chapterNumber))));
    }

    @Override
    @Cacheable(value = CacheNames.GITA, key = "'chapter_verses_' + #chapterNumber")
    public List<GitaVerseDto> getGitaVersesByChapter(int chapterNumber) {
        return gitaTheAumClient.getChapterVerses(chapterNumber)
                .map(list -> list.stream()
                        .map(v -> enrichGitaVerse(v, chapterNumber))
                        .collect(Collectors.toList()))
                .orElseThrow(() -> new ResourceNotFoundException("Gita chapter verses", String.valueOf(chapterNumber)));
    }

    @Override
    @Cacheable(value = CacheNames.GITA, key = "#chapterNumber + '_' + #verseNumber")
    public GitaVerseDto getGitaVerse(int chapterNumber, int verseNumber) {
        Optional<GitaVedicClient.VedicVerseResponse> vedicResp =
                gitaVedicClient.getSlok(chapterNumber, verseNumber);

        Optional<GitaTheAumClient.TheAumTranslationResponse> translationsResp =
                gitaTheAumClient.getVerseTranslations(chapterNumber, verseNumber);
        Optional<GitaTheAumClient.TheAumCommentaryResponse> commentaryResp =
                gitaTheAumClient.getVerseCommentary(chapterNumber, verseNumber);

        Map<String, String> translations = translationsResp
                .map(GitaTheAumClient.TheAumTranslationResponse::getTranslations)
                .orElse(new LinkedHashMap<>());

        Map<String, String> commentaries = commentaryResp
                .map(GitaTheAumClient.TheAumCommentaryResponse::getCommentaries)
                .orElse(new LinkedHashMap<>());

        if (vedicResp.isPresent()) {
            GitaVedicClient.VedicVerseResponse v = vedicResp.get();
            if (v.getTej() != null) {
                translations.put("tej", safeGet(v.getTej(), "ht"));
            }
            if (v.getSiva() != null) {
                translations.put("siva", safeGet(v.getSiva(), "et"));
            }
            if (v.getChinmay() != null) {
                translations.put("chinmay", safeGet(v.getChinmay(), "hc"));
            }
        }

        return GitaVerseDto.builder()
                .bgId(chapterNumber + "." + verseNumber)
                .chapter(chapterNumber)
                .verse(verseNumber)
                .shloka(vedicResp.map(GitaVedicClient.VedicVerseResponse::getSlok).orElse(""))
                .translations(translations)
                .commentaries(commentaries)
                .build();
    }

    @Override
    @Cacheable(value = CacheNames.RAMAYANA, key = "'kandas'")
    public List<RamayanaKandaDto> getRamayanaKandas() {
        return staticRegistry.getRamayanaKandas();
    }

    @Override
    @Cacheable(value = CacheNames.RAMAYANA, key = "'kanda_' + #kandaId")
    public RamayanaKandaDto getRamayanaKanda(String kandaId) {
        return staticRegistry.getRamayanaKandas().stream()
                .filter(k -> k.getKandaId().equalsIgnoreCase(kandaId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Ramayana kanda", kandaId));
    }

    @Override
    @Cacheable(value = CacheNames.RAMAYANA, key = "#kandaId + '_' + #sarga + '_' + #page")
    public List<RamayanaVerseDto> getRamayanaVerses(String kandaId, int sarga, int page, int size) {
        Optional<Map<String, Object>> raw = dharmicDataClient.getRamayanaKanda(kandaId);
        List<RamayanaVerseDto> all = raw.map(data -> parseRamayanaVerses(data, kandaId, sarga))
                .orElseGet(() -> staticRegistry.getRamayanaVerses(kandaId, sarga));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.RAMAYANA, key = "#kandaId + '_' + #sarga + '_' + #verse")
    public RamayanaVerseDto getRamayanaVerse(String kandaId, int sarga, int verse) {
        return getRamayanaVerses(kandaId, sarga, 0, Integer.MAX_VALUE).stream()
                .filter(v -> v.getVerse() == verse)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Ramayana verse",
                        kandaId + "/" + sarga + "/" + verse));
    }

    @Override
    @Cacheable(value = CacheNames.MAHABHARATA, key = "'parvas'")
    public List<MahabharataParvaDto> getMahabharataParvas() {
        return staticRegistry.getMahabharataParvas();
    }

    @Override
    @Cacheable(value = CacheNames.MAHABHARATA, key = "'parva_' + #parvaNumber")
    public MahabharataParvaDto getMahabharataParva(int parvaNumber) {
        return getMahabharataParvas().stream()
                .filter(p -> p.getParvaNumber() == parvaNumber)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Mahabharata parva", String.valueOf(parvaNumber)));
    }

    @Override
    @Cacheable(value = CacheNames.MAHABHARATA, key = "#parvaNumber + '_' + #chapterNumber + '_' + #page")
    public List<MahabharataVerseDto> getMahabharataVerses(int parvaNumber, int chapterNumber, int page, int size) {
        Optional<Map<String, Object>> raw = dharmicDataClient.getMahabharataParva(parvaNumber);
        List<MahabharataVerseDto> all = raw.map(data -> parseMahabharataVerses(data, parvaNumber, chapterNumber))
                .orElseGet(() -> staticRegistry.getMahabharataVerses(parvaNumber, chapterNumber));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.MAHABHARATA, key = "#parvaNumber + '_' + #chapterNumber + '_' + #verse")
    public MahabharataVerseDto getMahabharataVerse(int parvaNumber, int chapterNumber, int verse) {
        return getMahabharataVerses(parvaNumber, chapterNumber, 0, Integer.MAX_VALUE).stream()
                .filter(v -> v.getVerse() == verse)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Mahabharata verse",
                        parvaNumber + "/" + chapterNumber + "/" + verse));
    }

    private GitaChapterDto mapGitaChapter(GitaTheAumClient.TheAumChapterResponse c) {
        return GitaChapterDto.builder()
                .number(c.getNumber())
                .name(c.getName())
                .translation(c.getTranslation())
                .transliteration(c.getTransliteration())
                .versesCount(c.getVersesCount())
                .summary(c.getSummary())
                .build();
    }

    private GitaVerseDto enrichGitaVerse(GitaTheAumClient.TheAumVerseResponse v, int chapter) {
        return GitaVerseDto.builder()
                .bgId(v.getBgId())
                .chapter(chapter)
                .verse(v.getVerse())
                .shloka(v.getShloka())
                .build();
    }

    private String safeGet(Map<String, Object> map, String key) {
        Object val = map.get(key);
        return val != null ? val.toString() : "";
    }

    @SuppressWarnings("unchecked")
    private List<RamayanaVerseDto> parseRamayanaVerses(Map<String, Object> data, String kandaId, int sarga) {
        List<RamayanaVerseDto> result = new ArrayList<>();
        try {
            Object sargas = data.get("sargas");
            if (sargas instanceof List<?>) {
                List<Map<String, Object>> sargaList = (List<Map<String, Object>>) sargas;
                if (sarga - 1 < sargaList.size()) {
                    Map<String, Object> sargaData = sargaList.get(sarga - 1);
                    Object verses = sargaData.get("verses");
                    if (verses instanceof List<?>) {
                        List<Map<String, Object>> vList = (List<Map<String, Object>>) verses;
                        for (int i = 0; i < vList.size(); i++) {
                            Map<String, Object> v = vList.get(i);
                            result.add(RamayanaVerseDto.builder()
                                    .kandaId(kandaId)
                                    .sarga(sarga)
                                    .verse(i + 1)
                                    .original(String.valueOf(v.getOrDefault("text", "")))
                                    .translation(String.valueOf(v.getOrDefault("translation", "")))
                                    .build());
                        }
                    }
                }
            }
        } catch (Exception e) {
            log.error("Error parsing Ramayana data: {}", e.getMessage());
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    private List<MahabharataVerseDto> parseMahabharataVerses(Map<String, Object> data, int parva, int chapter) {
        List<MahabharataVerseDto> result = new ArrayList<>();
        try {
            Object chapters = data.get("chapters");
            if (chapters instanceof List<?>) {
                List<Map<String, Object>> chapterList = (List<Map<String, Object>>) chapters;
                if (chapter - 1 < chapterList.size()) {
                    Map<String, Object> chapterData = chapterList.get(chapter - 1);
                    Object verses = chapterData.get("verses");
                    if (verses instanceof List<?>) {
                        List<Map<String, Object>> vList = (List<Map<String, Object>>) verses;
                        for (int i = 0; i < vList.size(); i++) {
                            Map<String, Object> v = vList.get(i);
                            result.add(MahabharataVerseDto.builder()
                                    .parva(parva).chapter(chapter).verse(i + 1)
                                    .text(String.valueOf(v.getOrDefault("text", "")))
                                    .translation(String.valueOf(v.getOrDefault("translation", "")))
                                    .build());
                        }
                    }
                }
            }
        } catch (Exception e) {
            log.error("Error parsing Mahabharata data: {}", e.getMessage());
        }
        return result;
    }
}
