/**
 * Script de build monolithique
 * Génère un fichier HTML unique contenant toute l'application
 *
 * Usage: node build.js
 * Output: dist/prompt-manager.html
 */

const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, 'src');
const DIST_DIR = path.join(__dirname, 'dist');
const OUTPUT_FILE = path.join(DIST_DIR, 'prompt-manager.html');

// Ordre des fichiers pour respecter les dépendances
const JS_FILES = [
  // Config
  'config/actions.js',
  'config/subjects.js',
  'config/bricks.js',
  'config/structures.js',
  'config/concatenation-prompt.js',

  // Core
  'core/database.js',
  'core/prompt-builder.js',

  // UI Components
  'ui/components/wizard.js',
  'ui/components/prompt-list.js',
  'ui/components/builder-panel.js',
  'ui/components/concatenation-panel.js',
  'ui/components/settings-panel.js',
  'ui/components/save-modal.js',

  // App
  'app.js'
];

const CSS_FILE = 'ui/styles/main.css';

/**
 * Lit un fichier et retourne son contenu
 */
function readFile(filePath) {
  const fullPath = path.join(SRC_DIR, filePath);
  try {
    return fs.readFileSync(fullPath, 'utf-8');
  } catch (err) {
    console.error(`Erreur lecture: ${filePath}`);
    return '';
  }
}

/**
 * Nettoie le code JS des imports/exports pour le bundle
 */
function cleanJS(code, filename) {
  // Supprimer les imports
  code = code.replace(/^import\s+.*?from\s+['"].*?['"];?\s*$/gm, '');
  code = code.replace(/^import\s+{[^}]+}\s+from\s+['"].*?['"];?\s*$/gm, '');

  // Supprimer les exports mais garder les déclarations
  code = code.replace(/^export\s+(const|let|var|function|class)\s+/gm, '$1 ');
  code = code.replace(/^export\s+{\s*[^}]+\s*};?\s*$/gm, '');
  code = code.replace(/^export\s+default\s+/gm, '');
  code = code.replace(/^export\s+/gm, '');

  // Ajouter un commentaire de section
  return `\n// ============ ${filename} ============\n${code}`;
}

/**
 * Génère le HTML final
 */
function build() {
  console.log('🔨 Build en cours...');

  // Créer le dossier dist si nécessaire
  if (!fs.existsSync(DIST_DIR)) {
    fs.mkdirSync(DIST_DIR, { recursive: true });
  }

  // Lire et nettoyer les fichiers JS
  let jsBundle = '';
  for (const file of JS_FILES) {
    const content = readFile(file);
    jsBundle += cleanJS(content, file);
  }

  // Lire le CSS
  const cssContent = readFile(CSS_FILE);

  // Générer le HTML final
  const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prompt Manager - Gestionnaire de Prompts pour Élèves</title>
  <meta name="description" content="Application pour gérer, créer et organiser vos prompts IA">
  <style>
${cssContent}
  </style>
</head>
<body>
  <script>
(function() {
  'use strict';

${jsBundle}

  // Démarrage de l'application
  document.addEventListener('DOMContentLoaded', function() {
    const app = new App();
    app.init();
  });
})();
  </script>
</body>
</html>`;

  // Écrire le fichier
  fs.writeFileSync(OUTPUT_FILE, html, 'utf-8');

  // Créer aussi index.html pour Tauri
  const indexFile = path.join(DIST_DIR, 'index.html');
  fs.writeFileSync(indexFile, html, 'utf-8');

  const stats = fs.statSync(OUTPUT_FILE);
  const sizeKB = (stats.size / 1024).toFixed(1);

  console.log(`✅ Build terminé !`);
  console.log(`📄 Fichier: ${OUTPUT_FILE}`);
  console.log(`📄 Fichier Tauri: ${indexFile}`);
  console.log(`📦 Taille: ${sizeKB} KB`);
  console.log('');
  console.log('Pour utiliser l\'application :');
  console.log('- Web: Ouvre prompt-manager.html dans un navigateur');
  console.log('- Tauri: npm run tauri:dev');
  console.log('');
}

// Exécuter le build
build();
