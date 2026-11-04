import type ExcelJS from 'exceljs'
import type { jsPDF as JsPdfDocument } from 'jspdf'

export type ReportData = {
  applications: number
  servers: number
  audited_applications: number
  awaiting_audit: number
  vulnerabilities: { critical: number; high: number; moderate: number; low: number }
  open_remediations: number
  resolved: number
  unsupported_php: number
}

const totalFindings = (data: ReportData) => data.vulnerabilities.critical + data.vulnerabilities.high + data.vulnerabilities.moderate + data.vulnerabilities.low
const auditRate = (data: ReportData) => data.applications ? Math.round(data.audited_applications / data.applications * 100) : 0
const remediationRate = (data: ReportData) => data.resolved + data.open_remediations ? Math.round(data.resolved / (data.resolved + data.open_remediations) * 100) : 0
const dateLabel = (date = new Date()) => date.toLocaleDateString('fr-CD', { day: '2-digit', month: 'long', year: 'numeric' })
const fileDate = () => new Date().toISOString().slice(0, 10)
const emblemUrl = () => new URL(`${import.meta.env.BASE_URL}assets/drc-government-emblem.png`, window.location.href).href

async function readEmblem(): Promise<string> {
  const response = await fetch(emblemUrl())
  if (!response.ok) throw new Error('Impossible de charger l’emblème RDC pour le rapport.')
  const blob = await response.blob()
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => typeof reader.result === 'string' ? resolve(reader.result) : reject(new Error('Lecture de l’emblème impossible.'))
    reader.onerror = () => reject(new Error('Lecture de l’emblème impossible.'))
    reader.readAsDataURL(blob)
  })
}

async function makeWatermark(source: string): Promise<string> {
  const image = new Image()
  image.src = source
  await image.decode()
  const canvas = document.createElement('canvas')
  canvas.width = 640
  canvas.height = 640
  const context = canvas.getContext('2d')
  if (!context) throw new Error('Création du filigrane impossible sur cet appareil.')
  context.globalAlpha = 0.075
  context.drawImage(image, 0, 0, canvas.width, canvas.height)
  return canvas.toDataURL('image/png')
}

function addPageChrome(doc: JsPdfDocument, emblem: string, watermark: string, page: number) {
  if (page > 1) {
    doc.setFillColor(20, 23, 25)
    doc.rect(0, 0, 210, 26, 'F')
    doc.addImage(emblem, 'PNG', 16, 4, 18, 18)
    doc.setTextColor(243, 242, 237)
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(9)
    doc.text('PHP-SHIELD RDC  |  RAPPORT DE POSTURE CYBERNÉTIQUE', 40, 15)
  }
  doc.addImage(watermark, 'PNG', 68, 94, 74, 74)
  const height = doc.internal.pageSize.getHeight()
  doc.setDrawColor(195, 164, 71)
  doc.setLineWidth(0.35)
  doc.line(18, height - 15, 192, height - 15)
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(7)
  doc.setTextColor(105, 109, 109)
  doc.text('PHP-SHIELD RDC  ·  Diffusion réservée aux destinataires autorisés', 18, height - 9)
  doc.text(`Page ${page}`, 192, height - 9, { align: 'right' })
}

