#!/usr/bin/env node

/**
 * Hook de logging des erreurs d'agents
 *
 * Ce script est exécuté après chaque appel au Task tool (agents)
 * Il analyse le résultat et logue les erreurs dans un fichier dédié
 */

const fs = require('fs');
const path = require('path');

// Configuration
const PROJECT_DIR = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const LOG_FILE = path.join(PROJECT_DIR, '.claude', 'hooks', 'agent-errors.log');
const TOOL_OUTPUT = process.env.CLAUDE_TOOL_OUTPUT || '';

/**
 * Parse le résultat du tool pour détecter les erreurs
 */
function detectErrors(toolOutput) {
  const errors = [];

  // Détection d'erreurs LaTeX
  const latexErrors = toolOutput.match(/LaTeX Error:.*?(?=\n|$)/g);
  if (latexErrors) {
    errors.push(...latexErrors.map(err => ({
      type: 'latex',
      message: err,
      severity: 'error'
    })));
  }

  // Détection d'erreurs de compilation
  const compileErrors = toolOutput.match(/(?:Error|ERROR):.*?(?=\n|$)/gi);
  if (compileErrors) {
    errors.push(...compileErrors.map(err => ({
      type: 'compilation',
      message: err,
      severity: 'error'
    })));
  }

  // Détection de warnings
  const warnings = toolOutput.match(/(?:Warning|WARNING):.*?(?=\n|$)/gi);
  if (warnings) {
    errors.push(...warnings.map(warn => ({
      type: 'warning',
      message: warn,
      severity: 'warning'
    })));
  }

  // Détection d'erreurs Bash (exit code non-zero, command not found, etc.)
  if (toolOutput.match(/command not found|No such file or directory|Permission denied|syntax error/i)) {
    const bashError = toolOutput.match(/(command not found|No such file or directory|Permission denied|syntax error).*?(?=\n|$)/i);
    if (bashError) {
      errors.push({
        type: 'bash',
        message: bashError[0],
        severity: 'error'
      });
    }
  }

  // Détection d'erreurs d'outils (Edit, Write, Read, etc.)
  if (toolOutput.includes('<error>')) {
    const errorMatch = toolOutput.match(/<error>(.*?)<\/error>/s);
    errors.push({
      type: 'tool-error',
      message: errorMatch ? errorMatch[1].substring(0, 200) : 'Tool returned error',
      severity: 'error',
      details: toolOutput.substring(0, 500)
    });
  }

  // Détection d'échecs d'agents
  if (toolOutput.includes('Failed') || toolOutput.includes('ERREUR') || toolOutput.includes('Échec')) {
    errors.push({
      type: 'agent-failure',
      message: 'Agent returned failure status',
      severity: 'error',
      details: toolOutput.substring(0, 500)
    });
  }

  // Détection d'erreurs Python
  const pythonErrors = toolOutput.match(/(?:Traceback|Exception|.*Error):.*?(?=\n\n|$)/gs);
  if (pythonErrors) {
    errors.push(...pythonErrors.map(err => ({
      type: 'python',
      message: err.substring(0, 200),
      severity: 'error'
    })));
  }

  // Détection d'erreurs Node.js
  if (toolOutput.match(/Error:.*at.*\(.*:\d+:\d+\)/s)) {
    const nodeError = toolOutput.match(/(Error:.*?)(?=\n\n|$)/s);
    if (nodeError) {
      errors.push({
        type: 'nodejs',
        message: nodeError[1].substring(0, 200),
        severity: 'error'
      });
    }
  }

  // Détection de packages manquants
  if (toolOutput.match(/package.*not found|module.*not found|cannot find module/i)) {
    const pkgError = toolOutput.match(/(package.*not found|module.*not found|cannot find module).*?(?=\n|$)/i);
    if (pkgError) {
      errors.push({
        type: 'missing-dependency',
        message: pkgError[0],
        severity: 'error'
      });
    }
  }

  return errors;
}

/**
 * Logue les erreurs dans le fichier de log
 */
function logErrors(errors, hookData = {}) {
  if (errors.length === 0) return;

  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    errors,
    tool: hookData.tool || 'unknown',
    context: {
      toolOutput: TOOL_OUTPUT.substring(0, 1000), // Limiter la taille
      projectDir: PROJECT_DIR,
      filePaths: process.env.CLAUDE_FILE_PATHS || ''
    }
  };

  // Créer le dossier .claude si nécessaire
  const claudeDir = path.dirname(LOG_FILE);
  if (!fs.existsSync(claudeDir)) {
    fs.mkdirSync(claudeDir, { recursive: true });
  }

  // Ajouter au fichier de log (format JSONL)
  const logLine = JSON.stringify(logEntry) + '\n';
  fs.appendFileSync(LOG_FILE, logLine, 'utf8');

  console.error(`[Hook] ${errors.length} erreur(s) de ${logEntry.tool} loguée(s) dans ${LOG_FILE}`);
}

/**
 * Point d'entrée principal
 */
function main() {
  try {
    // Lire stdin (données JSON du hook)
    let stdinData = '';

    // Si pas de stdin, utiliser juste TOOL_OUTPUT
    if (!process.stdin.isTTY && process.stdin.readable) {
      process.stdin.on('data', chunk => {
        stdinData += chunk.toString();
      });

      process.stdin.on('end', () => {
        processHook(stdinData);
      });
    } else {
      processHook('');
    }
  } catch (error) {
    console.error('[Hook Error]', error.message);
    process.exit(0); // Ne pas bloquer l'exécution
  }
}

function processHook(stdinData) {
  let hookData = {};

  // Parser les données JSON du hook si disponibles
  if (stdinData && stdinData.trim()) {
    try {
      hookData = JSON.parse(stdinData);
    } catch (e) {
      // Ignorer l'erreur de parsing, continuer sans les données du hook
    }
  }

  const errors = detectErrors(TOOL_OUTPUT);

  if (errors.length > 0) {
    logErrors(errors, hookData);
  }

  // Toujours retourner succès pour ne pas bloquer
  process.exit(0);
}

// Exécution
main();
