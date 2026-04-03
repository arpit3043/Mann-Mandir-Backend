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
public class MantraDto {
    private String id;
    private String name;
    private String text;
    private String devanagari;
    private String transliteration;
    private String meaning;
    private String deity;
    private String veda;
    private List<String> tags;
}