export async function downloadPosturePdf(data: ReportData, demo: boolean) {
  const [{ jsPDF }, { autoTable }] = await Promise.all([import('jspdf'), import('jspdf-autotable')])
  const emblem = await readEmblem()
  const watermark = await makeWatermark(emblem)
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4', compress: true })
  const reportDate = dateLabel()
  doc.setProperties({
    title: 'Rapport de posture cybernétique — PHP-SHIELD RDC',
    subject: 'Synthèse des indicateurs de sécurité applicative',
    author: 'PHP-SHIELD RDC · DANTIC',
    creator: 'PHP-SHIELD RDC',
    keywords: 'cybersécurité, RDC, PHP-SHIELD, posture, audit',
  })

  doc.setFillColor(20, 23, 25)
  doc.rect(0, 0, 210, 39, 'F')
  doc.addImage(emblem, 'PNG', 18, 8, 23, 23)
  doc.setTextColor(241, 240, 234)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(10)
  doc.text('RÉPUBLIQUE DÉMOCRATIQUE DU CONGO', 48, 16)
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  doc.setTextColor(210, 202, 175)
  doc.text('DANTIC  ·  DIVISION BASES DE DONNÉES', 48, 23)
  doc.setDrawColor(195, 164, 71)
  doc.setLineWidth(0.6)
  doc.line(18, 33, 192, 33)

  doc.setTextColor(36, 41, 43)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(19)
  doc.text('RAPPORT DE POSTURE', 18, 53)
  doc.setTextColor(150, 119, 40)
  doc.setFontSize(11)
  doc.text('CYBERNÉTIQUE & SÉCURITÉ APPLICATIVE', 18, 61)
  doc.setTextColor(103, 110, 111)
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  doc.text(`Édité le ${reportDate}  ·  PHP-SHIELD RDC`, 18, 68)
  doc.setFillColor(demo ? 247 : 236, demo ? 240 : 245, demo ? 221 : 238)
  doc.roundedRect(18, 74, demo ? 53 : 62, 7, 1.5, 1.5, 'F')
  doc.setTextColor(demo ? 126 : 55, demo ? 91 : 109, demo ? 27 : 74)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(7)
  doc.text(demo ? 'JEU DE DONNÉES SIMULÉ' : 'SOURCE : API CONNECTÉE', 21, 78.7)

  const cards: [string, string, string][] = [
    ['APPLICATIONS', String(data.applications), 'Actifs recensés'],
    ['SERVEURS', String(data.servers), 'Environnements'],
    ['COUVERTURE AUDIT', `${auditRate(data)} %`, `${data.audited_applications} audités`],
    ['CORRECTIONS CLÔTURÉES', `${remediationRate(data)} %`, `${data.resolved} résolues`],
  ]
  cards.forEach(([label, value, note], index) => {
    const x = 18 + index * 44
    doc.setFillColor(247, 246, 241)
    doc.setDrawColor(226, 222, 210)
    doc.roundedRect(x, 88, 40, 25, 1.5, 1.5, 'FD')
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(6)
    doc.setTextColor(126, 119, 99)
    doc.text(label, x + 3, 94)
    doc.setFontSize(13)
    doc.setTextColor(36, 41, 43)
    doc.text(value, x + 3, 102)
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(5.8)
    doc.setTextColor(111, 117, 116)
    doc.text(note, x + 3, 108)
  })

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(9)
  doc.setTextColor(43, 48, 49)
  doc.text('INDICATEURS PAR NIVEAU DE SÉVÉRITÉ', 18, 124)
  const findings = [
    ['Critique', data.vulnerabilities.critical, [189, 59, 70]],
    ['Élevée', data.vulnerabilities.high, [207, 112, 54]],
    ['Modérée', data.vulnerabilities.moderate, [181, 145, 52]],
    ['Faible', data.vulnerabilities.low, [82, 125, 153]],
  ] as const
  const total = totalFindings(data)
  findings.forEach(([label, count, color], index) => {
    const y = 132 + index * 6
    const share = total ? count / total : 0
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(7)
    doc.setTextColor(76, 83, 83)
    doc.text(label, 18, y)
    doc.setFillColor(233, 231, 224)
    doc.roundedRect(47, y - 3, 105, 2.8, 1, 1, 'F')
    if (share > 0) {
      doc.setFillColor(color[0], color[1], color[2])
      doc.roundedRect(47, y - 3, 105 * share, 2.8, 1, 1, 'F')
    }
    doc.setTextColor(48, 53, 53)
    doc.setFont('helvetica', 'bold')
    doc.text(String(count), 160, y)
    doc.setFont('helvetica', 'normal')
    doc.text(`${Math.round(share * 100)} %`, 192, y, { align: 'right' })
  })

  autoTable(doc, {
    startY: 163,
    margin: { left: 18, right: 18, bottom: 22 },
    head: [['INDICATEUR', 'VALEUR', 'LECTURE']],
    body: [
      ['Applications auditées', `${data.audited_applications} / ${data.applications}`, `${auditRate(data)} % de couverture`],
      ['Applications à auditer', String(data.awaiting_audit), 'En attente de contrôle'],
      ['Constats recensés', String(total), 'Somme des niveaux de sévérité ci-dessus'],
      ['Remédiations ouvertes', String(data.open_remediations), 'Actions en attente de clôture'],
      ['Remédiations résolues', String(data.resolved), `${remediationRate(data)} % des actions clôturées`],
      ['Environnements PHP à vérifier', String(data.unsupported_php), 'Contrôle de version à confirmer'],
    ],
    theme: 'grid',
    styles: { font: 'helvetica', fontSize: 7.5, cellPadding: 3, textColor: [52, 58, 58], lineColor: [225, 222, 213], lineWidth: 0.15 },
    headStyles: { fillColor: [36, 41, 43], textColor: [246, 244, 235], fontStyle: 'bold', fontSize: 7 },
    alternateRowStyles: { fillColor: [248, 247, 243] },
    columnStyles: { 0: { cellWidth: 61 }, 1: { cellWidth: 34, halign: 'center' }, 2: { cellWidth: 'auto' } },
    willDrawPage: ({ pageNumber }) => addPageChrome(doc, emblem, watermark, pageNumber),
    didDrawPage: ({ pageNumber }) => {
      if (pageNumber > 1) {
        doc.setFont('helvetica', 'normal')
        doc.setFontSize(7)
        doc.setTextColor(105, 109, 109)
        doc.text('Synthèse produite depuis les indicateurs disponibles au moment de l’édition.', 18, 34)
      }
    },
  })

  const noteY = (doc as JsPdfDocument & { lastAutoTable?: { finalY: number } }).lastAutoTable?.finalY ?? 235
  if (noteY < 267) {
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(7)
    doc.setTextColor(102, 107, 106)
    const note = demo
      ? 'NOTE : Ce rapport utilise exclusivement des données synthétiques de démonstration. Il ne décrit aucun actif ni résultat d’audit réel.'
      : 'NOTE : Les indicateurs reflètent uniquement les données accessibles dans l’API au moment de la génération.'
    doc.text(doc.splitTextToSize(note, 174), 18, noteY + 8)
  }
  doc.save(`PHP-SHIELD-RDC-rapport-posture-${fileDate()}.pdf`)
}

