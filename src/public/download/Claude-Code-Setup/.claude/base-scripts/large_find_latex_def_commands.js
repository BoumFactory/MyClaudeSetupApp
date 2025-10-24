/**
 * large_find_latex_def_commands.js
 * Script pour rechercher de manière floue des commandes LaTeX dans un dossier de packages
 * avec gestion de la casse et suggestions de commandes similaires
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { spawn } = require('child_process');

// Patrons de recherche pour les différentes syntaxes de définition LaTeX
const DEFINITION_PATTERNS = [
  // Commandes standard
  /\\(re)?newcommand{?\\([^}]+)}?/g,
  /\\(re)?newcommand\*{?\\([^}]+)}?/g,
  /\\def\\([^{]+)/g,
  /\\gdef\\([^{]+)/g,
  /\\edef\\([^{]+)/g,
  /\\xdef\\([^{]+)/g,
  
  // Environnements
  /\\(re)?newenvironment{([^}]+)}/g,
  
  // tcolorbox
  /\\(re)?newtcolorbox{([^}]+)}/g,
  /\\DeclareTColorBox{([^}]+)}/g,
  
  // Autres définitions
  /\\newtheorem{([^}]+)}/g,
  /\\newcounter{([^}]+)}/g,
  
  // Syntaxes supplémentaires
  /\\NewDocumentEnvironment{([^}]+)}/g,
  /\\NewDocumentCommand{?\\([^}]+)}?/g,
  /\\NewDocumentCommand{([^}]+)}/g,
  /\\DeclareDocumentCommand{?\\([^}]+)}?/g,
  /\\DeclareDocumentCommand{([^}]+)}/g,
  /\\ProvideDocumentCommand{?\\([^}]+)}?/g,
  /\\ProvideDocumentCommand{([^}]+)}/g,

  //Couleurs
  /\\definecolor{?([^}]+)}?/g
];

// Charger la configuration depuis le fichier large_config.json
let CONFIG = null;
try {
  const configPath = path.join(__dirname, 'large_config.json');
  const configContent = fs.readFileSync(configPath, 'utf8');
  CONFIG = JSON.parse(configContent);
} catch (error) {
  console.error('Erreur lors du chargement du fichier large_config.json:', error);
  // Configuration de secours
  CONFIG = {
    packageDirs: [
      "C:\\Users\\Utilisateur\\Documents\\Professionnel\\1. Reims 2023 - 2024\\1. Cours\\366_fonctionnement\\366_Archetype\\0. Entetes\\localtexmf\\tex\\latex\\BFcours",
      "C:\\Users\\Utilisateur\\Documents\\Professionnel\\1. Reims 2023 - 2024\\1. Cours\\366_fonctionnement\\366_Archetype\\0. Entetes\\localtexmf\\tex\\latex\\BFcours_Chapter_commands"
    ],
    fileExtensions: ['.tex', '.sty', '.cls', '.dtx'],
    nbResultatMax: 20
  };
}

/**
 * Normalise une chaîne pour la comparaison (minuscules)
 * @param {string} str - Chaîne à normaliser
 * @returns {string} - Chaîne normalisée
 */
function normalizeString(str) {
  return str.toLowerCase().trim();
}

/**
 * Convertit une chaîne en format CamelCase/camelCase en snake_case pour la recherche
 * @param {string} str - Chaîne à convertir
 * @returns {string[]} - Tableau de variations possibles
 */
function getCaseVariations(str) {
  const variations = new Set();
  
  // Original
  variations.add(str);
  
  // Minuscules
  variations.add(str.toLowerCase());
  
  // Majuscules
  variations.add(str.toUpperCase());
  
  // Première lettre majuscule
  variations.add(str.charAt(0).toUpperCase() + str.slice(1).toLowerCase());
  
  // camelCase vers snake_case
  const snakeCase = str.replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '');
  variations.add(snakeCase);
  
  // snake_case vers camelCase
  const camelCase = str.replace(/_([a-z])/g, (match, p1) => p1.toUpperCase());
  variations.add(camelCase);
  
  // PascalCase
  const pascalCase = camelCase.charAt(0).toUpperCase() + camelCase.slice(1);
  variations.add(pascalCase);
  
  return Array.from(variations);
}

