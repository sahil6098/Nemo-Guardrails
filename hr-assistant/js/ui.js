/**
 * ui.js — HR Assistant UI Rendering & Interactions
 * ==================================================
 * Handles all DOM manipulation, event listeners, and visual effects.
 * Uses DOMPurify + marked.js for safe markdown rendering.
 *
 * Depends on: config.js, api.js, chatbot.js (chatbot loaded after this, but called via events)
 */

const UI = (() => {
    'use strict';

    // ── DOM references (cached after DOMContentLoaded) ────────────────────
    let $els = {};

    function _cacheDom() {
        $els = {
            // Layout
            sidebar:             document.getElementById('sidebar'),
            sidebarOverlay:      document.getElementById('sidebar-overlay'),
            mainContent:         document.getElementById('main-content'),
            hamburgerBtn:        document.getElementById('hamburger-btn'),
            closeSidebarBtn:     document.getElementById('close-sidebar-btn'),

            // Chat
            welcomeScreen:       document.getElementById('welcome-screen'),
            chatScreen:          document.getElementById('chat-screen'),
            messageContainer:    document.getElementById('message-container'),
            typingIndicator:     document.getElementById('typing-indicator'),

            // Input
            chatInput:           document.getElementById('chat-input'),
            sendBtn:             document.getElementById('send-btn'),
            charCounter:         document.getElementById('char-counter'),

            // Sidebar sections
            newConversationBtn:  document.getElementById('new-conversation-btn'),
            conversationList:    document.getElementById('conversation-list'),
            hrResourceList:      document.getElementById('hr-resource-list'),

            // Status
            statusDot:           document.getElementById('status-dot'),
            statusText:          document.getElementById('status-text'),

            // Quick questions
            quickQuestionsGrid:  document.getElementById('quick-questions-grid'),

            // Toast container
            toastContainer:      document.getElementById('toast-container'),

            // Profile menu
            profileBtn:          document.getElementById('profile-btn'),
            profileMenu:         document.getElementById('profile-menu'),

            // Disclaimer
            disclaimer:          document.getElementById('disclaimer'),
        };
    }


    // ── Markdown rendering (safe) ─────────────────────────────────────────
    function _renderMarkdown(text) {
        if (!text) return '';

        // Strip <think>...</think> tags from LLM responses
        let cleaned = text.replace(/<think>[\s\S]*?<\/think>\s*/gi, '').trim();

        // Use marked.js if available, otherwise basic formatting
        let html;
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                headerIds: false,
                mangle: false,
            });
            html = marked.parse(cleaned);
        } else {
            // Fallback: basic escaping and line breaks
            html = _escapeHtml(cleaned).replace(/\n/g, '<br>');
        }

        // Sanitize with DOMPurify if available
        if (typeof DOMPurify !== 'undefined') {
            html = DOMPurify.sanitize(html, {
                ALLOWED_TAGS: [
                    'p', 'br', 'strong', 'em', 'b', 'i', 'u', 'code', 'pre',
                    'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'hr', 'del', 'sup', 'sub', 'span', 'div',
                ],
                ALLOWED_ATTR: ['href', 'target', 'rel', 'class'],
            });
        }

        return html;
    }

    function _escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return text.replace(/[&<>"']/g, c => map[c]);
    }


    // ── Time formatting ───────────────────────────────────────────────────
    function _formatTime(isoString) {
        try {
            const d = new Date(isoString);
            return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } catch (_) {
            return '';
        }
    }

    function _formatDate(isoString) {
        try {
            const d = new Date(isoString);
            const now = new Date();
            const diff = now - d;
            const dayMs = 86400000;

            if (diff < dayMs && d.getDate() === now.getDate()) return 'Today';
            if (diff < dayMs * 2) return 'Yesterday';
            if (diff < dayMs * 7) return 'Previous 7 days';
            return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
        } catch (_) {
            return '';
        }
    }


    // ── Welcome screen ────────────────────────────────────────────────────
    function showWelcomeScreen() {
        if ($els.welcomeScreen) $els.welcomeScreen.classList.remove('hidden');
        if ($els.chatScreen) $els.chatScreen.classList.add('hidden');
        if ($els.messageContainer) $els.messageContainer.innerHTML = '';
    }

    function showChatScreen() {
        if ($els.welcomeScreen) $els.welcomeScreen.classList.add('hidden');
        if ($els.chatScreen) $els.chatScreen.classList.remove('hidden');
    }


    // ── Quick questions ───────────────────────────────────────────────────
    function _renderQuickQuestions() {
        if (!$els.quickQuestionsGrid) return;

        $els.quickQuestionsGrid.innerHTML = CONFIG.QUICK_QUESTIONS.map(q => `
            <button class="quick-question-card" data-question="${_escapeHtml(q.question)}"
                    aria-label="Ask: ${_escapeHtml(q.question)}">
                <span class="qq-icon" aria-hidden="true">${q.icon}</span>
                <span class="qq-category">${_escapeHtml(q.category)}</span>
                <span class="qq-text">${_escapeHtml(q.question)}</span>
            </button>
        `).join('');

        // Event delegation for quick question clicks
        $els.quickQuestionsGrid.addEventListener('click', (e) => {
            const card = e.target.closest('.quick-question-card');
            if (!card) return;
            const question = card.dataset.question;
            if (question) {
                Chatbot.sendMessage(question);
            }
        });
    }


    // ── HR Resources sidebar ──────────────────────────────────────────────
    function _renderHRResources() {
        if (!$els.hrResourceList) return;

        $els.hrResourceList.innerHTML = CONFIG.HR_RESOURCES.map(r => `
            <button class="sidebar-link hr-resource-link" data-query="${_escapeHtml(r.query)}"
                    aria-label="${_escapeHtml(r.label)}">
                <span class="sidebar-icon" aria-hidden="true">${r.icon}</span>
                <span>${_escapeHtml(r.label)}</span>
            </button>
        `).join('');

        $els.hrResourceList.addEventListener('click', (e) => {
            const link = e.target.closest('.hr-resource-link');
            if (!link) return;
            const query = link.dataset.query;
            if (query) {
                _closeSidebarMobile();
                Chatbot.sendMessage(query);
            }
        });
    }


    // ── Message rendering ─────────────────────────────────────────────────

    /**
     * Create the HTML for a single chat message.
     */
    function _createMessageElement(msg) {
        const div = document.createElement('div');
        div.className = `message message-${msg.role}`;
        div.id = `message-${msg.id}`;
        div.setAttribute('data-message-id', msg.id);

        if (msg.role === 'user') {
            div.innerHTML = `
                <div class="message-bubble user-bubble">
                    <div class="message-content">${_renderMarkdown(msg.content)}</div>
                    <div class="message-meta">
                        <span class="message-time">${_formatTime(msg.timestamp)}</span>
                    </div>
                </div>
            `;
        } else if (msg.role === 'assistant') {
            const sourcesHtml = _renderSources(msg.sources);
            const feedbackClass = msg.feedback ? ` feedback-${msg.feedback}` : '';

            div.innerHTML = `
                <div class="message-avatar" aria-hidden="true">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2a5 5 0 0 1 5 5v1a5 5 0 0 1-10 0V7a5 5 0 0 1 5-5z"/>
                        <path d="M2 21a10 10 0 0 1 20 0"/>
                        <circle cx="19" cy="4" r="2" fill="#2563EB" stroke="#2563EB"/>
                    </svg>
                </div>
                <div class="message-body">
                    <div class="message-bubble assistant-bubble">
                        <div class="message-content">${_renderMarkdown(msg.content)}</div>
                        ${sourcesHtml}
                        <div class="message-meta">
                            <span class="message-time">${_formatTime(msg.timestamp)}</span>
                            ${msg.processingTimeMs ? `<span class="message-timing">${(msg.processingTimeMs / 1000).toFixed(1)}s</span>` : ''}
                        </div>
                    </div>
                    <div class="message-actions${feedbackClass}">
                        <button class="action-btn copy-btn" title="Copy response" aria-label="Copy response"
                                data-message-id="${msg.id}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                            </svg>
                            <span>Copy</span>
                        </button>
                        <button class="action-btn helpful-btn ${msg.feedback === 'helpful' ? 'active' : ''}"
                                title="Helpful" aria-label="Mark as helpful" data-message-id="${msg.id}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="${msg.feedback === 'helpful' ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z"/>
                                <path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                            </svg>
                        </button>
                        <button class="action-btn not-helpful-btn ${msg.feedback === 'not_helpful' ? 'active' : ''}"
                                title="Not helpful" aria-label="Mark as not helpful" data-message-id="${msg.id}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="${msg.feedback === 'not_helpful' ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3H10z"/>
                                <path d="M17 2h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"/>
                            </svg>
                        </button>
                        <button class="action-btn regenerate-btn" title="Regenerate response"
                                aria-label="Regenerate response" data-message-id="${msg.id}">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="23 4 23 10 17 10"/>
                                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                            </svg>
                            <span>Retry</span>
                        </button>
                    </div>
                </div>
            `;
        } else if (msg.role === 'error') {
            div.innerHTML = `
                <div class="message-avatar error-avatar" aria-hidden="true">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                </div>
                <div class="message-body">
                    <div class="message-bubble error-bubble">
                        <div class="message-content">${_escapeHtml(msg.content)}</div>
                        <button class="retry-btn" aria-label="Retry">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="23 4 23 10 17 10"/>
                                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                            </svg>
                            Retry
                        </button>
                    </div>
                </div>
            `;
        }

        return div;
    }

    /**
     * Render RAG source citations.
     */
    function _renderSources(sources) {
        if (!sources || sources.length === 0) return '';

        const sourceItems = sources.map((s, i) => {
            const relevancePct = Math.round(s.relevance * 100);
            const contentPreview = s.content.length > 150
                ? s.content.substring(0, 150) + '…'
                : s.content;

            return `
                <div class="source-item">
                    <div class="source-header">
                        <svg class="source-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                            <line x1="16" y1="13" x2="8" y2="13"/>
                            <line x1="16" y1="17" x2="8" y2="17"/>
                        </svg>
                        <span class="source-title">${_escapeHtml(s.title)}</span>
                        ${relevancePct > 0 ? `<span class="source-relevance">${relevancePct}% match</span>` : ''}
                    </div>
                    <p class="source-content">${_escapeHtml(contentPreview)}</p>
                </div>
            `;
        }).join('');

        return `
            <div class="sources-panel">
                <button class="sources-toggle" aria-expanded="false" aria-controls="sources-list">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    <span>Sources & References (${sources.length})</span>
                    <svg class="chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"/>
                    </svg>
                </button>
                <div class="sources-list collapsed">
                    ${sourceItems}
                </div>
            </div>
        `;
    }

    /**
     * Append a single message to the chat.
     */
    function appendMessage(msg) {
        if (!$els.messageContainer) return;
        const el = _createMessageElement(msg);
        el.classList.add('message-enter');
        $els.messageContainer.appendChild(el);

        // Trigger animation
        requestAnimationFrame(() => {
            el.classList.add('message-enter-active');
        });
    }

    /**
     * Render all messages (for switching conversations).
     */
    function renderAllMessages(messages) {
        if (!$els.messageContainer) return;
        $els.messageContainer.innerHTML = '';
        messages.forEach(msg => {
            const el = _createMessageElement(msg);
            $els.messageContainer.appendChild(el);
        });
        scrollToBottom(false);
    }


    // ── Typing indicator ──────────────────────────────────────────────────
    function showTypingIndicator() {
        if ($els.typingIndicator) {
            $els.typingIndicator.classList.remove('hidden');
            scrollToBottom();
        }
    }

    function hideTypingIndicator() {
        if ($els.typingIndicator) {
            $els.typingIndicator.classList.add('hidden');
        }
    }


    // ── Chat input ────────────────────────────────────────────────────────
    function clearInput() {
        if ($els.chatInput) {
            $els.chatInput.value = '';
            _resizeTextarea();
            _updateCharCounter();
            _updateSendButton();
        }
    }

    function updateChatInput(isProcessing) {
        if ($els.chatInput) {
            $els.chatInput.disabled = isProcessing;
            if (!isProcessing) $els.chatInput.focus();
        }
        _updateSendButton();
    }

    function _resizeTextarea() {
        const ta = $els.chatInput;
        if (!ta) return;
        ta.style.height = 'auto';
        ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
    }

    function _updateCharCounter() {
        if (!$els.charCounter || !$els.chatInput) return;
        const len = $els.chatInput.value.length;
        if (len > CONFIG.MAX_MESSAGE_LENGTH * 0.8) {
            $els.charCounter.textContent = `${len}/${CONFIG.MAX_MESSAGE_LENGTH}`;
            $els.charCounter.classList.add('visible');
            if (len > CONFIG.MAX_MESSAGE_LENGTH) {
                $els.charCounter.classList.add('over-limit');
            } else {
                $els.charCounter.classList.remove('over-limit');
            }
        } else {
            $els.charCounter.classList.remove('visible');
            $els.charCounter.classList.remove('over-limit');
        }
    }

    function _updateSendButton() {
        if (!$els.sendBtn || !$els.chatInput) return;
        const hasText = $els.chatInput.value.trim().length > 0;
        const isDisabled = !hasText || $els.chatInput.disabled;
        $els.sendBtn.disabled = isDisabled;
        $els.sendBtn.classList.toggle('active', hasText && !$els.chatInput.disabled);
    }


    // ── Scroll management ─────────────────────────────────────────────────
    function scrollToBottom(smooth = true) {
        if (!$els.messageContainer) return;
        const container = $els.messageContainer.closest('.chat-messages') || $els.messageContainer;
        requestAnimationFrame(() => {
            container.scrollTo({
                top: container.scrollHeight,
                behavior: smooth ? 'smooth' : 'instant',
            });
        });
    }


    // ── Toast notifications ───────────────────────────────────────────────
    function showToast(message, type = 'info') {
        if (!$els.toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ',
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <span class="toast-message">${_escapeHtml(message)}</span>
            <button class="toast-close" aria-label="Close notification">&times;</button>
        `;

        $els.toastContainer.appendChild(toast);

        // Trigger animation
        requestAnimationFrame(() => toast.classList.add('toast-visible'));

        // Close handler
        const closeBtn = toast.querySelector('.toast-close');
        const dismiss = () => {
            toast.classList.remove('toast-visible');
            toast.addEventListener('transitionend', () => toast.remove(), { once: true });
            setTimeout(() => toast.remove(), 500); // Fallback
        };
        closeBtn.addEventListener('click', dismiss);

        // Auto-dismiss
        setTimeout(dismiss, CONFIG.TOAST_DURATION_MS);
    }


    // ── Sidebar ───────────────────────────────────────────────────────────
    function _toggleSidebar() {
        const isOpen = $els.sidebar.classList.contains('sidebar-open');
        if (isOpen) {
            _closeSidebarMobile();
        } else {
            $els.sidebar.classList.add('sidebar-open');
            $els.sidebarOverlay.classList.add('overlay-visible');
            document.body.classList.add('sidebar-active');
        }
    }

    function _closeSidebarMobile() {
        $els.sidebar.classList.remove('sidebar-open');
        $els.sidebarOverlay.classList.remove('overlay-visible');
        document.body.classList.remove('sidebar-active');
    }


    // ── Conversation history panel ────────────────────────────────────────
    function renderConversationHistory(conversations, activeId) {
        if (!$els.conversationList) return;

        if (conversations.length === 0) {
            $els.conversationList.innerHTML = `
                <div class="empty-conversations">
                    <p>No conversations yet</p>
                    <p class="empty-sub">Start a conversation with your AI HR Assistant.</p>
                </div>
            `;
            return;
        }

        // Group conversations by date
        const groups = {};
        conversations.forEach(c => {
            const dateLabel = _formatDate(c.updatedAt || c.createdAt);
            if (!groups[dateLabel]) groups[dateLabel] = [];
            groups[dateLabel].push(c);
        });

        let html = '';
        for (const [label, convs] of Object.entries(groups)) {
            html += `<div class="conversation-group-label">${_escapeHtml(label)}</div>`;
            convs.forEach(c => {
                const isActive = c.id === activeId;
                html += `
                    <div class="conversation-item ${isActive ? 'active' : ''}" data-conversation-id="${c.id}">
                        <button class="conversation-link" aria-label="Open conversation: ${_escapeHtml(c.title)}">
                            <svg class="conv-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                            </svg>
                            <span class="conv-title">${_escapeHtml(c.title)}</span>
                        </button>
                        <div class="conversation-actions">
                            <button class="conv-action-btn conv-rename-btn" title="Rename" aria-label="Rename conversation"
                                    data-conversation-id="${c.id}">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                                </svg>
                            </button>
                            <button class="conv-action-btn conv-delete-btn" title="Delete" aria-label="Delete conversation"
                                    data-conversation-id="${c.id}">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="3 6 5 6 21 6"/>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                `;
            });
        }

        $els.conversationList.innerHTML = html;
    }


    // ── Status indicator ──────────────────────────────────────────────────
    function updateStatusIndicator(isOnline) {
        if ($els.statusDot) {
            $els.statusDot.className = `status-dot ${isOnline ? 'online' : 'offline'}`;
        }
        if ($els.statusText) {
            $els.statusText.textContent = isOnline ? 'HR Knowledge Base Online' : 'Connecting…';
        }
    }


    // ── Profile menu ──────────────────────────────────────────────────────
    function _toggleProfileMenu() {
        if (!$els.profileMenu) return;
        const isOpen = $els.profileMenu.classList.contains('visible');
        $els.profileMenu.classList.toggle('visible', !isOpen);
    }


    // ── Event binding ─────────────────────────────────────────────────────
    function _bindEvents() {
        // Sidebar toggle
        $els.hamburgerBtn?.addEventListener('click', _toggleSidebar);
        $els.closeSidebarBtn?.addEventListener('click', _closeSidebarMobile);
        $els.sidebarOverlay?.addEventListener('click', _closeSidebarMobile);

        // New conversation
        $els.newConversationBtn?.addEventListener('click', () => {
            _closeSidebarMobile();
            Chatbot.newConversation();
        });

        // Chat input — auto-resize and send
        if ($els.chatInput) {
            $els.chatInput.addEventListener('input', () => {
                _resizeTextarea();
                _updateCharCounter();
                _updateSendButton();
            });

            $els.chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    const text = $els.chatInput.value.trim();
                    if (text && !Chatbot.isProcessing) {
                        Chatbot.sendMessage(text);
                    }
                }
            });
        }

        // Send button
        $els.sendBtn?.addEventListener('click', () => {
            const text = $els.chatInput?.value.trim();
            if (text && !Chatbot.isProcessing) {
                Chatbot.sendMessage(text);
            }
        });

        // Conversation list — event delegation
        $els.conversationList?.addEventListener('click', (e) => {
            // Switch conversation
            const link = e.target.closest('.conversation-link');
            if (link) {
                const item = link.closest('.conversation-item');
                if (item) {
                    _closeSidebarMobile();
                    Chatbot.switchConversation(item.dataset.conversationId);
                }
                return;
            }

            // Rename
            const renameBtn = e.target.closest('.conv-rename-btn');
            if (renameBtn) {
                e.stopPropagation();
                const convId = renameBtn.dataset.conversationId;
                const newTitle = prompt('Rename conversation:');
                if (newTitle && newTitle.trim()) {
                    Chatbot.renameConversation(convId, newTitle.trim());
                }
                return;
            }

            // Delete
            const deleteBtn = e.target.closest('.conv-delete-btn');
            if (deleteBtn) {
                e.stopPropagation();
                const convId = deleteBtn.dataset.conversationId;
                if (confirm('Delete this conversation?')) {
                    Chatbot.deleteConversation(convId);
                }
                return;
            }
        });

        // Message actions — event delegation on message container
        $els.messageContainer?.addEventListener('click', (e) => {
            // Copy
            const copyBtn = e.target.closest('.copy-btn');
            if (copyBtn) {
                const msgId = copyBtn.dataset.messageId;
                const msgEl = document.getElementById(`message-${msgId}`);
                if (msgEl) {
                    const content = msgEl.querySelector('.message-content')?.textContent || '';
                    navigator.clipboard.writeText(content).then(() => {
                        showToast('Response copied to clipboard', 'success');
                    }).catch(() => {
                        showToast('Failed to copy', 'error');
                    });
                }
                return;
            }

            // Helpful
            const helpfulBtn = e.target.closest('.helpful-btn');
            if (helpfulBtn) {
                const msgId = helpfulBtn.dataset.messageId;
                Chatbot.recordFeedback(msgId, 'helpful');
                // Update UI
                const actions = helpfulBtn.closest('.message-actions');
                if (actions) {
                    actions.classList.add('feedback-helpful');
                    actions.classList.remove('feedback-not_helpful');
                }
                helpfulBtn.classList.add('active');
                helpfulBtn.querySelector('svg')?.setAttribute('fill', 'currentColor');
                const notBtn = actions?.querySelector('.not-helpful-btn');
                notBtn?.classList.remove('active');
                notBtn?.querySelector('svg')?.setAttribute('fill', 'none');
                return;
            }

            // Not helpful
            const notHelpfulBtn = e.target.closest('.not-helpful-btn');
            if (notHelpfulBtn) {
                const msgId = notHelpfulBtn.dataset.messageId;
                Chatbot.recordFeedback(msgId, 'not_helpful');
                const actions = notHelpfulBtn.closest('.message-actions');
                if (actions) {
                    actions.classList.add('feedback-not_helpful');
                    actions.classList.remove('feedback-helpful');
                }
                notHelpfulBtn.classList.add('active');
                notHelpfulBtn.querySelector('svg')?.setAttribute('fill', 'currentColor');
                const helpBtn = actions?.querySelector('.helpful-btn');
                helpBtn?.classList.remove('active');
                helpBtn?.querySelector('svg')?.setAttribute('fill', 'none');
                return;
            }

            // Regenerate
            const regenBtn = e.target.closest('.regenerate-btn');
            if (regenBtn) {
                Chatbot.regenerateLastResponse();
                return;
            }

            // Retry (error messages)
            const retryBtn = e.target.closest('.retry-btn');
            if (retryBtn) {
                Chatbot.regenerateLastResponse();
                return;
            }

            // Sources toggle
            const srcToggle = e.target.closest('.sources-toggle');
            if (srcToggle) {
                const panel = srcToggle.closest('.sources-panel');
                const list = panel?.querySelector('.sources-list');
                if (list) {
                    const isCollapsed = list.classList.contains('collapsed');
                    list.classList.toggle('collapsed', !isCollapsed);
                    srcToggle.setAttribute('aria-expanded', isCollapsed);
                    srcToggle.querySelector('.chevron')?.classList.toggle('chevron-open', isCollapsed);
                }
                return;
            }
        });

        // Profile menu
        $els.profileBtn?.addEventListener('click', (e) => {
            e.stopPropagation();
            _toggleProfileMenu();
        });

        // Close profile menu on outside click
        document.addEventListener('click', (e) => {
            if ($els.profileMenu?.classList.contains('visible') &&
                !$els.profileMenu.contains(e.target) &&
                !$els.profileBtn?.contains(e.target)) {
                $els.profileMenu.classList.remove('visible');
            }
        });

        // Escape key — close modals/sidebar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                _closeSidebarMobile();
                $els.profileMenu?.classList.remove('visible');
            }
        });

        // Window resize — close mobile sidebar on desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                _closeSidebarMobile();
            }
        });
    }


    // ── Initialization ────────────────────────────────────────────────────
    function init() {
        _cacheDom();
        _bindEvents();
        _renderQuickQuestions();
        _renderHRResources();
        _updateSendButton();

        // Initialize chatbot after UI is ready
        Chatbot.init();
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }


    // ── Public interface ──────────────────────────────────────────────────
    return Object.freeze({
        showWelcomeScreen,
        showChatScreen,
        appendMessage,
        renderAllMessages,
        showTypingIndicator,
        hideTypingIndicator,
        clearInput,
        updateChatInput,
        scrollToBottom,
        showToast,
        renderConversationHistory,
        updateStatusIndicator,
    });
})();
