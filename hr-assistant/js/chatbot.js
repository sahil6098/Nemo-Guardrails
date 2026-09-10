/**
 * chatbot.js — HR Assistant Core Chat Logic
 * ==========================================
 * Manages conversation state, message flow, history persistence,
 * and coordinates between API calls and UI updates.
 *
 * Depends on: config.js, api.js, ui.js (all must be loaded first)
 */

const Chatbot = (() => {
    'use strict';

    // ── State ─────────────────────────────────────────────────────────────
    let _conversations = {};          // { conversationId: { id, title, messages[], createdAt, updatedAt } }
    let _activeConversationId = null;
    let _isProcessing = false;

    // ── Helpers ───────────────────────────────────────────────────────────
    function _generateId() {
        return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    function _generateConversationId() {
        return `conv-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    function _timestamp() {
        return new Date().toISOString();
    }

    /**
     * Derive a short title from the first user message.
     */
    function _deriveTitle(message) {
        const cleaned = message.replace(/\s+/g, ' ').trim();
        if (cleaned.length <= CONFIG.MAX_CONVERSATION_TITLE_LENGTH) return cleaned;
        return cleaned.substring(0, CONFIG.MAX_CONVERSATION_TITLE_LENGTH - 1) + '…';
    }


    // ── localStorage persistence ──────────────────────────────────────────
    function _saveToStorage() {
        try {
            // Trim old conversations if over limit
            const ids = Object.keys(_conversations);
            if (ids.length > CONFIG.MAX_CONVERSATIONS_STORED) {
                const sorted = ids.sort((a, b) => {
                    const ta = _conversations[a].updatedAt || _conversations[a].createdAt;
                    const tb = _conversations[b].updatedAt || _conversations[b].createdAt;
                    return new Date(ta) - new Date(tb);
                });
                const toRemove = sorted.slice(0, ids.length - CONFIG.MAX_CONVERSATIONS_STORED);
                toRemove.forEach(id => delete _conversations[id]);
            }

            localStorage.setItem(
                CONFIG.STORAGE_KEYS.CONVERSATIONS,
                JSON.stringify(_conversations)
            );
            localStorage.setItem(
                CONFIG.STORAGE_KEYS.ACTIVE_CONVERSATION,
                _activeConversationId || ''
            );
        } catch (e) {
            console.warn('Failed to save conversation history:', e);
        }
    }

    function _loadFromStorage() {
        try {
            const raw = localStorage.getItem(CONFIG.STORAGE_KEYS.CONVERSATIONS);
            if (raw) {
                _conversations = JSON.parse(raw);
            }
            _activeConversationId = localStorage.getItem(
                CONFIG.STORAGE_KEYS.ACTIVE_CONVERSATION
            ) || null;

            // Validate active conversation still exists
            if (_activeConversationId && !_conversations[_activeConversationId]) {
                _activeConversationId = null;
            }
        } catch (e) {
            console.warn('Failed to load conversation history:', e);
            _conversations = {};
            _activeConversationId = null;
        }
    }


    // ── Conversation management ───────────────────────────────────────────

    function _getActiveConversation() {
        if (!_activeConversationId) return null;
        return _conversations[_activeConversationId] || null;
    }

    /**
     * Create a new conversation and make it active.
     */
    function newConversation() {
        const id = _generateConversationId();
        _conversations[id] = {
            id,
            title: 'New Conversation',
            messages: [],
            createdAt: _timestamp(),
            updatedAt: _timestamp(),
        };
        _activeConversationId = id;
        _isProcessing = false;
        _saveToStorage();

        // Update UI
        UI.showWelcomeScreen();
        UI.renderConversationHistory(getConversationList(), _activeConversationId);
        UI.updateChatInput(false);
        return id;
    }

    /**
     * Switch to an existing conversation.
     */
    function switchConversation(conversationId) {
        if (!_conversations[conversationId]) return;
        if (_isProcessing) return; // Don't switch while processing

        _activeConversationId = conversationId;
        _saveToStorage();

        const conv = _conversations[conversationId];
        if (conv.messages.length === 0) {
            UI.showWelcomeScreen();
        } else {
            UI.showChatScreen();
            UI.renderAllMessages(conv.messages);
        }
        UI.renderConversationHistory(getConversationList(), _activeConversationId);
        UI.updateChatInput(false);
    }

    /**
     * Rename a conversation.
     */
    function renameConversation(conversationId, newTitle) {
        if (!_conversations[conversationId]) return;
        _conversations[conversationId].title = newTitle.substring(0, CONFIG.MAX_CONVERSATION_TITLE_LENGTH);
        _conversations[conversationId].updatedAt = _timestamp();
        _saveToStorage();
        UI.renderConversationHistory(getConversationList(), _activeConversationId);
        UI.showToast('Conversation renamed', 'success');
    }

    /**
     * Delete a conversation.
     */
    function deleteConversation(conversationId) {
        if (!_conversations[conversationId]) return;
        delete _conversations[conversationId];

        if (_activeConversationId === conversationId) {
            _activeConversationId = null;
            // Switch to most recent or show welcome
            const list = getConversationList();
            if (list.length > 0) {
                switchConversation(list[0].id);
            } else {
                newConversation();
            }
        }
        _saveToStorage();
        UI.renderConversationHistory(getConversationList(), _activeConversationId);
        UI.showToast('Conversation deleted', 'success');
    }

    /**
     * Get all conversations as sorted array (newest first).
     */
    function getConversationList() {
        return Object.values(_conversations)
            .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
    }


    // ── Message sending ───────────────────────────────────────────────────

    /**
     * Send a message to the HR Assistant.
     * Handles the full flow: validate → add user message → show typing → API call → add response.
     */
    async function sendMessage(messageText) {
        const text = messageText.trim();

        // Validation
        if (!text) return;
        if (text.length > CONFIG.MAX_MESSAGE_LENGTH) {
            UI.showToast(`Message too long. Maximum ${CONFIG.MAX_MESSAGE_LENGTH} characters.`, 'warning');
            return;
        }
        if (_isProcessing) {
            UI.showToast('Please wait for the current response.', 'info');
            return;
        }

        // Ensure we have an active conversation
        if (!_activeConversationId) {
            newConversation();
        }

        const conv = _getActiveConversation();
        if (!conv) return;

        // If this is the first message, transition to chat view and set title
        if (conv.messages.length === 0) {
            conv.title = _deriveTitle(text);
            UI.showChatScreen();
        }

        // ── Add user message ──────────────────────────────────────────────
        const userMessage = {
            id: _generateId(),
            role: 'user',
            content: text,
            timestamp: _timestamp(),
            sources: [],
        };
        conv.messages.push(userMessage);
        conv.updatedAt = _timestamp();
        _saveToStorage();

        UI.appendMessage(userMessage);
        UI.clearInput();
        UI.scrollToBottom();
        UI.renderConversationHistory(getConversationList(), _activeConversationId);

        // ── Show typing indicator & call API ──────────────────────────────
        _isProcessing = true;
        UI.updateChatInput(true);

        // Small delay before showing typing to avoid flash for fast responses
        const typingTimeout = setTimeout(() => {
            UI.showTypingIndicator();
        }, CONFIG.TYPING_INDICATOR_DELAY_MS);

        try {
            const response = await API.sendMessage(text, conv.id);

            clearTimeout(typingTimeout);
            UI.hideTypingIndicator();

            // ── Add assistant message ─────────────────────────────────────
            const assistantMessage = {
                id: _generateId(),
                role: 'assistant',
                content: response.answer,
                timestamp: _timestamp(),
                sources: response.sources,
                blocked: response.blocked,
                blockReason: response.blockReason,
                processingTimeMs: response.processingTimeMs,
            };
            conv.messages.push(assistantMessage);
            conv.updatedAt = _timestamp();
            _saveToStorage();

            UI.appendMessage(assistantMessage);
            UI.scrollToBottom();

        } catch (error) {
            clearTimeout(typingTimeout);
            UI.hideTypingIndicator();

            // Show error as a system message
            const errorMessage = {
                id: _generateId(),
                role: 'error',
                content: error.message || 'An unexpected error occurred. Please try again.',
                timestamp: _timestamp(),
                sources: [],
                errorType: error.type || 'unknown',
            };
            conv.messages.push(errorMessage);
            conv.updatedAt = _timestamp();
            _saveToStorage();

            UI.appendMessage(errorMessage);
            UI.scrollToBottom();
        } finally {
            _isProcessing = false;
            UI.updateChatInput(false);
        }
    }

    /**
     * Re-send the last user message (regenerate).
     */
    async function regenerateLastResponse() {
        const conv = _getActiveConversation();
        if (!conv || _isProcessing) return;

        // Find the last user message
        let lastUserMsg = null;
        for (let i = conv.messages.length - 1; i >= 0; i--) {
            if (conv.messages[i].role === 'user') {
                lastUserMsg = conv.messages[i];
                break;
            }
        }
        if (!lastUserMsg) return;

        // Remove the last assistant/error message
        const lastMsg = conv.messages[conv.messages.length - 1];
        if (lastMsg.role === 'assistant' || lastMsg.role === 'error') {
            conv.messages.pop();
            _saveToStorage();
        }

        // Re-render and re-send
        UI.renderAllMessages(conv.messages);
        await sendMessage(lastUserMsg.content);
    }

    /**
     * Record feedback for a message.
     */
    function recordFeedback(messageId, feedback) {
        const conv = _getActiveConversation();
        if (!conv) return;

        const msg = conv.messages.find(m => m.id === messageId);
        if (msg) {
            msg.feedback = feedback; // 'helpful' | 'not_helpful'
            _saveToStorage();
            UI.showToast(
                feedback === 'helpful' ? 'Thanks for the feedback!' : 'Feedback recorded. We\'ll improve.',
                'success'
            );
        }
    }


    // ── Initialization ────────────────────────────────────────────────────

    function init() {
        _loadFromStorage();

        // If we have an active conversation with messages, show it
        const conv = _getActiveConversation();
        if (conv && conv.messages.length > 0) {
            UI.showChatScreen();
            UI.renderAllMessages(conv.messages);
        } else {
            // Start fresh
            if (!_activeConversationId) {
                newConversation();
            } else {
                UI.showWelcomeScreen();
            }
        }

        UI.renderConversationHistory(getConversationList(), _activeConversationId);

        // Check backend health
        _checkBackendHealth();
    }

    async function _checkBackendHealth() {
        const health = await API.checkHealth();
        UI.updateStatusIndicator(health.status === 'online' && health.vectorstoreReady);
    }

    // ── Public interface ──────────────────────────────────────────────────
    return Object.freeze({
        init,
        sendMessage,
        newConversation,
        switchConversation,
        renameConversation,
        deleteConversation,
        regenerateLastResponse,
        recordFeedback,
        getConversationList,
        get isProcessing() { return _isProcessing; },
        get activeConversationId() { return _activeConversationId; },
    });
})();
