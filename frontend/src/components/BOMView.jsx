import React from 'react';
import { ClipboardList } from 'lucide-react';

const BOMView = ({ circuit }) => {
  const components = circuit?.components || [];

  return (
    <div className="bom-view">
      {!circuit ? (
        <div className="placeholder-viz">
          <ClipboardList size={48} />
          <p>Designing BOM...</p>
        </div>
      ) : (
        <div className="bom-card glass">
          <table>
            <thead>
              <tr>
                <th>Ref</th>
                <th>Component</th>
                <th>Package</th>
                <th>Qty</th>
              </tr>
            </thead>
            <tbody>
              {components.map((c, i) => (
                <tr key={i}>
                  <td className="mono">{c.designator}</td>
                  <td>{c.part_number}</td>
                  <td className="mono">{c.footprint}</td>
                  <td>1</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
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
