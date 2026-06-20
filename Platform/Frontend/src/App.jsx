import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import * as faceapi from 'face-api.js';

// ==========================================
// CUSTOM ICONS (SVG inline)
// ==========================================
const Icon = ({ size = 24, className = "", children }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>{children}</svg>
);

const ArrowRight = (p) => <Icon {...p}><path d="M5 12h14M12 5l7 7-7 7"/></Icon>;
const Shield = (p) => <Icon {...p}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></Icon>;
const Sparkles = (p) => <Icon {...p}><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1-1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></Icon>;
const User = (p) => <Icon {...p}><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></Icon>;
const Users = (p) => <Icon {...p}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></Icon>;
const MessageCircle = (p) => <Icon {...p}><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></Icon>;
const Clock = (p) => <Icon {...p}><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></Icon>;
const Activity = (p) => <Icon {...p}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></Icon>;
const TrendingDown = (p) => <Icon {...p}><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></Icon>;
const Brain = (p) => <Icon {...p}><path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v15a2.5 2.5 0 0 0 4.9 1 2.5 2.5 0 0 0 4.2 0 2.5 2.5 0 0 0 4.9-1v-15A2.5 2.5 0 0 0 18.5 2H9.5z"/><path d="M12 2v20"/></Icon>;
const Database = (p) => <Icon {...p}><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></Icon>;
const PhoneCall = (p) => <Icon {...p}><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></Icon>;
const Camera = (p) => <Icon {...p}><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></Icon>;
const CameraOff = (p) => <Icon {...p}><line x1="2" y1="2" x2="22" y2="22"/><path d="M10.41 4H14l2.5 3h3.5a2 2 0 0 1 2 2v9m-1.55 2.45c-.44.34-1 .55-1.56.55H4a2 2 0 0 1-2-2V9c0-.55.2-1.05.55-1.5M10.5 10.5a3 3 0 0 0 4 4"/></Icon>;
const Settings = (p) => <Icon {...p}><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></Icon>;

// Patient Dashboard Icons
const BookOpen = (p) => <Icon {...p}><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></Icon>;
const TrendingUp = (p) => <Icon {...p}><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></Icon>;
const Mic = (p) => <Icon {...p}><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></Icon>;
const Send = (p) => <Icon {...p}><line x1="22" x2="11" y1="2" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></Icon>;
const Star = (p) => <Icon {...p}><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></Icon>;
const MapPin = (p) => <Icon {...p}><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></Icon>;
const Gift = (p) => <Icon {...p}><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" x2="12" y1="22" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></Icon>;
const Search = (p) => <Icon {...p}><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/></Icon>;
const Bell = (p) => <Icon {...p}><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></Icon>;
const AlertTriangle = (p) => <Icon {...p}><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></Icon>;
const Volume2 = (p) => <Icon {...p}><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></Icon>;
const VolumeX = (p) => <Icon {...p}><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></Icon>;
const PieChart = (p) => <Icon {...p}><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></Icon>;
const Smile = (p) => <Icon {...p}><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></Icon>;
const Frown = (p) => <Icon {...p}><circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></Icon>;
const Meh = (p) => <Icon {...p}><circle cx="12" cy="12" r="10"/><line x1="8" y1="15" x2="16" y2="15"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></Icon>;

const Heart = (p) => <Icon {...p}><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></Icon>;
const HeartPulse = (p) => <Icon {...p}><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M22 12h-4l-3 5-3-10-3 8-2-3H2"/></Icon>;
const Target = (p) => <Icon {...p}><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></Icon>;
const Zap = (p) => <Icon {...p}><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></Icon>;

const theme = {
  bg: 'bg-[#F2F9F6]/25 backdrop-blur-md', 
  textMain: 'text-[#2C5555]',
  textDark: 'text-slate-800',
  outset: 'glass-card rounded-[2rem]',
  outsetHover: 'glass-card-hover',
  btnTeal: 'bg-gradient-to-r from-[#3A7070] to-[#2C5555] text-white shadow-[0_10px_20px_rgba(58,112,112,0.25)] hover:shadow-[0_15px_30px_rgba(58,112,112,0.35)] hover:-translate-y-0.5 transition-all border border-white/20',
  btnOutline: 'border border-[#3A7070]/25 text-[#3A7070] shadow-[0_10px_20px_rgba(58,112,112,0.03)] hover:border-[#3A7070]/40 hover:shadow-[0_15px_30px_rgba(58,112,112,0.08)] hover:-translate-y-0.5 transition-all bg-white/45 backdrop-blur-sm'
};
const KeffiLogo = ({ size = "w-10 h-10", onClick }) => (
  <div onClick={onClick} className={`${size} relative flex items-center justify-center cursor-pointer group`}>
    <div className="absolute inset-0 bg-[#3A7070] rounded-xl blur-[6px] group-hover:blur-[8px] transition-all opacity-30"></div>
    <div className={`absolute inset-0 bg-transparent rounded-xl flex items-center justify-center z-10`}>
      <Star size={size === "w-10 h-10" ? 28 : 36} className="text-[#3A7070] fill-[#3A7070]" />
    </div>
  </div>
);

const DynamicLoginIllustration = ({ step, className }) => {
  return (
    <svg viewBox="0 0 400 400" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <style>
        {`
          @keyframes scan-line {
            0%, 100% { transform: translateY(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            50% { transform: translateY(60px); }
          }
        `}
      </style>
      
      {/* Universal Background for all steps */}
      <circle cx="200" cy="200" r="180" fill="#E6F0F0" opacity="0.6" />
      <circle cx="200" cy="200" r="130" fill="white" opacity="0.8" />
      <ellipse cx="200" cy="340" rx="90" ry="12" fill="#3A7070" opacity="0.2" className="animate-pulse" />

      {step === 1 && (
        <g className="animate-bounce" style={{ animationDuration: '3s' }}>
          {/* Step 1: Secure Identity & Trust (Glowing Keyhole Shield) */}
          <path d="M200 60 L280 90 V180 C280 250 200 310 200 330 C200 310 120 250 120 180 V90 L200 60 Z" fill="white" stroke="#3A7070" strokeWidth="8" strokeLinejoin="round" />
          <path d="M200 80 L260 100 V180 C260 230 200 280 200 295 C200 280 140 230 140 180 V100 L200 80 Z" fill="#F2F9F6" />
          
          {/* Keyhole */}
          <circle cx="200" cy="180" r="18" fill="#F43F5E" className="animate-pulse" />
          <path d="M192 190 L188 220 H212 L208 190 Z" fill="#F43F5E" className="animate-pulse" />
          
          {/* Trust Network Nodes */}
          <circle cx="200" cy="220" r="80" fill="none" stroke="#8FA989" strokeWidth="2" strokeDasharray="8 8" className="animate-spin" style={{animationDuration: '10s'}} />
          <circle cx="100" cy="120" r="6" fill="#D4A373" className="animate-ping" />
          <circle cx="300" cy="250" r="5" fill="#8FA989" />
          <circle cx="130" cy="280" r="4" fill="#3A7070" />
        </g>
      )}

      {step === 2 && (
        <g className="animate-bounce" style={{ animationDuration: '3s' }}>
          {/* Step 2: OTP Verification Scanner */}
          <rect x="130" y="100" width="140" height="220" rx="20" fill="#2C5555" stroke="#3A7070" strokeWidth="6" />
          <rect x="140" y="110" width="120" height="200" rx="12" fill="#F2F9F6" />
          
          {/* Phone Screen Elements */}
          <rect x="175" y="120" width="50" height="6" rx="3" fill="#8FA989" opacity="0.5" />
          
          <circle cx="200" cy="180" r="22" fill="white" stroke="#3A7070" strokeWidth="4" />
          <path d="M190 175 V165 C190 155 210 155 210 165 V175" stroke="#8FA989" strokeWidth="4" strokeLinecap="round" />
          <circle cx="200" cy="183" r="4" fill="#F43F5E" />
          
          <rect x="160" y="225" width="80" height="8" rx="4" fill="#E6F0F0" />
          <rect x="160" y="240" width="60" height="8" rx="4" fill="#E6F0F0" />
          <rect x="160" y="260" width="80" height="18" rx="9" fill="#3A7070" />
          
          {/* Scanning Laser Line */}
          <line x1="130" y1="160" x2="270" y2="160" stroke="#F43F5E" strokeWidth="2" opacity="0" style={{animation: 'scan-line 3s infinite ease-in-out'}} />
          <polygon points="130,160 270,160 250,180 150,180" fill="#F43F5E" opacity="0.08" style={{animation: 'scan-line 3s infinite ease-in-out'}} />

          {/* Floating OTP Bubble */}
          <g className="animate-pulse" style={{ animationDuration: '2s' }}>
            <path d="M250 120 C250 100 270 90 290 90 C310 90 320 100 320 120 C320 140 310 150 290 150 L270 160 L275 145 C260 140 250 130 250 120 Z" fill="#D4A373" />
            <circle cx="275" cy="120" r="3" fill="white" />
            <circle cx="285" cy="120" r="3" fill="white" />
            <circle cx="295" cy="120" r="3" fill="white" />
          </g>

          <ellipse cx="200" cy="210" rx="100" ry="20" fill="none" stroke="#8FA989" strokeWidth="3" opacity="0.6" strokeDasharray="10 10" transform="rotate(-15 200 210)" />
          
          <circle cx="100" cy="140" r="5" fill="#8FA989" className="animate-pulse" />
          <circle cx="300" cy="230" r="4" fill="#D4A373" className="animate-ping" />
        </g>
      )}

      {step === 3 && (
        <g className="animate-bounce" style={{ animationDuration: '3s' }}>
          {/* Step 3: Natural Sanctuary (Geometric Character under Leaf) */}
          <path d="M200 50 C320 50 360 150 280 230 C200 310 80 310 40 230 C0 150 80 50 200 50 Z" fill="#8FA989" opacity="0.2" />
          <path d="M200 80 C270 80 290 150 240 200 C190 250 110 250 90 200 C70 150 130 80 200 80 Z" fill="#3A7070" opacity="0.1" />

          <circle cx="160" cy="150" r="28" fill="#3A7070" />
          <path d="M160 185 C185 185 205 205 205 240 L205 290 L115 290 L115 240 C115 205 135 185 160 185 Z" fill="#2C5555" />
          <path d="M110 275 C70 275 60 305 90 315 L230 315 C260 305 250 275 210 275 Z" fill="#3A7070" />
          
          <path d="M210 205 L260 190 L285 215 L235 230 Z" fill="#D4A373" className="animate-pulse" />
          <path d="M210 200 L260 185 L285 210 L235 225 Z" fill="white" />
          
          <path d="M250 160 C235 160 220 145 220 130 C220 115 235 100 250 115 C265 100 280 115 280 130 C280 145 265 160 250 160 Z" fill="#F43F5E" className="animate-bounce" style={{animationDuration: '2s'}} />
          
          <circle cx="310" cy="130" r="6" fill="#D4A373" className="animate-ping" />
          <circle cx="90" cy="110" r="5" fill="#8FA989" className="animate-pulse" />
          <circle cx="270" cy="250" r="4" fill="#D4A373" />
        </g>
      )}
    </svg>
  );
};