/**
 * Calcule un score de similarité entre deux chaînes
 * @param {string} searchTerm - Terme de recherche
 * @param {string} commandName - Nom de la commande trouvée
 * @param {string} definitionContent - Contenu complet de la définition
 * @param {string} filePath - Chemin du fichier contenant la définition
 * @returns {number} - Score de similarité (0-100)
 */
function calculateSimilarityScore(searchTerm, commandName, definitionContent = '', filePath = '') {
  const search = normalizeString(searchTerm);
  const command = normalizeString(commandName);
  
  // Malus éliminatoire pour les commandes qui commencent par 'old'
  if (command.startsWith('old')) {
    return 0;
  }
  
  let baseScore = 0;
  
  // Correspondance exacte
  if (search === command) {
    baseScore = 100;
  }
  // Commence par le terme recherché
  else if (command.startsWith(search)) {
    baseScore = 90;
  }
  // Contient le terme recherché
  else if (command.includes(search)) {
    baseScore = 70;
  }
  // Distance de Levenshtein simplifiée
  else {
    const maxLen = Math.max(search.length, command.length);
    const distance = levenshteinDistance(search, command);
    baseScore = ((maxLen - distance) / maxLen) * 50;
  }
  
  // Bonus pour la longueur de la définition (0-15 points)
  const lengthBonus = Math.min(15, definitionContent.length / 100);
  
  // Bonus pour la présence d'environnements (0-20 points)
  let environmentBonus = 0;
  const envPatterns = [
    /\\begin{/g,
    /\\end{/g,
    /\\newenvironment/g,
    /\\renewenvironment/g,
    /\\NewDocumentEnvironment/g,
    /\\newtcolorbox/g,
    /\\DeclareTColorBox/g,
    /minipage/g,
    /tabular/g,
    /array/g,
    /enumerate/g,
    /itemize/g,
    /align/g,
    /equation/g,
    /tikzpicture/g
  ];
  
  for (const pattern of envPatterns) {
    if (pattern.test(definitionContent)) {
      environmentBonus += 5;
      if (environmentBonus >= 20) break;
    }
  }
  
  // Score avant malus
  let finalScore = Math.min(100, baseScore + lengthBonus + environmentBonus);
  
  // Malus quasi éliminatoire pour le fichier bfcours-useCanMathalea.sty
  if (filePath.toLowerCase().includes('bfcours-usecanmathalea.sty')) {
    finalScore = Math.max(0, finalScore * 0.1); // Réduit le score à 10% de sa valeur
  }
  
  return Math.max(0, finalScore);
}

/**
 * Calcule la distance de Levenshtein entre deux chaînes
 * @param {string} a - Première chaîne
 * @param {string} b - Deuxième chaîne
 * @returns {number} - Distance
 */
function levenshteinDistance(a, b) {
  const matrix = [];
  
  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }
  
  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }
  
  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i - 1][j - 1] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j] + 1
        );
      }
    }
  }
  
  return matrix[b.length][a.length];
}

/**
 * Recherche les définitions dans un fichier avec recherche floue
 * @param {string} filePath - Chemin du fichier à analyser
 * @param {string} searchTerm - Terme de recherche
 * @returns {Promise<Array>} - Tableau des résultats trouvés avec scores
 */
