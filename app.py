import streamlit as st
import pandas as pd
import os
import pickle

st.set_page_config(layout="wide", page_title="Fantaculo Personale - Pro Live")

SAVE_FILE = "salvataggio_asta.pkl"

def salva_stato():
    with open(SAVE_FILE, "wb") as f:
        pickle.dump({
            'nomi_squadre': st.session_state.nomi_squadre,
            'squadre': st.session_state.squadre,
            'listone': st.session_state.listone
        }, f)

# --- DATABASE TATTICI ---
rigoristi_primi = ['Scamacca', 'Orsolini', 'Fazzini', 'Mina', 'Da Cunha', 'Pellegrino', 'Mastantuono', 'Schmid', 'Colombo', 'Calhanoglu', 'Kolo Muani', 'Zaccagni', 'Taylor', 'Geubbels', 'Goncalo Ramos', 'Cutrone', 'Pessina', 'De Bruyne', 'Hojlund', 'Toure E.', 'Elphege', 'Malen', 'Dybala', 'Berardi', 'Vlasic', 'Davis', 'Busio']
rigoristi_secondi = ['Samardzic', 'Ederson', 'Krstovic', 'Dovbyk', 'Bernardeschi', 'Ferguson', 'Deiola', 'Borrelli', 'Douvikas', 'Baturina', 'Nico Paz', 'Gudmundsson', 'Mandragora', 'Calo', 'Grillitsch', 'Vitinha', 'Messias', 'Ostigard', 'Zielinski', 'Lautaro Martinez', 'Locatelli', 'David', 'Cataldi', 'Stulic', 'Pierotti', 'Gallo', 'Pulisic', 'Modric', 'Petagna', 'Politano', 'Valeri', 'Bernabe', 'Pellegrini Lo.', 'Soule', 'Lauriente', 'Bowie', 'Kulenovic', 'Zapata D.', 'Simeone', 'Solet', 'Ekkelenkamp', 'Rrahmani', 'Adams A.']
finti_attaccanti = ['Pulisic', 'Zaccagni', 'Orsolini', 'Gudmundsson', 'Nico Paz', 'Paz N.', 'Fazzini', 'Mastantuono', 'Cambiaghi', 'Rowe', 'Maldini', 'Oristanio', 'Man', 'Neres', 'Chukwueze', 'Politano', 'Ngonge', 'Suslov']
difensori_avanzati = ['Dimarco', 'Hernandez T.', 'Theo Hernandez', 'Dumfries', 'Bellanova', 'Cambiaso', 'Zappacosta', 'Ruggeri', 'Carlos Augusto', 'Dorgu', 'Tchatchoua', 'Kyriakopoulos', 'Gosens', 'Spinazzola', 'Biraghi', 'Gallo', 'Lazzari', 'Dodò', 'Dodo']

