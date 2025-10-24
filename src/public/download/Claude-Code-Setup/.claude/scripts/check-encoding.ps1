# Script pour vérifier et corriger automatiquement l'encodage UTF-8 des fichiers
param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Vérifier que le fichier existe
if (-not (Test-Path $FilePath)) {
    Write-Host "Fichier non trouvé: $FilePath"
    exit 0
}

# Ne traiter que les fichiers supportés
if ($FilePath -notmatch '\.(tex|md|py|html|js|json)$') {
    exit 0
}

# Chemin vers le script Python de correction d'encodage
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "fix_encoding_simple.py"

# Vérifier que le script Python existe
if (-not (Test-Path $PythonScript)) {
    Write-Host "Script Python non trouvé: $PythonScript"
    exit 1
}

# Exécuter le script Python pour corriger l'encodage
try {
    python $PythonScript $FilePath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Encodage UTF-8 vérifié/corrigé: $FilePath"
    }
} catch {
    Write-Host "Erreur lors de la vérification de l'encodage: $_"
    exit 1
}

exit 0
