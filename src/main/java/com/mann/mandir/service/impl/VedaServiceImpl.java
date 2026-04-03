package com.mann.mandir.service.impl;

import com.mann.mandir.client.impl.DharmicDataClient;
import com.mann.mandir.client.impl.HavyakaApiClient;
import com.mann.mandir.client.impl.RigVedaApiClient;
import com.mann.mandir.constants.CacheNames;
import com.mann.mandir.dto.domain.VedaDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.RigVedaVerseDto;
import com.mann.mandir.dto.domain.UpanishadDto;
import com.mann.mandir.dto.domain.UpanishadVerseDto;
import com.mann.mandir.exception.ResourceNotFoundException;
import com.mann.mandir.service.VedaService;
import com.mann.mandir.util.PaginationUtils;
import com.mann.mandir.util.StaticContentRegistry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.Random;

@Slf4j
@Service
@RequiredArgsConstructor
public class VedaServiceImpl implements VedaService {

    private final RigVedaApiClient rigVedaApiClient;
    private final HavyakaApiClient havyakaApiClient;
    private final DharmicDataClient dharmicDataClient;
    private final StaticContentRegistry staticRegistry;

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'all_vedas'")
    public List<VedaDto> getAllVedas() {
        return staticRegistry.getAllVedas();
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'veda_' + #vedaId")
    public VedaDto getVeda(String vedaId) {
        return getAllVedas().stream()
                .filter(v -> v.getVedaId().equalsIgnoreCase(vedaId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Veda", vedaId));
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'rig_mandala_' + #mandala + '_' + #page")
    public List<RigVedaVerseDto> getRigVedaByMandala(int mandala, int page, int size) {
        List<RigVedaVerseDto> all = rigVedaApiClient.getByMandala(mandala)
                .map(list -> list.stream().map(this::mapRigVedaVerse).collect(Collectors.toList()))
                .orElseGet(() -> staticRegistry.getRigVedaVerses(mandala));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'rig_deity_' + #deity + '_' + #page")
    public List<RigVedaVerseDto> getRigVedaByDeity(String deity, int page, int size) {
        List<RigVedaVerseDto> all = rigVedaApiClient.getByDeity(deity)
                .map(list -> list.stream().map(this::mapRigVedaVerse).collect(Collectors.toList()))
                .orElseGet(ArrayList::new);
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'rig_poet_' + #poet + '_' + #page")
    public List<RigVedaVerseDto> getRigVedaByPoet(String poet, int page, int size) {
        List<RigVedaVerseDto> all = rigVedaApiClient.getByPoet(poet)
                .map(list -> list.stream().map(this::mapRigVedaVerse).collect(Collectors.toList()))
                .orElseGet(ArrayList::new);
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'rig_' + #mandala + '_' + #sukta + '_' + #stanza")
    public RigVedaVerseDto getRigVedaVerse(int mandala, int sukta, int stanza) {
        return getRigVedaByMandala(mandala, 0, Integer.MAX_VALUE).stream()
                .filter(v -> v.getSukta() == sukta && v.getStanza() == stanza)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Rig Veda verse",
                        mandala + "/" + sukta + "/" + stanza));
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'yajur_' + #page + '_' + #size")
    public List<MantraDto> getYajurVedaMantras(int page, int size) {
        List<MantraDto> all = dharmicDataClient.getYajurVeda()
                .map(data -> parseVedaMantras(data, "Yajur"))
                .orElseGet(() -> staticRegistry.getVedaMantras("yajur"));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'sama_' + #page + '_' + #size")
    public List<MantraDto> getSamaVedaMantras(int page, int size) {
        List<MantraDto> all = havyakaApiClient.getMantras("sama", 500)
                .map(list -> list.stream().map(this::mapMantra).collect(Collectors.toList()))
                .orElseGet(() -> staticRegistry.getVedaMantras("sama"));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'atharva_' + #page + '_' + #size")
    public List<MantraDto> getAtharvaVedaMantras(int page, int size) {
        List<MantraDto> all = dharmicDataClient.getAtharvaVeda()
                .map(data -> parseVedaMantras(data, "Atharva"))
                .orElseGet(() -> staticRegistry.getVedaMantras("atharva"));
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'upanishads'")
    public List<UpanishadDto> getUpanishads() {
        return staticRegistry.getAllUpanishads();
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'upanishad_' + #upanishadId")
    public UpanishadDto getUpanishad(String upanishadId) {
        return getUpanishads().stream()
                .filter(u -> u.getId().equalsIgnoreCase(upanishadId))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Upanishad", upanishadId));
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'upanishad_' + #upanishadId + '_ch_' + #chapter + '_' + #page")
    public List<UpanishadVerseDto> getUpanishadVerses(String upanishadId, int chapter, int page, int size) {
        List<UpanishadVerseDto> all = staticRegistry.getUpanishadVerses(upanishadId, chapter);
        return PaginationUtils.paginate(all, page, size);
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'upanishad_' + #upanishadId + '_' + #chapter + '_' + #verse")
    public UpanishadVerseDto getUpanishadVerse(String upanishadId, int chapter, int verse) {
        return getUpanishadVerses(upanishadId, chapter, 0, Integer.MAX_VALUE).stream()
                .filter(v -> v.getVerse() == verse)
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Upanishad verse",
                        upanishadId + "/" + chapter + "/" + verse));
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'random_mantra'")
    public MantraDto getRandomVedicMantra() {
        List<MantraDto> pool = staticRegistry.getVedaMantras(null);
        if (pool.isEmpty()) return MantraDto.builder().text("ॐ").meaning("The primordial sound").build();
        return pool.get(new Random().nextInt(pool.size()));
    }

    @Override
    @Cacheable(value = CacheNames.VEDA, key = "'search_' + #deity + '_' + #limit")
    public List<MantraDto> searchMantras(String deity, int limit) {
        return havyakaApiClient.getMantras(deity, limit)
                .map(list -> list.stream().map(this::mapMantra).collect(Collectors.toList()))
                .orElseGet(() -> staticRegistry.getMantras(deity, limit));
    }

    private RigVedaVerseDto mapRigVedaVerse(RigVedaApiClient.RigVedaVerseResponse r) {
        return RigVedaVerseDto.builder()
                .mandala(r.getMandal())
                .sukta(r.getSukta())
                .stanza(r.getStanza())
                .poet(r.getSungby())
                .poetCategory(r.getSungbycategory())
                .deity(r.getSungfor())
                .deityCategory(r.getSungforcategory())
                .meter(r.getMeter())
                .build();
    }

    private MantraDto mapMantra(HavyakaApiClient.MantraResponse r) {
        return MantraDto.builder()
                .id(r.getId())
                .name(r.getName())
                .text(r.getText())
                .meaning(r.getMeaning())
                .deity(r.getDeity())
                .tags(r.getTags())
                .build();
    }

    @SuppressWarnings("unchecked")
    private List<MantraDto> parseVedaMantras(Map<String, Object> data, String vedaName) {
        List<MantraDto> result = new ArrayList<>();
        try {
            Object mantras = data.get("mantras");
            if (mantras instanceof List<?>) {
                List<Map<String, Object>> list = (List<Map<String, Object>>) mantras;
                for (int i = 0; i < list.size(); i++) {
                    Map<String, Object> m = list.get(i);
                    result.add(MantraDto.builder()
                            .id(vedaName.toLowerCase() + "_" + (i + 1))
                            .text(String.valueOf(m.getOrDefault("text", "")))
                            .meaning(String.valueOf(m.getOrDefault("meaning", "")))
                            .veda(vedaName)
                            .build());
                }
            }
        } catch (Exception e) {
            log.error("Error parsing {} Veda data: {}", vedaName, e.getMessage());
        }
        return result;
    }
}
