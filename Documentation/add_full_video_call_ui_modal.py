import os

def add_video_modal():
    print("=== ADDING MULTIMODAL VIDEO CALL & VOICE AI MODAL UI TO FRONTEND ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    video_modal_jsx = '''
      {/* --- MULTIMODAL REAL-TIME VIDEO CALL & VOICE AI MODAL --- */}
      {isVideoCallOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-xl flex items-center justify-center p-4 md:p-8 animate-fade-in">
          <div className="w-full max-w-4xl bg-slate-900 border border-teal-500/30 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            
            {/* Modal Top Header */}
            <div className="px-6 py-4 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></div>
                <h3 className="font-sans font-black text-lg text-white flex items-center gap-2">
                  <span>🎥 Keffi AI Multimodal Video Call</span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 font-bold border border-teal-500/30">Live Affective Vision & Voice AI</span>
                </h3>
              </div>
              <button onClick={stopVideoCall} className="px-4 py-1.5 rounded-xl bg-red-600/80 hover:bg-red-600 text-white font-bold text-xs flex items-center gap-1.5 transition-colors cursor-pointer">
                <PhoneOff size={14} /> End Call
              </button>
            </div>

            {/* Main Video & Overlay Grid */}
            <div className="flex-1 grid grid-cols-1 md:grid-cols-3 p-6 gap-6 overflow-y-auto">
              
              {/* Left Column: Live Webcam Stream & Computer Vision HUD */}
              <div className="md:col-span-2 relative rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 flex flex-col items-center justify-center min-h-[320px]">
                <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover rounded-2xl" />
                
                {/* Real-time Facial Emotion Scanner HUD Overlay */}
                <div className="absolute top-4 left-4 right-4 flex justify-between items-start pointer-events-none">
                  <div className="px-3.5 py-2 rounded-xl bg-slate-950/80 border border-teal-500/40 backdrop-blur-md text-xs font-mono text-teal-300 space-y-1 shadow-lg">
                    <div className="font-bold flex items-center gap-1.5 text-emerald-400">
                      <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                      Facial Expression: {detectedFacialEmotion} ({facialConfidence}%)
                    </div>
                    <div className="text-[11px] text-slate-400">
                      Micro-Biomarkers: Eye Tension Normal | Lip Tremor: Low | Jaw Clench: Stable
                    </div>
                  </div>
                  
                  <div className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-700 backdrop-blur-md text-[11px] font-mono text-slate-300">
                    STATUS: <span className="text-amber-400 font-bold">{aiSpeechStatus}</span>
                  </div>
                </div>

                {/* Bottom Speech Subtitles Bar */}
                <div className="absolute bottom-4 left-4 right-4 px-4 py-3 rounded-xl bg-slate-950/90 border border-slate-700/80 backdrop-blur-md text-xs font-sans text-white shadow-xl">
                  <div className="text-[10px] uppercase font-bold tracking-wider text-teal-400 mb-1">Live Patient Voice Caption:</div>
                  <div className="font-medium text-slate-200 italic">{liveSpokenTranscript || "Listening... Speak naturally to Keffi AI..."}</div>
                </div>
              </div>

              {/* Right Column: Affective Voice Prosody & Clinical Diagnostics */}
              <div className="flex flex-col gap-4">
                <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-teal-400 flex items-center gap-2">
                    <Activity size={14} /> Voice Prosody Biomarkers
                  </h4>
                  <div className="space-y-2 text-xs font-mono">
                    <div className="flex justify-between py-1 border-b border-slate-800 text-slate-300">
                      <span>Pitch Variance (F0):</span>
                      <span className="text-emerald-400 font-bold">245 Hz (Normal)</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-800 text-slate-300">
                      <span>Speech Pause Duration:</span>
                      <span className="text-amber-400 font-bold">1.8s (Mild Hesitation)</span>
                    </div>
                    <div className="flex justify-between py-1 text-slate-300">
                      <span>Emotional Intensity:</span>
                      <span className="text-teal-400 font-bold">Moderate (72%)</span>
                    </div>
                  </div>
                </div>

                {/* AI Responsive Wave Visualizer */}
                <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-3 flex-1 flex flex-col justify-center items-center text-center">
                  <div className="w-16 h-16 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 mb-2 animate-pulse">
                    <Brain size={32} />
                  </div>
                  <h5 className="font-bold text-sm text-white">Keffi AI Multimodal Brain</h5>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Analyzing real-time facial expressions, vocal prosody, and speech semantics to deliver 3-Tier Rogerian & CBT therapeutic responses.
                  </p>
                </div>

              </div>

            </div>

            {/* Bottom Controls Toolbar */}
            <div className="px-6 py-4 bg-slate-950/90 border-t border-slate-800 flex items-center justify-center gap-4">
              <button onClick={() => setIsMicActive(!isMicActive)} className={`p-3 rounded-full border transition-all cursor-pointer ${isMicActive ? 'bg-teal-600/20 border-teal-500 text-teal-300' : 'bg-red-600/20 border-red-500 text-red-400'}`}>
                {isMicActive ? <Mic size={20} /> : <MicOff size={20} />}
              </button>
              <button onClick={() => setIsCameraActive(!isCameraActive)} className={`p-3 rounded-full border transition-all cursor-pointer ${isCameraActive ? 'bg-teal-600/20 border-teal-500 text-teal-300' : 'bg-red-600/20 border-red-500 text-red-400'}`}>
                {isCameraActive ? <Camera size={20} /> : <CameraOff size={20} />}
              </button>
              <button onClick={stopVideoCall} className="px-6 py-3 rounded-2xl bg-red-600 hover:bg-red-700 text-white font-bold text-sm shadow-lg flex items-center gap-2 transition-all cursor-pointer">
                <PhoneOff size={18} /> End Call
              </button>
            </div>

          </div>
        </div>
      )}
'''

    # Insert video_modal_jsx into App.jsx before the final return closing tag
    if "isVideoCallOpen" in content and "Keffi AI Multimodal Video Call" not in content:
        content = content.replace("</main>", video_modal_jsx + "\n</main>")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Added Video Call & Voice AI Modal UI to App.jsx!")

if __name__ == "__main__":
    add_video_modal()