function styleHeader(row: ExcelJS.Row) {
  row.height = 25
  row.eachCell(cell => {
    cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF202426' } }
    cell.font = { name: 'Aptos', size: 10, bold: true, color: { argb: 'FFF5F2E8' } }
    cell.alignment = { vertical: 'middle', wrapText: true }
    cell.border = { bottom: { style: 'medium', color: { argb: 'FFC4A245' } } }
  })
}

export async function downloadPostureExcel(data: ReportData, demo: boolean) {
  const { default: ExcelJS } = await import('exceljs')
  const emblem = await readEmblem()
  const workbook = new ExcelJS.Workbook()
  workbook.creator = 'PHP-SHIELD RDC · DANTIC'
  workbook.subject = 'Rapport de posture cybernétique et sécurité applicative'
  workbook.title = 'Rapport de posture PHP-SHIELD RDC'
  workbook.company = 'PHP-SHIELD RDC'
  workbook.created = new Date()
  workbook.modified = new Date()

  const summary = workbook.addWorksheet('Synthèse', { views: [{ state: 'frozen', ySplit: 5, showGridLines: false }] })
  summary.columns = [{ width: 34 }, { width: 22 }, { width: 47 }, { width: 18 }, { width: 18 }]
  summary.mergeCells('A1:C1')
  summary.getCell('A1').value = 'RAPPORT DE POSTURE CYBERNÉTIQUE'
  summary.getCell('A1').font = { name: 'Aptos Display', size: 19, bold: true, color: { argb: 'FFF5F2E8' } }
  summary.getCell('A1').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF202426' } }
  summary.getRow(1).height = 36
  summary.mergeCells('A2:C2')
  summary.getCell('A2').value = `RÉPUBLIQUE DÉMOCRATIQUE DU CONGO  ·  DANTIC  ·  Édité le ${dateLabel()}`
  summary.getCell('A2').font = { name: 'Aptos', size: 10, color: { argb: 'FF80651F' }, bold: true }
  summary.getCell('A2').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF0EBDD' } }
  summary.getRow(2).height = 23
  summary.mergeCells('A3:C3')
  summary.getCell('A3').value = demo ? 'DÉMONSTRATION — jeu de données synthétiques, sans actifs ni résultats réels.' : 'SOURCE — données lues depuis le service API au moment de la génération.'
  summary.getCell('A3').font = { name: 'Aptos', size: 9, italic: true, color: { argb: demo ? 'FF805C18' : 'FF426B55' } }
  summary.getRow(3).height = 22
  const imageId = workbook.addImage({ base64: emblem, extension: 'png' })
  summary.addImage(imageId, 'D1:E3')
  summary.addRow([])
  const header = summary.addRow(['INDICATEUR', 'VALEUR', 'COMMENTAIRE'])
  styleHeader(header)
  const rows: [string, number | string, string][] = [
    ['Applications inventoriées', data.applications, 'Total disponible dans l’inventaire'],
    ['Serveurs recensés', data.servers, 'Environnements suivis'],
    ['Applications auditées', data.audited_applications, `${auditRate(data)} % de couverture`],
    ['Applications à auditer', data.awaiting_audit, 'En attente de contrôle'],
    ['Constats recensés', totalFindings(data), 'Somme des niveaux de sévérité'],
    ['Remédiations ouvertes', data.open_remediations, 'Actions en attente de clôture'],
    ['Remédiations résolues', data.resolved, `${remediationRate(data)} % des actions clôturées`],
    ['Environnements PHP à vérifier', data.unsupported_php, 'Versions à confirmer'],
  ]
  rows.forEach((values, index) => {
    const row = summary.addRow(values)
    row.height = 22
    row.eachCell(cell => {
      cell.font = { name: 'Aptos', size: 10, color: { argb: 'FF333938' } }
      cell.alignment = { vertical: 'middle', wrapText: true }
      if (index % 2 === 1) cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF4F2EC' } }
      cell.border = { bottom: { style: 'hair', color: { argb: 'FFDDD9CF' } } }
    })
  })
  summary.autoFilter = { from: 'A5', to: 'C13' }

  const severity = workbook.addWorksheet('Sévérité', { views: [{ state: 'frozen', ySplit: 4, showGridLines: false }] })
  severity.columns = [{ width: 24 }, { width: 18 }, { width: 18 }, { width: 46 }]
  severity.mergeCells('A1:D1')
  severity.getCell('A1').value = 'RÉPARTITION DES CONSTATS PAR SÉVÉRITÉ'
  severity.getCell('A1').font = { name: 'Aptos Display', size: 15, bold: true, color: { argb: 'FFF5F2E8' } }
  severity.getCell('A1').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF202426' } }
  severity.getRow(1).height = 32
  severity.mergeCells('A2:D2')
  severity.getCell('A2').value = demo ? 'Série simulée pour démonstration uniquement' : `Export du ${dateLabel()}`
  severity.getCell('A2').font = { name: 'Aptos', size: 9, italic: true, color: { argb: 'FF80651F' } }
  severity.addRow([])
  styleHeader(severity.addRow(['SÉVÉRITÉ', 'CONSTATS', 'PART DU TOTAL', 'PRIORITÉ DE TRAITEMENT']))
  const total = totalFindings(data)
  const levels: [string, number, string][] = [
    ['Critique', data.vulnerabilities.critical, 'Prise en charge immédiate'],
    ['Élevée', data.vulnerabilities.high, 'Plan de correction prioritaire'],
    ['Modérée', data.vulnerabilities.moderate, 'Correction planifiée'],
    ['Faible', data.vulnerabilities.low, 'Suivi selon les politiques internes'],
  ]
  levels.forEach(([label, count, priority], index) => {
    const row = severity.addRow([label, count, total ? count / total : 0, priority])
    row.height = 24
    row.getCell(3).numFmt = '0.0%'
    row.eachCell(cell => {
      cell.font = { name: 'Aptos', size: 10, color: { argb: 'FF333938' } }
      cell.alignment = { vertical: 'middle', wrapText: true }
      if (index % 2 === 1) cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF4F2EC' } }
      cell.border = { bottom: { style: 'hair', color: { argb: 'FFDDD9CF' } } }
    })
  })
  severity.autoFilter = { from: 'A4', to: 'D8' }

  const methodology = workbook.addWorksheet('Notes & méthode', { views: [{ showGridLines: false }] })
  methodology.columns = [{ width: 31 }, { width: 95 }]
  methodology.addRow(['NOTE MÉTHODOLOGIQUE', 'DÉFINITION / SOURCE'])
  styleHeader(methodology.getRow(1))
  methodology.addRows([
    ['Source', demo ? 'Données locales synthétiques destinées à la démonstration. Elles ne représentent aucun actif réel.' : 'API PHP-SHIELD RDC — photographie des données disponibles au moment de l’export.'],
    ['Couverture audit', 'Applications auditées divisées par le nombre total d’applications inventoriées.'],
    ['Taux de clôture', 'Remédiations résolues divisées par le total des remédiations résolues et ouvertes.'],
    ['Constats', 'Somme des constats classés critique, élevé, modéré et faible.'],
    ['Limites', 'Ce rapport est une synthèse des champs disponibles dans la plateforme; il ne remplace pas une expertise ni un audit technique.'],
  ])
  methodology.eachRow((row, rowNumber) => {
    row.height = rowNumber === 1 ? 25 : 38
    row.eachCell(cell => {
      if (rowNumber > 1) {
        cell.font = { name: 'Aptos', size: 10, color: { argb: 'FF404642' } }
        cell.alignment = { vertical: 'middle', wrapText: true }
        if (rowNumber % 2 === 0) cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF4F2EC' } }
      }
    })
  })

  const buffer = await workbook.xlsx.writeBuffer()
  const blob = new Blob([buffer as BlobPart], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
  const href = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = href
  link.download = `PHP-SHIELD-RDC-rapport-posture-${fileDate()}.xlsx`
  document.body.append(link)
  link.click()
  link.remove()
  window.setTimeout(() => URL.revokeObjectURL(href), 1000)
}
