package com.mann.mandir.dto.god;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
class ChalisaVerseDto {
    private int verseNumber;
    private String type;          // DOHA, CHAUPAI, SORTHA
    private String devanagari;
    private String transliteration;
    private String englishTranslation;
    private String hindiTranslation;
    private String meter;
    private List<String> tags;
}
