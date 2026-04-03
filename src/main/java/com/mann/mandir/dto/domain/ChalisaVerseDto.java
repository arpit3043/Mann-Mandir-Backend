package com.mann.mandir.dto.domain;

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
public class ChalisaVerseDto {
    private int verseNumber;
    private String type;
    private String devanagari;
    private String transliteration;
    private String englishTranslation;
    private String hindiTranslation;
    private List<String> tags;
}
