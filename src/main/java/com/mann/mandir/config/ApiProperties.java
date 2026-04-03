package com.mann.mandir.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@Component
@ConfigurationProperties(prefix = "api")
public class ApiProperties {

    private Gita gita = new Gita();
    private Shloka shloka = new Shloka();
    private Havyaka havyaka = new Havyaka();
    private Rigveda rigveda = new Rigveda();
    private Chalisa chalisa = new Chalisa();
    private Ramayana ramayana = new Ramayana();
    private DharmicData dharmicdata = new DharmicData();

    @Data
    public static class Gita {
        /** Binds {@code api.gita.theaum.base-url} */
        private Theaum theaum = new Theaum();
        /** Binds {@code api.gita.vedic.base-url} */
        private Vedic vedic = new Vedic();

        @Data
        public static class Theaum {
            private String baseUrl;
        }

        @Data
        public static class Vedic {
            private String baseUrl;
        }
    }

    @Data
    public static class Shloka {
        private String baseUrl;
    }

    @Data
    public static class Havyaka {
        private String baseUrl;
    }

    @Data
    public static class Rigveda {
        private String baseUrl;
    }

    @Data
    public static class Chalisa {
        private Hanuman hanuman = new Hanuman();

        @Data
        public static class Hanuman {
            private String baseUrl;
        }
    }

    @Data
    public static class Ramayana {
        private String baseUrl;
    }

    @Data
    public static class DharmicData {
        private String baseUrl;
    }
}