// ==========================================
// 1. ULTIMATE LANDING PAGE (Level 3 Design)
// ==========================================
const LandingPage = ({ setView }) => {


  return (
    <>
    <div className="min-h-screen bg-transparent overflow-x-hidden text-[#1E293B] font-inter selection:bg-[#3A7070] selection:text-white relative">
      
      <div className="floating-blob w-[600px] h-[600px] bg-[#8FA989] top-[-100px] right-[-200px]"></div>
      <div className="floating-blob w-[800px] h-[800px] bg-[#E6F0F0] top-[800px] left-[-400px]"></div>
      <div className="floating-blob w-[600px] h-[600px] bg-[#3A7070] opacity-10 top-[2200px] right-[-200px]" style={{animationDelay: '2s'}}></div>

      {/* 🚀 HEADER */}
      <div className="sticky top-4 z-[100] w-full max-w-[1200px] mx-auto px-4">
        <nav className="w-full px-6 py-4 flex justify-between items-center rounded-2xl glass-nav backdrop-blur-md">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setView('landing')}>
            <KeffiLogo size="w-10 h-10" />
            <span className="text-2xl font-poppins font-bold text-[#2C5555] tracking-tight">Keffi AI</span>
          </div>
          
          <div className="hidden lg:flex items-center gap-10 font-inter text-[15px] font-semibold text-slate-600">
            <button onClick={() => setView('landing')} className="text-slate-900 font-bold transition-colors cursor-pointer">Home</button>
            <button onClick={() => {document.getElementById('story').scrollIntoView({behavior: 'smooth'})}} className="hover:text-[#3A7070] transition-colors cursor-pointer">Our Story</button>
            <button onClick={() => setView('login-admin')} className="hover:text-[#3A7070] transition-colors cursor-pointer">Clinical Hub</button>
            <button onClick={() => setView('login-patient')} className="hover:text-[#3A7070] transition-colors cursor-pointer">Sanctuary</button>
          </div>

          <div className="flex items-center gap-6">
            <button onClick={() => setView('login-patient')} className="hidden md:block font-inter text-[15px] font-semibold text-slate-600 hover:text-[#3A7070] transition-colors cursor-pointer">
              Log in
            </button>
            <button onClick={() => setView('login-patient')} className="px-6 py-2.5 rounded-xl bg-[#3A7070] text-white font-inter font-bold text-[15px] shadow-md shadow-[#3A7070]/20 hover:bg-[#2C5555] hover:scale-105 transition-all cursor-pointer">
              Get Started
            </button>
          </div>
        </nav>
      </div>

      <main className="relative z-10 w-full">
        
        {/* 🚀 SECTION 1: THE HERO (Gradient Layout) */}
        <section className="w-full min-h-[90vh] flex items-center relative overflow-hidden pt-24 pb-12">
          {/* Soft Blue/Green Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#E6F0F0]/40 via-white/40 to-[#E8F4F8]/40 backdrop-blur-md z-0"></div>
          <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-[#3A7070]/5 rounded-full blur-[100px] z-0"></div>
          <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-blue-500/5 rounded-full blur-[100px] z-0"></div>

          <div className="max-w-[1200px] mx-auto px-4 lg:px-12 flex flex-row items-center justify-between gap-2 md:gap-12 lg:gap-20 relative z-10 w-full">
            <div className="flex flex-col items-start text-left w-[60%] md:flex-1 z-20">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 md:px-4 md:py-2 rounded-full glass-card border border-white/30 text-[#3A7070] font-bold text-[10px] md:text-sm mb-4 shadow-sm">
                <Sparkles size={16} className="text-[#3A7070]" /> Keffi is an Emotion Engine
              </div>
              <h1 className="font-poppins font-black text-2xl md:text-5xl lg:text-6xl text-slate-900 mb-4 md:mb-6 leading-tight md:leading-[1.1]">
                Bridging the <br className="block md:hidden" /><span className="cursive-accent text-transparent bg-clip-text bg-gradient-to-r from-[#3A7070] to-blue-600">Invisible Gap</span> <br className="hidden md:block"/>in Mental Healthcare.
              </h1>
              
              <p className="font-inter text-xs md:text-lg text-slate-600 leading-relaxed md:leading-relaxed max-w-lg mb-6 font-medium">
                Keffi is your Emotionally Intelligent AI Companion. While traditional therapy supports you for one hour a week, Keffi bridges the 167-hour gap. It deeply understands 96 emotional states, safely remembers your journey, and delivers personalized, human-like therapeutic support exactly when you need it. A safe sanctuary where advanced AI meets profound empathy.
              </p>
              
              <div className="flex flex-col sm:flex-row items-start gap-3 w-full sm:w-auto mt-2">
                <button onClick={() => setView('login-patient')} className="group relative w-full sm:w-auto px-6 py-3 md:px-10 md:py-5 rounded-xl md:rounded-2xl bg-gradient-to-r from-[#3A7070] to-[#2C5555] text-white font-inter font-bold text-xs md:text-lg shadow-[0_10px_20px_rgba(58,112,112,0.25)] md:shadow-[0_20px_40px_rgba(58,112,112,0.35)] hover:-translate-y-0.5 transition-all overflow-hidden flex items-center justify-center gap-2 md:gap-3 cursor-pointer">
                  <div className="absolute inset-0 bg-white/20 blur-md transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-out"></div>
                  🌟 <span className="hidden md:inline">Enter Keffi Chat</span><span className="inline md:hidden">Chat</span> <ArrowRight size={16} className="transform group-hover:translate-x-1 transition-transform"/>
                </button>
                <button onClick={() => setView('login-admin')} className="group relative w-full sm:w-auto px-6 py-3 md:px-10 md:py-5 rounded-xl md:rounded-2xl bg-white/40 backdrop-blur-sm border border-white/30 text-[#3A7070] font-inter font-bold text-xs md:text-lg shadow-sm hover:shadow-md hover:border-[#3A7070]/30 hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2 md:gap-3 cursor-pointer">
                  🩺 <span className="hidden md:inline">Doctor / Clinical Hub</span><span className="inline md:hidden">Clinic</span>
                </button>
              </div>
            </div>
            
            <div className="flex justify-end relative w-[40%] md:flex-1 max-w-[600px] transform scale-[0.45] md:scale-100 origin-right md:origin-center z-10">
               <div className="relative w-80 h-80 flex items-center justify-center">
                  <div className="absolute inset-0 bg-[#3A7070] rounded-full blur-[80px] opacity-25 animate-pulse"></div>
                  <div className="absolute inset-4 bg-emerald-400 rounded-full blur-[40px] opacity-15"></div>
                  
                  <div className="relative z-10 w-56 h-56 rounded-full bg-white/20 backdrop-blur-md shadow-[inset_-10px_-10px_20px_rgba(255,255,255,0.2),_inset_10px_10px_20px_rgba(255,255,255,0.4),_0_20px_40px_rgba(58,112,112,0.2)] flex items-center justify-center border-[8px] border-white/50 group">
                     <div className="absolute inset-4 bg-[#3A7070] rounded-full blur-xl opacity-15 group-hover:opacity-30 transition-opacity duration-700"></div>
                     <Star size={96} className="text-[#3A7070] fill-[#3A7070] relative z-10 animate-[spin_12s_linear_infinite] drop-shadow-[0_15px_15px_rgba(58,112,112,0.4)]" />
                  </div>
                  
                  {/* Orbiting elements */}
                  <div className="absolute top-0 right-10 w-16 h-16 bg-white rounded-full shadow-xl flex items-center justify-center border border-emerald-100 text-emerald-500 transform hover:scale-110 transition-transform z-20"><Heart size={28} className="fill-emerald-100"/></div>
                  <div className="absolute bottom-10 left-0 w-20 h-20 bg-white rounded-full shadow-xl flex items-center justify-center border border-slate-100 text-[#3A7070] transform hover:scale-110 transition-transform z-20"><MessageCircle size={36} className="fill-slate-50"/></div>
               </div>
            </div>
          </div>
        </section>

        {/* 🚀 SECTION 2: THE PROBLEM (Story Zig-Zag) */}
        <section id="story" className="scroll-3d w-full py-32 bg-[#F2F9F6]/35 backdrop-blur-md border-y border-white/20 transition-all duration-75 ease-out">
          <div className="max-w-[1200px] mx-auto px-6 lg:px-12 flex flex-col lg:flex-row-reverse items-center gap-24 relative">
             <div className="absolute top-10 left-0 text-[300px] font-poppins font-bold text-slate-100 opacity-50 z-[-1] leading-none select-none">01</div>
            
             <div className="flex-1 flex justify-center lg:justify-start">
               <img src="https://illustrations.popsy.co/amber/surreal-hourglass.svg" alt="Hourglass Drawing" className="w-full max-w-[500px] drop-shadow-xl" />
             </div>

             <div className="flex-1 flex flex-col items-start text-left">
              <h2 className="h2-title font-poppins text-slate-900 mb-8">The Silent <span className="cursive-accent">Crisis</span> We Ignore.</h2>
              <div className="space-y-6">
                <p className="p-text">
                  Therapy typically happens for one hour a week. But emotional struggles don't follow a schedule. What happens during the remaining 167 hours? Patients are left alone to fight their anxiety, burnout, and depression in silence.
                </p>
                <p className="p-text">
                  Healing is incredibly hard, and it isn't linear. Due to stigma, high costs, and a lack of immediate support, nearly 60% of patients drop out of treatment before fully recovering. 
                </p>
                <p className="p-text">
                  When they drop out, relapses go completely undetected. Doctors have no proactive way to monitor these at-risk patients outside the clinic walls. This is the gap Keffi AI was built to close.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 🚀 NEW SECTION 3: HOW KEFFI WORKS (Timeline Layout) */}
        <section className="scroll-3d w-full py-32 bg-white/30 backdrop-blur-md border-y border-white/20 transition-all duration-75 ease-out">
           <div className="max-w-[1200px] mx-auto px-6 lg:px-12 text-center">
             <h2 className="h2-title font-poppins text-slate-900 mb-20">How Keffi Heals.</h2>
             
             <div className="relative flex flex-col items-center">
                {/* Vertical Line */}
                <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-1 bg-gradient-to-b from-[#3A7070]/20 via-[#8FA989]/20 to-transparent"></div>
                
                {/* Step 1 */}
                <div className="w-full flex justify-between items-center mb-24 relative">
                   <div className="w-[45%] text-right pr-10">
                     <h3 className="h3-title font-poppins text-slate-900 mb-3">1. You Express.</h3>
                     <p className="p-small">Enter the Sanctuary whenever anxiety hits. Type or speak your thoughts into Keffi exactly as you feel them, without fear of judgment.</p>
                   </div>
                   <div className="w-16 h-16 rounded-full bg-white border-4 border-[#3A7070] flex items-center justify-center text-[#3A7070] z-10 shadow-lg font-bold text-xl">1</div>
                   <div className="w-[45%] text-left pl-10 opacity-50"><MessageCircle size={64}/></div>
                </div>

                {/* Step 2 */}
                <div className="w-full flex justify-between items-center mb-24 relative">
                   <div className="w-[45%] text-right pr-10 opacity-50 flex justify-end"><Brain size={64}/></div>
                   <div className="w-16 h-16 rounded-full bg-[#3A7070] border-4 border-white flex items-center justify-center text-white z-10 shadow-lg font-bold text-xl">2</div>
                   <div className="w-[45%] text-left pl-10">
                     <h3 className="h3-title font-poppins text-slate-900 mb-3">2. Keffi Analyzes.</h3>
                     <p className="p-small">Behind the scenes, Keffi's BERT engine detects your exact emotional state across 96 fine-grained categories, pulling from your Pinecone memory history.</p>
                   </div>
                </div>

                {/* Step 3 */}
                <div className="w-full flex justify-between items-center relative">
                   <div className="w-[45%] text-right pr-10">
                     <h3 className="h3-title font-poppins text-slate-900 mb-3">3. Immediate Relief.</h3>
                     <p className="p-small">Keffi dynamically responds using 1 of 7 therapeutic modes—from guiding a breathing exercise to reframing negative thoughts using CBT principles.</p>
                   </div>
                   <div className="w-16 h-16 rounded-full bg-[#8FA989] border-4 border-white flex items-center justify-center text-white z-10 shadow-lg font-bold text-xl">3</div>
                   <div className="w-[45%] text-left pl-10 opacity-50"><Heart size={64}/></div>
                </div>
             </div>
           </div>
        </section>

        {/* 🚀 NEW SECTION 4: THE SCIENCE (Grid Layout) */}
        <section className="scroll-3d w-full py-32 bg-[#F2F9F6]/35 backdrop-blur-md border-y border-white/20 transition-all duration-75 ease-out">
          <div className="max-w-[1200px] mx-auto px-6 lg:px-12 flex flex-col lg:flex-row items-center gap-24 relative">
            <div className="absolute top-10 right-10 text-[300px] font-poppins font-bold text-slate-100 opacity-50 z-[-1] leading-none select-none">02</div>
            
            <div className="flex-1 grid grid-cols-2 gap-6 relative">
              <div className="absolute -inset-4 bg-gradient-to-tr from-[#3A7070]/10 to-[#8FA989]/10 rounded-[3rem] blur-xl z-[-1]"></div>
              <div className="glass-card glass-card-hover p-8 rounded-3xl flex flex-col gap-4 transform translate-y-8">
                <div className="w-12 h-12 bg-[#3A7070]/10 text-[#3A7070] rounded-full flex items-center justify-center"><Activity size={24}/></div>
                <h4 className="font-poppins font-bold text-lg text-slate-800">96-State BERT</h4>
                <p className="text-sm text-slate-500 font-medium">Not just "sad". Keffi detects complex states like Atypical Depression.</p>
              </div>
              <div className="glass-card glass-card-hover p-8 rounded-3xl flex flex-col gap-4">
                <div className="w-12 h-12 bg-amber-500/10 text-amber-600 rounded-full flex items-center justify-center"><Database size={24}/></div>
                <h4 className="font-poppins font-bold text-lg text-slate-800">Pinecone Memory</h4>
                <p className="text-sm text-slate-500 font-medium">Vector memory ensures Keffi never forgets your past triggers or progress.</p>
              </div>
              <div className="glass-card glass-card-hover p-8 rounded-3xl flex flex-col gap-4 transform translate-y-8">
                <div className="w-12 h-12 bg-emerald-500/10 text-emerald-600 rounded-full flex items-center justify-center"><Target size={24}/></div>
                <h4 className="font-poppins font-bold text-lg text-slate-800">Dynamic MHQ</h4>
                <p className="text-sm text-slate-500 font-medium">Silent, continuous evaluation of your Mental Health Quotient during chats.</p>
              </div>
              <div className="glass-card glass-card-hover p-8 rounded-3xl flex flex-col gap-4">
                <div className="w-12 h-12 bg-rose-500/10 text-rose-600 rounded-full flex items-center justify-center"><Zap size={24}/></div>
                <h4 className="font-poppins font-bold text-lg text-slate-800">7-Mode Engine</h4>
                <p className="text-sm text-slate-500 font-medium">Switches seamlessly between active listening, CBT reframing, and crisis mode.</p>
              </div>
            </div>

            <div className="flex-1 flex flex-col items-start text-left">
              <h2 className="h2-title font-poppins text-slate-900 mb-8">An Engine Built on <span className="cursive-accent">Empathy</span>.</h2>
              <div className="space-y-6">
                <p className="p-text">
                  Behind the calming interface lies a robust Triple-AI Architecture. We don't rely on simple prompts. Keffi is powered by a custom-trained clinical classification system that understands the deepest nuances of human emotion.
                </p>
                <p className="p-text">
                  By combining semantic search with real-time generative capabilities, Keffi replaces tedious weekly assessment forms with natural, empathetic dialogue. It learns your unique psychological profile to offer deeply personalized care.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 🚀 SECTION 5: DUAL PLATFORM (True Split-Screen) */}
        <section className="scroll-3d w-full flex flex-col lg:flex-row mt-20 border-y border-white/20 transition-all duration-75 ease-out bg-white/20 backdrop-blur-md">
           {/* Left Side: Patient (Light) */}
           <div className="flex-1 bg-[#F2F9F6]/20 p-16 lg:p-24 flex flex-col items-center text-center border-r border-white/10">
             <div className="h-48 flex items-end justify-center mb-10">
               <img src="https://illustrations.popsy.co/amber/success.svg" alt="Patient Sanctuary" className="h-full drop-shadow-xl" />
             </div>
              <h2 className="h2-title font-poppins text-slate-900 mb-6">For Patients.<br/>The <span className="cursive-accent">Sanctuary</span>.</h2>
             <p className="p-text text-slate-600 mb-10 max-w-sm font-medium">
               A completely judgment-free zone to vent, track your shifting moods, and receive real-time emotional first-aid without having to wait weeks for an appointment.
             </p>
             <button onClick={() => setView('login-patient')} className={`mt-auto px-10 py-4 rounded-2xl font-inter font-bold text-lg ${theme.btnTeal} cursor-pointer`}>
               Keffi
             </button>
           </div>

           {/* Right Side: Doctor (Light) */}
           <div className="flex-1 bg-white/15 p-16 lg:p-24 flex flex-col items-center text-center border-l border-white/10">
             <div className="h-48 flex items-end justify-center mb-10">
               <img src="https://illustrations.popsy.co/amber/video-call.svg" alt="Clinical Hub" className="h-full drop-shadow-2xl" />
             </div>
              <h2 className="h2-title font-poppins text-slate-900 mb-6">For Clinicians.<br/>The <span className="cursive-accent">Hub</span>.</h2>
             <p className="p-text text-slate-600 mb-10 max-w-sm font-medium">
               A predictive dashboard giving you a real-time view of your entire roster's emotional trajectory. If a patient shows signs of relapse, Keffi alerts you instantly.
             </p>
             <button onClick={() => setView('login-admin')} className={`mt-auto px-10 py-4 rounded-2xl font-inter font-bold text-lg ${theme.btnOutline} cursor-pointer`}>
               Access Hub
             </button>
           </div>
        </section>

        {/* 🚀 SECTION 6: SAFETY (Light Mode Alert Block) */}
        <section className="scroll-3d w-full bg-[#F2F9F6]/30 backdrop-blur-md py-32 relative overflow-hidden border-y border-red-500/20 transition-all duration-75 ease-out">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-red-500/5 rounded-full blur-[120px]"></div>
          <div className="max-w-[800px] mx-auto px-6 text-center relative z-10 flex flex-col items-center">
             <div className="w-24 h-24 mb-10 text-red-500 animate-pulse"><Shield size={96} strokeWidth={1} /></div>
              <h2 className="h2-title font-poppins text-slate-900 mb-8">Clinical <span className="cursive-accent text-red-500">Safety First</span>. Always.</h2>
             <p className="p-text text-slate-600 max-w-3xl font-medium">
               Built with strict WHO-compliant crisis protocols and the n8n automation engine, Keffi continuously monitors conversations for high-risk signals. In moments of severe distress or suicidal ideation, it overrides AI independence and instantly triggers an SOS alert to emergency contacts and your clinical supervisor. 
               <br/><br/>
               <span className="text-red-500 font-bold">We prioritize human safety over everything else.</span>
             </p>
          </div>
        </section>

        {/* 🚀 FINAL CTA */}
        <section className="w-full py-32 bg-transparent flex flex-col items-center text-center relative overflow-hidden">
          <div className="w-full max-w-[1000px] mx-auto glass-panel border border-white/35 rounded-[3rem] p-16 lg:p-24 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-[#3A7070]/5 rounded-full blur-[80px]"></div>
            <h2 className="h1-title font-poppins text-slate-900 mb-6 relative z-10">Ready to Heal?</h2>
            <p className="p-text text-slate-600 mb-12 relative z-10 max-w-lg mx-auto font-medium">Whether you are seeking support or providing care, Keffi AI is here to bridge the gap.</p>
            <button onClick={() => setView('login-patient')} className={`px-12 py-5 rounded-2xl font-inter font-bold text-xl relative z-10 ${theme.btnTeal} cursor-pointer`}>
              Keffi
            </button>
          </div>
        </section>
      </main>

      {/* 🚀 ULTIMATE FOOTER */}
      <footer className="w-full relative z-10 bg-[#E6F0F0]/30 backdrop-blur-md text-slate-900 overflow-hidden mt-10 border-t border-white/20">
        {/* Glow Effects */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-px bg-gradient-to-r from-transparent via-[#3A7070]/50 to-transparent"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-white rounded-full blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-emerald-100/50 rounded-full blur-[100px] pointer-events-none"></div>

        <div className="max-w-[1200px] mx-auto px-6 lg:px-12 pt-24 pb-12 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-16 lg:gap-8 mb-20">
            
            {/* Column 1: Brand & Emergency */}
            <div className="col-span-1 md:col-span-5 flex flex-col items-start">
              <div className="flex items-center gap-3 mb-8 glass-card px-6 py-4 rounded-2xl border border-white/30 backdrop-blur-sm w-fit shadow-sm">
                 <Star size={32} className="text-[#3A7070] fill-[#3A7070]" />
                 <span className="text-3xl font-poppins font-bold tracking-tight text-[#2C5555]">Keffi AI</span>
              </div>
              <p className="font-inter text-slate-600 text-lg mb-8 max-w-sm leading-relaxed font-semibold">
                Bridging the invisible gap in mental healthcare with continuous, empathetic AI tracking.
              </p>
              <div className="p-6 rounded-2xl bg-red-500/10 border border-red-200/35 backdrop-blur-sm w-full max-w-md shadow-sm">
                <div className="flex items-center gap-2 mb-3">
                  <Shield size={20} className="text-red-500" />
                  <h4 className="font-poppins font-semibold text-red-600 uppercase tracking-widest text-xs">Emergency Support</h4>
                </div>
                <p className="font-inter text-slate-700 text-sm leading-relaxed">
                  If you are in a life-threatening situation, please call local emergency services immediately. This platform is not a substitute for emergency medical care.
                </p>
              </div>
            </div>

            {/* Column 2: Navigation */}
            <div className="col-span-1 md:col-span-3 lg:col-span-2">
              <h4 className="font-poppins font-semibold text-slate-900 mb-6 uppercase tracking-wider text-sm">Platform</h4>
              <ul className="flex flex-col gap-4 font-inter text-slate-600">
                <li><button onClick={() => setView('login-patient')} className="hover:text-[#3A7070] font-medium transition-colors">Patient Sanctuary</button></li>
                <li><button onClick={() => setView('login-admin')} className="hover:text-[#3A7070] font-medium transition-colors">Clinical Hub</button></li>
                <li><button onClick={() => {document.getElementById('story')?.scrollIntoView({behavior: 'smooth'})}} className="hover:text-[#3A7070] font-medium transition-colors">How it Works</button></li>
              </ul>
            </div>

            {/* Column 3: Legal */}
            <div className="col-span-1 md:col-span-4 lg:col-span-5 flex flex-col lg:items-end lg:text-right">
              <h4 className="font-poppins font-semibold text-slate-900 mb-6 uppercase tracking-wider text-sm">Project Details</h4>
              <p className="font-inter text-slate-700 font-medium text-xl mb-2">
                Naan Mudhalvan - Niral Thiruvizha
              </p>
              <p className="font-inter text-[#3A7070] font-bold text-lg mb-10">
                Built with ❤️ by Team Keffi @ UCE Panruti
              </p>
              <div className="flex flex-wrap gap-6 font-inter text-sm text-slate-500 mt-auto justify-start lg:justify-end">
                <a href="#" className="hover:text-slate-900 transition-colors">Privacy Policy</a>
                <a href="#" className="hover:text-slate-900 transition-colors">Terms of Service</a>
                <a href="#" className="hover:text-slate-900 transition-colors">Clinical Guidelines</a>
              </div>
            </div>

          </div>

          <div className="pt-8 border-t border-[#3A7070]/10 flex flex-col md:flex-row justify-between items-center gap-4 text-slate-500 text-sm font-inter">
            <p>© 2026 Keffi AI Platform. All rights reserved.</p>
            <p className="flex items-center gap-2">Version 3.0.0 <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Systems Operational</p>
          </div>
        </div>
      </footer>
    </div>
    </>
  );
};