async function searchInFileFuzzy(filePath, searchTerm) {
  return new Promise((resolve, reject) => {
    const results = [];
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const lines = fileContent.split('\n');
    
    const searchVariations = getCaseVariations(searchTerm);
    
    for (let lineNumber = 0; lineNumber < lines.length; lineNumber++) {
      const line = lines[lineNumber];
      
      for (const pattern of DEFINITION_PATTERNS) {
        pattern.lastIndex = 0;
        
        let match;
        while ((match = pattern.exec(line)) !== null) {
          const foundName = match[2] || match[1];
          
          if (foundName) {
            // Capturer le contenu de la définition (jusqu'à 50 lignes max)
            let definitionContent = line;
            let braceCount = 0;
            let inDefinition = true;
            let linesRead = 1;
            
            // Compter les accolades dans la première ligne
            for (let char of line) {
              if (char === '{') braceCount++;
              if (char === '}') braceCount--;
            }
            
            // Continuer à lire jusqu'à ce que les accolades soient équilibrées
            let currentLine = lineNumber + 1;
            while (inDefinition && currentLine < lines.length && linesRead < 50) {
              const nextLine = lines[currentLine];
              definitionContent += '\n' + nextLine;
              
              for (let char of nextLine) {
                if (char === '{') braceCount++;
                if (char === '}') braceCount--;
              }
              
              if (braceCount <= 0) {
                inDefinition = false;
              }
              
              currentLine++;
              linesRead++;
            }
            
            // Calculer le score de similarité avec le contenu
            let maxScore = 0;
            for (const variation of searchVariations) {
              const score = calculateSimilarityScore(variation, foundName, definitionContent, filePath);
              maxScore = Math.max(maxScore, score);
            }
            
            // Ne garder que les résultats avec un score minimum
            if (maxScore > 20) {
              // Créer le contexte (5 lignes avant et après)
              const contextStart = Math.max(0, lineNumber - 2);
              const contextEnd = Math.min(lines.length - 1, lineNumber + 2);
              const context = [];
              for (let i = contextStart; i <= contextEnd; i++) {
                context.push(`${i + 1}: ${lines[i]}`);
              }
              
              results.push({
                filePath,
                lineNumber: lineNumber + 1, // +1 car les lignes commencent à 1
                line,
                context,
                match: match[0],
                commandName: foundName,
                score: maxScore,
                definitionType: getDefinitionType(match[0]),
                definitionLength: definitionContent.length,
                hasEnvironments: /\\(begin|end|newenvironment|newtcolorbox|minipage|tabular|array|enumerate|itemize|align|equation|tikzpicture)/.test(definitionContent)
              });
            }
          }
        }
      }
    }
    
    resolve(results);
  });
}

/**
 * Détermine le type de définition LaTeX
 * @param {string} match - Chaîne correspondante
 * @returns {string} - Type de définition
 */
function getDefinitionType(match) {
  if (match.includes('newcommand')) return 'Commande';
  if (match.includes('def')) return 'Définition';
  if (match.includes('newenvironment')) return 'Environnement';
  if (match.includes('newtcolorbox')) return 'TColorBox';
  if (match.includes('newtheorem')) return 'Théorème';
  if (match.includes('newcounter')) return 'Compteur';
  if (match.includes('definecolor')) return 'Couleur';
  return 'Autre';
}

/**
 * Parcourt récursivement un répertoire avec recherche floue
 * @param {string} dirPath - Chemin du répertoire
 * @param {string} searchTerm - Terme de recherche
 * @param {Array<string>} fileExtensions - Extensions de fichiers
 * @returns {Promise<Array>} - Résultats trouvés
 */
async function scanDirectoryFuzzy(dirPath, searchTerm, fileExtensions) {
  let results = [];
  
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        const subResults = await scanDirectoryFuzzy(fullPath, searchTerm, fileExtensions);
        results = results.concat(subResults);
      } else if (entry.isFile() && fileExtensions.includes(path.extname(entry.name))) {
        try {
          const fileResults = await searchInFileFuzzy(fullPath, searchTerm);
          results = results.concat(fileResults);
        } catch (error) {
          console.error(`Erreur lors de l'analyse du fichier ${fullPath}:`, error);
        }
      }
    }
  } catch (error) {
    console.error(`Erreur lors de la lecture du répertoire ${dirPath}:`, error);
  }
  
  return results;
}

/**
 * Lance une recherche floue dans tous les répertoires
 * @param {string} searchTerm - Terme de recherche
 * @returns {Promise<Array>} - Résultats triés par score
 */
async function findLatexCommandFuzzy(searchTerm) {
  console.log(`\nRecherche floue pour '${searchTerm}'...`);
  console.log('Analyse des variations de casse et des commandes similaires...\n');
  
  if (!searchTerm) {
    return [];
  }
  
  // Supprimer le backslash initial si présent
  if (searchTerm.startsWith('\\')) {
    searchTerm = searchTerm.substring(1);
  }
  
  let allResults = [];
  
  // Rechercher dans tous les répertoires configurés
  for (const packageDir of CONFIG.packageDirs) {
    try {
      console.log(`Analyse du répertoire ${packageDir}...`);
      const results = await scanDirectoryFuzzy(
        packageDir,
        searchTerm,
        CONFIG.fileExtensions
      );
      allResults = allResults.concat(results);
    } catch (error) {
      console.error(`Erreur lors de la recherche dans ${packageDir}:`, error);
    }
  }
  
  // Trier par score décroissant et limiter au nombre max
  allResults.sort((a, b) => b.score - a.score);
  
  return allResults.slice(0, CONFIG.nbResultatMax);
}

/**
 * Lance la recherche exacte (appel au script original)
 * @param {string} commandName - Nom exact de la commande
 */
