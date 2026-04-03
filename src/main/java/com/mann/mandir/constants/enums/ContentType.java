package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum ContentType {

    AARTI("Aarti", ContentDomain.GOD),
    CHALISA("Chalisa", ContentDomain.GOD),
    STOTRAM("Stotram", ContentDomain.GOD),
    MANTRA("Mantra", ContentDomain.GOD),
    CHAPTER("Chapter", ContentDomain.SCRIPTURES),
    VERSE("Verse", ContentDomain.SCRIPTURES),
    VEDA("Veda", ContentDomain.VEDAS),
    UPANISHAD("Upanishad", ContentDomain.VEDAS);

    private final String displayName;
    private final ContentDomain domain;
}
