import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu,
  Layers,
  Activity,
  FileCheck,
  ChevronRight,
  Terminal,
  Maximize2,
  Download,
  Search,
  Sparkles,
  Zap,
  Box,
  Layout,
  ClipboardList,
  Truck
} from 'lucide-react';

import BlockDiagram from './components/BlockDiagram';
import SchematicView from './components/SchematicView';
import PCBView from './components/PCBView';
import BOMView from './components/BOMView';
import { generateHardware, getDownloadUrl } from './api';

const App = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [activeTab, setActiveTab] = useState('block');
  const [prompt, setPrompt] = useState('');
  const [circuitData, setCircuitData] = useState(null);
  const [files, setFiles] = useState({});
  const [error, setError] = useState(null);

  const steps = [
    { id: 'parsing', label: 'Understanding Intent', icon: Search },
    { id: 'planning', label: 'Planning Electronics', icon: Zap },
    { id: 'selection', label: 'Selecting Components', icon: Cpu },
    { id: 'schematic', label: 'Designing Schematic', icon: Activity },
    { id: 'pcb', label: 'Laying out PCB', icon: Layers },
    { id: 'verify', label: 'Verifying Design', icon: FileCheck },
  ];

  const examples = [
    "Smart irrigation controller",
    "IoT energy meter",
    "EV battery monitor",
    "Robotics motor driver",
    "Smart door lock"
  ];

  const handleGenerate = async () => {
    if (!prompt) return;
    setIsGenerating(true);
    setCurrentStep(0);
    setError(null);
    setCircuitData(null);

    try {
      // Start mock progress while fetching
      const progressTimer = setInterval(() => {
        setCurrentStep(prev => (prev < 2 ? prev + 1 : prev));
      }, 1000);

      const result = await generateHardware(prompt);

      clearInterval(progressTimer);

      // Fast forward to complete
      setCurrentStep(steps.length);
      setCircuitData(result.circuit);
      setFiles(result.files);
    } catch (err) {
      setError(err.message);
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <div className="lab-grid" />

      {/* Background Glows */}
      <div className="glow glow-1" />
      <div className="glow glow-2" />

      {/* Main Layout */}
      <div className="layout-root">

        {/* Header / Brand */}
        <header className="app-header glass">
          <div className="brand">
            <div className="brand-icon pulse">
              <Zap size={18} fill="currentColor" />
            </div>
            <h1>AI Hardware Designer</h1>
            <span className="version">v1.2.0 • PRO</span>
          </div>
          <div className="header-actions">
            <button className="btn-icon"><Maximize2 size={18} /></button>
            <div className="divider" />
            <button className="btn-primary">
              <Sparkles size={16} />
              <span>Connect CAD</span>
            </button>
          </div>
        </header>

        <main className="app-content">
          {/* Landing State or Workspace */}
          <AnimatePresence mode="wait">
            {!isGenerating ? (
              <motion.div
                key="landing"
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, y: -20 }}
                className="hero-section"
              >
                <div className="hero-content">
                  <div className="hero-tag">Next-Gen Electronics Design</div>
                  <h2>What hardware are you building?</h2>

                  <div className="input-container glass">
                    <input
                      type="text"
                      placeholder="Describe your hardware idea (e.g. ESP32 irrigation controller...)"
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                    />
                    <button
                      className={`generate-btn ${prompt ? 'active' : ''}`}
                      onClick={handleGenerate}
                    >
                      <Sparkles size={18} />
                      <span>Generate PCB</span>
                    </button>
                  </div>

                  <div className="example-chips">
                    {examples.map(ex => (
                      <button
                        key={ex}
                        className="chip"
                        onClick={() => setPrompt(ex)}
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="workspace"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="workspace-layout"
              >
                {/* Left Panel: Design Brain */}
                <aside className="panel-left glass">
                  <div className="panel-header">
                    <Terminal size={16} />
                    <h3>Design Brain</h3>
                  </div>
                  <div className="timeline">
                    {steps.map((step, idx) => {
                      const Icon = step.icon;
                      const isActive = idx === currentStep;
                      const isCompleted = idx < currentStep;
                      return (
                        <div key={step.id} className={`timeline-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                          <div className="step-indicator">
                            <Icon size={14} />
                            {isCompleted && <div className="check-dot" />}
                          </div>
                          <span>{step.label}</span>
                          {isActive && <motion.div layoutId="pulse" className="active-glow" />}
                        </div>
                      );
                    })}
                  </div>

                  <div className="intelligence-log">
                    <h4>Internal Reasoning</h4>
                    <div className="log-entries">
                      <div className="log-entry">Identifying power requirements: 12V DC input confirmed.</div>
                      {currentStep > 1 && <div className="log-entry">Selecting ESP32-WROOM-32E for WiFi/BLE support.</div>}
                      {currentStep > 2 && <div className="log-entry">Adding 10uF and 100nF decoupling capacitors to MCU.</div>}
                      {currentStep > 3 && <div className="log-entry">Calculating trace widths for power nets (20 mil).</div>}
                    </div>
                  </div>
                </aside>

                {/* Center Panel: Workspace */}
                <section className="panel-center">
                  <div className="workspace-viewer glass">
                    <div className="viewer-header">
                      <div className="tabs-mini">
                        {['block', 'schematic', 'pcb'].map(tab => (
                          <button
                            key={tab}
                            className={`tab-mini ${activeTab === tab ? 'active' : ''}`}
                            onClick={() => setActiveTab(tab)}
                          >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                          </button>
                        ))}
                      </div>
                      <div className="viewer-actions">
                        <button className="btn-ghost"><Maximize2 size={14} /></button>
                      </div>
                    </div>

                    <div className="viewer-content">
                      <AnimatePresence mode="wait">
                        {activeTab === 'block' && (
                          <motion.div
                            key="block"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="viz-container"
                          >
                            <BlockDiagram currentStep={currentStep} />
                          </motion.div>
                        )}
                        {activeTab === 'schematic' && (
                          <motion.div
                            key="schematic"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="viz-container"
                          >
                            <SchematicView />
                          </motion.div>
                        )}
                        {activeTab === 'pcb' && (
                          <motion.div
                            key="pcb"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="viz-container"
                          >
                            <PCBView />
                          </motion.div>
                        )}
                        {activeTab === 'bom' && (
                          <motion.div
                            key="bom"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="viz-container"
                          >
                            <BOMView circuit={circuitData} />
                          </motion.div>
                        )}
                        {activeTab === 'manufacturing' && (
                          <motion.div
                            key="mfg"
                            className="viz-container"
                          >
                            <div className="placeholder-viz">
                              <Download size={48} />
                              <p>Manufacturing Files Ready</p>
                              <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                                <a
                                  href={files.bom ? getDownloadUrl(files.bom) : '#'}
                                  className="btn-primary"
                                  download
                                >
                                  Download BOM
                                </a>
                                <a
                                  href={files.schematic ? getDownloadUrl(files.schematic) : '#'}
                                  className="btn-primary"
                                  download
                                >
                                  Download KiCad Schematic
                                </a>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>

                  {/* Navigation Tabs (Bottom) */}
                  <nav className="bottom-nav glass">
                    {[
                      { id: 'block', label: 'Block Diagram', icon: Box },
                      { id: 'schematic', label: 'Schematic', icon: Activity },
                      { id: 'pcb', label: 'PCB Layout', icon: Layout },
                      { id: 'bom', label: 'BOM', icon: ClipboardList },
                      { id: 'manufacturing', label: 'Manufacturing', icon: Truck },
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                      >
                        <tab.icon size={16} />
                        <span>{tab.label}</span>
                        {activeTab === tab.id && (
                          <motion.div layoutId="nav-glow" className="nav-glow" />
                        )}
                      </button>
                    ))}
                  </nav>
                </section>

                {/* Right Panel: Inspector */}
                <aside className="panel-right glass">
                  <div className="panel-header">
                    <Activity size={16} />
                    <h3>Design Inspector</h3>
                  </div>

                  <div className="inspector-grid">
                    <div className="stat-card">
                      <label>MCU</label>
                      <div className="value">
                        {circuitData?.blocks.find(b => b.type === 'mcu')?.metadata.part_number || 'Detecting...'}
                      </div>
                    </div>
                    <div className="stat-card">
                      <label>Voltage</label>
                      <div className="value">
                        {circuitData?.intent.power_source === 'USB_5V' ? '5V' : '12V'} → 3.3V
                      </div>
                    </div>
                    <div className="stat-card">
                      <label>Board Size</label>
                      <div className="value">
                        {circuitData?.intent.pcb_size.width} x {circuitData?.intent.pcb_size.height} mm
                      </div>
                    </div>
                    <div className="stat-card">
                      <label>Est. Cost</label>
                      <div className="value">
                        ${((circuitData?.components.length || 0) * 0.28).toFixed(2)}
                      </div>
                    </div>
                  </div>

                  <div className="readiness-section">
                    <div className="readiness-header">
                      <label>Manufacturing Readiness</label>
                      <span>{circuitData ? '100%' : '20%'}</span>
                    </div>
                    <div className="progress-bar">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: circuitData ? '100%' : '20%' }}
                        className="progress-fill"
                      />
                    </div>
                  </div>

                  <button
                    className={`btn-download primary ${circuitData ? 'pulse' : 'disabled'}`}
                    onClick={() => setActiveTab('manufacturing')}
                  >
                    <Download size={18} />
                    <span>Download Production Files</span>
                  </button>
                </aside>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>

      <style jsx>{`
        .app-container {
          width: 100vw;
          height: 100vh;
          overflow: hidden;
          position: relative;
        }

        .layout-root {
          display: flex;
          flex-direction: column;
          height: 100%;
          padding: 1rem;
          gap: 1rem;
        }

        .app-header {
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 1.5rem;
          border-radius: 12px;
          z-index: 10;
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .brand-icon {
          width: 32px;
          height: 32px;
          background: var(--primary-color);
          color: white;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .brand h1 {
          font-size: 1.1rem;
          font-weight: 600;
          letter-spacing: -0.02em;
        }

        .version {
          font-size: 0.65rem;
          font-family: var(--font-mono);
          color: var(--text-muted);
          background: var(--border-color);
          padding: 2px 6px;
          border-radius: 4px;
        }

        .app-content {
          flex: 1;
          position: relative;
        }

        /* Hero / Landing */
        .hero-section {
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
        }

        .hero-tag {
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          color: var(--primary-color);
          margin-bottom: 1rem;
        }

        .hero-section h2 {
          font-size: 2.5rem;
          font-weight: 700;
          margin-bottom: 2rem;
          letter-spacing: -0.04em;
        }

        .input-container {
          width: 600px;
          margin: 0 auto;
          display: flex;
          padding: 0.5rem;
          border-radius: 16px;
          border: 1px solid rgba(37, 99, 235, 0.2);
          transition: all 0.3s ease;
        }

        .input-container:focus-within {
          border-color: var(--primary-color);
          box-shadow: 0 0 20px rgba(37, 99, 235, 0.1);
        }

        .input-container input {
          flex: 1;
          border: none;
          background: transparent;
          padding: 1rem;
          font-size: 1.1rem;
          outline: none;
          font-family: var(--font-main);
        }

        .generate-btn {
          background: #eee;
          color: #999;
          border: none;
          padding: 0 1.5rem;
          border-radius: 12px;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 600;
          cursor: not-allowed;
          transition: all 0.3s ease;
        }

        .generate-btn.active {
          background: var(--primary-color);
          color: white;
          cursor: pointer;
          box-shadow: var(--shadow-md);
        }

        .generate-btn.active:hover {
          transform: translateY(-1px);
          box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.3);
        }

        .example-chips {
          display: flex;
          gap: 0.75rem;
          justify-content: center;
          margin-top: 1.5rem;
        }

        .chip {
          padding: 0.5rem 1rem;
          border-radius: 20px;
          background: rgba(226, 232, 240, 0.4);
          border: 1px solid var(--border-color);
          font-size: 0.85rem;
          color: var(--text-muted);
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .chip:hover {
          background: white;
          border-color: var(--primary-color);
          color: var(--primary-color);
        }

        /* Workspace Grid */
        .workspace-layout {
          display: grid;
          grid-template-columns: 280px 1fr 300px;
          height: 100%;
          gap: 1rem;
        }

        .panel-left, .panel-right {
          border-radius: 16px;
          display: flex;
          flex-direction: column;
        }

        .panel-header {
          padding: 1rem;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .panel-header h3 {
          font-size: 0.9rem;
          font-weight: 600;
        }

        .timeline {
          padding: 1.5rem;
          flex: 1;
        }

        .timeline-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem 0;
          position: relative;
          color: var(--text-muted);
          font-size: 0.85rem;
          font-weight: 500;
        }

        .step-indicator {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          background: var(--border-color);
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          z-index: 2;
        }

        .timeline-item.active {
          color: var(--primary-color);
        }

        .timeline-item.active .step-indicator {
          background: var(--primary-color);
          color: white;
        }

        .timeline-item.completed {
          color: var(--accent-color);
        }
        
        .timeline-item.completed .step-indicator {
          background: var(--accent-color);
          color: white;
        }

        .check-dot {
          position: absolute;
          top: -2px;
          right: -2px;
          width: 10px;
          height: 10px;
          background: var(--accent-color);
          border: 2px solid white;
          border-radius: 50%;
        }

        .active-glow {
          position: absolute;
          left: -0.5rem;
          right: -0.5rem;
          height: 36px;
          background: var(--primary-glow);
          border-radius: 8px;
          z-index: 1;
        }

        .intelligence-log {
          padding: 1rem;
          background: rgba(0,0,0,0.02);
          border-top: 1px solid var(--border-color);
          font-family: var(--font-mono);
          max-height: 200px;
          overflow-y: auto;
        }

        .intelligence-log h4 {
          font-size: 0.65rem;
          text-transform: uppercase;
          color: var(--text-muted);
          margin-bottom: 0.5rem;
        }

        .log-entry {
          font-size: 0.7rem;
          color: var(--secondary-color);
          padding: 2px 0;
          line-height: 1.4;
        }

        /* Left/Right Gaps & Glows */
        .panel-center {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .workspace-viewer {
          flex: 1;
          border-radius: 16px;
          position: relative;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .viewer-header {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .tab-mini {
          padding: 0.4rem 0.8rem;
          border-radius: 6px;
          border: none;
          background: transparent;
          font-size: 0.75rem;
          font-weight: 600;
          color: var(--text-muted);
          cursor: pointer;
        }

        .tab-mini.active {
          background: white;
          color: var(--primary-color);
          box-shadow: var(--shadow-sm);
        }

        .viewer-content {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          background: white;
          position: relative;
        }

        .placeholder-viz {
          text-align: center;
          color: var(--border-color);
        }

        .placeholder-viz p {
          margin-top: 1rem;
          font-weight: 500;
        }

        .bottom-nav {
          height: 64px;
          border-radius: 16px;
          display: flex;
          padding: 0.5rem;
          gap: 0.5rem;
          position: relative;
        }

        .nav-item {
          flex: 1;
          border: none;
          background: transparent;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 600;
          color: var(--text-muted);
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          position: relative;
          z-index: 2;
        }

        .nav-item.active {
          color: var(--primary-color);
        }

        .nav-glow {
          position: absolute;
          inset: 0;
          background: white;
          border-radius: 10px;
          box-shadow: var(--shadow-sm);
          z-index: -1;
        }

        .nav-item:hover:not(.active) {
          background: rgba(255,255,255,0.4);
        }

        .viz-container {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: absolute;
          inset: 0;
        }

        /* Inspector Components */
        .inspector-grid {
          padding: 1rem;
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 0.75rem;
        }

        .stat-card {
          padding: 0.75rem;
          background: rgba(226, 232, 240, 0.3);
          border-radius: 12px;
          border: 1px solid var(--border-color);
        }

        .stat-card label {
          display: block;
          font-size: 0.65rem;
          text-transform: uppercase;
          color: var(--text-muted);
          margin-bottom: 0.25rem;
        }

        .stat-card .value {
          font-size: 0.9rem;
          font-weight: 600;
          color: var(--text-main);
        }

        .readiness-section {
          padding: 1.5rem 1rem;
        }

        .readiness-header {
          display: flex;
          justify-content: space-between;
          font-size: 0.8rem;
          margin-bottom: 0.5rem;
          font-weight: 600;
        }

        .progress-bar {
          height: 8px;
          background: var(--border-color);
          border-radius: 4px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
          border-radius: 4px;
        }

        .btn-download {
          margin: 1rem;
          padding: 1rem;
          border-radius: 12px;
          border: none;
          background: var(--primary-color);
          color: white;
          font-weight: 700;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.75rem;
          cursor: pointer;
          margin-top: auto;
        }

        /* Utils */
        .btn-primary {
          background: var(--primary-color);
          color: white;
          padding: 0.5rem 1rem;
          border: none;
          border-radius: 8px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
        }

        .btn-ghost {
          background: transparent;
          border: none;
          color: var(--text-muted);
          padding: 0.4rem;
          cursor: pointer;
        }

        .glow {
          position: absolute;
          width: 400px;
          height: 400px;
          border-radius: 50%;
          filter: blur(100px);
          opacity: 0.3;
          z-index: -1;
        }

        .glow-1 { top: -100px; right: -100px; background: var(--primary-color); }
        .glow-2 { bottom: -100px; left: -100px; background: var(--accent-color); }

        .divider {
          width: 1px;
          height: 24px;
          background: var(--border-color);
          margin: 0 0.75rem;
        }
      `}</style>
    </div>
  );
};

export default App;
