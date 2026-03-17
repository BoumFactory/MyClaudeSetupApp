import type { CartItem } from '@/types/cart-theme'

/**
 * Génère un rapport HTML inclus dans le ZIP de téléchargement
 * Contient la liste des items téléchargés avec liens et descriptions
 */
export function generateDownloadReport(items: CartItem[], themeName: string): string {
  const date = new Date().toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  const itemsHtml = items
    .map(
      (item) => `
      <tr>
        <td style="padding: 8px 12px; border-bottom: 1px solid #333;">
          <strong>${escapeHtml(item.name)}</strong>
          ${item.description ? `<br><small style="color: #888;">${escapeHtml(item.description)}</small>` : ''}
        </td>
        <td style="padding: 8px 12px; border-bottom: 1px solid #333; text-align: center;">
          <span style="background: #1a1a2e; padding: 2px 8px; border-radius: 4px; font-size: 12px;">
            ${escapeHtml(item.type)}
          </span>
        </td>
        <td style="padding: 8px 12px; border-bottom: 1px solid #333; font-family: monospace; font-size: 12px; color: #7c7cf7;">
          ${escapeHtml(item.path)}
        </td>
      </tr>`
    )
    .join('\n')

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rapport de téléchargement - bfcours.dev</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0a0a1a;
      color: #e0e0e0;
      margin: 0;
      padding: 40px 20px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
      background: #12122a;
      border-radius: 16px;
      padding: 40px;
      border: 1px solid #333;
    }
    h1 {
      background: linear-gradient(135deg, #7c7cf7, #c77dff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 4px;
    }
    .meta {
      color: #888;
      font-size: 14px;
      margin-bottom: 24px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
    }
    th {
      text-align: left;
      padding: 8px 12px;
      border-bottom: 2px solid #7c7cf7;
      color: #7c7cf7;
      font-size: 13px;
      text-transform: uppercase;
    }
    .footer {
      margin-top: 32px;
      padding-top: 16px;
      border-top: 1px solid #333;
      text-align: center;
      color: #666;
      font-size: 13px;
    }
    a { color: #7c7cf7; }
  </style>
</head>
<body>
  <div class="container">
    <h1>${escapeHtml(themeName)}</h1>
    <p class="meta">Téléchargé le ${date} depuis <a href="https://bfcours.dev">bfcours.dev</a></p>
    <p>${items.length} élément${items.length > 1 ? 's' : ''} dans ce téléchargement :</p>
    <table>
      <thead>
        <tr>
          <th>Élément</th>
          <th>Type</th>
          <th>Chemin</th>
        </tr>
      </thead>
      <tbody>
        ${itemsHtml}
      </tbody>
    </table>
    <div class="footer">
      <p>Généré automatiquement par <a href="https://bfcours.dev">bfcours.dev</a></p>
      <p>IA & Enseignement des Mathematiques</p>
    </div>
  </div>
</body>
</html>`
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
