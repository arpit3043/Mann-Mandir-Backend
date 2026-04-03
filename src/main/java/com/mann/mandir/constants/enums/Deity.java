package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum Deity {

    GANESH("Ganesh", "गणेश"),
    LAKSHMI("Lakshmi", "लक्ष्मी"),
    SHIVA("Shiva", "शिव"),
    KRISHNA("Krishna", "कृष्ण"),
    VISHNU("Vishnu", "विष्णु"),
    DURGA("Durga", "दुर्गा"),
    SARASWATI("Saraswati", "सरस्वती"),
    HANUMAN("Hanuman", "हनुमान"),
    RAM("Ram", "राम"),
    SURYA("Surya", "सूर्य"),
    PARVATI("Parvati", "पार्वती");

    private final String displayName;
    private final String devanagari;

    public static Deity fromString(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        for (Deity deity : values()) {
            if (deity.displayName.equalsIgnoreCase(value) || deity.name().equalsIgnoreCase(value)) {
                return deity;
            }
        }
        throw new IllegalArgumentException("Unknown deity: " + value);
    }
}
