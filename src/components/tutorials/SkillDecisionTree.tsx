'use client';

import { useState } from 'react';
import { Copy, Check, ChevronRight, Sparkles } from 'lucide-react';

interface StepState {
  format: string;
  niveau: string;
  theme: string;
  nombre: string;
  objectif: string;
  source: string;
  type: string;
}

interface StepOverride {
  format: string;
  niveau: string;
  theme: string;
  nombre: string;
  objectif: string;
  source: string;
  type: string;
}

const FORMAT_OPTIONS = ['LaTeX (bfcours)', 'HTML interactif', 'Diaporama Reveals', 'PDF simple'];
const NIVEAU_OPTIONS = ['6ème', '5ème', '4ème', '3ème', '2nde', '1ère', 'Terminale'];
const THEME_OPTIONS = [
  'Nombres et calculs',
  'Géométrie',
  'Grandeurs et mesures',
  'Organisation de données',
  'Algèbre et fonctions',
  'Probabilités et statistiques',
];
const NOMBRE_OPTIONS = ['3', '5', '8', '10', 'Personnalisé'];
const OBJECTIF_OPTIONS = [
  'Évaluation diagnostique',
  'Entraînement',
  'Évaluation sommative',
  'Remédiation',
];
const SOURCE_OPTIONS = [
  'Programmes officiels (BO)',
  'Mon cours personnel',
  'Pas de source spécifique',
];
const TYPE_OPTIONS = ['Statique (document)', 'Dynamique (application web)'];

