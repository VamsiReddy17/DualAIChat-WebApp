import React from 'react';

interface DualAILogoProps {
    size?: number;
    className?: string;
}

export const DualAILogo: React.FC<DualAILogoProps> = ({ size = 32, className }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
        aria-label="Dual AI Chat logo"
    >
        <defs>
            {/* Gradient for the blue bubble */}
            <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#60A5FA" />
                <stop offset="100%" stopColor="#3B82F6" />
            </linearGradient>
            {/* Gradient for the violet bubble */}
            <linearGradient id="violetGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#A78BFA" />
                <stop offset="100%" stopColor="#7C3AED" />
            </linearGradient>
            {/* Blend gradient for the overlap */}
            <linearGradient id="blendGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#818CF8" />
                <stop offset="100%" stopColor="#6D28D9" />
            </linearGradient>
            {/* Glow filter */}
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="1.5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>

        {/* Background circle (subtle) */}
        <circle cx="24" cy="24" r="23" fill="url(#blueGrad)" opacity="0.08" />

        {/* Blue chat bubble (left, behind) */}
        <g filter="url(#glow)">
            <path
                d="M6 10C6 7.79 7.79 6 10 6H26C28.21 6 30 7.79 30 10V24C30 26.21 28.21 28 26 28H14L8 33V28H10C7.79 28 6 26.21 6 24V10Z"
                fill="url(#blueGrad)"
                opacity="0.9"
            />
            {/* Neural dots on blue bubble */}
            <circle cx="13" cy="14" r="1.2" fill="white" opacity="0.7" />
            <circle cx="19" cy="11" r="1" fill="white" opacity="0.5" />
            <circle cx="23" cy="16" r="1.2" fill="white" opacity="0.7" />
            <circle cx="16" cy="19" r="1" fill="white" opacity="0.5" />
            {/* Connection lines */}
            <line x1="13" y1="14" x2="19" y2="11" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="19" y1="11" x2="23" y2="16" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="13" y1="14" x2="16" y2="19" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="23" y1="16" x2="16" y2="19" stroke="white" strokeWidth="0.5" opacity="0.35" />
        </g>

        {/* Violet chat bubble (right, in front) */}
        <g filter="url(#glow)">
            <path
                d="M18 18C18 15.79 19.79 14 22 14H38C40.21 14 42 15.79 42 18V32C42 34.21 40.21 36 38 36H36V41L30 36H22C19.79 36 18 34.21 18 32V18Z"
                fill="url(#violetGrad)"
                opacity="0.9"
            />
            {/* Neural dots on violet bubble */}
            <circle cx="26" cy="22" r="1.2" fill="white" opacity="0.7" />
            <circle cx="32" cy="19" r="1" fill="white" opacity="0.5" />
            <circle cx="36" cy="24" r="1.2" fill="white" opacity="0.7" />
            <circle cx="29" cy="27" r="1" fill="white" opacity="0.5" />
            <circle cx="34" cy="30" r="1" fill="white" opacity="0.5" />
            {/* Connection lines */}
            <line x1="26" y1="22" x2="32" y2="19" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="32" y1="19" x2="36" y2="24" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="26" y1="22" x2="29" y2="27" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="36" y1="24" x2="34" y2="30" stroke="white" strokeWidth="0.5" opacity="0.35" />
            <line x1="29" y1="27" x2="34" y2="30" stroke="white" strokeWidth="0.5" opacity="0.35" />
        </g>

        {/* Overlap glow accent */}
        <rect x="18" y="14" width="12" height="14" rx="3" fill="url(#blendGrad)" opacity="0.25" />

        {/* Center spark — the "dual" connection point */}
        <circle cx="24" cy="22" r="2" fill="white" opacity="0.9" />
        <circle cx="24" cy="22" r="3.5" fill="white" opacity="0.15" />
    </svg>
);
