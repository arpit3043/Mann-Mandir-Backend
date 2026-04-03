package com.mann.mandir.util;

import lombok.NoArgsConstructor;

import java.util.Collections;
import java.util.List;

@NoArgsConstructor
public final class PaginationUtils {

    public static <T> List<T> paginate(List<T> source, int page, int size) {
        if (source == null || source.isEmpty()) {
            return Collections.emptyList();
        }
        if (size == Integer.MAX_VALUE) {
            return source;
        }
        int from = Math.min(page * size, source.size());
        int to = Math.min(from + size, source.size());
        return source.subList(from, to);
    }

    public static int totalPages(int total, int size) {
        return (int) Math.ceil((double) total / size);
    }
}
