/**
 * find_latex_def_command.js
 * Script pour rechercher la définition d'une commande LaTeX dans un dossier de packages
 * et ouvrir automatiquement le fichier à la ligne spécifique
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


// Configuration par défaut pour l'éditeur
const EDITOR_CONFIG = {
  // Commande pour ouvrir l'éditeur (à adapter selon votre éditeur préféré)
  editorCommand: 'code',
  editorArgs: ['%f', '-g', '%f:%l']
};

// Charger la configuration depuis le fichier config.json
let CONFIG = null;
try {
  const configPath = path.join(__dirname, 'config.json');
  const configContent = fs.readFileSync(configPath, 'utf8');
  CONFIG = JSON.parse(configContent);
} catch (error) {
  console.error('Erreur lors du chargement du fichier config.json:', error);
  console.error('Utilisation de la configuration par défaut...');
  // Configuration de secours si le fichier n'existe pas
  CONFIG = {
    packageDirs: [
      "C:\\Users\\Utilisateur\\Documents\\Professionnel\\1. Reims 2023 - 2024\\1. Cours\\366_fonctionnement\\366_Archetype\\0. Entetes\\localtexmf\\tex\\latex\\BFcours",
      "C:\\Users\\Utilisateur\\Documents\\Professionnel\\1. Reims 2023 - 2024\\1. Cours\\366_fonctionnement\\366_Archetype\\0. Entetes\\localtexmf\\tex\\latex\\BFcours_Chapter_commands"
    ],
    fileExtensions: ['.tex', '.sty', '.cls', '.dtx']
  };
}

/**
 * Recherche les définitions dans un fichier donné
 * @param {string} filePath - Chemin du fichier à analyser
 * @param {string} commandName - Nom de la commande à rechercher
 * @returns {Promise<Array>} - Tableau des résultats trouvés
 */
