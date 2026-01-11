import React from 'react';
import { motion } from 'framer-motion';

const SchematicView = () => {
    return (
        <div className="schematic-container">
            <div className="schematic-blueprint">
                {/* Placeholder for real schematic symbols */}
                <svg width="100%" height="100%" viewBox="0 0 800 600">
                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e2e8f0" strokeWidth="0.5" />
                    </pattern>
                    <rect width="100%" height="100%" fill="url(#grid)" />

                    <motion.g
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 1 }}
                    >
                        {/* Mock symbols */}
                        <rect x="200" y="200" width="100" height="150" fill="none" stroke="#2563eb" strokeWidth="2" />
                        <text x="250" y="190" fontSize="12" fill="#2563eb" textAnchor="middle" fontWeight="bold">U1 ESP32</text>

                        {/* Pins */}
                        {[0, 20, 40, 60, 80, 100, 120].map(y => (
                            <line key={y} x1="180" y1={215 + y} x2="200" y2={215 + y} stroke="#2563eb" strokeWidth="1.5" />
                        ))}

                        <path d="M 180 235 L 100 235 L 100 100" fill="none" stroke="#2563eb" strokeWidth="1.5" />
                        <circle cx="100" cy="100" r="4" fill="#2563eb" />
                        <text x="110" y="105" fontSize="10" fill="#2563eb">VCC (+3.3V)</text>
                    </motion.g>
                </svg>
            </div>
            <style jsx>{`
        .schematic-container {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #fcfdfe;
        }
        .schematic-blueprint {
          width: 90%;
          height: 90%;
          border: 1px solid var(--border-color);
          border-radius: 8px;
          background: white;
          overflow: hidden;
        }
      `}</style>
        </div>
    );
};

export default SchematicView;
