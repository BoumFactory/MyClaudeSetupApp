# Script PowerShell pour jouer des sons sur Windows
param(
    [string]$SoundFile
)

if (Test-Path $SoundFile) {
    # Utilise la classe SoundPlayer de .NET pour jouer le son
    Add-Type -AssemblyName System.Windows.Forms
    $sound = New-Object System.Media.SoundPlayer $SoundFile
    $sound.PlaySync()
} else {
    Write-Warning "Fichier audio introuvable : $SoundFile"
}