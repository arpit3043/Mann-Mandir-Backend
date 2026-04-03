package com.mann.mandir.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resourceType, String identifier) {
        super(resourceType + " not found: " + identifier);
    }
}
