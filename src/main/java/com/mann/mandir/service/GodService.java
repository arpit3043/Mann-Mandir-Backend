package com.mann.mandir.service;

import com.mann.mandir.dto.domain.ChalisaDto;
import com.mann.mandir.dto.domain.ChalisaVerseDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.StotramDto;
import com.mann.mandir.dto.god.AartiDto;

import java.util.List;

public interface GodService {
    List<AartiDto> getAartis(String deity, int page, int size);
    AartiDto getAartiById(String id);
    List<String> getAartiDeities();
    List<ChalisaDto> getChalisas(int page, int size);
    ChalisaDto getChalisaByDeity(String deity);
    ChalisaVerseDto getChalisaVerse(String deity, int verseNumber);
    List<StotramDto> getStotrams(String deity, int page, int size);
    StotramDto getStotramById(String stotramId);
    MantraDto getRandomMantra();
    List<MantraDto> getMantras(String deity, int limit);
}
