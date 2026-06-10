import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

function App() {
  return (
    <main className="app-shell">
      <section className="hero-card">
        <p className="eyebrow">MVP-00</p>
        <h1>Reconciliere WMS-WME prin ERP</h1>
        <p>
          Aplicatie read-only pentru import, normalizare, matching, audit si raportare pe
          evenimente economice WMS/WME.
        </p>
        <ul>
          <li>Import automat prin ERP ca flux principal</li>
          <li>Upload manual doar fallback</li>
          <li>Verdicturi: MATCH, MATCH dupa netare, REVIEW, NOT MATCH</li>
        </ul>
      </section>
    </main>
  );
}

const rootElement = document.getElementById('root');

if (rootElement) {
  createRoot(rootElement).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
}
