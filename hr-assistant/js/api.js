/**
 * api.js — HR Assistant API Service Layer
 * ========================================
 * All backend communication is isolated here.
 * The rest of the app never makes direct fetch() calls.
 *
 * Depends on: config.js (must be loaded first)
 */

const API = (() => {
    'use strict';

    // Prevent duplicate in-flight requests
    let _pendingRequest = null;

    // ── Error types ───────────────────────────────────────────────────────
    class APIError extends Error {
        constructor(message, type, statusCode = null) {
            super(message);
            this.name = 'APIError';
            this.type = type;           // 'network' | 'timeout' | 'server' | 'validation' | 'unknown'
            this.statusCode = statusCode;
        }
    }

    /**
     * Map raw fetch errors and HTTP status codes to user-friendly messages.
     */
    function _friendlyError(error, response = null) {
        // Network failure (offline, DNS, CORS, etc.)
        if (error instanceof TypeError && error.message.includes('fetch')) {
            return new APIError(
                'Unable to connect to the HR Assistant service. Please check your connection and try again.',
                'network'
            );
        }

        // Abort / timeout
        if (error.name === 'AbortError') {
            return new APIError(
                'The request took too long. The HR knowledge service may be busy — please try again.',
                'timeout'
            );
        }

        // HTTP errors from server
        if (response) {
            const status = response.status;
            if (status === 429) {
                return new APIError(
                    'Too many requests. Please wait a moment before trying again.',
                    'server', status
                );
            }
            if (status === 503) {
                return new APIError(
                    'The HR knowledge base is still loading. Please try again in a moment.',
                    'server', status
                );
            }
            if (status >= 500) {
                return new APIError(
                    'The HR Assistant service encountered an issue. Please try again later.',
                    'server', status
                );
            }
            if (status === 422) {
                return new APIError(
                    'Your message could not be processed. Please check and try again.',
                    'validation', status
                );
            }
            return new APIError(
                'Something went wrong. Please try again.',
                'unknown', status
            );
        }

        // Generic fallback
        return new APIError(
            'An unexpected error occurred. Please try again.',
            'unknown'
        );
    }


    // ── Response normalization ────────────────────────────────────────────
    /**
     * Normalize the backend response into a consistent shape
     * so the rest of the app doesn't depend on raw API structure.
     */
    function _normalizeResponse(data) {
        return {
            answer:           data.answer || '',
            sources:          (data.sources || []).map(s => ({
                title:     s.title || 'HR Policy Document',
                content:   s.content || '',
                relevance: s.relevance || 0,
            })),
            blocked:          !!data.blocked,
            blockReason:      data.block_reason || null,
            sessionId:        data.session_id || null,
            processingTimeMs: data.processing_time_ms || 0,
        };
    }


    // ── Core request helper ───────────────────────────────────────────────
    async function _request(url, options = {}) {
        const controller = new AbortController();
        const timeout = setTimeout(
            () => controller.abort(),
            CONFIG.REQUEST_TIMEOUT_MS
        );

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...(options.headers || {}),
                },
            });

            if (!response.ok) {
                let errorDetail = '';
                try {
                    const errBody = await response.json();
                    errorDetail = errBody.detail || '';
                } catch (_) { /* ignore parse error */ }

                throw _friendlyError(
                    new Error(errorDetail || response.statusText),
                    response
                );
            }

            return await response.json();
        } catch (error) {
            if (error instanceof APIError) throw error;
            throw _friendlyError(error);
        } finally {
            clearTimeout(timeout);
        }
    }


    // ── Public API ────────────────────────────────────────────────────────

    /**
     * Send a chat message to the HR Assistant backend.
     * @param {string}  message    - The user's question.
     * @param {string?} sessionId  - Optional session/conversation ID.
     * @returns {Promise<object>}  - Normalized response object.
     */
    async function sendMessage(message, sessionId = null) {
        // Prevent duplicate simultaneous requests
        if (_pendingRequest) {
            throw new APIError('A request is already in progress. Please wait.', 'validation');
        }

        const body = { message };
        if (sessionId) body.session_id = sessionId;

        _pendingRequest = _request(CONFIG.ENDPOINTS.CHAT, {
            method: 'POST',
            body: JSON.stringify(body),
        });

        try {
            const data = await _pendingRequest;
            return _normalizeResponse(data);
        } finally {
            _pendingRequest = null;
        }
    }

    /**
     * Check backend health / readiness.
     * @returns {Promise<{status: string, vectorstoreReady: boolean, policiesLoaded: number}>}
     */
    async function checkHealth() {
        try {
            const data = await _request(CONFIG.ENDPOINTS.HEALTH, { method: 'GET' });
            return {
                status:           data.status || 'unknown',
                vectorstoreReady: !!data.vectorstore_ready,
                policiesLoaded:   data.policies_loaded || 0,
            };
        } catch (_) {
            return { status: 'offline', vectorstoreReady: false, policiesLoaded: 0 };
        }
    }

    /**
     * Whether a request is currently in flight.
     */
    function isBusy() {
        return _pendingRequest !== null;
    }

    // Expose public interface
    return Object.freeze({
        sendMessage,
        checkHealth,
        isBusy,
        APIError,
    });
})();