# --- DATABASE INFORTUNI E SQUALIFICHE (AGGIORNATO DA BOLLETTINO MEDICO) ---
infortunati = {
    'Hien': 'Rientro a ottobre', 'Sulemana': 'Rientro a ottobre', 'Kristensen': 'In dubbio', 'Scalvini': 'In dubbio', 'De Ketelaere': 'In dubbio', 'Ahanor': 'In dubbio',
    'Orsolini': 'Rientro tra fine settembre e inizio ottobre', 'El Azzouzi': 'Rientro a ottobre', 'Casale': 'In dubbio',
    'Idrissi': 'Rientro a novembre', 'Trepy': 'In dubbio', 'Mina': 'In dubbio', 'Borrelli': 'In dubbio',
    'Addai': 'Rientro a ottobre',
    'Parisi': 'Rientro a fine novembre',
    'Venturino': 'Rientro a metà settembre', 'Messias': 'In dubbio', 'Havel': 'In dubbio',
    'Mkhitaryan': 'Squalificato', 
    'Yildiz': 'Rientro a dicembre', 'Ekhator': 'Rientro a novembre', 'Gatti': 'In dubbio', 'Perin': 'In dubbio', 'Thuram': 'Rientro a inizio 2027', 'McKennie': 'In dubbio', 'Cabal': 'In dubbio', 'Cambiaso': 'In dubbio',
    'Marusic': 'Rientro a ottobre', 'Dele-Bashiru': 'Rientro a metà settembre', 'Cataldi': 'Rientro a metà settembre', 'Rovella': 'Rientro a metà ottobre', 'Patric': 'In dubbio', 'Pellegrini': 'In dubbio',
    'Berisha': 'In dubbio', 'Gallo': 'In dubbio',
    'Pulisic': 'In dubbio', 'Leao': 'In dubbio', 'Gimenez': 'In dubbio', 'Geubbels': 'Rientro a metà settembre',
    'Pessina': 'Rientro tra ottobre e novembre', 'Toure': 'In dubbio', 'Varela': 'In dubbio', 'Ciurria': 'In dubbio', 'Colombo': 'In dubbio', 'Akinsanmiro': 'In dubbio',
    'Buongiorno': 'Rientro a fine novembre', 'Marianucci': 'Rientro a ottobre', 'McTominay': 'Rientro a metà ottobre', 'Lucca': 'In dubbio', 'Beukema': 'In dubbio',
    'Nicolussi Caviglia': 'Rientro a novembre', 'Cremaschi': 'Rientro a fine settembre', 'Britschgi': 'Squalificato', 'Daffara': 'In dubbio',
    'Vaz': 'Rientro a metà settembre', 'Ndicka': 'In dubbio', 'Rensch': 'In dubbio', 
    'Cande': 'Rientro a metà settembre', 'Kone': 'Rientro a dicembre/gennaio', 'Pieragnolo': 'Rientro a ottobre', 'Walukiewicz': 'In dubbio', 'Boloca': 'In dubbio', 'Berardi': 'In dubbio',
    'Israel': 'Rientro a novembre', 'Casadei': 'In dubbio', 'Zapata': 'In dubbio', 'Comuzzo': 'In dubbio',
    'Chakvetadze': 'Rientro a metà settembre', 'Zanoli': 'Rientro a ottobre', 'Zaniolo': 'Rientro a fine settembre', 'Palma': 'Rientro a metà settembre', 'Kabasele': 'Squalificato', 'Okoye': 'In dubbio',
    'Sverko': 'Rientro a ottobre', 'Adorante': 'Rientro a ottobre', 'Franjic': 'In dubbio', 'Moreno': 'In dubbio'
}