// ==========================================
// 2. PATIENT ONBOARDING
// ==========================================
const PatientLogin = ({ setView, setUserData }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({ phone: '', email: '', otp: '', name: '', age: '', dob: '', gender: '', place: '' });
  const [error, setError] = useState('');

  const handleNext = () => {
    setError('');
    if (step === 1) {
      const phoneClean = formData.phone.replace(/\D/g, '');
      if (!formData.phone) return setError('Please enter your mobile number.');
      if (phoneClean.length !== 10) return setError('Mobile number must be exactly 10 digits.');
      if (!formData.email) return setError('Please enter your email address.');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) return setError('Please enter a valid email address.');
      setStep(2);
    } else if (step === 2) {
      if (!formData.name.trim()) return setError('Please enter your preferred name.');
      if (!formData.age || isNaN(formData.age) || +formData.age < 5 || +formData.age > 120) return setError('Please enter a valid age (5–120).');
      if (!formData.gender) return setError('Please select your gender.');
      const phoneClean = formData.phone.replace(/\D/g, '');
      const patientId = 'P-' + phoneClean.slice(-6);
      const fullData = { ...formData, patient_id: patientId };
      localStorage.setItem('keffi_user', JSON.stringify(fullData));
      setUserData(fullData);
      setView('patient-dashboard');
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center p-6 md:p-10 bg-transparent`}>
      <div className={`max-w-5xl w-full min-h-[700px] lg:h-[700px] rounded-[2.5rem] glass-panel flex flex-col md:flex-row overflow-hidden border border-white/20`}>
        {/* Left Image Side */}
        <div className="hidden md:flex md:w-5/12 relative overflow-hidden bg-[#E6F0F0]/25 rounded-l-[2.5rem] items-center justify-center p-8 border-r border-white/20">
           <DynamicLoginIllustration step={step} className="w-full h-full max-w-[300px] object-contain relative z-10 drop-shadow-2xl transition-all duration-500" />
           <div className="absolute inset-0 bg-gradient-to-t from-[#2C5555]/30 via-transparent to-transparent flex flex-col justify-end p-12 text-[#1E293B] z-20">
              <h2 className="text-3xl font-black mb-3">
                {step === 1 && "Secure Entry"}
                {step === 2 && "Your Sanctuary"}
              </h2>
              <p className="text-base opacity-90 font-medium">
                {step === 1 && "Enter your details below to establish a secure connection."}
                {step === 2 && "Let's build your personal profile for a better experience."}
              </p>
           </div>
        </div>
        
        {/* Right Form Side */}
        <div className="w-full md:w-7/12 p-10 md:p-16 flex flex-col justify-center bg-white/25 backdrop-blur-sm">
          <div className="flex justify-start gap-3 mb-10">
            {[1,2].map(i => (
              <div key={i} className={`h-1.5 rounded-full transition-all duration-500 ${i === step ? 'w-12 bg-[#3A7070]' : 'w-4 bg-white/40'}`}></div>
            ))}
          </div>

          {step === 1 && (
            <div className="space-y-8 animate-fade-in">
              <div>
                <h2 className="text-3xl font-black text-slate-800 mb-3">Secure Entry</h2>
                <p className="text-slate-500 text-base">Your privacy is our priority. Enter details for a secure OTP.</p>
              </div>
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Mobile Number</label>
                  <input type="tel" placeholder="+91 98765 43210" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Email Address</label>
                  <input type="email" placeholder="you@example.com" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} />
                </div>
              </div>
              {error && <div className="text-red-500 text-sm font-bold bg-red-50 border border-red-200 rounded-xl px-4 py-3">{error}</div>}
              <div className="pt-2 space-y-4">
                <button onClick={handleNext} className={`w-full py-4 rounded-xl font-bold text-base ${theme.btnTeal}`}>Continue</button>
                <button onClick={() => setView('landing')} className="w-full text-center text-slate-400 font-bold text-sm hover:text-[#3A7070] transition-colors">Back to Home</button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-8 animate-fade-in h-full flex flex-col justify-center">
              <div>
                <h2 className="text-3xl font-black text-slate-800 mb-3">Your Profile</h2>
                <p className="text-slate-500 text-base">Help Keffi understand you better.</p>
              </div>
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">Preferred Name</label>
                  <input type="text" placeholder="What should we call you?" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} />
                </div>
                <div className="flex gap-5">
                  <div className="w-1/3">
                    <label className="block text-sm font-bold text-slate-700 mb-2">Age</label>
                    <input type="number" placeholder="Age" value={formData.age} onChange={e => setFormData({...formData, age: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} />
                  </div>
                  <div className="w-2/3">
                    <label className="block text-sm font-bold text-slate-700 mb-2">Date of Birth</label>
                    <input type="date" value={formData.dob} onChange={e => setFormData({...formData, dob: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-600 font-medium text-base focus:border-[#3A7070] transition-all`} />
                  </div>
                </div>
                <div className="flex gap-5">
                  <div className="w-1/2">
                    <label className="block text-sm font-bold text-slate-700 mb-2">Gender</label>
                    <select value={formData.gender} onChange={e => setFormData({...formData, gender: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all appearance-none`}>
                      <option value="" disabled>Select</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Non-binary">Non-binary</option>
                      <option value="Prefer not to say">Prefer not to say</option>
                    </select>
                  </div>
                  <div className="w-1/2">
                    <label className="block text-sm font-bold text-slate-700 mb-2">Location</label>
                    <input type="text" placeholder="City / District" value={formData.place} onChange={e => setFormData({...formData, place: e.target.value})} className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} />
                  </div>
                </div>
              </div>
              {error && <div className="text-red-500 text-sm font-bold bg-red-50 border border-red-200 rounded-xl px-4 py-3">{error}</div>}
              <div className="pt-2 mt-auto">
                <button onClick={handleNext} className={`w-full py-4 rounded-xl font-bold text-base ${theme.btnTeal}`}>Enter Keffi</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 3. ADMIN LOGIN
// ==========================================
const AdminLogin = ({ setView }) => {
  const [doctorId, setDoctorId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {
    if (doctorId === 'balaji' && password === 'balaji') {
      setView('admin-dashboard');
    } else {
      setError('Invalid ID or Passcode');
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center p-6 bg-transparent`}>
      <div className={`max-w-md w-full rounded-[2rem] glass-panel p-10 flex flex-col gap-8 border border-white/20`}>
        <div className="flex justify-center mb-2">
          <div className={`w-20 h-20 rounded-2xl glass-card flex items-center justify-center text-[#3A7070] border border-white/20`}><Shield size={40} /></div>
        </div>
        <div className="text-center">
          <h2 className="text-3xl font-black text-slate-800 mb-3">Clinical Hub</h2>
          <p className="text-slate-500 font-bold text-sm">Strictly for authorized medical personnel.</p>
        </div>
        
        {error && (
          <div className="p-3 bg-red-500/10 border border-red-200/30 text-red-600 rounded-xl text-center text-sm font-bold backdrop-blur-sm">
            {error}
          </div>
        )}

        <div className="space-y-5 mt-2">
          <div>
            <label className="block text-sm font-bold text-slate-700 mb-2">Doctor ID / Email</label>
            <input 
              type="text" 
              value={doctorId}
              onChange={(e) => setDoctorId(e.target.value)}
              placeholder="Doctor ID" 
              className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} 
            />
          </div>
          <div>
             <label className="block text-sm font-bold text-slate-700 mb-2">Secure Passcode</label>
             <input 
               type="password" 
               value={password}
               onChange={(e) => setPassword(e.target.value)}
               placeholder="••••••••" 
               className={`w-full p-4 rounded-xl glass-input outline-none text-slate-800 font-medium text-base focus:border-[#3A7070] transition-all`} 
             />
          </div>
        </div>
        <div className="pt-4 space-y-4">
          <button onClick={handleLogin} className={`w-full py-4 rounded-xl font-bold text-base ${theme.btnTeal}`}>Authenticate</button>
          <button onClick={() => setView('landing')} className="w-full text-center text-slate-400 font-bold text-sm hover:text-slate-600 transition-colors">Back to Home</button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 4. FUNCTIONAL PATIENT COMPONENTS
// ==========================================

const DailyMoodCheckIn = ({ patientId, onComplete }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const moods = [
    { score: 1, label: 'Heavy', emoji: '😔', color: 'text-slate-600', hover: 'hover:bg-slate-100 hover:border-slate-300' },
    { score: 2, label: 'Anxious', emoji: '😰', color: 'text-orange-500', hover: 'hover:bg-orange-50 hover:border-orange-200' },
    { score: 3, label: 'Numb', emoji: '😐', color: 'text-slate-500', hover: 'hover:bg-slate-50 hover:border-slate-300' },
    { score: 4, label: 'Okay', emoji: '🙂', color: 'text-teal-600', hover: 'hover:bg-teal-50 hover:border-teal-200' },
    { score: 5, label: 'Calm', emoji: '🌿', color: 'text-green-600', hover: 'hover:bg-green-50 hover:border-green-200' }
  ];

  const handleMoodSelect = async (mood) => {
    setIsSubmitting(true);
    try {
      const response = await fetch('https://balajikrishnan031-keffi-backend.hf.space/api/patient/check-in', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: patientId || "P-102",
          emoji_score: mood.score,
          sentiment_label: mood.label
        })
      });
      await response.json();
      onComplete(mood);
    } catch (error) {
      console.error("Failed to log mood", error);
      onComplete(mood);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full w-full animate-fade-in p-6">
      <div className="w-full max-w-3xl p-10 md:p-14 rounded-[2.5rem] glass-panel border border-white/35 flex flex-col items-center shadow-2xl backdrop-blur-xl">
        <h2 className="text-3xl font-black text-slate-800 mb-4 text-center">
          Welcome to your Sanctuary.
        </h2>
        <p className="text-lg text-slate-600 mb-12 text-center font-semibold">
          Before we begin, how is your mind feeling today?
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-6 w-full">
          {moods.map((m) => (
            <button 
              key={m.score} 
              disabled={isSubmitting}
              onClick={() => handleMoodSelect(m)} 
              className={`p-6 md:p-8 rounded-[2rem] glass-card border border-white/20 shadow-sm flex flex-col items-center gap-4 transition-all duration-300 hover:-translate-y-1 hover:bg-white/60 hover:border-white/40 cursor-pointer`}
            >
              <span className="text-5xl">{m.emoji}</span>
              <span className={`font-bold text-base ${m.color}`}>{m.label}</span>
            </button>
          ))}
        </div>
        {isSubmitting && <p className="mt-12 text-sm font-bold text-slate-400 animate-pulse">Syncing with Keffi...</p>}
      </div>
    </div>
  );
};

