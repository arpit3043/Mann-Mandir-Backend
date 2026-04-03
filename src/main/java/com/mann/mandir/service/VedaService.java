package com.mann.mandir.service;

import com.mann.mandir.dto.domain.*;

import java.util.List;

public interface VedaService {
    List<VedaDto> getAllVedas();
    VedaDto getVeda(String vedaId);
    List<RigVedaVerseDto> getRigVedaByMandala(int mandala, int page, int size);
    List<RigVedaVerseDto> getRigVedaByDeity(String deity, int page, int size);
    List<RigVedaVerseDto> getRigVedaByPoet(String poet, int page, int size);
    RigVedaVerseDto getRigVedaVerse(int mandala, int sukta, int stanza);
    List<MantraDto> getYajurVedaMantras(int page, int size);
    List<MantraDto> getSamaVedaMantras(int page, int size);
    List<MantraDto> getAtharvaVedaMantras(int page, int size);
    List<UpanishadDto> getUpanishads();
    UpanishadDto getUpanishad(String upanishadId);
    List<UpanishadVerseDto> getUpanishadVerses(String upanishadId, int chapter, int page, int size);
    UpanishadVerseDto getUpanishadVerse(String upanishadId, int chapter, int verse);
    MantraDto getRandomVedicMantra();
    List<MantraDto> searchMantras(String deity, int limit);
}
