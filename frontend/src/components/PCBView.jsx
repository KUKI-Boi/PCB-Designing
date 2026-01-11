import React from 'react';
import { motion } from 'framer-motion';

const PCBView = () => {
    return (
        <div className="pcb-container">
            <div className="pcb-board">
                <svg width="100%" height="100%" viewBox="0 0 500 400">
                    {/* Board substrate */}
                    <rect x="50" y="50" width="400" height="300" rx="20" fill="#1b4332" />

                    {/* Grid on PCB */}
                    <pattern id="pcb-grid" width="10" height="10" patternUnits="userSpaceOnUse">
                        <circle cx="1" cy="1" r="0.5" fill="rgba(255,255,255,0.1)" />
                    </pattern>
                    <rect x="50" y="50" width="400" height="300" rx="20" fill="url(#pcb-grid)" />

                    {/* Traces (Layer 1 - Top Copper) */}
                    <motion.path
                        d="M 100 100 L 200 100 L 200 200"
                        stroke="#ffcc33"
                        strokeWidth="3"
                        fill="none"
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{ duration: 2, delay: 0.5 }}
                    />

                    {/* Footprints */}
                    <motion.g initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }}>
                        {/* ESP32 Footprint */}
                        <rect x="180" y="150" width="80" height="100" fill="none" stroke="rgba(255,255,255,0.5)" strokeWidth="1" />
                        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90].map(y => (
                            <rect key={y} x="175" y={155 + y} width="10" height="4" fill="# silver" />
                        ))}
                    </motion.g>

                    {/* Via */}
                    <circle cx="200" cy="200" r="4" fill="#b45309" stroke="white" strokeWidth="1" />
                </svg>
            </div>
            <style jsx>{`
        .pcb-container {
          width: 100%;
          height: 100%;
          background: #eee;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .pcb-board {
          width: 90%;
          height: 90%;
          filter: drop-shadow(0 20px 30px rgba(0,0,0,0.2));
        }
      `}</style>
        </div>
    );
};

export default PCBView;