export function SkillDecisionTree() {
  const [state, setState] = useState<StepState>({
    format: '',
    niveau: '',
    theme: '',
    nombre: '',
    objectif: '',
    source: '',
    type: '',
  });

  const [overrides, setOverrides] = useState<StepOverride>({
    format: '',
    niveau: '',
    theme: '',
    nombre: '',
    objectif: '',
    source: '',
    type: '',
  });

  const [copied, setCopied] = useState(false);

  const getSkillsForState = () => {
    const skills = new Set<string>();

    const formatMap: Record<string, string> = {
      'LaTeX (bfcours)': 'bfcours-latex',
      'HTML interactif': 'educational-app-builder',
      'Diaporama Reveals': 'reveals-presentation',
      'PDF simple': 'pdf',
    };

    const format = overrides.format || state.format;
    const theme = overrides.theme || state.theme;
    const type = overrides.type || state.type;
    const source = overrides.source || state.source;

    if (format && formatMap[format]) {
      skills.add(formatMap[format]);
    }

    if (theme === 'Géométrie') {
      skills.add('image-generator');
      skills.add('pdf2tikz');
    }

    if (source === 'Programmes officiels (BO)') {
      skills.add('programmes-officiels');
    }

    if (type === 'Dynamique (application web)' && format !== 'HTML interactif') {
      skills.add('educational-app-builder');
    }

    return Array.from(skills);
  };

  const generatePrompt = () => {
    const format = overrides.format || state.format;
    const niveau = overrides.niveau || state.niveau;
    const theme = overrides.theme || state.theme;
    const nombre = overrides.nombre || state.nombre;
    const objectif = overrides.objectif || state.objectif;
    const source = overrides.source || state.source;
    const type = overrides.type || state.type;

    const skills = getSkillsForState();
    const skillMappings: Record<string, string> = {
      'bfcours-latex': '/createTex',
      'educational-app-builder': '/create-app',
      'reveals-presentation': '/createReveals',
      'pdf': '/pdf',
      'image-generator': '/generate-image',
      'pdf2tikz': '/pdf2tikz',
      'programmes-officiels': '/programmes-officiels',
    };

    let prompt = '# Rôle\nTu es un enseignant de mathématiques expérimenté.\n\n';
    prompt += '# Contexte\n';

    if (niveau) prompt += `- Niveau : ${niveau}\n`;
    if (theme) prompt += `- Thème : ${theme}\n`;
    if (objectif) prompt += `- Objectif : ${objectif}\n`;

    prompt += '\n# Source\n';
    if (source === 'Programmes officiels (BO)') {
      prompt += `${skillMappings['programmes-officiels']} ${niveau} ${theme}\n`;
    } else if (source === 'Mon cours personnel') {
      prompt += '@mon-cours.tex\n';
    } else {
      prompt += '(Pas de source spécifique)\n';
    }

    prompt += '\n# Tâche\n';
    prompt += '## Étape 1 : Recherche des compétences\n';
    if (source === 'Programmes officiels (BO)') {
      prompt += 'Consulte les programmes officiels pour identifier les compétences visées.\n\n';
    } else {
      prompt += 'Identifie les objectifs pédagogiques visés.\n\n';
    }

    prompt += '## Étape 2 : Création du QCM\n';
    const primarySkill = skills.find(
      (s) => s === 'bfcours-latex' || s === 'educational-app-builder' || s === 'reveals-presentation'
    );
    if (primarySkill && skillMappings[primarySkill]) {
      prompt += `${skillMappings[primarySkill]}\n`;
    }
    if (nombre) prompt += `- ${nombre} questions\n`;
    prompt += '- Difficulté progressive\n';
    prompt += '- Correction détaillée\n\n';

    if (theme === 'Géométrie') {
      prompt += 'Pour les figures géométriques :\n';
      prompt += `${skillMappings['image-generator']}\n`;
      prompt += `${skillMappings['pdf2tikz']}\n\n`;
    }

    prompt += '## Étape 3 : Vérification\n';
    prompt += 'Vérifie la cohérence mathématique et l\'alignement avec le programme.\n\n';

    prompt += '# Format\n';
    prompt += `- QCM ${type} au format ${format}\n`;
    prompt += '- Correction détaillée\n';

    return prompt;
  };

  const handleCopy = () => {
    const prompt = generatePrompt();
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const prompt = generatePrompt();
  const skills = getSkillsForState();

  const Step = ({
    title,
    options,
    value,
    onChange,
    overrideValue,
    onOverrideChange,
  }: {
    title: string;
    options: string[];
    value: string;
    onChange: (v: string) => void;
    overrideValue: string;
    onOverrideChange: (v: string) => void;
  }) => (
    <div className="space-y-3 p-4 rounded-lg bg-white/5 border border-white/10 hover:bg-white/7 transition-colors">
      <div className="flex items-center gap-2">
        {value && <ChevronRight className="w-4 h-4 text-blue-400" />}
        <h3 className="font-medium text-gray-200">{title}</h3>
      </div>

      <div className="space-y-2">
        <div className="grid grid-cols-2 gap-2">
          {options.map((option) => (
            <button
              key={option}
              onClick={() => {
                onChange(option);
                onOverrideChange('');
              }}
              className={`px-3 py-2 rounded-md text-sm transition-all ${
                value === option && !overrideValue
                  ? 'bg-blue-500/30 border border-blue-400/50 text-blue-200'
                  : 'bg-white/5 border border-white/10 text-gray-400 hover:bg-white/10'
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="pt-2 border-t border-white/5">
          <input
            type="text"
            placeholder="Ou saisir une valeur personnalisée..."
            value={overrideValue}
            onChange={(e) => {
              onOverrideChange(e.target.value);
              if (e.target.value) onChange('');
            }}
            className="w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-sm"
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 py-6">
      <div className="flex items-center gap-2 mb-8">
        <Sparkles className="w-5 h-5 text-blue-400" />
        <h2 className="text-2xl font-bold text-gray-100">Assistants de création de QCM</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Decision Tree */}
        <div className="lg:col-span-2 space-y-4">
          <Step
            title="1. Format de sortie"
            options={FORMAT_OPTIONS}
            value={state.format}
            onChange={(v) => setState({ ...state, format: v })}
            overrideValue={overrides.format}
            onOverrideChange={(v) => setOverrides({ ...overrides, format: v })}
          />

          {state.format || overrides.format ? (
            <Step
              title="2. Niveau"
              options={NIVEAU_OPTIONS}
              value={state.niveau}
              onChange={(v) => setState({ ...state, niveau: v })}
              overrideValue={overrides.niveau}
              onOverrideChange={(v) => setOverrides({ ...overrides, niveau: v })}
            />
          ) : null}

          {(state.niveau || overrides.niveau) && (state.format || overrides.format) ? (
            <Step
              title="3. Thème mathématique"
              options={THEME_OPTIONS}
              value={state.theme}
              onChange={(v) => setState({ ...state, theme: v })}
              overrideValue={overrides.theme}
              onOverrideChange={(v) => setOverrides({ ...overrides, theme: v })}
            />
          ) : null}

          {(state.theme || overrides.theme) && (state.niveau || overrides.niveau) ? (
            <Step
              title="4. Nombre de questions"
              options={NOMBRE_OPTIONS}
              value={state.nombre}
              onChange={(v) => setState({ ...state, nombre: v })}
              overrideValue={overrides.nombre}
              onOverrideChange={(v) => setOverrides({ ...overrides, nombre: v })}
            />
          ) : null}

          {(state.nombre || overrides.nombre) && (state.theme || overrides.theme) ? (
            <Step
              title="5. Objectif pédagogique"
              options={OBJECTIF_OPTIONS}
              value={state.objectif}
              onChange={(v) => setState({ ...state, objectif: v })}
              overrideValue={overrides.objectif}
              onOverrideChange={(v) => setOverrides({ ...overrides, objectif: v })}
            />
          ) : null}

          {(state.objectif || overrides.objectif) && (state.nombre || overrides.nombre) ? (
            <Step
              title="6. Source du contenu"
              options={SOURCE_OPTIONS}
              value={state.source}
              onChange={(v) => setState({ ...state, source: v })}
              overrideValue={overrides.source}
              onOverrideChange={(v) => setOverrides({ ...overrides, source: v })}
            />
          ) : null}

          {(state.source || overrides.source) && (state.objectif || overrides.objectif) ? (
            <Step
              title="7. Type de QCM"
              options={TYPE_OPTIONS}
              value={state.type}
              onChange={(v) => setState({ ...state, type: v })}
              overrideValue={overrides.type}
              onOverrideChange={(v) => setOverrides({ ...overrides, type: v })}
            />
          ) : null}
        </div>

        {/* Meta Info Panel */}
        {(state.source || overrides.source) && (state.type || overrides.type) ? (
          <div className="lg:col-span-1">
            <div className="sticky top-6 p-4 rounded-lg bg-gradient-to-b from-blue-500/10 to-purple-500/10 border border-blue-500/20 space-y-4">
              <h3 className="font-semibold text-gray-100 flex items-center gap-2">
                <Check className="w-4 h-4 text-green-400" />
                Configuration
              </h3>

              <div className="space-y-3 text-sm">
                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <div className="text-gray-500 text-xs mb-1">Sections du prompt</div>
                  <div className="text-lg font-bold text-blue-300">5</div>
                </div>

                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <div className="text-gray-500 text-xs mb-1">Skills utilisés</div>
                  <div className="text-lg font-bold text-blue-300">{skills.length}</div>
                </div>

                <div className="bg-white/5 rounded p-3 border border-white/10">
                  <div className="text-gray-500 text-xs mb-1">Étapes du workflow</div>
                  <div className="text-lg font-bold text-blue-300">3</div>
                </div>

                <div className="border-t border-white/10 pt-3">
                  <div className="text-gray-500 text-xs mb-2">Skills activés</div>
                  <div className="space-y-2">
                    {skills.length > 0 ? (
                      skills.map((skill) => (
                        <div
                          key={skill}
                          className="px-2 py-1 bg-blue-500/20 border border-blue-500/30 rounded text-xs text-blue-300 font-mono"
                        >
                          {skill}
                        </div>
                      ))
                    ) : (
                      <div className="text-gray-600 text-xs">Aucun skill</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : null}
      </div>

      {/* Generated Prompt */}
      {(state.source || overrides.source) && (state.type || overrides.type) ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-100">Prompt généré</h3>
            <button
              onClick={handleCopy}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                copied
                  ? 'bg-green-500/30 border border-green-500/50 text-green-200'
                  : 'bg-blue-500/30 border border-blue-500/50 text-blue-200 hover:bg-blue-500/40'
              }`}
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4" />
                  Copié !
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  Copier le prompt
                </>
              )}
            </button>
          </div>

          <div className="p-4 rounded-lg bg-white/5 border border-white/10 font-mono text-sm text-gray-300 overflow-auto max-h-96 space-y-1">
            {prompt.split('\n').map((line, i) => (
              <div key={i} className={line.startsWith('#') ? 'text-blue-300 font-semibold mt-2' : ''}>
                {line || <div className="h-2" />}
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Progress indicator */}
      {(state.format || overrides.format) && !(state.source || overrides.source) ? (
        <div className="p-4 rounded-lg bg-white/5 border border-white/10 text-center text-gray-400 text-sm">
          Continuez en sélectionnant les options suivantes...
        </div>
      ) : null}
    </div>
  );
}
