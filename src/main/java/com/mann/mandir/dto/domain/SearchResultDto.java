package com.mann.mandir.dto.domain;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SearchResultDto {
    private String id;
    private String type;
    private String source;
    private String title;
    private String snippet;
    private double relevanceScore;
    private Map<String, Object> metadata;
}
