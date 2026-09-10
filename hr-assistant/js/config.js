/**
 * config.js — HR Assistant Frontend Configuration
 * ================================================
 * Single source of truth for all configurable values.
 * Update API_BASE_URL to point to your running backend server.
 */

const CONFIG = (() => {
    'use strict';

    // ── Backend URL ───────────────────────────────────────────────────────
    // Change this to your deployed backend URL in production.
    const API_BASE_URL = 'http://localhost:8000';

    return Object.freeze({
        // API
        API_BASE_URL,
        ENDPOINTS: {
            CHAT:   `${API_BASE_URL}/api/chat`,
            HEALTH: `${API_BASE_URL}/api/health`,
        },

        // Request settings
        REQUEST_TIMEOUT_MS: 60000,       // 60 seconds (RAG + guardrails can be slow)
        MAX_MESSAGE_LENGTH: 2000,        // Max characters per message
        MIN_MESSAGE_LENGTH: 1,

        // UI settings
        ANIMATION_DURATION_MS: 250,
        TOAST_DURATION_MS: 4000,
        TYPING_INDICATOR_DELAY_MS: 300,  // Delay before showing typing indicator
        MAX_CONVERSATION_TITLE_LENGTH: 50,
        MAX_CONVERSATIONS_STORED: 50,    // Limit for localStorage

        // Local Storage keys
        STORAGE_KEYS: {
            CONVERSATIONS: 'hr_assistant_conversations',
            ACTIVE_CONVERSATION: 'hr_assistant_active_conversation',
            USER_PREFERENCES: 'hr_assistant_preferences',
        },

        // Quick suggestion cards displayed on the welcome screen
        QUICK_QUESTIONS: [
            {
                icon: '🏖️',
                category: 'Leave & Time Off',
                question: 'How many paid leaves can I take each year?',
            },
            {
                icon: '❤️',
                category: 'Benefits',
                question: 'What health benefits are available to employees?',
            },
            {
                icon: '🏠',
                category: 'Workplace Policy',
                question: 'What is the company\'s remote work policy?',
            },
            {
                icon: '👋',
                category: 'Onboarding',
                question: 'What documents are required for onboarding?',
            },
            {
                icon: '💰',
                category: 'Payroll',
                question: 'When is the monthly salary processed?',
            },
            {
                icon: '⏰',
                category: 'Attendance',
                question: 'What are the working hour policies?',
            },
        ],

        // HR resource categories for the sidebar
        HR_RESOURCES: [
            { icon: '📘', label: 'Employee Handbook', query: 'What does the employee handbook cover?' },
            { icon: '🏖️', label: 'Leave & Attendance', query: 'Tell me about the leave and attendance policy.' },
            { icon: '❤️', label: 'Benefits', query: 'What employee benefits are available?' },
            { icon: '📋', label: 'Workplace Policies', query: 'What are the main workplace policies?' },
            { icon: '👋', label: 'Onboarding', query: 'What is the onboarding process for new employees?' },
            { icon: '💰', label: 'Payroll & Compensation', query: 'How does the payroll and compensation work?' },
            { icon: '⚖️', label: 'Compliance', query: 'What are the company compliance policies?' },
        ],

        // User profile placeholder (would come from auth in production)
        USER: {
            name: 'Employee',
            role: 'Team Member',
            avatar: null,
        },
    });
})();
