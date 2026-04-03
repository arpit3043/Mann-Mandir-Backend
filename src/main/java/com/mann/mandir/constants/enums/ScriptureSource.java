package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum ScriptureSource {

    BHAGAVAD_GITA("Bhagavad Gita"),
    VALMIKI_RAMAYANA("Valmiki Ramayana"),
    MAHABHARATA("Mahabharata");

    private final String displayName;
}
