import React from 'react';

const BOMView = () => {
    const components = [
        { ref: 'U1', designator: 'ESP32-S3', package: 'QFN-56', qty: 1, cost: '$2.50' },
        { ref: 'U2', designator: 'AMS1117-3.3', package: 'SOT-223', qty: 1, cost: '$0.15' },
        { ref: 'C1', designator: '10uF', package: '0805', qty: 2, cost: '$0.04' },
        { ref: 'R1', designator: '10k', package: '0603', qty: 5, cost: '$0.02' },
        { ref: 'D1', designator: '1N4148', package: 'SOD-123', qty: 1, cost: '$0.05' },
    ];

    return (
        <div className="bom-view">
            <div className="bom-card glass">
                <table>
                    <thead>
                        <tr>
                            <th>Ref</th>
                            <th>Component</th>
                            <th>Package</th>
                            <th>Qty</th>
                            <th>Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        {components.map((c, i) => (
                            <tr key={i}>
                                <td className="mono">{c.ref}</td>
                                <td>{c.designator}</td>
                                <td className="mono">{c.package}</td>
                                <td>{c.qty}</td>
                                <td className="price">{c.cost}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <style jsx>{`
        .bom-view {
          padding: 2rem;
          width: 100%;
          height: 100%;
          background: #f8fafc;
          overflow-y: auto;
        }
        .bom-card {
          width: 100%;
          border-radius: 12px;
          overflow: hidden;
          background: white;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.9rem;
        }
        th {
          text-align: left;
          padding: 1rem;
          background: #f1f5f9;
          color: #64748b;
          font-weight: 600;
          text-transform: uppercase;
          font-size: 0.7rem;
        }
        td {
          padding: 1rem;
          border-bottom: 1px solid var(--border-color);
        }
        .mono {
          font-family: var(--font-mono);
          font-size: 0.8rem;
          color: var(--primary-color);
        }
        .price {
          font-weight: 600;
          color: var(--text-main);
        }
        tr:hover {
          background: var(--primary-glow);
        }
      `}</style>
        </div>
    );
};

export default BOMView;