function launchExactSearch(commandName) {
  console.log(`\nLancement de la recherche exacte pour '${commandName}'...\n`);
  
  const scriptPath = path.join(__dirname, 'find_latex_def_command.js');
  const child = spawn('node', [scriptPath, commandName], {
    stdio: 'inherit'
  });
  
  child.on('error', (error) => {
    console.error('Erreur lors du lancement de la recherche exacte:', error);
  });
  
  child.on('close', (code) => {
    if (code !== 0) {
      console.error(`La recherche exacte s'est terminée avec le code ${code}`);
    }
  });
}

/**
 * Interface interactive pour la recherche floue
 */
async function interactiveMode() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  function promptUser() {
    return new Promise((resolve) => {
      rl.question('\nEntrez un terme de recherche approximatif (sans le \\) ou "q" pour quitter : ', (answer) => {
        resolve(answer.trim());
      });
    });
  }
  
  function promptChoice(max) {
    return new Promise((resolve) => {
      rl.question(`\nChoisissez un résultat (1-${max}) ou "r" pour revenir : `, (answer) => {
        resolve(answer.trim());
      });
    });
  }
  
  console.log('\n=== Recherche floue de commandes LaTeX ===');
  console.log('Trouvez des commandes même si vous n\'êtes pas sûr de l\'orthographe !');
  console.log('----------------------------------------');
  
  while (true) {
    const searchTerm = await promptUser();
    
    if (searchTerm.toLowerCase() === 'q') {
      console.log('Au revoir !');
      rl.close();
      break;
    }
    
    if (!searchTerm) {
      console.log('Veuillez entrer un terme de recherche.');
      continue;
    }
    
    try {
      const results = await findLatexCommandFuzzy(searchTerm);
      
      if (results.length === 0) {
        console.log(`\nAucun résultat trouvé pour '${searchTerm}'.`);
        console.log('Essayez avec un terme différent ou plus court.');
      } else {
        console.log(`\n${results.length} résultat(s) trouvé(s), trié(s) par pertinence :`);
        console.log('================================================================\n');
        
        results.forEach((result, index) => {
          console.log(`[${index + 1}] ${result.commandName} (Score: ${result.score.toFixed(0)}%)`);
          console.log(`    Type: ${result.definitionType}`);
          console.log(`    Fichier: ${path.basename(result.filePath)}`);
          console.log(`    Ligne ${result.lineNumber}: ${result.line.trim()}`);
          console.log(`    Longueur: ${result.definitionLength} caractères${result.hasEnvironments ? ' | ✓ Contient des environnements' : ''}`);
          console.log('    ---');
        });
        
        const choice = await promptChoice(results.length);
        
        if (choice.toLowerCase() !== 'r') {
          const index = parseInt(choice) - 1;
          if (index >= 0 && index < results.length) {
            const selectedResult = results[index];
            rl.close();
            launchExactSearch(selectedResult.commandName);
            break;
          } else {
            console.log('Choix invalide.');
          }
        }
      }
    } catch (error) {
      console.error('Erreur lors de la recherche :', error);
    }
  }
}

/**
 * Point d'entrée principal
 */
async function main() {
  const searchTerm = process.argv[2];
  
  if (searchTerm) {
    // Mode non-interactif avec argument
    try {
      const results = await findLatexCommandFuzzy(searchTerm);
      
      if (results.length === 0) {
        console.log(`\nAucun résultat trouvé pour '${searchTerm}'.`);
      } else if (results.length === 1) {
        // Un seul résultat, lancer directement la recherche exacte
        console.log(`\nUn seul résultat trouvé : ${results[0].commandName}`);
        launchExactSearch(results[0].commandName);
      } else {
        // Afficher les résultats et demander un choix
        console.log(`\n${results.length} résultat(s) trouvé(s) :`);
        results.forEach((result, index) => {
          console.log(`[${index + 1}] ${result.commandName} (Score: ${result.score.toFixed(0)}%) - ${result.definitionLength} car.${result.hasEnvironments ? ' [ENV]' : ''}`);
        });
        
        // Lancer automatiquement le premier résultat
        console.log(`\nLancement automatique du premier résultat...`);
        launchExactSearch(results[0].commandName);
      }
    } catch (error) {
      console.error('Erreur lors de la recherche :', error);
    }
  } else {
    // Mode interactif
    await interactiveMode();
  }
}

// Exécuter le script
main();
