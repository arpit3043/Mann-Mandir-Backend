package com.mann.mandir.dto.domain;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class VerseDto {
    private String id;
    private int chapter;
    private int verse;
    private String sanskrit;
    private String transliteration;
    private Map<String, String> translations;
    private Map<String, String> commentaries;
    private List<WordMeaningDto> wordByWord;
    private String audioUrl;
    private String source;
}