// HELPER: No longer stripping options so numbered lists stay in text
const parseMessageText = (text) => {
  return { mainText: text || '', options: [] };
};

const MediaPlayer = ({ onClose }) => {
  const tracks = [
    { title: 'Ambient River Flow', desc: 'Soothing stream water', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3' },
    { title: 'Deep Meditation Ambient', desc: 'Slow synth waves', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' },
    { title: 'Calm Horizon Melodies', desc: 'Healing keyboards & pad', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3' },
    { title: 'Tranquil Sanctuary', desc: 'Gentle acoustic ambient', url: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3' }
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const currentTrack = tracks[currentIndex];

  return (
    <div className="absolute inset-0 z-[70] bg-black/30 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="w-full max-w-md glass-panel border border-white/30 rounded-[2.5rem] p-8 shadow-2xl flex flex-col items-center relative overflow-hidden">
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-[#8FA989]/20 rounded-full blur-2xl"></div>
        <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-[#3A7070]/20 rounded-full blur-2xl"></div>
        
        {/* Record/Vinyl Animation */}
        <div className="w-40 h-40 rounded-full bg-gradient-to-tr from-slate-100 to-white border-4 border-slate-50 shadow-[0_10px_30px_rgba(0,0,0,0.1)] flex items-center justify-center animate-[spin_8s_linear_infinite] mb-6 relative z-10">
          <div className="w-12 h-12 bg-gradient-to-br from-[#3A7070] to-[#2C5555] rounded-full shadow-inner flex items-center justify-center">
            <div className="w-4 h-4 bg-white rounded-full"></div>
          </div>
          <div className="absolute inset-4 rounded-full border border-slate-200/50"></div>
          <div className="absolute inset-8 rounded-full border border-slate-200/50"></div>
          <div className="absolute inset-12 rounded-full border border-slate-200/50"></div>
        </div>

        <h3 className="text-xl font-black text-slate-800 mb-1 relative z-10 text-center">{currentTrack.title}</h3>
        <p className="text-sm text-[#8FA989] font-bold tracking-widest uppercase mb-4 relative z-10 text-center">{currentTrack.desc}</p>
        
        {/* Audio element with key to force reload and autoplay on source change */}
        <audio key={currentTrack.url} controls autoPlay className="w-full mb-6 relative z-10 opacity-80 hover:opacity-100 transition-opacity">
          <source src={currentTrack.url} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>

        {/* Track Playlist Selector */}
        <div className="w-full mb-6 z-10 max-h-40 overflow-y-auto space-y-2 pr-1">
          {tracks.map((track, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentIndex(idx)}
              className={`w-full flex items-center justify-between p-3 rounded-xl border transition-all text-left cursor-pointer ${
                idx === currentIndex
                  ? 'border-[#3A7070] bg-[#3A7070]/10 text-[#3A7070] font-bold'
                  : 'border-white/20 bg-white/20 hover:bg-white/40 text-slate-700'
              }`}
            >
              <div className="flex flex-col">
                <span className="text-xs font-bold leading-tight">{track.title}</span>
                <span className="text-[10px] opacity-75">{track.desc}</span>
              </div>
              <span className="text-[10px] font-bold">{idx === currentIndex ? '▶ Playing' : 'Select'}</span>
            </button>
          ))}
        </div>
        
        <button onClick={onClose} className="w-full py-4 rounded-2xl bg-white/40 backdrop-blur-sm border border-white/30 text-slate-700 font-bold hover:bg-white/60 hover:text-red-500 transition-all relative z-10 cursor-pointer">Close Player</button>
      </div>
    </div>
  );
};

// 4.0 Camera Emotion Tracker
const CameraEmotionTracker = ({ onEmotionDetected, isCameraActive }) => {
  const videoRef = useRef();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const loadModels = async () => {
      try {
        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
          faceapi.nets.faceExpressionNet.loadFromUri('/models')
        ]);
        setIsLoaded(true);
      } catch (err) {
        console.error("Failed to load face-api models", err);
      }
    };
    if (isCameraActive) loadModels();
  }, [isCameraActive]);

  useEffect(() => {
    let interval;
    if (isCameraActive && isLoaded) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch(err => console.error("Webcam error:", err));
      
      interval = setInterval(async () => {
        if (videoRef.current && !videoRef.current.paused) {
          const detections = await faceapi.detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions()).withFaceExpressions();
          if (detections) {
            const emotions = detections.expressions;
            const dominant = Object.keys(emotions).reduce((a, b) => emotions[a] > emotions[b] ? a : b);
            onEmotionDetected(dominant);
          }
        }
      }, 3000);
    } else {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(t => t.stop());
        videoRef.current.srcObject = null;
      }
    }
    return () => clearInterval(interval);
  }, [isCameraActive, isLoaded, onEmotionDetected]);

  if (!isCameraActive) return null;

  return (
    <div className="absolute top-24 left-6 z-30 w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-lg bg-slate-100 hidden md:flex items-center justify-center">
      {!isLoaded && <div className="text-[10px] font-bold text-slate-400 text-center px-2">Loading AI Vision...</div>}
      <video ref={videoRef} autoPlay muted className="object-cover w-full h-full" />
    </div>
  );
};

