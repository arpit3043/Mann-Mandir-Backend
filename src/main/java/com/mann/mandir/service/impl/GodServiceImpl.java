package com.mann.mandir.service.impl;

import com.mann.mandir.client.impl.HanumanChalisaClient;
import com.mann.mandir.client.impl.HanumanChalisaClient.ChalisaVerseResponse;
import com.mann.mandir.client.impl.HavyakaApiClient;
import com.mann.mandir.client.impl.ShlokaApiClient;
import com.mann.mandir.constants.CacheNames;
import com.mann.mandir.dto.domain.ChalisaDto;
import com.mann.mandir.dto.domain.ChalisaVerseDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.StotramDto;
import com.mann.mandir.dto.god.AartiDto;
import com.mann.mandir.exception.ResourceNotFoundException;
import com.mann.mandir.service.GodService;
import com.mann.mandir.util.PaginationUtils;
import com.mann.mandir.util.StaticContentRegistry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class GodServiceImpl implements GodService {

    private final HanumanChalisaClient hanumanChalisaClient;
    private final HavyakaApiClient havyakaApiClient;
    private final ShlokaApiClient shlokaApiClient;
    private final StaticContentRegistry staticRegistry;

    @Override
    @Cacheable(value = CacheNames.AARTI, key = "#deity + '_' + #page + '_' + #size")
    public List<AartiDto> getAartis(String deity, int page, int size) {
        List<AartiDto> all = staticRegistry.getAllAartis();
        if (deity != null && !deity.isBlank()) {
            all = all.stream()
                    .filter(a -> a.getDeity().equalsIgnoreCase(deity))
                    .collect(Collectors.toList());
        }
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.AARTI, key = "#aartiId")
    public AartiDto getAartiById(String aartiId) {
        return staticRegistry.getAllAartis().stream()
                .filter(a -> a.getId().equals(aartiId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Aarti", aartiId));
    }

    @Override
    @Cacheable(value = CacheNames.AARTI, key = "'deities'")
    public List<String> getAartiDeities() {
        return staticRegistry.getAllAartis().stream()
                .map(AartiDto::getDeity)
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }

    @Override
    @Cacheable(value = CacheNames.CHALISA, key = "'list_' + #page + '_' + #size")
    public List<ChalisaDto> getChalisas(int page, int size) {
        List<ChalisaDto> all = staticRegistry.getAllChalisas();
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.CHALISA, key = "#deity")
    public ChalisaDto getChalisaByDeity(String deity) {
        if ("hanuman".equalsIgnoreCase(deity)) {
            return fetchHanumanChalisa();
        }
        return staticRegistry.getChalisaByDeity(deity)
                .orElseThrow(() -> new ResourceNotFoundException("Chalisa", deity));
    }

    @Override
    @Cacheable(value = CacheNames.CHALISA, key = "#deity + '_' + #verseNumber")
    public ChalisaVerseDto getChalisaVerse(String deity, int verseNumber) {
        if ("hanuman".equalsIgnoreCase(deity)) {
            return hanumanChalisaClient.getVerse(verseNumber)
                    .map(this::mapChalisaVerse)
                    .orElseThrow(() -> new ResourceNotFoundException("Chalisa verse", String.valueOf(verseNumber)));
        }
        ChalisaDto chalisa = getChalisaByDeity(deity);
        return chalisa.getVerses().stream()
                .filter(v -> v.getVerseNumber() == verseNumber)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Chalisa verse", String.valueOf(verseNumber)));
    }

    private ChalisaDto fetchHanumanChalisa() {
        List<ChalisaVerseResponse> verses = hanumanChalisaClient.getAllVerses()
                .orElseGet(() -> {
                    log.warn("Hanuman Chalisa API unavailable, using static fallback");
                    return staticRegistry.getHanumanChalisaVerses();
                });

        List<ChalisaVerseDto> verseDtos = verses.stream()
                .map(this::mapChalisaVerse)
                .collect(Collectors.toList());

        return ChalisaDto.builder()
                .id("hanuman-chalisa")
                .deity("Hanuman")
                .title("Hanuman Chalisa")
                .totalVerses(verseDtos.size())
                .verses(verseDtos)
                .build();
    }

    private ChalisaVerseDto mapChalisaVerse(ChalisaVerseResponse r) {
        return ChalisaVerseDto.builder()
                .verseNumber(r.getNumber())
                .type(r.getType())
                .devanagari(r.getDevanagari())
                .transliteration(r.getTransliteration())
                .englishTranslation(r.getEnglishTranslation())
                .hindiTranslation(r.getHindiTranslation())
                .tags(r.getTags())
                .build();
    }

    @Override
    @Cacheable(value = CacheNames.STOTRAM, key = "#deity + '_' + #page + '_' + #size")
    public List<StotramDto> getStotrams(String deity, int page, int size) {
        List<StotramDto> all = staticRegistry.getAllStotrams();
        if (deity != null && !deity.isBlank()) {
            all = all.stream()
                    .filter(s -> s.getDeity().equalsIgnoreCase(deity))
                    .collect(Collectors.toList());
        }
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.STOTRAM, key = "#stotramId")
    public StotramDto getStotramById(String stotramId) {
        return staticRegistry.getAllStotrams().stream()
                .filter(s -> s.getId().equals(stotramId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Stotram", stotramId));
    }

    @Override
    @Cacheable(value = CacheNames.MANTRA, key = "'random'")
    public MantraDto getRandomMantra() {
        return shlokaApiClient.getRandomShloka()
                .map(r -> MantraDto.builder()
                        .id(r.getId())
                        .text(r.getText())
                        .meaning(r.getMeaning())
                        .deity(r.getDeity())
                        .veda(r.getSource())
                        .build())
                .orElseGet(() -> staticRegistry.getRandomMantra());
    }

    @Override
    @Cacheable(value = CacheNames.MANTRA, key = "#deity + '_' + #limit")
    public List<MantraDto> getMantras(String deity, int limit) {
        Optional<List<HavyakaApiClient.MantraResponse>> response = deity != null
                ? havyakaApiClient.getMantras(deity, limit)
                : havyakaApiClient.getMantras(limit);

        return response.map(list -> list.stream()
                        .map(r -> MantraDto.builder()
                                .id(r.getId())
                                .name(r.getName())
                                .text(r.getText())
                                .meaning(r.getMeaning())
                                .deity(r.getDeity())
                                .tags(r.getTags())
                                .build())
                        .collect(Collectors.toList()))
                .orElseGet(() -> staticRegistry.getMantras(deity, limit));
    }
}
