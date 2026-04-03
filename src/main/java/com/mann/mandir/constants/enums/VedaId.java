package com.mann.mandir.constants.enums;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public enum VedaId {

    RIG("rig", "Rig Veda"),
    YAJUR("yajur", "Yajur Veda"),
    SAMA("sama", "Sama Veda"),
    ATHARVA("atharva", "Atharva Veda");

    private final String id;
    private final String displayName;

    public static VedaId fromString(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        for (VedaId vedaId : values()) {
            if (vedaId.id.equalsIgnoreCase(value) || vedaId.name().equalsIgnoreCase(value)) {
                return vedaId;
            }
        }
        throw new IllegalArgumentException("Unknown veda: " + value);
    }
}