// 4.1 Enhanced Chat Page
const ChatArea = ({ setGlobalPoints, globalPoints, userData }) => {
  const [moodSet, setMoodSet] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(false);
  const [showSOS, setShowSOS] = useState(false);
  const [showMediaPlayer, setShowMediaPlayer] = useState(false);
  const [showAppointmentPopup, setShowAppointmentPopup] = useState(false);
  const [appointmentPrompted, setAppointmentPrompted] = useState(false);
  const [lastEmotionalMessage, setLastEmotionalMessage] = useState('');
  const chatEndRef = useRef(null);

  // Biofeedback & Camera States
  const [heartRate, setHeartRate] = useState(72);
  const [hasTriggeredPanic, setHasTriggeredPanic] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [visualEmotion, setVisualEmotion] = useState('neutral');
  const recognitionRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(prev => prev + (prev ? " " : "") + transcript);
        setIsRecording(false);
      };

      recognitionRef.current.onerror = () => setIsRecording(false);
      recognitionRef.current.onend = () => setIsRecording(false);
    }
  }, []);

  const toggleRecording = () => {
    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
    } else {
      if(recognitionRef.current) {
         recognitionRef.current.start();
         setIsRecording(true);
      } else {
         alert("Voice recognition is not supported in this browser.");
      }
    }
  };

  const handleMoodSelect = (mood) => {
    setMoodSet(true);
    setMessages([
      { id: 1, sender: 'keffi', time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), text: `Hi ${userData?.name || 'there'}. I see you're feeling a bit ${mood.label.toLowerCase()}. I'm here for you. Do you want to talk about it?` }
    ]);
  };

  useEffect(() => {
    // Biofeedback Panic Trigger
    if (heartRate > 110 && !hasTriggeredPanic && !isTyping) {
      setHasTriggeredPanic(true);
      const panicMsg = "[BIOFEEDBACK ALERT]: My heart is racing at " + heartRate + " BPM. I feel like I'm having a panic attack, I can't breathe!";
      setMessages(prev => [...prev, { id: Date.now(), sender: 'user', time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), text: panicMsg }]);
      
      // Auto-trigger the send handler with the panic message
      handleSend(panicMsg, true);
    }
  }, [heartRate, hasTriggeredPanic, isTyping]);

  const handleSend = async (forcedMessage = null, isPanicTrigger = false) => {
    const message = forcedMessage || input;
    if (!message.trim()) return;

    const newMsg = { id: Date.now(), sender: 'user', time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), text: message };
    setMessages(prev => [...prev, newMsg]);
    setInput('');
    setGlobalPoints(p => p + 10);
    setIsTyping(true);

    // Track last real emotional message (not button shortcuts)
    const BUTTON_OPTIONS = [
      "Tell me a story", "Play me a song", "Hear a joke", "Give me a joke", "Give me a puzzle",
      "I want to vent", "I need to vent", "I need to talk", "I want to talk more",
      "Tell me another", "Give me another", "Tell me more",
      "Help me reframe", "Guide me through grounding", "Give me a distress skill",
      "What small step can I take", "Help me understand this feeling",
      "I feel a bit better", "I feel calmer", "Feeling better", "I feel better",
      "Play me a calming song", "Calming song", "I need to vent this out",
      "I want to share more", "I need to talk"
    ];
    const isButtonClick = BUTTON_OPTIONS.some(opt => message.includes(opt));
    
    // Store context for next queries
    if (!isPanicTrigger && message.length > 10 && !isButtonClick) {
      setLastEmotionalMessage(message);
    }

    // Auto-trigger music player immediately if user requests song/music
    const lowerMessage = message.toLowerCase();
    const isMusicRequest = lowerMessage.includes('song') || lowerMessage.includes('music') || lowerMessage.includes('audio') || lowerMessage.includes('soundscape') || lowerMessage.includes('ambient');
    if (isMusicRequest) {
      setTimeout(() => setShowMediaPlayer(true), 500);
    }
    
    try {
      const payloadContext = isCameraActive && visualEmotion ? `[Visual Face Emotion Detected via Webcam: ${visualEmotion}] ` + lastEmotionalMessage : lastEmotionalMessage;
      
      const response = await axios.post('https://balajikrishnan031-keffi-backend.hf.space/api/chat', {
        message: message,
        patient_id: userData?.patient_id || "P-102",
        emotional_context: payloadContext
      });
      
      let botResponse = response.data.reply || "I'm here for you.";
      
      if (botResponse.includes('[TRIGGER_MUSIC_PLAYER]')) {
        botResponse = botResponse.replace('[TRIGGER_MUSIC_PLAYER]', '').trim();
        setTimeout(() => setShowMediaPlayer(true), 1500); // Popup the music player after a small delay
      }
      
      setIsTyping(false);
      setMessages(prev => [...prev, { 
        id: Date.now() + 1, 
        sender: 'keffi', 
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), 
        text: botResponse,
        options: response.data.options
      }]);
      
      if (response.data.requires_appointment && !appointmentPrompted) {
        setAppointmentPrompted(true);
        setTimeout(() => setShowAppointmentPopup(true), 1500);
      }

      if ('speechSynthesis' in window && isVoiceEnabled) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(botResponse.replace(/[#*]/g, ''));
        utterance.lang = 'en-US';
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google UK English Female') || v.name.includes('Google US English') || v.name.includes('Female'));
        if (preferredVoice) utterance.voice = preferredVoice;
        utterance.pitch = 0.95;
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      }
    } catch (err) {
      console.error(err);
      setIsTyping(false);
      setMessages(prev => [...prev, { 
        id: Date.now() + 1, 
        sender: 'keffi', 
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), 
        text: "I'm having a hard time reaching my thoughts right now (Backend Offline). Let's take a deep breath together." 
      }]);
    }
  };

  const handleBookAppointment = async () => {
    setShowAppointmentPopup(false);
    try {
      await axios.post('https://balajikrishnan031-keffi-backend.hf.space/api/book_appointment', {
        patient_id: "P-102",
        name: userData?.name || "Patient",
        phone: userData?.phone || "9876543210",
        email: userData?.email || "patient@keffi.ai"
      });
      alert("Appointment automation triggered successfully! You will receive a WhatsApp message shortly.");
    } catch (err) {
      console.error("Failed to book appointment", err);
      alert("Failed to trigger appointment automation.");
    }
  };

  if (!moodSet) {
    return <DailyMoodCheckIn patientId="P-102" onComplete={handleMoodSelect} />;
  }

  return (
    <div className="grid grid-rows-[auto_1fr_auto] h-full w-full relative animate-fade-in mx-auto overflow-hidden bg-transparent">
      <div className="flex justify-between items-center px-6 md:px-8 pt-6 pb-4 z-20 border-b border-white/20 bg-white/20 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 glass-card border border-white/45 rounded-full flex items-center justify-center shadow-sm">
            <KeffiLogo size="w-7 h-7" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Keffi</h2>
            <div className="flex items-center gap-2 text-xs text-[#8FA989] font-bold">
              <div className="w-2 h-2 rounded-full bg-[#8FA989] animate-pulse"></div> Active & Listening
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setIsCameraActive(!isCameraActive)} 
            className={`px-3 py-2 rounded-full font-bold text-xs flex items-center gap-2 transition-colors hidden md:flex cursor-pointer ${isCameraActive ? 'bg-[#3A7070] text-white border border-white/20' : 'glass-card text-slate-600 hover:bg-white/50 border border-white/30'}`}
            title="Toggle Visual Emotion Tracking"
          >
            {isCameraActive ? <Camera size={16}/> : <CameraOff size={16}/>}
          </button>
          <button 
            onClick={() => {
              setIsVoiceEnabled(!isVoiceEnabled);
              if (isVoiceEnabled && 'speechSynthesis' in window) window.speechSynthesis.cancel();
            }} 
            className={`px-3 py-2 rounded-full font-bold text-xs flex items-center gap-2 transition-colors cursor-pointer ${isVoiceEnabled ? 'bg-[#3A7070] text-white border border-white/20' : 'glass-card text-slate-600 hover:bg-white/50 border border-white/30'}`}
            title="Toggle Voice Therapy"
          >
            {isVoiceEnabled ? <Volume2 size={16}/> : <VolumeX size={16}/>}
          </button>
          <button 
            onClick={() => setShowMediaPlayer(true)} 
            className="px-4 py-2 rounded-full bg-emerald-500/12 backdrop-blur-sm border border-emerald-500/20 text-[#2C5555] font-bold text-xs hover:bg-emerald-500/20 flex items-center gap-2 transition-colors cursor-pointer"
            title="Open Calming Music Sanctuary"
          >
            🎵 Music
          </button>
          <button onClick={() => setShowAppointmentPopup(true)} className="px-4 py-2 rounded-full glass-card text-slate-600 font-bold text-xs hover:bg-white/50 border border-white/30 flex items-center gap-2 transition-colors cursor-pointer">
            <User size={14}/> Therapist
          </button>
          <button onClick={() => setShowSOS(true)} className="px-4 py-2 rounded-full bg-red-500/12 border border-red-500/20 text-red-600 font-bold text-xs hover:bg-red-500/20 backdrop-blur-sm flex items-center gap-2 transition-colors cursor-pointer">
            <PhoneCall size={14}/> SOS
          </button>
        </div>
      </div>
      
      <CameraEmotionTracker isCameraActive={isCameraActive} onEmotionDetected={setVisualEmotion} />

      {showSOS && (
        <div className="absolute top-24 left-1/2 transform -translate-x-1/2 z-50 glass-panel p-8 rounded-[2rem] shadow-2xl border border-red-500/20 flex flex-col items-center animate-fade-in w-80 text-center">
          <div className="w-16 h-16 bg-red-500/10 rounded-2xl flex items-center justify-center text-red-500 mb-6"><AlertTriangle size={32}/></div>
          <h3 className="text-xl font-black text-slate-800 mb-2">Emergency Hotline</h3>
          <p className="text-sm text-slate-600 mb-6 font-semibold">You are not alone. Please call iCall India for immediate support.</p>
          <div className="text-2xl font-black text-[#2C5555] mb-6 tracking-widest">9152987821</div>
          <button onClick={() => setShowSOS(false)} className="px-8 py-3 rounded-xl glass-card border border-white/30 text-slate-700 font-bold text-sm hover:bg-white/50 w-full transition-colors cursor-pointer">Close</button>
        </div>
      )}

      {showMediaPlayer && <MediaPlayer onClose={() => setShowMediaPlayer(false)} />}

      {showAppointmentPopup && (
        <div className="absolute top-24 left-1/2 transform -translate-x-1/2 z-[60] glass-panel p-8 rounded-[2rem] shadow-2xl border border-white/30 flex flex-col items-center animate-fade-in w-80 text-center">
          <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center text-[#3A7070] mb-6 text-3xl">🫂</div>
          <h3 className="text-xl font-black text-slate-800 mb-2">You're not alone</h3>
          <p className="text-sm text-slate-600 mb-8 font-semibold">We noticed you're going through a tough time. Would you like to schedule an automatic appointment with a human therapist?</p>
          <div className="flex flex-col gap-3 w-full">
            <button onClick={handleBookAppointment} className={`w-full py-3.5 rounded-xl font-bold text-sm ${theme.btnTeal} cursor-pointer`}>Yes, Book Session</button>
            <button onClick={() => setShowAppointmentPopup(false)} className={`w-full py-3.5 rounded-xl font-bold text-sm glass-card border border-white/30 text-slate-600 hover:bg-white/50 transition-colors cursor-pointer`}>Not Right Now</button>
          </div>
        </div>
      )}

      {/* Biofeedback Watch Simulator */}
      <div className="absolute right-6 top-24 z-30 glass-card border border-white/40 p-4 rounded-3xl shadow-lg flex flex-col items-center gap-2 animate-fade-in hidden md:flex">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">
          <HeartPulse size={14} className={heartRate > 100 ? 'text-red-500 animate-pulse' : 'text-[#3A7070]'} />
          Watch Sync
        </div>
        <div className={`text-3xl font-black ${heartRate > 100 ? 'text-red-500' : 'text-slate-800'}`}>
          {heartRate} <span className="text-sm font-bold text-slate-400">BPM</span>
        </div>
        <input 
          type="range" 
          min="60" 
          max="140" 
          value={heartRate} 
          onChange={(e) => {
            const val = parseInt(e.target.value);
            setHeartRate(val);
            if (val < 100) setHasTriggeredPanic(false); // Reset panic if they calm down
          }}
          className="w-24 mt-2 accent-[#3A7070]"
        />
        <div className="text-[9px] text-slate-400 mt-1 max-w-[100px] text-center leading-tight">Drag above 110 BPM to trigger panic.</div>
      </div>

      <div className="overflow-y-auto p-6 md:p-8 flex flex-col gap-6 z-10 min-h-0 relative bg-white/5 backdrop-blur-[6px]">
        {messages.map(m => {
          const { mainText } = m.sender === 'keffi' ? parseMessageText(m.text) : { mainText: m.text };
          return (
            <div key={m.id} className={`flex w-full ${m.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in-up`}>
              <div className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'} max-w-[85%]`}>
                <div className={`whitespace-pre-wrap p-4 md:p-5 text-sm md:text-base font-medium leading-relaxed rounded-[1.5rem] ${
                  m.sender === 'user' 
                  ? 'glass-message-user text-slate-800 rounded-tr-sm shadow-sm' 
                  : 'glass-message-keffi text-[#1A2E2E] rounded-tl-sm'
                }`}>
                  {mainText}
                </div>
                
                <span className={`text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-2 px-1`}>
                  {m.time}
                </span>

                {/* Option Buttons beneath Keffi's reply (Horizontal Card Layout) */}
                {m.sender === 'keffi' && m.options && m.options.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4 w-full">
                    {m.options.map((qr, i) => (
                      <button 
                        key={i} 
                        onClick={() => handleSend(qr)} 
                        className="flex items-start text-left p-4 rounded-2xl glass-card glass-card-hover border border-white/30 shadow-sm group cursor-pointer"
                      >
                        <div className="w-5 h-5 rounded-full bg-white/20 border border-white/30 text-slate-600 group-hover:bg-[#3A7070]/20 group-hover:text-[#3A7070] group-hover:border-[#3A7070]/30 flex items-center justify-center text-[10px] font-bold shrink-0 mr-3 mt-0.5 transition-colors">
                          {i + 1}
                        </div>
                        <span className="text-[13px] font-bold text-slate-700 group-hover:text-slate-900 leading-snug">
                          {qr}
                        </span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
        {isTyping && (
          <div className="flex flex-col self-start items-start max-w-[85%]">
            <div className="p-4 rounded-[1.5rem] glass-message-keffi flex gap-1.5 items-center rounded-tl-sm border border-[#3A7070]/10">
              <div className="w-2 h-2 rounded-full bg-[#3A7070] animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 rounded-full bg-[#3A7070] animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 rounded-full bg-[#3A7070] animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} className="h-4" />
      </div>

      <div className="p-4 md:p-6 bg-white/15 backdrop-blur-md border-t border-white/20 z-20">
        <div className="flex gap-2 relative">
          <button onClick={toggleRecording} className={`p-4 rounded-2xl ${isRecording ? 'bg-red-500/10 text-red-500 animate-pulse border border-red-500/20' : 'glass-card border border-white/30 text-slate-500 hover:text-[#3A7070] hover:bg-white/50'} shadow-sm transition-colors shrink-0 cursor-pointer`}>
            <Mic size={20} />
          </button>
          <input 
            value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder={isRecording ? "Listening..." : "Type your feelings safely here..."} 
            className="flex-1 rounded-2xl glass-input px-5 py-4 text-sm focus:ring-2 focus:ring-[#3A7070]/20 shadow-sm transition-all"
          />
          <button onClick={() => handleSend()} className="px-6 rounded-2xl bg-[#3A7070] hover:bg-[#2C5555] text-white flex items-center justify-center transition-colors shadow-sm shrink-0 cursor-pointer">
            <Send size={18} />
          </button>
        </div>
        <div className="text-center text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-4">
          Keffi AI is not a substitute for medical diagnosis.
        </div>
      </div>
    </div>
  );
};

// 4.2 Peace Log
const PeaceLog = () => (
  <div className="h-full flex flex-col max-w-5xl mx-auto w-full p-8 md:p-12 rounded-[2.5rem] glass-panel border border-white/20 shadow-xl overflow-hidden my-6">
    <h2 className="text-2xl font-black text-slate-800 mb-8">Peace Log</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 overflow-y-auto pb-8 pr-2">
      {[
        { date: 'Today, 10:00 AM', mood: 'Anxious', title: 'Morning Panic', desc: 'Discussed work pressure and did a quick 4-7-8 breathing session.' },
        { date: 'Yesterday, 9:00 PM', mood: 'Calm', title: 'Night Reflections', desc: 'Used the gratitude jar. Felt significantly calmer before bed.' },
        { date: '25 April 2026', mood: 'Heavy', title: 'Trauma Processing', desc: 'Keffi guided through severe anxiety. Grounding techniques used.' },
        { date: '22 April 2026', mood: 'Stressed', title: 'Work Stress', desc: 'Vented about the upcoming presentation. Keffi helped reframe thoughts.' }
      ].map((log, i) => (
        <div key={i} className={`p-8 rounded-[2rem] ${theme.outset} cursor-pointer ${theme.outsetHover} flex flex-col`}>
          <div className="flex justify-between items-center mb-5">
            <span className="text-xs text-[#8FA989] font-bold uppercase tracking-widest">{log.date}</span>
            <span className="px-3 py-1 rounded-md bg-white/20 border border-white/30 text-xs font-bold text-slate-600">{log.mood}</span>
          </div>
          <h3 className="text-lg font-bold text-slate-800 mb-3">{log.title}</h3>
          <p className="text-slate-500 leading-relaxed text-sm flex-1">{log.desc}</p>
          <div className="mt-6 flex items-center text-[#3A7070] font-bold text-sm group">
             Read full log <ArrowRight size={16} className="ml-1 group-hover:translate-x-1 transition-transform"/>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// 4.3 My Journey
const MyJourney = () => (
  <div className="h-full flex flex-col max-w-5xl mx-auto w-full p-8 md:p-12 rounded-[2.5rem] glass-panel border border-white/20 shadow-xl overflow-y-auto my-6">
    <h2 className="text-2xl font-black text-slate-800 mb-8">Emotional Landscape</h2>
    
    <div className={`w-full h-80 rounded-[2.5rem] glass-panel border border-white/30 mb-8 relative overflow-hidden flex items-end justify-center shadow-inner`}>
      <div className="absolute top-8 right-12 w-24 h-24 rounded-full bg-gradient-to-tr from-[#D4A373] to-white blur-md shadow-[0_0_40px_#D4A373]"></div>
      <div className="w-[120%] h-40 bg-[#8FA989] rounded-[100%] absolute -bottom-8 opacity-40"></div>
      <div className="w-[80%] h-48 bg-[#3A7070] rounded-[100%] absolute -bottom-10 opacity-60 left-[-10%]"></div>
      <div className="w-[90%] h-44 bg-[#548a8a] rounded-[100%] absolute -bottom-8 opacity-70 right-[-10%]"></div>
      <div className={`absolute top-8 left-8 px-6 py-3 rounded-2xl glass-card border border-white/40 shadow-sm`}>
        <h3 className="text-lg font-bold text-slate-800">You are Thriving 🌿</h3>
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className={`p-8 rounded-[2rem] glass-card border border-white/30 shadow-sm flex flex-col items-center justify-center gap-3`}>
        <div className="text-4xl font-black text-[#3A7070]">12</div>
        <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Day Streak</div>
      </div>
      <div className={`p-8 rounded-[2rem] glass-card border border-white/30 shadow-sm flex flex-col items-center justify-center gap-3`}>
        <div className="text-4xl font-black text-[#8FA989]">85%</div>
        <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Calm Status</div>
      </div>
      <div className={`p-8 rounded-[2rem] glass-card border border-white/30 shadow-sm flex flex-col items-center justify-center gap-3`}>
        <div className="text-4xl font-black text-[#D4A373]">4</div>
        <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Tools Used</div>
      </div>
    </div>
  </div>
);

// 4.4 Mind Tools
const MindTools = () => {
  const [activeTool, setActiveTool] = useState(null); 
  const [worryText, setWorryText] = useState('');
  const [isBurning, setIsBurning] = useState(false);
  const [gratitudeText, setGratitudeText] = useState('');
  const [gratitudeList, setGratitudeList] = useState([]);
  const [groundingStep, setGroundingStep] = useState(0);

  const handleBurn = () => {
    setIsBurning(true);
    setTimeout(() => { setWorryText(''); setIsBurning(false); setActiveTool(null); }, 2000);
  };

  if (activeTool === 'breathing') {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-12 animate-fade-in">
        <div className="text-center">
          <h2 className="text-3xl font-black text-slate-800 mb-4">4-7-8 Breathing</h2>
          <p className="text-slate-500 text-base">Follow the circle to reduce anxiety.</p>
        </div>
        <div className="relative w-80 h-80 flex items-center justify-center">
          <div className="absolute inset-0 bg-[#3A7070] rounded-full opacity-10 animate-ping" style={{animationDuration: '4s'}}></div>
          <div className={`w-48 h-48 rounded-full glass-card shadow-xl border border-white/40 flex items-center justify-center text-[#3A7070] font-black text-xl z-10 backdrop-blur-md`}>Breathe In</div>
        </div>
        <button onClick={() => setActiveTool(null)} className={`px-8 py-3 rounded-xl font-bold text-base ${theme.btnOutline} cursor-pointer`}>Stop & Go Back</button>
      </div>
    );
  }

  if (activeTool === 'worry') {
    return (
      <div className="h-full flex flex-col items-center justify-center max-w-2xl mx-auto space-y-8 w-full animate-fade-in">
        <div className="text-center">
          <h2 className="text-3xl font-black text-[#D4A373] mb-4">Worry Burner</h2>
          <p className="text-slate-500 text-base">Type what's bothering you, and let it go into the ash.</p>
        </div>
        <textarea 
          value={worryText} onChange={(e) => setWorryText(e.target.value)}
          className={`w-full h-64 p-8 rounded-[2rem] glass-input shadow-inner outline-none text-slate-800 text-base resize-none transition-all duration-1000 ${isBurning ? 'blur-xl opacity-0 scale-110' : ''}`}
          placeholder="I am worried about..."
        />
        <div className="flex gap-4 w-full">
          <button onClick={() => setActiveTool(null)} className={`flex-1 py-4 rounded-xl font-bold text-base ${theme.btnOutline} cursor-pointer`}>Cancel</button>
          <button onClick={handleBurn} className={`flex-1 py-4 rounded-xl font-bold text-base bg-[#D4A373] text-white shadow-lg hover:-translate-y-0.5 transition-transform cursor-pointer`}>Burn Worry</button>
        </div>
      </div>
    );
  }

  if (activeTool === 'gratitude') {
    return (
      <div className="h-full flex flex-col items-center max-w-3xl mx-auto space-y-8 w-full animate-fade-in p-6">
        <div className="text-center">
          <h2 className="text-3xl font-black text-[#8FA989] mb-4">Gratitude Jar</h2>
          <p className="text-slate-500 text-base">Drop small moments of joy here.</p>
        </div>
        <div className="flex w-full gap-4">
           <input 
             value={gratitudeText} onChange={e => setGratitudeText(e.target.value)} 
             placeholder="I am grateful for..." 
             className={`flex-1 p-4 rounded-2xl glass-input shadow-sm outline-none text-slate-800 font-medium text-base`}
             onKeyPress={e => {
               if(e.key === 'Enter' && gratitudeText) {
                 setGratitudeList([{id: Date.now(), text: gratitudeText}, ...gratitudeList]);
                 setGratitudeText('');
               }
             }}
           />
           <button onClick={() => {
             if(gratitudeText) {
               setGratitudeList([{id: Date.now(), text: gratitudeText}, ...gratitudeList]);
               setGratitudeText('');
             }
           }} className={`px-8 py-4 rounded-2xl bg-[#8FA989] text-white font-bold shadow-md hover:-translate-y-0.5 transition-transform text-base cursor-pointer`}>Drop</button>
        </div>
        <div className={`flex-1 w-full rounded-[2.5rem] glass-panel border-8 border-[#8FA989]/20 p-8 flex flex-col-reverse items-center justify-start overflow-y-auto relative`}>
           <div className="w-48 h-8 rounded-[100%] bg-slate-200 absolute -top-4 opacity-50 blur-md"></div>
           {gratitudeList.length === 0 && <div className="text-slate-500 font-bold text-sm absolute top-1/2">Your jar is empty.</div>}
           {gratitudeList.map(g => (
             <div key={g.id} className="bg-gradient-to-r from-[#8FA989] to-[#649e9e] text-white px-6 py-3.5 rounded-full mb-3 shadow-lg transform rotate-[-2deg] font-bold text-sm animate-fade-in">
                 {g.text}
             </div>
           ))}
        </div>
        <button onClick={() => setActiveTool(null)} className={`w-full py-4 rounded-xl font-bold text-base ${theme.btnOutline} cursor-pointer`}>Back to Tools</button>
      </div>
    );
  }

  if (activeTool === 'grounding') {
    const steps = [
      { num: 5, text: "Things you can SEE", color: "text-[#3A7070]", bg: "bg-[#3A7070]" },
      { num: 4, text: "Things you can FEEL", color: "text-[#D4A373]", bg: "bg-[#D4A373]" },
      { num: 3, text: "Things you can HEAR", color: "text-[#8FA989]", bg: "bg-[#8FA989]" },
      { num: 2, text: "Things you can SMELL", color: "text-slate-600", bg: "bg-slate-600" },
      { num: 1, text: "Thing you can TASTE", color: "text-[#3A7070]", bg: "bg-[#3A7070]" },
    ];
    const current = steps[groundingStep];

    return (
      <div className="h-full flex flex-col items-center justify-center max-w-3xl mx-auto w-full animate-fade-in">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-black text-slate-800 mb-4">5-4-3-2-1 Grounding</h2>
          <p className="text-slate-500 text-base">Halt panic and come back to the present.</p>
        </div>
        
        {groundingStep < 5 ? (
          <div className={`p-16 rounded-[3rem] glass-panel border border-white/30 shadow-xl flex flex-col items-center text-center w-full`}>
            <div className={`text-7xl font-black ${current.color} mb-6`}>{current.num}</div>
            <h3 className={`text-2xl font-black text-slate-800 mb-10 uppercase tracking-widest`}>{current.text}</h3>
            <p className="text-slate-600 font-bold text-base mb-10">Take your time. Look around you. Name them silently or out loud.</p>
            <button onClick={() => setGroundingStep(s => s + 1)} className={`w-full py-4 rounded-xl text-white font-bold text-base ${current.bg} shadow-lg hover:-translate-y-0.5 transition-transform cursor-pointer`}>Next Step</button>
          </div>
        ) : (
          <div className={`p-16 rounded-[3rem] glass-panel border border-white/30 shadow-xl flex flex-col items-center text-center w-full`}>
            <div className={`w-24 h-24 rounded-2xl bg-[#8FA989]/20 text-[#8FA989] flex items-center justify-center mb-8 border border-white/30`}><Star size={48}/></div>
            <h3 className="text-2xl font-black text-slate-800 mb-6">You did great.</h3>
            <p className="text-slate-600 font-bold text-base mb-10">Welcome back to the present moment.</p>
            <button onClick={() => {setGroundingStep(0); setActiveTool(null);}} className={`w-full py-4 rounded-xl font-bold text-base ${theme.btnOutline} cursor-pointer`}>Finish</button>
          </div>
        )}
      </div>
    );
  }

  const allTools = [
    { id: 'breathing', title: '4-7-8 Breathing', desc: 'Reduce heart rate', icon: Activity, color: 'text-[#3A7070]', active: true },
    { id: 'worry', title: 'Worry Burner', desc: 'Release anxiety visually', icon: Sparkles, color: 'text-[#D4A373]', active: true },
    { id: 'gratitude', title: 'Gratitude Jar', desc: 'Shift perspective', icon: Heart, color: 'text-[#8FA989]', active: true },
    { id: 'grounding', title: '5-4-3-2-1 Grounding', desc: 'Halt panic attacks', icon: Star, color: 'text-[#3A7070]', active: true },
    { id: 'bodyscan', title: 'Body Scan', desc: 'Release physical tension', icon: User, color: 'text-[#D4A373]', active: false },
    { id: 'moodtracker', title: 'Mood Tracker', desc: 'Identify daily patterns', icon: PieChart, color: 'text-[#8FA989]', active: false },
    { id: 'reframing', title: 'Cognitive Reframing', desc: 'Challenge negative thoughts', icon: MessageCircle, color: 'text-[#3A7070]', active: false },
    { id: 'thermometer', title: 'Anxiety Thermometer', desc: 'Measure distress', icon: AlertTriangle, color: 'text-[#D4A373]', active: false },
    { id: 'sleep', title: 'Sleep Wind-down', desc: 'Prepare for deep rest', icon: Smile, color: 'text-[#8FA989]', active: false },
    { id: 'journal', title: 'Guided Journal', desc: 'Unlocks at Level 2', icon: BookOpen, color: 'text-slate-400', active: false, locked: true },
  ];

  return (
    <div className="h-full flex flex-col max-w-7xl mx-auto w-full p-8 md:p-12 rounded-[2.5rem] glass-panel border border-white/20 shadow-xl overflow-hidden my-6">
      <h2 className="text-2xl font-black text-slate-800 mb-8">Mind Tools Sandbox</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 overflow-y-auto pb-8 pr-2">
        {allTools.map((tool) => (
          <div key={tool.id} onClick={() => tool.active ? setActiveTool(tool.id) : null} 
            className={`p-6 rounded-[2rem] glass-card border border-white/20 shadow-sm flex flex-col items-center justify-center gap-4 text-center ${tool.active ? theme.outsetHover : 'opacity-65'} ${tool.locked ? 'cursor-not-allowed opacity-40' : 'cursor-pointer'}`}>
            <div className={`w-14 h-14 rounded-2xl bg-white/20 border border-white/10 flex items-center justify-center ${tool.color}`}><tool.icon size={24} /></div>
            <div>
              <h3 className="font-bold text-slate-800 text-base mb-1">{tool.title}</h3>
              <p className="text-xs text-slate-500 font-medium">{tool.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// 4.5 Rewards
const Rewards = ({ points }) => (
  <div className="h-full flex flex-col items-center justify-center max-w-2xl mx-auto w-full p-8 md:p-12 rounded-[2.5rem] glass-panel border border-white/20 shadow-xl my-6">
    <div className={`w-full p-10 rounded-[2.5rem] bg-white/20 border border-white/20 flex flex-col items-center text-center mb-10`}>
      <Gift size={48} className="text-[#D4A373] mb-6" />
      <h2 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4">Total Keffi Points</h2>
      <div className="text-5xl font-black text-[#3A7070]">{points}</div>
    </div>
    
    <div className="w-full space-y-4">
      <h3 className="font-black text-slate-800 text-xl mb-4">Unlock Goals</h3>
      <div className={`p-5 rounded-2xl bg-white/10 border border-white/10 flex justify-between items-center opacity-60`}>
        <span className="font-bold text-slate-600 text-base">Mindfulness Badge</span>
        <span className="font-bold text-[#3A7070] text-base">100 pts (Unlocked)</span>
      </div>
      <div className={`p-5 rounded-2xl glass-card border border-white/35 shadow-sm flex justify-between items-center`}>
        <span className="font-bold text-slate-800 text-base">Free Therapist Session</span>
        <span className="font-bold text-[#D4A373] text-base">1000 pts</span>
      </div>
      <div className="w-full bg-white/15 rounded-full h-3 mt-4 overflow-hidden border border-white/20">
        <div className="bg-[#3A7070] h-3 transition-all duration-1000" style={{width: `${Math.min((points/1000)*100, 100)}%`}}></div>
      </div>
      {points >= 1000 ? (
        <button className={`w-full py-4 mt-6 rounded-xl font-bold text-base ${theme.btnTeal} cursor-pointer`}>Claim Therapist Session</button>
      ) : (
        <button disabled className={`w-full py-4 mt-6 rounded-xl font-bold text-base glass-card border border-white/10 text-slate-500 cursor-not-allowed`}>Chat more to Unlock</button>
      )}
    </div>
  </div>
);

// 4.6 Friends
const FriendsSync = () => (
  <div className="h-full flex flex-col items-center justify-center max-w-3xl mx-auto w-full p-8 md:p-12 rounded-[2.5rem] glass-panel border border-white/20 shadow-xl my-6">
    <div className="text-center mb-10">
      <h2 className="text-2xl font-black text-slate-800 mb-3">Neighbor Sync</h2>
      <p className="text-slate-600 text-base font-semibold">You are not alone. See the abstract mood of people near you.</p>
    </div>
    
    <div className={`w-80 h-80 rounded-full bg-white/10 border border-white/25 relative flex items-center justify-center shadow-inner`}>
      <div className="absolute w-64 h-64 rounded-full border border-white/10 opacity-70"></div>
      <div className="absolute w-40 h-40 rounded-full border border-white/10 opacity-70"></div>
      
      <div className={`w-10 h-10 bg-[#3A7070] rounded-full z-10 shadow-lg animate-pulse`}></div>
      <div className="absolute mt-16 font-bold text-xs text-[#3A7070] bg-white/70 px-3 py-1 rounded-full border border-white/30 shadow-sm">You</div>
 
      <div className="absolute top-16 left-16 w-8 h-8 bg-[#8FA989] rounded-full shadow-[0_0_20px_#8FA989] cursor-pointer hover:scale-125 transition-transform" title="Calm Neighbor"></div>
      <div className="absolute bottom-20 right-16 w-8 h-8 bg-[#D4A373] rounded-full shadow-[0_0_20px_#8FA989] cursor-pointer hover:scale-125 transition-transform" title="Anxious Neighbor"></div>
      <div className="absolute top-24 right-10 w-8 h-8 bg-[#8FA989] rounded-full shadow-[0_0_20px_#8FA989] cursor-pointer hover:scale-125 transition-transform" title="Calm Neighbor"></div>
    </div>
 
    <div className={`mt-12 p-6 rounded-2xl glass-card border border-white/30 shadow-sm flex items-center gap-5`}>
      <Heart className="text-[#D4A373]" size={24} />
      <span className="font-bold text-slate-800 text-base">Send a Virtual Hug</span>
      <button className={`px-5 py-2.5 rounded-xl text-sm font-bold ${theme.btnOutline} cursor-pointer`}>Send Love</button>
    </div>
  </div>
);

// 4.7 Profile
const ProfileVault = ({ userData }) => (
  <div className="h-full flex flex-col items-center justify-center">
    <div className={`max-w-2xl w-full p-10 rounded-[2.5rem] glass-panel border border-white/30 shadow-sm`}>
      <div className="flex flex-col items-center mb-8">
        <div className={`w-24 h-24 rounded-3xl bg-white/20 border border-white/35 flex items-center justify-center text-[#3A7070] mb-5`}>
          <User size={40} />
        </div>
        <h2 className="text-2xl font-black text-slate-800">Identity Vault</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className={`p-5 rounded-2xl glass-card border border-white/20`}>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Full Name</div>
          <div className="text-lg font-bold text-slate-800">{userData?.name || 'Guest User'}</div>
        </div>
        <div className={`p-5 rounded-2xl glass-card border border-white/20`}>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Age / DOB / Gender</div>
          <div className="text-lg font-bold text-slate-800">{userData?.age || '25'} • {userData?.dob || 'Not Set'} • {userData?.gender || 'Not Set'}</div>
        </div>
        <div className={`p-5 rounded-2xl glass-card border border-white/20`}>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Phone / Email</div>
          <div className="text-lg font-bold text-slate-800">{userData?.phone || '+91 00000000'} <br/><span className="text-sm font-semibold text-slate-600 mt-1 inline-block">{userData?.email || 'email@example.com'}</span></div>
        </div>
        <div className={`p-5 rounded-2xl glass-card border border-white/20`}>
          <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Sanctuary Location</div>
          <div className="text-lg font-bold text-slate-800 flex items-center gap-2"><MapPin size={20} className="text-[#3A7070]"/> {userData?.place || 'Salem, TN'}</div>
        </div>
      </div>
    </div>
  </div>
);

// ==========================================
// 5. MASTER PATIENT DASHBOARD
// ==========================================
const PatientDashboard = ({ setView, userData }) => {
  const [activePage, setActivePage] = useState('chat');
  const [globalPoints, setGlobalPoints] = useState(0);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth >= 768);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (!mobile) setIsSidebarOpen(true);
      else setIsSidebarOpen(false);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const menuItems = [
    { id: 'chat', label: 'Chat with Keffi', icon: MessageCircle },
    { id: 'history', label: 'Peace Log', icon: BookOpen },
    { id: 'journey', label: 'My Journey', icon: TrendingUp },
    { id: 'tools', label: 'Mind Tools', icon: Sparkles },
    { id: 'rewards', label: 'Rewards', icon: Gift },
    { id: 'friends', label: 'Neighbor Sync', icon: Users }, 
    { id: 'account', label: 'My Account', icon: Shield },
  ];

  const renderContent = () => {
    switch(activePage) {
      case 'chat': return <ChatArea setGlobalPoints={setGlobalPoints} globalPoints={globalPoints} userData={userData} />;
      case 'history': return <PeaceLog />;
      case 'journey': return <MyJourney />;
      case 'tools': return <MindTools />;
      case 'rewards': return <Rewards points={globalPoints} />;
      case 'friends': return <FriendsSync />;
      case 'account': return <ProfileVault userData={userData} />;
      default: return <ChatArea setGlobalPoints={setGlobalPoints} globalPoints={globalPoints} userData={userData} />;
    }
  };

  return (
    <div className="flex h-screen w-screen bg-transparent overflow-hidden font-inter text-slate-800 relative">
      
      {/* Mobile Overlay */}
      {isMobile && isSidebarOpen && (
        <div className="absolute inset-0 bg-black/40 z-20 backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)}></div>
      )}

      {/* Sleek Collapsible Sidebar */}
      <div className={`${isSidebarOpen ? 'w-64 md:w-72 translate-x-0' : 'w-64 md:w-0 -translate-x-full md:translate-x-0 md:opacity-0'} absolute md:relative z-30 transition-all duration-300 h-full glass-sidebar flex flex-col shrink-0 overflow-hidden`}>
        {/* Light Green Animated Background */}
        <div className="absolute -top-[10%] -left-[10%] w-[120%] h-[50%] bg-[#8FA989] rounded-full mix-blend-multiply blur-[80px] opacity-[0.12] animate-pulse pointer-events-none z-0" style={{animationDuration: '4s'}}></div>
        <div className="absolute -bottom-[10%] -right-[10%] w-[120%] h-[50%] bg-[#EAF4F0] rounded-full mix-blend-multiply blur-[80px] opacity-40 pointer-events-none z-0" style={{animation: 'pulse 8s infinite alternate'}}></div>

        {isSidebarOpen && (
          <div className="flex flex-col h-full w-full p-6 relative z-10">
            <div className="flex items-center gap-3 cursor-pointer mb-8" onClick={() => setView('landing')}>
               <KeffiLogo size="w-8 h-8" />
               <h1 className="text-2xl font-black text-[#2C5555] tracking-tight">Keffi AI</h1>
            </div>
            
            <div className="flex-1 space-y-2 overflow-y-auto scrollbar-hide">
              {menuItems.map(item => {
                const IconComponent = item.icon;
                const isActive = activePage === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActivePage(item.id);
                      if (isMobile) setIsSidebarOpen(false);
                    }}
                    className={`w-full flex items-center gap-4 px-5 py-4 rounded-[1.2rem] font-bold text-sm transition-all duration-300 cursor-pointer ${
                      isActive 
                      ? 'bg-[#3A7070] text-white shadow-md shadow-[#3A7070]/20' 
                      : 'text-slate-600 hover:bg-white/40 hover:text-[#3A7070]'
                    }`}
                  >
                    <IconComponent size={18} /> {item.label}
                  </button>
                )
              })}
            </div>

            <div className="mt-6 px-4 py-4 rounded-[1.2rem] glass-card border border-white/30 font-bold text-xs text-[#D4A373] flex items-center justify-center gap-2 shrink-0">
              <Star size={16} className="fill-[#D4A373] text-[#D4A373] animate-pulse" /> {globalPoints} Sanctuary Points
            </div>

            <button onClick={() => setView('landing')} className="mt-4 text-slate-500 hover:text-slate-700 font-bold text-sm transition-all w-full text-center shrink-0 cursor-pointer">
              Exit Sanctuary
            </button>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div className="flex-1 h-full w-full min-w-0 bg-transparent relative flex flex-col overflow-hidden">
        {(!isSidebarOpen || isMobile) && (
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="absolute top-4 md:top-6 left-4 md:left-6 z-10 p-2.5 text-slate-600 hover:text-[#3A7070] glass-card border border-white/20 rounded-xl hover:bg-white/50 hover:-translate-y-0.5 transition-all cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
        )}
        
        {/* Render Active View */}
        {renderContent()}
      </div>
    </div>
  );
};

// ==========================================
// 6. ENHANCED ADMIN DASHBOARD
// ==========================================
const AdminDashboard = ({ setView }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patients, setPatients] = useState([]);
  const [inactivePatients, setInactivePatients] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resPat, resInact, resAnalyt] = await Promise.all([
          axios.get('https://balajikrishnan031-keffi-backend.hf.space/api/admin/patients'),
          axios.get('https://balajikrishnan031-keffi-backend.hf.space/api/admin/inactive-patients'),
          axios.get('https://balajikrishnan031-keffi-backend.hf.space/api/admin/analytics')
        ]);
        if (resPat.data && resPat.data.patients) setPatients(resPat.data.patients);
        if (resInact.data && resInact.data.patients) setInactivePatients(resInact.data.patients);
        if (resAnalyt.data) setAnalytics(resAnalyt.data);
      } catch (err) {
        console.error("Failed to fetch admin data", err);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const adminTabs = [
    { id: 'overview', label: 'System Overview', icon: Activity },
    { id: 'roster', label: 'Patient Roster', icon: Users },
    { id: 'inactive', label: 'Inactive Patients', icon: Frown },
    { id: 'analytics', label: 'NLP Analytics', icon: PieChart },
    { id: 'therapists', label: 'Therapists Allocation', icon: Shield },
    { id: 'settings', label: 'System Settings', icon: Settings },
  ];

  const handleExportAbstract = async (patientId) => {
    try {
      const res = await axios.get(`https://balajikrishnan031-keffi-backend.hf.space/api/patient/${patientId}/report`);
      const data = res.data;
      const content = `Clinical Abstract for ${data.name || data.patient_id}\n\nMHQ Score: ${data.current_mhq}\nRisk Level: ${data.depression_level}\nAssigned Doctor: ${data.assigned_doctor || 'Unassigned'}\n\nSummary:\n${data.clinical_abstract}\n`;
      const blob = new Blob([content], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `abstract_${patientId}.txt`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch(err) {
      console.error(err);
      alert("Failed to export abstract.");
    }
  };

  const assignTherapist = async (patientId, docName) => {
    try {
      await axios.post('https://balajikrishnan031-keffi-backend.hf.space/api/admin/assign-therapist', { patient_id: patientId, doctor_name: docName });
      alert(`Successfully assigned ${docName} to ${patientId}`);
    } catch(err) {
      console.error(err);
    }
  };

  return (
    <div className="flex h-screen w-full bg-transparent overflow-hidden p-6 gap-6 font-sans text-slate-800">
      <div className="w-72 h-full rounded-[2rem] glass-panel border border-white/20 shadow-sm flex flex-col p-6 shrink-0">
        <div className="flex flex-col items-center mb-8 pt-4 cursor-pointer" onClick={() => setView('landing')}>
          <div className="w-12 h-12 rounded-2xl bg-white/20 border border-white/30 flex items-center justify-center text-[#3A7070] mb-4"><Shield size={24} /></div>
          <h1 className="text-xl font-black text-[#2C5555] tracking-tight text-center">Clinical Hub</h1>
        </div>
        
        <div className="flex-1 space-y-2">
          {adminTabs.map(tab => (
            <button key={tab.id} onClick={() => {setActiveTab(tab.id); setSelectedPatient(null);}} 
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all duration-300 cursor-pointer ${activeTab === tab.id ? `bg-[#3A7070]/10 border border-[#3A7070]/15 text-[#3A7070] shadow-sm` : `text-slate-600 hover:text-[#3A7070] hover:bg-white/40`}`}>
               <tab.icon size={18} /> {tab.label}
            </button>
          ))}
        </div>
        <button onClick={() => setView('landing')} className="mt-auto font-bold text-sm text-slate-500 hover:text-red-500 hover:bg-red-500/10 p-4 rounded-xl transition-all cursor-pointer">Logout</button>
      </div>

      <div className="flex-1 h-full relative">
        <div className="absolute inset-0 rounded-[2rem] glass-panel border border-white/25 shadow-inner p-8 overflow-hidden">
          {selectedPatient ? (
             <div className={`h-full flex flex-col animate-fade-in`}>
                <div className="flex justify-between items-center mb-6">
                  <div className="flex items-center gap-4">
                    <button onClick={() => setSelectedPatient(null)} className={`p-2.5 rounded-full bg-white border border-slate-200 shadow-sm text-slate-500 hover:bg-slate-50`}><ArrowRight className="rotate-180" size={18}/></button>
                    <h2 className="text-xl font-black text-slate-800">Patient: {selectedPatient.id}</h2>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="px-4 py-1.5 rounded-xl bg-white border border-slate-100 shadow-sm font-bold text-xs text-slate-600 flex items-center gap-2">
                      Current Chat Category: <span className={
                        selectedPatient.category?.includes("Depression") || selectedPatient.category?.includes("Panic") || selectedPatient.category?.includes("Grief") ? "text-red-500" :
                        selectedPatient.category?.includes("Anxiety") || selectedPatient.category?.includes("Exhaustion") || selectedPatient.category?.includes("Burnout") ? "text-orange-500" :
                        "text-emerald-500"
                      }>
                        {selectedPatient.category?.includes("Depression") || selectedPatient.category?.includes("Panic") || selectedPatient.category?.includes("Grief") ? "🔴" :
                        selectedPatient.category?.includes("Anxiety") || selectedPatient.category?.includes("Exhaustion") || selectedPatient.category?.includes("Burnout") ? "🟠" :
                        "🟢"} [{selectedPatient.category || 'Normal Stress / Positive'}]
                      </span>
                    </div>
                    <div className={`px-4 py-1.5 rounded-xl bg-white border border-slate-100 shadow-sm font-bold text-xs ${selectedPatient.color}`}>Risk: {selectedPatient.risk}</div>
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-6 flex-1">
                  <div className={`col-span-1 p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col gap-4`}>
                    <h3 className="text-base font-bold text-slate-800">Depression / MHQ Score</h3>
                    <div className="flex-1 flex flex-col justify-center items-center gap-2">
                       <span className={`text-4xl font-black ${selectedPatient.color}`}>{selectedPatient.score}</span>
                       <span className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-2">Current Score</span>
                    </div>
                  </div>
                  <div className={`col-span-2 p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col`}>
                    <h3 className="text-base font-bold text-slate-800 mb-3">Recent Logs</h3>
                    <div className={`flex-1 bg-white/10 border border-white/10 rounded-xl p-4 overflow-y-auto`}>
                      {selectedPatient.logs.map((l,i) => <div key={i} className="p-3 mb-3 glass-card rounded-lg shadow-sm border border-white/15 text-xs font-semibold text-slate-700">{l}</div>)}
                    </div>
                  </div>
                </div>
             </div>
          ) : activeTab === 'overview' ? (
            <div className="h-full flex flex-col animate-fade-in">
               <h2 className="text-2xl font-black text-slate-800 mb-6">System Overview</h2>
               <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                 <div className={`p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col items-center text-center gap-1`}>
                    <div className="text-3xl font-black text-[#3A7070]">{analytics?.total_patients || patients.length}</div>
                    <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Active Patients</div>
                 </div>
                 <div className={`p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col items-center text-center gap-1`}>
                    <div className="text-3xl font-black text-[#8FA989]">{analytics?.safety_score || '0'}%</div>
                    <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">AI Safety Score</div>
                 </div>
                 <div className={`p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col items-center text-center gap-1`}>
                    <div className="text-3xl font-black text-red-500">{patients.filter(p => p.risk === 'Critical').length}</div>
                    <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Critical Interventions</div>
                 </div>
               </div>
               <div className={`flex-1 p-5 rounded-2xl glass-card border border-white/25 shadow-sm flex flex-col`}>
                  <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2"><Bell size={20}/> Urgent Alerts Stream</h3>
                  <div className={`flex-1 rounded-xl bg-white/15 border border-white/10 p-4 overflow-y-auto space-y-3`}>
                    {patients.filter(p => p.risk === 'Critical').length === 0 && <div className="text-slate-500 font-semibold text-sm">No urgent alerts.</div>}
                    {patients.filter(p => p.risk === 'Critical').map(p => (
                      <div key={p.id} className="p-4 rounded-xl glass-card border border-red-500/25 border-l-4 border-l-red-500 shadow-sm">
                        <div className="font-bold text-red-600 text-sm mb-1">{p.id} ({p.name}): Critical Risk Detected.</div>
                        <div className="text-slate-700 text-xs font-semibold">MHQ Score: {p.score}. AI monitoring closely. Consider manual intervention.</div>
                      </div>
                    ))}
                  </div>
               </div>
            </div>
          ) : activeTab === 'roster' ? (
            <div className="h-full flex flex-col animate-fade-in">
               <div className="flex justify-between items-center mb-5">
                 <h2 className="text-2xl font-black text-slate-800">Patient Roster</h2>
                 <div className={`flex items-center gap-3 px-3 py-2 rounded-xl glass-input w-64 shadow-sm`}>
                   <Search size={18} className="text-slate-500"/>
                   <input type="text" placeholder="Search ID..." className="bg-transparent outline-none flex-1 text-slate-800 font-bold text-sm"/>
                 </div>
               </div>
               <div className={`flex-1 rounded-2xl glass-card border border-white/25 shadow-sm p-5 flex flex-col`}>
                  <div className="flex justify-between items-center px-4 font-bold text-slate-500 uppercase text-xs tracking-widest border-b border-white/10 pb-2 mb-3">
                    <span className="w-1/4">Patient ID</span>
                    <span className="w-1/4">Condition</span>
                    <span className="w-1/4 text-center">Risk Level</span>
                    <span className="w-1/4 text-right">Action</span>
                  </div>
                  <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                    {patients.length === 0 && <div className="text-center text-slate-500 font-semibold mt-6 text-sm">No patients tracked yet.</div>}
                    {patients.map(p => (
                      <div key={p.id} className={`flex justify-between items-center p-3 rounded-xl bg-white/20 border border-white/10`}>
                        <span className="w-1/4 font-black text-slate-800 text-sm">{p.id}</span>
                        <span className="w-1/4 text-slate-700 font-semibold text-xs">{p.condition}</span>
                        <span className={`w-1/4 text-center font-bold text-xs ${p.color}`}>{p.risk}</span>
                        <span className="w-1/4 text-right">
                          <button onClick={() => setSelectedPatient(p)} className={`px-3 py-1.5 rounded-lg text-xs font-bold border border-white/30 text-slate-700 hover:bg-white/40 mr-2 transition-colors cursor-pointer`}>Inspect</button>
                          <button onClick={() => handleExportAbstract(p.id)} className={`px-3 py-1.5 rounded-lg text-xs font-bold bg-[#8FA989] text-white shadow-sm hover:bg-[#7a9474] transition-colors cursor-pointer`}>Export Abstract</button>
                        </span>
                      </div>
                    ))}
                  </div>
               </div>
            </div>
          ) : activeTab === 'inactive' ? (
            <div className="h-full flex flex-col animate-fade-in">
               <h2 className="text-2xl font-black text-slate-800 mb-5">Inactive Patients (3+ Days)</h2>
               <div className={`flex-1 rounded-2xl glass-card border border-white/25 shadow-sm p-5 flex flex-col`}>
                  <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                    {inactivePatients.length === 0 && <div className="text-center text-slate-500 font-semibold mt-6 text-sm">No inactive patients found.</div>}
                    {inactivePatients.map((p, i) => (
                      <div key={i} className={`flex justify-between items-center p-4 rounded-xl bg-white/20 border border-white/10`}>
                        <div>
                           <div className="font-black text-slate-800 text-sm mb-1">{p.patient_id} ({p.name})</div>
                           <div className="text-slate-600 text-xs font-semibold">Inactive for {p.days_inactive} days</div>
                        </div>
                        <div className="text-right">
                           <div className="font-bold text-slate-800 text-sm mb-1">MHQ: {p.mhq_score}</div>
                           <div className="text-slate-600 text-xs font-semibold">{p.depression_level}</div>
                        </div>
                      </div>
                    ))}
                  </div>
               </div>
            </div>
          ) : activeTab === 'analytics' ? (
            <div className="h-full flex flex-col animate-fade-in">
               <h2 className="text-2xl font-black text-slate-800 mb-5">NLP & Sentiment Analytics</h2>
               <div className="grid grid-cols-2 gap-5 flex-1">
                 <div className={`p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col`}>
                    <h3 className="text-base font-bold text-slate-800 mb-3">Platform Sentiment Trend</h3>
                    <div className={`flex-1 bg-white/15 border border-white/10 rounded-xl p-3 flex items-end gap-2`}>
                      {[40, 60, 30, 80, 90, 50, 70].map((h, i) => (
                        <div key={i} className="flex-1 bg-[#3A7070] rounded-t-md transition-all hover:bg-[#8FA989]" style={{height: `${h}%`}}></div>
                      ))}
                    </div>
                    <div className="flex justify-between mt-2 text-slate-500 font-bold text-[10px] uppercase tracking-widest"><span>Mon</span><span>Sun</span></div>
                 </div>
                 <div className={`p-5 rounded-2xl glass-card border border-white/20 shadow-sm flex flex-col`}>
                    <h3 className="text-base font-bold text-slate-800 mb-4">Top Detected Emotions</h3>
                    <div className="flex flex-col gap-3 flex-1 justify-center overflow-y-auto pr-2">
                       {analytics && analytics.category_distribution && Object.entries(analytics.category_distribution).length > 0 ? Object.entries(analytics.category_distribution).map(([emotion, count], i) => (
                         <div key={i}>
                           <div className="flex justify-between font-bold text-xs text-slate-700 mb-1"><span>{emotion}</span><span>{count} msgs</span></div>
                           <div className="w-full bg-white/15 border border-white/10 rounded-full h-2.5"><div className="bg-[#3A7070] h-2.5 rounded-full" style={{width: `${Math.min(count * 5, 100)}%`}}></div></div>
                         </div>
                       )) : <div className="text-slate-500 text-sm font-semibold">No data available yet.</div>}
                    </div>
                 </div>
               </div>
            </div>
          ) : activeTab === 'therapists' ? (
            <div className="h-full flex flex-col animate-fade-in">
               <h2 className="text-2xl font-black text-slate-800 mb-5">Therapist Allocation</h2>
               <div className={`flex-1 rounded-2xl glass-card border border-white/25 shadow-sm p-5 flex flex-col`}>
                  <div className="grid grid-cols-1 gap-3 overflow-y-auto">
                    {patients.filter(p => p.risk === 'Critical' || p.risk === 'High').length === 0 && <div className="text-slate-500 font-semibold p-4 text-sm">No critical or high-risk patients needing assignment.</div>}
                    {patients.filter(p => p.risk === 'Critical' || p.risk === 'High').map((p) => (
                      <div key={p.id} className={`p-3 rounded-xl bg-white/20 border border-white/10 flex items-center justify-between`}>
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-full bg-white/30 border border-white/40 shadow-sm flex items-center justify-center text-[#3A7070]`}><User size={18}/></div>
                          <div>
                            <h4 className="text-sm font-bold text-slate-800">{p.id} ({p.name})</h4>
                            <span className={`text-[10px] font-bold ${p.color} uppercase tracking-widest`}>{p.risk} Risk</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <select id={`doc-select-${p.id}`} className="p-2 rounded-lg glass-input outline-none text-xs font-bold text-slate-800 shadow-sm cursor-pointer">
                            <option value="">Select Doctor</option>
                            <option value="Dr. Sarah Jenkins">Dr. Sarah Jenkins</option>
                            <option value="Dr. Arun Kumar">Dr. Arun Kumar</option>
                            <option value="Dr. Emily Chen">Dr. Emily Chen</option>
                          </select>
                          <button onClick={() => {
                            const sel = document.getElementById(`doc-select-${p.id}`);
                            if(sel.value) assignTherapist(p.id, sel.value);
                          }} className={`px-3 py-2 rounded-lg font-bold text-xs bg-white/40 border border-[#3A7070]/30 text-[#3A7070] hover:bg-[#3A7070] hover:text-white transition-all shadow-sm cursor-pointer`}>
                            {p.assigned_doctor && p.assigned_doctor !== 'Unassigned' ? `Reassign` : 'Assign'}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
               </div>
            </div>
          ) : (
            <div className="h-full flex flex-col animate-fade-in">
               <h2 className="text-2xl font-black text-slate-800 mb-5">System Settings</h2>
               <div className={`flex-1 rounded-2xl glass-card border border-white/25 shadow-sm p-6 flex flex-col gap-5`}>
                  <div className={`p-5 rounded-xl bg-white/20 border border-white/10 flex items-center justify-between`}>
                     <div>
                        <h3 className="text-sm font-bold text-slate-800 mb-1">AI Empathy Level</h3>
                        <p className="text-xs text-slate-500 font-medium">Adjust the depth of Socratic questioning.</p>
                     </div>
                     <input type="range" min="1" max="100" defaultValue="80" className="w-40 accent-[#3A7070] cursor-pointer"/>
                  </div>
                  <div className={`p-5 rounded-xl bg-white/20 border border-white/10 flex items-center justify-between`}>
                     <div>
                        <h3 className="text-sm font-bold text-slate-800 mb-1">Emergency Hotlines (iCall India)</h3>
                        <p className="text-xs text-slate-500 font-medium">Automatically trigger on Critical Risk detection.</p>
                     </div>
                     <div className="w-10 h-6 bg-[#8FA989] rounded-full relative cursor-pointer"><div className="absolute right-1 top-1 bg-white w-4 h-4 rounded-full shadow-sm"></div></div>
                  </div>
                  <div className={`p-5 rounded-xl bg-white/20 border border-white/10 flex items-center justify-between`}>
                     <div>
                        <h3 className="text-sm font-bold text-slate-800 mb-1">Clear NLP Cache</h3>
                        <p className="text-xs text-slate-500 font-medium">Free up memory used by BERT classifier.</p>
                     </div>
                     <button className={`px-4 py-2 rounded-lg font-bold text-xs bg-white/40 border border-slate-300 text-slate-700 shadow-sm hover:bg-white/60 transition-all cursor-pointer`}>Clear Cache</button>
                  </div>
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// MAIN APP ROUTER
// ==========================================
export default function App() {
  const saved = (() => { try { return JSON.parse(localStorage.getItem('keffi_user')); } catch { return null; } })();
  const [view, setView] = useState(saved ? 'patient-dashboard' : 'landing');
  const [userData, setUserData] = useState(saved || null);

  const handleLogout = () => {
    localStorage.removeItem('keffi_user');
    setUserData(null);
    setView('landing');
  };

  const viewComponent = () => {
    switch(view) {
      case 'landing': return <LandingPage setView={setView} />;
      case 'login-patient': return <PatientLogin setView={setView} setUserData={setUserData} />;
      case 'login-admin': return <AdminLogin setView={setView} />;
      case 'patient-dashboard': return <PatientDashboard setView={setView} userData={userData} onLogout={handleLogout} />;
      case 'admin-dashboard': return <AdminDashboard setView={setView} />;
      default: return <LandingPage setView={setView} />;
    }
  };

  return (
    <div className="font-inter min-h-screen w-full">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800;900&family=Playfair+Display:ital,wght@1,500;1,700&display=swap');
        
        .cursive-accent {
          font-family: 'Playfair Display', serif;
          font-style: italic;
          font-weight: 700;
        }
        
        body {
          margin: 0;
          padding: 0;
          background-image: url('/keffi-bg.png');
          background-size: cover;
          background-position: center;
          background-attachment: fixed;
          background-repeat: no-repeat;
          background-color: #F2F9F6;
          font-family: 'Inter', sans-serif;
          color: #1E293B;
        }
        h1, h2, h3, h4, h5, h6 { font-family: 'Poppins', sans-serif; }
        
        .font-poppins { font-family: 'Poppins', sans-serif; }
        .font-inter { font-family: 'Inter', sans-serif; }
        
        .h1-title { font-size: 64px; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em; }
        .h2-title { font-size: 48px; font-weight: 700; line-height: 1.15; letter-spacing: -0.01em; }
        .h3-title { font-size: 28px; font-weight: 600; line-height: 1.3; }
        .p-text { font-size: 20px; font-weight: 400; line-height: 1.7; color: #475569; }
        .p-small { font-size: 18px; font-weight: 400; line-height: 1.7; color: #64748B; }
        
        @media (max-width: 768px) {
          .h1-title { font-size: 42px; }
          .h2-title { font-size: 36px; }
        }

        .floating-blob {
          position: absolute;
          border-radius: 50%;
          filter: blur(120px);
          opacity: 0.4;
          z-index: 0;
          animation: float 10s ease-in-out infinite;
        }
        
        @keyframes float {
          0% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(-30px) scale(1.05); }
          100% { transform: translateY(0px) scale(1); }
        }
      `}</style>
      
      {viewComponent()}
    </div>
  );
}