async function searchInFile(filePath, commandName) {
  return new Promise((resolve, reject) => {
    const results = [];
    const fileStream = fs.createReadStream(filePath, { encoding: 'utf8' });
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });
    
    let lineNumber = 0;
    let buffer = [];
    
    rl.on('line', (line) => {
      lineNumber++;
      
      // Gardons un tampon des 5 dernières lignes pour le contexte
      buffer.push({ line, number: lineNumber });
      if (buffer.length > 5) buffer.shift();
      
      // Vérifier chaque patron pour voir s'il correspond à la ligne
      for (const pattern of DEFINITION_PATTERNS) {
        pattern.lastIndex = 0; // Réinitialiser le regex pour la nouvelle ligne
        
        let match;
        while ((match = pattern.exec(line)) !== null) {
          // match[1] ou match[2] contient généralement le nom de la commande/environnement
          // selon le patron qui a été utilisé
          const foundName = match[2] || match[1];
          
          // Si c'est la commande que nous recherchons
          if (foundName && foundName.trim() === commandName.trim()) {
            results.push({
              filePath,
              lineNumber,
              line,
              context: [...buffer].map(b => `${b.number}: ${b.line}`),
              match: match[0]
            });
          }
        }
      }
    });
    
    rl.on('close', () => {
      resolve(results);
    });
    
    rl.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * Parcourt récursivement un répertoire à la recherche de fichiers LaTeX
 * @param {string} dirPath - Chemin du répertoire à analyser
 * @param {string} commandName - Nom de la commande à rechercher
 * @param {Array<string>} fileExtensions - Extensions de fichiers à analyser
 * @returns {Promise<Array>} - Tableau cumulatif des résultats trouvés
 */
async function scanDirectory(dirPath, commandName, fileExtensions) {
  let results = [];
  
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        // Récursion dans les sous-répertoires
        const subResults = await scanDirectory(fullPath, commandName, fileExtensions);
        results = results.concat(subResults);
      } else if (entry.isFile() && fileExtensions.includes(path.extname(entry.name))) {
        // Analyser le fichier si son extension est dans la liste
        try {
          const fileResults = await searchInFile(fullPath, commandName);
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
 * Lance la recherche dans les répertoires spécifiés
 * @param {string} commandName - Nom de la commande à rechercher
 * @returns {Promise<Array>} - Tableau des résultats de recherche
 */
async function findLatexCommand(commandName) {
  console.log(`Recherche de la commande '${commandName}'...`);
  console.log('Cette opération peut prendre quelques minutes. Veuillez patienter...');
  
  if (!commandName) {
    return [];
  }
  
  // Supprimer le backslash initial si présent
  if (commandName.startsWith('\\')) {
    commandName = commandName.substring(1);
  }
  
  let searchResults = [];
  
  // Rechercher dans tous les répertoires configurés
  for (const packageDir of CONFIG.packageDirs) {
    try {
      console.log(`Analyse du répertoire ${packageDir}`);
      const results = await scanDirectory(
        packageDir,
        commandName,
        CONFIG.fileExtensions
      );
      searchResults = searchResults.concat(results);
    } catch (error) {
      console.error(`Erreur lors de la recherche dans ${packageDir}:`, error);
    }
  }
  
  return searchResults;
}

/**
 * Crée un lien cliquable pour les terminaux qui supportent cette fonctionnalité
 * @param {string} filePath - Chemin du fichier
 * @param {number} lineNumber - Numéro de ligne
 * @returns {string} - Lien formaté
 */
function createClickableLink(filePath, lineNumber) {
  // Convertir le chemin en URI valide
  const fileUri = `file:///${filePath.replace(/\\/g, '/')}`;
  // Format VSCode: vscode://file/{file}:{line}
  const vscodeUri = `vscode://file/${fileUri.substring(8)}:${lineNumber}`;
  return vscodeUri;
}

/**
 * Ouvre le fichier dans l'éditeur à la ligne spécifique
 * @param {string} filePath - Chemin du fichier à ouvrir
 * @param {number} lineNumber - Numéro de ligne à afficher
 * @param {Function} callback - Fonction à appeler une fois l'opération terminée
 */
function openFileAtLine(filePath, lineNumber, callback = () => {}) {
  console.log(`Ouverture de ${filePath} à la ligne ${lineNumber}...`);
  const childProcess = require('child_process');
  
  // Utiliser l'option 2 qui fonctionne pour vous
  const command = `code -g "${filePath}:${lineNumber}"`;
  
  childProcess.exec(command, (error) => {
    if (!error) {
      console.log(`Fichier ouvert avec VS Code à la ligne ${lineNumber}.`);
    } else {
      // Fallback en cas d'échec
      console.error(`Erreur avec VS Code: ${error.message}`);
      childProcess.exec(`start "" "${filePath}"`, (fallbackError) => {
        if (!fallbackError) {
          console.log(`Fichier ouvert avec l'application par défaut. Allez manuellement à la ligne ${lineNumber}.`);
        } else {
          console.error(`Erreur lors de l'ouverture du fichier: ${fallbackError.message}`);
        }
      });
    }
    
    // Appeler le callback quand c'est terminé
    callback();
  });
}
/**
 * Interface en ligne de commande interactive
 */
/**
 * Interface en ligne de commande interactive avec meilleure gestion de l'asynchronicité
 */
async function interactiveMode() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  function promptUser() {
    return new Promise((resolve) => {
      rl.question('\nEntrez le nom de la commande LaTeX à rechercher (sans le \\) ou "q" pour quitter : ', (answer) => {
        resolve(answer.trim());
      });
    });
  }
  
  console.log('\n=== Recherche de commandes LaTeX ===');
  console.log('-----------------------------------');
  
  while (true) {
    const commandName = await promptUser();
    
    if (commandName.toLowerCase() === 'q') {
      console.log('Au revoir !');
      rl.close();
      break;
    }
    
    if (!commandName) {
      console.log('Veuillez entrer un nom de commande valide.');
      continue;
    }
    
    try {
      const results = await findLatexCommand(commandName);
      
      if (results.length === 0) {
        console.log(`\nAucun résultat trouvé pour la commande '${commandName}'.`);
      } else if (results.length === 1) {
        // Un seul résultat, l'afficher et ouvrir le fichier
        console.log(`\nUn résultat trouvé pour '${commandName}' dans ${results[0].filePath} (ligne ${results[0].lineNumber})`);
        console.log('----------------------------------------------------------------------');
        console.log(results[0].line);
        console.log('----------------------------------------------------------------------');
        console.log('Ouverture du fichier...');
        
        // Attendre que le fichier soit ouvert avant de continuer
        await new Promise(resolve => {
          openFileAtLine(results[0].filePath, results[0].lineNumber, () => {
            // Callback appelé lorsque l'ouverture est terminée
            setTimeout(resolve, 1000); // Attendre encore 1 seconde pour être sûr
          });
        });
        
      } else {
        // Plusieurs résultats, les afficher
        console.log(`\n${results.length} résultats trouvés pour la commande '${commandName}' :`);
        
        results.forEach((result, index) => {
          console.log(`\n[${index + 1}] ${result.filePath} (ligne ${result.lineNumber})`);
          console.log('----------------------------------------------------------------------');
          console.log(result.line);
          console.log('----------------------------------------------------------------------');
        });
        
        // Demander quel résultat ouvrir
        const chooseResult = async () => {
          return new Promise((resolve) => {
            rl.question(`\nEntrez le numéro du résultat à ouvrir (1-${results.length}) ou "r" pour revenir : `, (answer) => {
              resolve(answer.trim());
            });
          });
        };
        
        const choice = await chooseResult();
        
        if (choice.toLowerCase() !== 'r') {
          const index = parseInt(choice) - 1;
          if (index >= 0 && index < results.length) {
            const result = results[index];
            console.log('Ouverture du fichier...');
            
            // Attendre que le fichier soit ouvert avant de continuer
            await new Promise(resolve => {
              openFileAtLine(result.filePath, result.lineNumber, () => {
                setTimeout(resolve, 1000);
              });
            });
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
  // Si un argument est fourni, l'utiliser comme nom de commande
  const commandName = process.argv[2];
  
  if (commandName) {
    try {
      const results = await findLatexCommand(commandName);
      
      if (results.length === 0) {
        console.log(`\nAucun résultat trouvé pour la commande '${commandName}'.`);
      } else if (results.length === 1) {
        // Ouvrir directement le fichier si un seul résultat est trouvé
        console.log(`\nUn résultat trouvé pour '${commandName}' dans ${results[0].filePath} (ligne ${results[0].lineNumber})`);
        console.log('----------------------------------------------------------------------');
        console.log(results[0].line);
        console.log('----------------------------------------------------------------------');
        console.log('Ouverture du fichier...');
        openFileAtLine(results[0].filePath, results[0].lineNumber);
      } else {
        // Afficher la liste si plusieurs résultats
        console.log(`\n${results.length} résultats trouvés pour la commande '${commandName}' :`);
        
        results.forEach((result, index) => {
          console.log(`\n[${index + 1}] ${result.filePath} (ligne ${result.lineNumber})`);
          console.log('----------------------------------------------------------------------');
          console.log(result.line);
          console.log('----------------------------------------------------------------------');
        });
        
        // Demander directement quel fichier ouvrir
        const choice = await new Promise((resolve) => {
          rl.question(`\nEntrez le numéro du résultat à ouvrir (1-${results.length}) : `, (answer) => {
            resolve(answer.trim());
          });
        });
        
        const index = parseInt(choice) - 1;
        if (index >= 0 && index < results.length) {
          const result = results[index];
          openFileAtLine(result.filePath, result.lineNumber);
        } else {
          console.log('Choix invalide.');
        }
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