# --- BLOCCO TRADUZIONE CHROME ---
st.markdown("""
    <meta name="google" content="notranslate">
    <style>
        body { font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

if 'inizializzato' not in st.session_state:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "rb") as f:
                dati_salvati = pickle.load(f)
                st.session_state.nomi_squadre = dati_salvati['nomi_squadre']
                st.session_state.squadre = dati_salvati['squadre']
                st.session_state.listone = dati_salvati['listone']
        except Exception as e:
            st.error(f"Errore caricamento: {e}")
    else:
        st.session_state.nomi_squadre = ['Il Mio Team', 'Avversario 1', 'Avversario 2', 'Avversario 3', 'Avversario 4', 'Avversario 5', 'Avversario 6', 'Avversario 7']
        st.session_state.squadre = {nome: {'budget': 500, 'giocatori': []} for nome in st.session_state.nomi_squadre}
        
        try:
            df = pd.read_excel('Quotazioni_Fantacalcio_Stagione_2026_27.xlsx', sheet_name='Tutti', skiprows=1)
            mappa_ruoli = {'P': 'POR', 'D': 'DIF', 'C': 'CEN', 'A': 'ATT'}
            df['Ruolo'] = df['R'].map(mappa_ruoli)
            
            df['Quotazione'] = df['Qt.A'].fillna(1).astype(int)
            df['FVM'] = df['FVM'].fillna(1).astype(int)
            df['PFC'] = (df['FVM'] / 2).astype(int)
            df['PMA'] = df['Quotazione'] + 2 
            df['Titolarita'] = df['FVM'].apply(lambda x: 95 if x > 70 else (80 if x > 30 else (60 if x > 10 else 30)))
            
            voti_calendario = {'Atalanta': 5, 'Bologna': 3, 'Cagliari': 4, 'Como': 2, 'Fiorentina': 3, 'Frosinone': 2, 'Genoa': 3, 'Inter': 4, 'Juventus': 5, 'Lazio': 3, 'Lecce': 3, 'Milan': 4, 'Monza': 4, 'Napoli': 4, 'Parma': 4, 'Roma': 4, 'Sassuolo': 4, 'Torino': 2, 'Udinese': 3, 'Venezia': 5}
            df['Calendario'] = df['Squadra'].map(voti_calendario).fillna(3)
                
            def get_rigorista_status(nome):
                for r in rigoristi_primi:
                    if r.lower() in nome.lower(): return "1° Rigorista"
                for r in rigoristi_secondi:
                    if r.lower() in nome.lower(): return "Alternativa"
                return "No"
                
            def get_finto_att_status(nome):
                for f in finti_attaccanti:
                    if f.lower() in nome.lower(): return "Finto Attaccante"
                return "No"

            def get_difensore_avanzato_status(nome):
                for d in difensori_avanzati:
                    if d.lower() in nome.lower(): return "Esterno d'Attacco"
                return "No"
                
            def get_infortunio_status(nome):
                for inf, stato in infortunati.items():
                    if inf.lower() in nome.lower(): return stato
                return "No"
                
            df['Rigorista'] = df['Nome'].apply(get_rigorista_status)
            df['Trequartista'] = df['Nome'].apply(get_finto_att_status)
            df['Esterno_Attacco'] = df['Nome'].apply(get_difensore_avanzato_status)
            df['Infortunio'] = df['Nome'].apply(get_infortunio_status)
            
            st.session_state.listone = df[['Nome', 'Ruolo', 'Squadra', 'Quotazione', 'Calendario', 'Titolarita', 'PFC', 'PMA', 'FVM', 'Rigorista', 'Trequartista', 'Esterno_Attacco', 'Infortunio']]
            salva_stato()
        except Exception as e:
            st.error(f"⚠️ Errore Excel: {e}")
            st.stop()
    st.session_state.inizializzato = True

team_names = st.session_state.nomi_squadre

st.sidebar.title("⚙️ Impostazioni")

st.sidebar.subheader("👥 Gestione Partecipanti")
c_add1, c_add2 = st.sidebar.columns([2, 1])
nuovo_nome_sq = c_add1.text_input("Nome", key="nuovo_team_input", placeholder="Es. Squadra 9")
if c_add2.button("Aggiungi"):
    if nuovo_nome_sq and nuovo_nome_sq not in team_names:
        st.session_state.nomi_squadre.append(nuovo_nome_sq)
        st.session_state.squadre[nuovo_nome_sq] = {'budget': 500, 'giocatori': []}
        salva_stato()
        st.rerun()

c_rem1, c_rem2 = st.sidebar.columns([2, 1])
squadra_da_rimuovere = c_rem1.selectbox("Rimuovi", team_names, key="rimuovi_team_sel")
if c_rem2.button("Elimina"):
    if len(team_names) > 2:
        giocatori_restituiti = st.session_state.squadre[squadra_da_rimuovere]['giocatori']
        for g_r in giocatori_restituiti:
            g_rim = {k: v for k, v in g_r.items() if k != 'Prezzo Pagato'}
            st.session_state.listone = pd.concat([st.session_state.listone, pd.DataFrame([g_rim])], ignore_index=True)
        
        st.session_state.nomi_squadre.remove(squadra_da_rimuovere)
        del st.session_state.squadre[squadra_da_rimuovere]
        salva_stato()
        st.rerun()
    else:
        st.sidebar.error("Devono restare almeno 2 squadre!")

st.sidebar.divider()

st.sidebar.subheader("✏️ Rinomina Squadre")
for i, vecchio_nome in enumerate(team_names):
    nuovo_nome = st.sidebar.text_input(f"Nome {i+1}", value=vecchio_nome, key=f"input_nome_{i}")
    if nuovo_nome != vecchio_nome and nuovo_nome not in st.session_state.squadre:
        st.session_state.squadre[nuovo_nome] = st.session_state.squadre.pop(vecchio_nome)
        st.session_state.nomi_squadre[i] = nuovo_nome
        salva_stato()
        st.rerun()

st.sidebar.divider()
st.sidebar.subheader("🚨 Gestione Emergenze")
if st.sidebar.button("⚠️ RESETTA TUTTA L'ASTA"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

st.image("https://cdn-icons-png.flaticon.com/512/8853/8853106.png", width=60)
st.title("⚽ Fantaculo Personale - Squad Builder & Live Pro")

st.subheader("💰 Portafogli e Slot")
cols = st.columns(4) 
for i, nome_sq in enumerate(team_names):
    dati_sq = st.session_state.squadre[nome_sq]
    with cols[i % 4]: 
        st.metric(label=f"{nome_sq} ({len(dati_sq['giocatori'])}/25)", value=f"{dati_sq['budget']} cr")

st.divider()
st.subheader("🎯 Centro di Comando")
col_ia, col_radar = st.columns([1.5, 1])

with col_ia:
    st.write("### 🏆 Squad Builder IA (Auto-Live)")
    team_ia = st.selectbox("Squadra da ottimizzare:", team_names, key="ai_builder_team")
    dati_team = st.session_state.squadre[team_ia]
    rosa_team = dati_team['giocatori']
    
    conteggio = pd.DataFrame(rosa_team)['Ruolo'].value_counts().to_dict() if rosa_team else {}
    mancanti = {'POR': 3 - conteggio.get('POR', 0), 'DIF': 8 - conteggio.get('DIF', 0), 'CEN': 8 - conteggio.get('CEN', 0), 'ATT': 6 - conteggio.get('ATT', 0)}
    slot_rimasti = sum(mancanti.values())
    
    if slot_rimasti == 0:
        st.success("🎉 Rosa completata!")
    else:
        ruolo_focus = 'POR' if mancanti['POR'] > 0 else 'DIF' if mancanti['DIF'] > 0 else 'CEN' if mancanti['CEN'] > 0 else 'ATT'
        budget_max = dati_team['budget'] - max(0, slot_rimasti - 1)
        max_spesa_avversari = max([sq['budget'] - max(0, 25 - len(sq['giocatori']) - 1) for n, sq in st.session_state.squadre.items() if n != team_ia] or [0])
        limite_matematico = max_spesa_avversari + 1
        
        df_disp = st.session_state.listone[st.session_state.listone['Ruolo'] == ruolo_focus].copy()
        
        if not df_disp.empty:
            df_disp['Delta'] = df_disp['PFC'] - df_disp['PMA']
            bonus_rig = df_disp['Rigorista'].map({'1° Rigorista': 10.0, 'Alternativa': 5.0, 'No': 0.0})
            bonus_treq = df_disp['Trequartista'].map({'Finto Attaccante': 8.0, 'No': 0.0})
            bonus_est = df_disp['Esterno_Attacco'].map({"Esterno d'Attacco": 6.0, 'No': 0.0})
            malus_inf = df_disp['Infortunio'].apply(lambda x: -20.0 if x != "No" else 0.0)
            
            df_disp['Score IA'] = (df_disp['FVM'] * 0.2) + df_disp['Delta'] - (df_disp['Calendario'] * 2) + (df_disp['Titolarita'] / 10) + bonus_rig + bonus_treq + bonus_est + malus_inf
            
            def calc_spesa_max(row):
                if row['Titolarita'] < 50: return 0 
                
                base_spesa = row['PFC']
                inf = str(row['Infortunio']).lower()
                
                if inf != "no": 
                    if "dubbio" in inf or "settembre" in inf or "squalificato" in inf:
                        base_spesa = max(1, base_spesa * 0.8) 
                    elif "ottobre" in inf:
                        base_spesa = max(1, base_spesa * 0.5)
                    elif "novembre" in inf or "dicembre" in inf or "2027" in inf or "gennaio" in inf:
                        base_spesa = max(1, base_spesa * 0.2)
                    else:
                        base_spesa = max(1, base_spesa * 0.5)
                
                df_ruolo = st.session_state.listone[st.session_state.listone['Ruolo'] == row['Ruolo']]
                num_meglio = len(df_ruolo[(df_ruolo['FVM'] > row['FVM']) & (df_ruolo['Titolarita'] > 60) & (df_ruolo['Nome'] != row['Nome'])])
                    
                if num_meglio > 0:
                    base_spesa *= 0.85 if num_meglio > 3 else 0.90
                    
                if (row['PFC'] - row['PMA']) < -5:
                    base_spesa *= 0.85
                    
                return min(int(base_spesa), budget_max, limite_matematico)
            
            df_disp['Spesa MAX 🛑'] = df_disp.apply(calc_spesa_max, axis=1)
            df_disp = df_disp[df_disp['Spesa MAX 🛑'] > 0]
            
            top_consigli = df_disp.sort_values(by='Score IA', ascending=False).head(5).reset_index(drop=True)
            top_consigli.insert(0, 'Classifica', ['🥇 1°', '🥈 2°', '🥉 3°', '4°', '5°'][:len(top_consigli)])
            
            st.info(f"**FASE ASTA ATTUALE:** Cerchiamo i **{ruolo_focus}** (Ne mancano {mancanti[ruolo_focus]})\n\n"
                    f"📊 **PORTAFOGLIO:** Rimasti **{dati_team['budget']} cr** | Utilizzabili ora: **{budget_max} cr**")
            
            if ruolo_focus == 'POR':
                 st.dataframe(top_consigli[['Classifica', 'Nome', 'Squadra', 'FVM', 'Titolarita', 'Spesa MAX 🛑', 'Infortunio']], hide_index=True)
            elif ruolo_focus == 'DIF':
                 st.dataframe(top_consigli[['Classifica', 'Nome', 'Squadra', 'Esterno_Attacco', 'Rigorista', 'FVM', 'Spesa MAX 🛑', 'Infortunio']], hide_index=True)
            elif ruolo_focus == 'CEN':
                 st.dataframe(top_consigli[['Classifica', 'Nome', 'Squadra', 'Trequartista', 'Rigorista', 'FVM', 'Spesa MAX 🛑', 'Infortunio']], hide_index=True)
            else:
                 st.dataframe(top_consigli[['Classifica', 'Nome', 'Squadra', 'Rigorista', 'FVM', 'Titolarita', 'Spesa MAX 🛑', 'Infortunio']], hide_index=True)

with col_radar:
    st.write("### 🔎 Radar e Assegnazione")
    if not st.session_state.listone.empty:
        fase_asta = st.radio("Filtro:", ["POR", "DIF", "CEN", "ATT", "TUTTI"], horizontal=True, key="filtro_radar")
        df_ricerca = st.session_state.listone if fase_asta == 'TUTTI' else st.session_state.listone[st.session_state.listone['Ruolo'] == fase_asta]
        
        giocatore_sel = st.selectbox("Cerca Calciatore:", df_ricerca['Nome'].sort_values(), key="ricerca_giocatore")
        mio_team = team_names[0]
        
        idx = st.session_state.listone[st.session_state.listone['Nome'] == giocatore_sel].index
        if not idx.empty:
            g = st.session_state.listone.loc[idx[0]]
            
            rosa_radar = st.session_state.squadre[mio_team]['giocatori']
            conteggio_r = pd.DataFrame(rosa_radar)['Ruolo'].value_counts().to_dict() if rosa_radar else {}
            mancanti_reparto_r = {'POR': 3, 'DIF': 8, 'CEN': 8, 'ATT': 6}.get(g['Ruolo'], 0) - conteggio_r.get(g['Ruolo'], 0)
            
            budget_disp = st.session_state.squadre[mio_team]['budget'] - max(0, 25 - len(rosa_radar) - 1)
            lim_mat = max([sq['budget'] - max(0, 25 - len(sq['giocatori']) - 1) for n, sq in st.session_state.squadre.items() if n != mio_team] or [0]) + 1
            
            base_spesa = g['PFC']
            avviso = ""
            
            if g['Infortunio'] != "No":
                inf_str = g['Infortunio'].lower()
                if "dubbio" in inf_str or "settembre" in inf_str or "squalificato" in inf_str:
                    base_spesa = max(1, base_spesa * 0.8)
                    avviso += f"🚑 **INFORTUNIO LIEVE:** {g['Infortunio']}. Spesa abbassata del 20%.\n\n"
                elif "ottobre" in inf_str:
                    base_spesa = max(1, base_spesa * 0.5)
                    avviso += f"🚑 **INFORTUNIO MEDIO:** {g['Infortunio']}. Spesa dimezzata!\n\n"
                else:
                    base_spesa = max(1, base_spesa * 0.2)
                    avviso += f"🚑 **INFORTUNIO GRAVE:** {g['Infortunio']}. Budget tagliato dell'80%!\n\n"
                
            df_ruolo = st.session_state.listone[st.session_state.listone['Ruolo'] == g['Ruolo']]
            df_meglio = df_ruolo[(df_ruolo['FVM'] > g['FVM']) & (df_ruolo['Titolarita'] > 60) & (df_ruolo['Nome'] != g['Nome'])]
            
            num_meglio = len(df_meglio)
            if num_meglio > 0:
                top_alt = df_meglio.sort_values(by='FVM', ascending=False).head(2)['Nome'].tolist()
                base_spesa *= 0.85 if num_meglio > 3 else 0.90
                avviso += f"💡 **Guarda Oltre:** Ci sono ancora **{num_meglio} {g['Ruolo']} migliori** (es. *{', '.join(top_alt)}*).\n📉 *Spesa Max abbassata per fare disturbo.*\n\n"
            else:
                avviso += f"👑 **È IL TOP SUL MERCATO!** Nessuno svincolato ha un Valore Mercato (FVM) superiore.\n\n"
                
            if (g['PFC'] - g['PMA']) < -5:
                avviso += f"⚠️ **ATTENZIONE:** Giocatore in hype! Rischio di pagarlo troppo.\n\n"
                base_spesa *= 0.85 
                
            spesa_max = 0
            if mancanti_reparto_r <= 0:
                avviso = "❌ **NON PRENDERE:** Hai già completato i giocatori per questo reparto!"
                spesa_max = 0
            elif g['Titolarita'] < 50:
                avviso = "❌ **NON PRENDERE:** Giocatore con valore bassissimo o riserva fissa. Ignoralo e lascia che lo comprino gli altri!"
                spesa_max = 0
            else:
                spesa_max = int(min(base_spesa, budget_disp))
                if spesa_max > lim_mat: 
                    spesa_max = lim_mat
                    avviso += f"🛑 **LIMITATORE ATTIVO:** Non superare i {lim_mat} cr!"

            badge = ""
            if g['Rigorista'] == '1° Rigorista': badge += " | 🎯 **1° RIGORISTA**"
            elif g['Rigorista'] == 'Alternativa': badge += " | 🎯 **Alternativa Rigori**"
            if g['Trequartista'] == 'Finto Attaccante': badge += " | 🚀 **FINTO ATTACCANTE**"
            if g['Esterno_Attacco'] == "Esterno d'Attacco": badge += " | 🚄 **ESTERNO D'ATTACCO**"
            
            stats_str = f"📊 **Quotazione Attuale: {g['Quotazione']}** | 💰 **FVM (Valore Mercato): {g['FVM']}**\n{badge}"
            
            with st.container():
                if spesa_max == 0 or g['Infortunio'] != "No":
                    st.error(f"**{g['Nome']} ({g['Ruolo']})**\n\n{stats_str}\n\n{avviso}\n\n🛑 **LA TUA SPESA MAX: {spesa_max} cr**")
                else:
                    st.info(f"**{g['Nome']} ({g['Ruolo']})**\n\n{stats_str}\n\n{avviso}\n\n🛑 **LA TUA SPESA MAX: {spesa_max} cr**")
        
        c1, c2 = st.columns([2, 1])
        with c1: acquirente = st.selectbox("Acquistato da:", team_names, key="sq_acq")
        with c2: prezzo = st.number_input("Prezzo:", min_value=1, value=1, step=1, key="prz_acq")
        
        if st.button("Assegna 🔨", use_container_width=True):
            if not idx.empty:
                g_dict = st.session_state.listone.loc[idx[0]].to_dict()
                st.session_state.listone = st.session_state.listone.drop(idx)
                g_dict['Prezzo Pagato'] = prezzo
                st.session_state.squadre[acquirente]['giocatori'].append(g_dict)
                st.session_state.squadre[acquirente]['budget'] -= prezzo
                salva_stato()
                st.rerun()

st.divider()
st.subheader("🏟️ Valutatore Rosa")
sq_vis = st.selectbox("Esamina:", team_names, key="val_sq")
rosa = st.session_state.squadre[sq_vis]['giocatori']
if rosa:
    for idx_r, g_r in enumerate(rosa):
        c_inf, c_btn = st.columns([5, 1])
        
        extra_badge = ""
        if g_r.get('Rigorista', 'No') != 'No': extra_badge += f" 🎯"
        if g_r.get('Trequartista', 'No') == 'Finto Attaccante': extra_badge += f" 🚀"
        if g_r.get('Esterno_Attacco', 'No') == "Esterno d'Attacco": extra_badge += f" 🚄"
        if g_r.get('Infortunio', 'No') != 'No': extra_badge += f" 🚑"
        
        c_inf.write(f"**{g_r['Nome']}** ({g_r['Ruolo']}){extra_badge} | Costo: {g_r['Prezzo Pagato']} cr | FVM: {g_r['FVM']}")
        
        if c_btn.button("❌", key=f"rm_{sq_vis}_{idx_r}"):
            g_rim = {k: v for k, v in g_r.items() if k != 'Prezzo Pagato'}
            st.session_state.listone = pd.concat([st.session_state.listone, pd.DataFrame([g_rim])], ignore_index=True)
            st.session_state.squadre[sq_vis]['budget'] += g_r['Prezzo Pagato']
            st.session_state.squadre[sq_vis]['giocatori'].pop(idx_r)
            salva_stato()
            st.rerun()
else:
    st.info("Nessun acquisto.")
