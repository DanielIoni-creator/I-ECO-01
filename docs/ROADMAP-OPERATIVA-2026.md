# MyZubster — Roadmap Operativa 2026

## Priorità immediate

Queste attività entrano nella roadmap operativa come passaggi necessari per consolidare il progetto prima dei prossimi pilot, call tecniche e collaborazioni esterne.

### P0 — Stabilità del sito e presenza pubblica

**Obiettivo:** verificare e rendere affidabile il sito MyZubster e i principali endpoint pubblici.

- [ ] verificare disponibilità del sito e delle pagine pubbliche;
- [ ] controllare deploy Vercel / DNS / routing;
- [ ] verificare i link condivisi con partner esterni;
- [ ] predisporre una pagina essenziale di fallback/status;
- [ ] rieseguire un controllo esterno dopo il fix.

**Motivazione:** Greenholds ha segnalato che il sito non risultava funzionante durante la valutazione iniziale della proposta LIFE 2026.

### P0 — CI GitHub e affidabilità tecnica

**Obiettivo:** riportare i repository principali in stato CI verde e ridurre i failure ricorrenti.

- [ ] correggere i test falliti su `MyZubster-Ecosystem/myzubster`;
- [ ] verificare il test relativo a Zorgax RAG;
- [ ] controllare research crawler / RAG stack;
- [ ] sistemare i workflow `tari` che falliscono;
- [ ] firmare o rigenerare i commit richiesti dalle PR Tari;
- [ ] documentare le cause dei failure e le relative correzioni.

**Criterio di completamento:** workflow principali verdi o failure residui esplicitamente documentati e non bloccanti.

### P1 — Call tecnica CNR

**Obiettivo:** utilizzare la breve call confermata dal CNR come confronto tecnico-scientifico, separandola dalla candidatura LIFE 2026 immediata.

- [ ] preparare una sintesi tecnica di MyZubster;
- [ ] definire 3–5 domande su water quality, sensori, metodologia e validazione;
- [ ] presentare il pilot acqua in termini tecnici e misurabili;
- [ ] raccogliere feedback su metodologia, dataset e possibili collaborazioni future;
- [ ] redigere una nota post-call con next step e punti validati.

**Nota:** il CNR ha indicato che le tempistiche per LIFE 2026 sono troppo strette, ma ha mantenuto disponibile un confronto tecnico.

## Sequenza operativa

1. **Sito MyZubster stabile e verificato**
2. **CI GitHub riportata sotto controllo**
3. **Pacchetto tecnico pronto per la call CNR**
4. **Follow-up Greenholds con richiesta di collaborazione più circoscritta**
5. **Ripresa dei pilot e delle visual/documentazioni della roadmap**

## Stato

| Area | Priorità | Stato |
|---|---|---|
| Sito / presenza pubblica | P0 | 🔄 Da verificare e correggere |
| CI MyZubster / Tari | P0 | 🔄 In lavorazione |
| Call tecnica CNR | P1 | 📅 Da preparare |
| Follow-up Greenholds | P1 | ⏳ Dopo verifica sito |

---

Questa roadmap operativa integra la roadmap strategica MyZubster 2025 → 2027+ e rappresenta il blocco di consolidamento tecnico e relazionale immediatamente precedente ai prossimi pilot real-world.
