# Guide LaTeX dans H5P

## Probleme Identifie

La gestion du LaTeX dans H5P necessite une attention particuliere car :
1. Le JSON requiert des backslashes doubles (`\\(` au lieu de `\(`)
2. L'echappement HTML peut casser les formules LaTeX
3. L'ordre des operations est critique

## Syntaxe LaTeX dans H5P

### Notations supportees
| Notation | Rendu | Usage |
|----------|-------|-------|
| `\(x^2\)` | inline | Formule dans le texte |
| `\[x^2\]` | block | Formule centree |
| `$x^2$` | inline | Alternative (convertir) |
| `$$x^2$$` | block | Alternative (convertir) |

### Dans le JSON
```json
{
  "question": "<p>Calculer \\(x^2\\) pour \\(x=3\\).</p>",
  "options": [
    {"text": "<p>\\(9\\)</p>", "correct": true},
    {"text": "<p>\\(6\\)</p>", "correct": false}
  ],
  "feedback": "<p>Car \\(3^2 = 3 \\times 3 = 9\\)</p>"
}
```

## Probleme Questions vs Reponses

### Symptome
Le LaTeX s'affiche correctement dans les questions mais pas dans les reponses/options.

### Cause
L'ordre des fonctions `escape_html()` et `wrap_math()` est incorrect :
```python
# MAUVAIS - dans h5p_advanced_generator.py ligne 513
"text": f"<p>{wrap_math(escape_html(opt))}</p>"

# Le probleme :
# 1. escape_html(opt) echappe les \ en &92; ou similaire
# 2. wrap_math() ne peut plus detecter \( \)
```

### Solution
Utiliser une fonction unifiee qui protege le LaTeX AVANT d'echapper :
```python
def escape_html_preserve_math(text: str) -> str:
    """Echappe HTML tout en preservant les formules LaTeX"""
    if not text:
        return ""

    result = str(text)
    math_blocks = []

    def protect_block(m):
        math_blocks.append(m.group(0))
        return f"__MATH_{len(math_blocks)-1}__"

    # 1. Proteger les formules LaTeX
    result = re.sub(r'\\\[.*?\\\]', protect_block, result, flags=re.DOTALL)
    result = re.sub(r'\\\(.*?\\\)', protect_block, result, flags=re.DOTALL)
    result = re.sub(r'\$\$.*?\$\$', protect_block, result, flags=re.DOTALL)
    result = re.sub(r'(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)', protect_block, result)

    # 2. Echapper HTML si necessaire
    if not any(tag in result for tag in ['<p>', '<div>', '<strong>']):
        result = html.escape(result)

    # 3. Restaurer les formules
    for i, block in enumerate(math_blocks):
        result = result.replace(f"__MATH_{i}__", block)

    return result
```

## Implementation Correcte

### Pour les questions
```python
"question": f"<p>{escape_html_preserve_math(q.get('text', ''))}</p>"
```

### Pour les options/reponses
```python
for opt in options:
    answers.append({
        "text": f"<div>{escape_html_preserve_math(opt)}</div>",
        "correct": is_correct
    })
```

### Pour les feedbacks
```python
"feedback": f"<p>{escape_html_preserve_math(feedback)}</p>"
```

## Test de Validation

Creer un H5P avec ces questions :
```python
questions = [
    {
        "type": "multichoice",
        "text": "Si \\(f(x) = x^2\\), que vaut \\(f(3)\\) ?",
        "options": ["\\(9\\)", "\\(6\\)", "\\(3\\)", "\\(12\\)"],
        "correct_index": 0,
        "feedback": "On calcule \\(f(3) = 3^2 = 9\\)"
    }
]
```

Verifier que le LaTeX s'affiche :
- [ ] Dans l'enonce de la question
- [ ] Dans TOUTES les options
- [ ] Dans le feedback

## Fichiers a Corriger

| Fichier | Statut | Action |
|---------|--------|--------|
| `h5p_generator.py` | A corriger | Remplacer `escape_html` |
| `h5p_advanced_generator.py` | A corriger | Unifier l'approche |
| `h5p_generator_v2.py` | OK | Reference |

## Notes MathJax

H5P utilise MathJax pour le rendu. Configurer dans Moodle :
1. Activer le filtre MathJax
2. Ou installer H5P Math Display library

Certains symboles speciaux :
- `:` peut etre interprete comme separateur -> utiliser `\colon`
- `|` pour valeur absolue -> utiliser `\lvert` et `\rvert`
