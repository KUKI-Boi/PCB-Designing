import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Cpu, Bell, Activity } from 'lucide-react';

const Node = ({ x, y, icon: Icon, label, status = 'idle' }) => (
    <motion.g
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
    >
        <rect
            x={x - 40} y={y - 40} width={80} height={80}
            rx={12}
            fill="white"
            stroke="#e2e8f0"
            strokeWidth="2"
            className="node-box"
        />
        <foreignObject x={x - 20} y={y - 25} width={40} height={40}>
            <div className={`node-icon ${status}`}>
                <Icon size={24} />
            </div>
        </foreignObject>
        <text
            x={x} y={y + 55}
            textAnchor="middle"
            fontSize="11"
            fontWeight="600"
            fill="#64748b"
            fontFamily="var(--font-main)"
        >
            {label}
        </text>
    </motion.g>
);

const Wire = ({ x1, y1, x2, y2, active = false }) => (
    <g>
        <path
            d={`M ${x1} ${y1} L ${x1 + (x2 - x1) / 2} ${y1} L ${x1 + (x2 - x1) / 2} ${y2} L ${x2} ${y2}`}
            stroke="#e2e8f0"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
        />
        {active && (
            <motion.path
                d={`M ${x1} ${y1} L ${x1 + (x2 - x1) / 2} ${y1} L ${x1 + (x2 - x1) / 2} ${y2} L ${x2} ${y2}`}
                stroke="var(--primary-color)"
                strokeWidth="3"
                fill="none"
                strokeLinecap="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 2, repeat: Infinity }}
            />
        )}
    </g>
);

const BlockDiagram = ({ currentStep }) => {
    return (
        <svg width="100%" height="100%" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid meet">
            {/* Power to MCU */}
            <Wire x1={100} y1={200} x2={250} y2={200} active={currentStep > 1} />

            {/* MCU to Sensor */}
            <Wire x1={350} y1={200} x2={450} y2={100} active={currentStep > 2} />

            {/* MCU to Output */}
            <Wire x1={350} y1={200} x2={450} y2={300} active={currentStep > 3} />

            {/* Nodes */}
            <Node x={100} y={200} icon={Zap} label="12V POWER" status={currentStep >= 1 ? 'active' : 'idle'} />
            <Node x={300} y={200} icon={Cpu} label="ESP32-S3" status={currentStep >= 2 ? 'active' : 'idle'} />
            <Node x={500} y={100} icon={Activity} label="SENSOR" status={currentStep >= 3 ? 'active' : 'idle'} />
            <Node x={500} y={300} icon={Bell} label="RELAY" status={currentStep >= 4 ? 'active' : 'idle'} />

            <style jsx>{`
        .node-icon {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-muted);
          transition: all 0.3s;
        }
        .node-icon.active {
          color: var(--primary-color);
        }
        .node-box {
          filter: drop-shadow(0 4px 6px rgba(0,0,0,0.02));
        }
      `}</style>
        </svg>
    );
};

export default BlockDiagram;
