'use client';

import { useState } from 'react';
import { Copy, Check, Sparkles, FileText } from 'lucide-react';

export function PrePlanDemo() {
  const [objectives, setObjectives] = useState({
    addition: true,
    comparison: true,
    multiplication: false,
    problems: false,
  });

  const [structure, setStructure] = useState({
    discovery: true,
    course: true,
    exercises: true,
    computer: false,
    evaluation: true,
  });

  const [supports, setSupports] = useState({
    latex: true,
    slideshow: false,
    exerciseSheet: true,
    qcm: false,
  });

  const [remarks, setRemarks] = useState({
    objectives: '',
    structure: '',
    supports: '',
  });

  const [generatedPrompt, setGeneratedPrompt] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const objectiveLabels = {
    addition: 'Additionner et soustraire des fractions',
    comparison: 'Comparer des fractions',
    multiplication: 'Multiplier des fractions',
    problems: 'Résoudre des problèmes avec fractions',
  };

  const structureLabels = {
    discovery: 'Séance découverte (activité de manipulation)',
    course: 'Séance de cours (institutionnalisation)',
    exercises: 'Séance d\'exercices (entraînement)',
    computer: 'Séance informatique (tableur/GeoGebra)',
    evaluation: 'Séance d\'évaluation',
  };

  const supportsLabels = {
    latex: 'Documents LaTeX (bfcours)',
    slideshow: 'Diaporama de cours',
    exerciseSheet: 'Fiche d\'exercices séparée',
    qcm: 'QCM d\'évaluation interactif',
  };

  const supportsSkills = {
    latex: '/skills/tex-document-creator',
    slideshow: '/skills/beamer-presentation',
    exerciseSheet: '/skills/tex-document-creator',
    qcm: '/skills/qcm-creator',
  };

  const handleObjectiveChange = (key: keyof typeof objectives) => {
    setObjectives(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleStructureChange = (key: keyof typeof structure) => {
    setStructure(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSupportsChange = (key: keyof typeof supports) => {
    setSupports(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleRemarksChange = (section: keyof typeof remarks, value: string) => {
    setRemarks(prev => ({ ...prev, [section]: value }));
  };

  const generatePrompt = () => {
    const checkedObjectives = Object.entries(objectives)
      .filter(([_, checked]) => checked)
      .map(([key]) => objectiveLabels[key as keyof typeof objectiveLabels]);

    const checkedStructure = Object.entries(structure)
      .filter(([_, checked]) => checked)
      .map(([key]) => structureLabels[key as keyof typeof structureLabels]);

    const checkedSupports = Object.entries(supports)
      .filter(([_, checked]) => checked)
      .map(([key]) => supportsLabels[key as keyof typeof supportsLabels]);

    let prompt = `# Rôle
Tu es un enseignant de mathématiques en collège.

# Contexte
- Classe de 5ème
- Séquence sur les fractions
- Objectifs : ${checkedObjectives.length > 0 ? checkedObjectives.map((obj, i) => `${i + 1}. ${obj}`).join('\n  ') : 'non spécifiés'}

# Structure de la séquence
`;

    checkedStructure.forEach((item, index) => {
      prompt += `${index + 1}. ${item}\n`;
    });

    prompt += `\n# Supports demandés\n`;
    checkedSupports.forEach((item, index) => {
      prompt += `${index + 1}. ${item}\n`;
    });

    const allRemarks = [
      remarks.objectives && `**Objectifs :** ${remarks.objectives}`,
      remarks.structure && `**Structure :** ${remarks.structure}`,
      remarks.supports && `**Supports :** ${remarks.supports}`,
    ]
      .filter(Boolean)
      .join('\n\n');

    if (allRemarks) {
      prompt += `\n# Remarques de l'enseignant\n${allRemarks}\n`;
    }

    prompt += `\n# Consigne
Produis cette séquence étape par étape en suivant la structure ci-dessus.`;

    setGeneratedPrompt(prompt);
  };

  const copyPrompt = () => {
    if (generatedPrompt) {
      navigator.clipboard.writeText(generatedPrompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-6 h-6 text-violet-400" />
          <h2 className="text-3xl font-bold text-white">Mini pré-plan interactif</h2>
        </div>
        <p className="text-gray-300">Cochez vos choix, ajoutez vos remarques, puis générez le prompt</p>
      </div>

      <div className="space-y-6 mb-8">
        {/* Objectifs Section */}
        <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-violet-500/20 flex items-center justify-center text-violet-400 font-bold text-sm">
              1
            </div>
            <h3 className="text-xl font-semibold text-white">Objectifs de la séquence</h3>
          </div>

          <div className="space-y-3 mb-4">
            {Object.entries(objectives).map(([key, checked]) => (
              <label key={key} className="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleObjectiveChange(key as keyof typeof objectives)}
                  className="w-5 h-5 rounded accent-violet-500 cursor-pointer"
                />
                <span className="text-gray-300 group-hover:text-white transition-colors">
                  {objectiveLabels[key as keyof typeof objectiveLabels]}
                </span>
              </label>
            ))}
          </div>

          <textarea
            value={remarks.objectives}
            onChange={e => handleRemarksChange('objectives', e.target.value)}
            placeholder="Remarques sur les objectifs..."
            className="w-full px-4 py-2 bg-black/30 border border-white/10 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-violet-500/50 transition-colors resize-none"
            rows={3}
          />
        </div>

        {/* Structure Section */}
        <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-violet-500/20 flex items-center justify-center text-violet-400 font-bold text-sm">
              2
            </div>
            <h3 className="text-xl font-semibold text-white">Structure des séances</h3>
          </div>

          <div className="space-y-3 mb-4">
            {Object.entries(structure).map(([key, checked]) => (
              <label key={key} className="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleStructureChange(key as keyof typeof structure)}
                  className="w-5 h-5 rounded accent-violet-500 cursor-pointer"
                />
                <span className="text-gray-300 group-hover:text-white transition-colors">
                  {structureLabels[key as keyof typeof structureLabels]}
                </span>
              </label>
            ))}
          </div>

          <textarea
            value={remarks.structure}
            onChange={e => handleRemarksChange('structure', e.target.value)}
            placeholder="Remarques sur la structure..."
            className="w-full px-4 py-2 bg-black/30 border border-white/10 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-violet-500/50 transition-colors resize-none"
            rows={3}
          />
        </div>

        {/* Supports Section */}
        <div className="backdrop-blur-md bg-white/5 border border-white/10 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-violet-500/20 flex items-center justify-center text-violet-400 font-bold text-sm">
              3
            </div>
            <h3 className="text-xl font-semibold text-white">Supports et format</h3>
          </div>

          <div className="space-y-3 mb-4">
            {Object.entries(supports).map(([key, checked]) => (
              <label key={key} className="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleSupportsChange(key as keyof typeof supports)}
                  className="w-5 h-5 rounded accent-violet-500 cursor-pointer"
                />
                <span className="text-gray-300 group-hover:text-white transition-colors">
                  {supportsLabels[key as keyof typeof supportsLabels]}
                </span>
              </label>
            ))}
          </div>

          <textarea
            value={remarks.supports}
            onChange={e => handleRemarksChange('supports', e.target.value)}
            placeholder="Remarques sur les supports..."
            className="w-full px-4 py-2 bg-black/30 border border-white/10 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-violet-500/50 transition-colors resize-none"
            rows={3}
          />
        </div>
      </div>

      {/* Generate Button */}
      <div className="mb-8 flex gap-4 items-center">
        <button
          onClick={generatePrompt}
          className="px-6 py-3 rounded-lg font-medium text-white transition-all duration-300 flex items-center gap-2 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 shadow-lg hover:shadow-violet-500/20"
        >
          <Sparkles className="w-5 h-5" />
          Générer le prompt optimisé
        </button>

        <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
          <FileText className="w-4 h-4 text-emerald-400" />
          <span className="text-sm text-emerald-300">~2000 tokens économisés</span>
        </div>
      </div>

      {/* Generated Prompt */}
      {generatedPrompt && (
        <div className="animate-in fade-in duration-300">
          <div className="backdrop-blur-md bg-black/40 border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                <FileText className="w-5 h-5 text-violet-400" />
                Prompt généré
              </h3>
              <button
                onClick={copyPrompt}
                className="p-2 rounded-lg bg-violet-500/20 hover:bg-violet-500/30 text-violet-300 transition-colors flex items-center gap-2"
                title="Copier le prompt"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4" />
                    <span className="text-sm">Copié !</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    <span className="text-sm">Copier</span>
                  </>
                )}
              </button>
            </div>

            <pre className="bg-black/50 border border-white/5 rounded-lg p-4 overflow-x-auto text-sm text-gray-200 font-mono whitespace-pre-wrap break-words">
              {generatedPrompt}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
