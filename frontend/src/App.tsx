import { useEffect, useState } from 'react'
import { Activity, AlertTriangle, AppWindow, Bell, ChevronDown, CircleHelp, FileBarChart, Gauge, Globe2, HardDrive, LockKeyhole, Menu, Search, Settings, Shield, ShieldCheck, Users, X } from 'lucide-react'

const nav = [
  { title: 'PILOTAGE', links: [['Vue d’ensemble', Gauge], ['Applications', AppWindow], ['Infrastructure', HardDrive]] },
  { title: 'SÉCURITÉ', links: [['Vulnérabilités', Shield], ['Audits PHP', Activity], ['Audits web', Globe2], ['Remédiation', ShieldCheck]] },
  { title: 'GOUVERNANCE', links: [['Rapports', FileBarChart], ['Utilisateurs & rôles', Users], ['Paramètres', Settings]] },
] as const
type Dashboard = { applications:number; servers:number; audited_applications:number; awaiting_audit:number; vulnerabilities:{critical:number;high:number;moderate:number;low:number};open_remediations:number;resolved:number;unsupported_php:number;notice:string }
const empty: Dashboard={applications:0,servers:0,audited_applications:0,awaiting_audit:0,vulnerabilities:{critical:0,high:0,moderate:0,low:0},open_remediations:0,resolved:0,unsupported_php:0,notice:'Connexion au service en cours…'}
export default function App(){
  const [active,setActive]=useState('Vue d’ensemble'),[data,setData]=useState(empty),[online,setOnline]=useState(false),[mobile,setMobile]=useState(false)
  useEffect(()=>{fetch('/api/v1/dashboard').then(r=>r.ok?r.json():Promise.reject()).then(d=>{setData(d);setOnline(true)}).catch(()=>setData({...empty,notice:'API indisponible. Lancez le service backend pour consulter les données réelles.'}))},[])
  const cards=[['Applications',data.applications,'inventoriées'],['Serveurs',data.servers,'inventoriés'],['Audits réalisés',data.audited_applications,'applications auditées'],['À auditer',data.awaiting_audit,'en attente']]
  return <div className="shell">
    {mobile&&<button className="scrim" onClick={()=>setMobile(false)} aria-label="Fermer le menu"/>}
    <aside className={`sidebar ${mobile?'show':''}`}>
      <div className="brand"><img src="/assets/drc-government-emblem.png" onError={e=>{(e.currentTarget as HTMLImageElement).style.display='none'}}/><div><strong>PHP-SHIELD <span>RDC</span></strong><small>APPLICATION SECURITY<br/> & CYBER RESILIENCE</small></div><button className="close" onClick={()=>setMobile(false)}><X size={18}/></button></div>
      <div className="scope"><span className="dot"/> ENVIRONNEMENT LOCAL <ChevronDown size={14}/></div>
      <nav>{nav.map(group=><section key={group.title}><label>{group.title}</label>{group.links.map(([name,Icon])=><button key={name} className={active===name?'selected':''} onClick={()=>{setActive(name);setMobile(false)}}><Icon size={17}/>{name}{name==='Vulnérabilités'&&<i>0</i>}</button>)}</section>)}</nav>
      <div className="sidebar-bottom"><div className="profile"><div className="avatar">PS</div><div><b>Session locale</b><small>Accès de démonstration</small></div><ChevronDown size={15}/></div><small className="version">VERSION 0.1.0 · PHASE FONDATION</small></div>
    </aside>
    <main><header><button className="mobile-menu" onClick={()=>setMobile(true)}><Menu/></button><div className="crumb">ESPACE DE SÉCURITÉ <span>/</span> <b>{active.toUpperCase()}</b></div><div className="head-actions"><div className="search"><Search size={16}/><input placeholder="Rechercher"/><kbd>⌘ K</kbd></div><button className="icon-btn" aria-label="Notifications"><Bell size={18}/><em/></button><div className="user"><div className="avatar">AD</div><span>Administrateur<small>Session locale</small></span><ChevronDown size={14}/></div></div></header>
      <div className="content"><div className="welcome"><div><div className="eyebrow"><span/> CENTRE DES OPÉRATIONS DE SÉCURITÉ</div><h1>{active==='Vue d’ensemble'?'Vue d’ensemble':active}</h1><p>Surveillez l’exposition, les audits et la posture de sécurité de votre parc applicatif.</p></div><button className="date"><Activity size={15}/> DONNÉES EN DIRECT <span className={online?'green':''}>{online?'API CONNECTÉE':'API HORS LIGNE'}</span></button></div>
      <div className="notice"><div className="notice-icon"><AlertTriangle size={17}/></div><div><b>Plateforme en construction</b><p>{data.notice} Les fonctions métier ne sont pas encore activées.</p></div><button aria-label="Aide"><CircleHelp size={17}/></button></div>
      <div className="section-title"><div><h2>Vue de la posture</h2><p>Inventaire et activité de sécurité</p></div><span>MISE À JOUR À L’INSTANT</span></div>
      <div className="stats">{cards.map(([title,value,note],i)=><div className="stat" key={title}><div className="stat-top"><span>{title}</span><div className={`stat-icon ic${i}`}><IconFor i={i}/></div></div><strong>{value}</strong><small>{note}</small><div className="mini-line"><span style={{width:'0%'}}/></div></div>)}</div>
      <div className="section-title vuln-title"><div><h2>Vulnérabilités ouvertes</h2><p>Constats suivis par niveau de sévérité</p></div><button className="text-link" onClick={()=>setActive('Vulnérabilités')}>Voir le registre <span>→</span></button></div>
      <div className="severity">{[['Critique',data.vulnerabilities.critical,'red'],['Élevée',data.vulnerabilities.high,'orange'],['Modérée',data.vulnerabilities.moderate,'gold'],['Faible',data.vulnerabilities.low,'blue']].map(([n,v,c])=><div className="sev" key={n}><div className="sev-label"><span className={`sev-dot ${c}`}/>{n}<b>{v}</b></div><div className="bar"><span className={c} style={{width:`${Number(v)?Math.min(100,Number(v)*9):0}%`}}/></div></div>)}</div>
      <div className="lower"><div className="panel"><div className="panel-head"><div><h3>Répartition du risque</h3><p>Évaluations actuelles par niveau</p></div><button aria-label="Options">···</button></div><div className="empty-chart"><div className="ring"><ShieldCheck size={24}/></div><b>Aucune évaluation disponible</b><span>Les niveaux de risque apparaîtront après le premier audit.</span></div></div><div className="panel"><div className="panel-head"><div><h3>Activité récente</h3><p>Historique des opérations</p></div><button aria-label="Filtrer">···</button></div><div className="activity-empty"><div><LockKeyhole size={18}/></div><p>Aucune activité enregistrée</p><small>Les événements seront listés ici une fois les modules activés.</small></div><div className="panel-foot"><span><i className={online?'green-bg':''}/>{online?'API opérationnelle':'Connexion API requise'}</span><span>{data.resolved} éléments résolus</span></div></div></div>
      <footer><span>PHP-SHIELD RDC <i>·</i> Produit proposé pour évaluation technique</span><span><Shield size={13}/> ENVIRONNEMENT NON PRODUCTION</span></footer></div></main>
  </div>
}
function IconFor({i}:{i:number}){const icons=[AppWindow,HardDrive,ShieldCheck,Activity],I=icons[i];return <I size={17}/>}
