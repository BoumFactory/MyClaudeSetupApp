"use client"

import { useState, useRef } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Code2,
  BookOpen,
  Download,
  Presentation,
  GraduationCap,
  ChevronDown,
  Menu,
  X,
  Sparkles,
  Package,
  Image,
  Terminal,
  BarChart3,
  Video,
  Shuffle,
  FileVideo2,
  FileText,
  History,
  Settings,
  AlignJustify
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useBackgroundAnimation } from "@/contexts/BackgroundAnimationContext"

/**
 * Navigation principale de l'application avec sous-menus
 */
export function MainNav() {
  const pathname = usePathname()
  const [openMenu, setOpenMenu] = useState<string | null>(null)
  const [openCategory, setOpenCategory] = useState<string | null>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [openMobileSubmenu, setOpenMobileSubmenu] = useState<string | null>(null)
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const { currentAnimation, cycleAnimation, animations } = useBackgroundAnimation()

  const currentAnimationInfo = animations.find(a => a.id === currentAnimation)

  const navItems = [
    {
      title: "Formations",
      href: "/formations",
      icon: FileText,
      featured: true, // Item mis en avant
      submenu: [
        {
          title: "Formation IA & LaTeX",
          href: "/formations/ia-latex",
          icon: Sparkles,
          description: "Document formatif sur les bases avec claude code"
        },
        {
          title: "Formation LaTeX",
          href: "/formations/latex",
          icon: BookOpen,
          description: "Document formatif sur LaTeX pour l'enseignement"
        },
        
      ]
    },
    {
      title: "Vidéos",
      href: "/claude-code/videos",
      icon: Video,
      featured: true, // Item mis en avant
      submenu: [
        {
          title: "Vidéos Claude Code",
          href: "/claude-code/videos",
          icon: FileVideo2,
          description: "Démonstration de mon utilisation de Claude Code"
        },
      ]
    },
    {
      title: "Tutoriels",
      href: "/claude-code/tutorials",
      icon: GraduationCap,
      submenu: [
        {
          title: "Installation VS Code & MikTeX",
          href: "/claude-code/tutorials/vscode-miktex",
          icon: Code2,
          description: "La fondation : éditeur et distribution LaTeX"
        },
        {
          title: "Installation de Node.js",
          href: "/claude-code/tutorials/nodejs-install",
          icon: Terminal,
          description: "Environnement JavaScript pour Claude Code"
        },
        {
          title: "Installation de Python x64",
          href: "/claude-code/tutorials/python-install",
          icon: Terminal,
          description: "Environnement Python pour les outils IA"
        },
        {
          title: "Installation du package bfcours",
          href: "/claude-code/tutorials/bfcours-setup",
          icon: Package,
          description: "Package personnalisé pour l'enseignement"
        },
        {
          title: "Installation de Claude Code",
          href: "/claude-code/tutorials/claude-code-install",
          icon: Sparkles,
          description: "L'outil IA principal pour automatiser"
        },
        {
          title: "Configuration de Claude Code",
          href: "/claude-code/tutorials/claude-code-config",
          icon: Settings,
          description: "Configurer avec mes outils personnalisés"
        },
        {
          title: "Configuration de l'API Google",
          href: "/claude-code/tutorials/google-api-setup",
          icon: Image,
          description: "Générez des images avec l'IA (optionnel)"
        },
      ]
    },
    {
      title: "Présentations",
      href: "/claude-code/presentations",
      icon: Presentation,
      isMultiLevel: true,
      submenu: [
        {
          title: "Architecture de ma config Claude Code",
          isCategory: true,
          icon: Code2,
          description: "Architecture et interface",
          presentations: [
            {
              title: "Architecture Claude Code",
              href: "/claude-code/presentations/architecture-claude-code-reveals",
              icon: Presentation,
              description: "Architecture de ma configuration"
            },
            {
              title: "Interface Claude Code",
              href: "/claude-code/presentations/claude-code-interface",
              icon: Presentation,
              description: "Guide de l'interface"
            },
            {
              title: "Commandes disponibles",
              href: "/claude-code/presentations/commandes-disponibles",
              icon: Presentation,
              description: "Catalogue des commandes"
            },
          ]
        },
        {
          title: "Agents et Skills",
          isCategory: true,
          icon: Sparkles,
          description: "Systèmes de création automatisés",
          presentations: [
            {
              title: "Tex Document Creator",
              href: "/claude-code/presentations/tex-document-creator-system",
              icon: Presentation,
              description: "Création de documents LaTeX"
            },
            {
              title: "Agent Make Images",
              href: "/claude-code/presentations/agent-make-images",
              icon: Presentation,
              description: "Génération d'images IA"
            },
            {
              title: "Skill Creator",
              href: "/claude-code/presentations/skill-creator-system",
              icon: Presentation,
              description: "Création de skills"
            },
            {
              title: "Beamer Presentation",
              href: "/claude-code/presentations/beamer-presentation-system",
              icon: Presentation,
              description: "Diaporamas Beamer LaTeX"
            },
            {
              title: "Reveals Presentation",
              href: "/claude-code/presentations/reveals-presentation-system",
              icon: Presentation,
              description: "Présentations web Reveal.js"
            },
            {
              title: "Educational App Builder",
              href: "/claude-code/presentations/educational-app-builder-system",
              icon: Presentation,
              description: "Applications éducatives Flask"
            },
            {
              title: "Programmes Officiels",
              href: "/claude-code/presentations/programmes-officiels-system",
              icon: Presentation,
              description: "Extraction programmes officiels"
            },
          ]
        },
        {
          title: "Skills expérimentaux",
          isCategory: true,
          icon: Package,
          description: "Skills disponibles dans Claude-Code-Setup",
          presentations: [
            {
              title: "Jupyter Notebook",
              href: "/claude-code/presentations/jupyter-notebook-skill",
              icon: Presentation,
              description: "Notebooks pédagogiques Python"
            },
            {
              title: "Interactive Animation",
              href: "/claude-code/presentations/interactive-animation-skill",
              icon: Presentation,
              description: "Animations mathématiques HTML/JS"
            },
            {
              title: "QCM Creator",
              href: "/claude-code/presentations/qcm-creator-skill",
              icon: Presentation,
              description: "QCM mathématiques rdmcq"
            },
            {
              title: "Infography Generator",
              href: "/claude-code/presentations/infography-generator-skill",
              icon: Presentation,
              description: "Infographies éducatives Gemini 3 Pro"
            },
            {
              title: "Blueprint Eval",
              href: "/claude-code/presentations/blueprint-eval-skill",
              icon: Presentation,
              description: "Fiches de révision interactives"
            },
          ]
        },
        {
          title: "Outils LaTeX",
          isCategory: true,
          icon: BookOpen,
          description: "Création et compilation LaTeX",
          presentations: [
            {
              title: "Package bfcours",
              href: "/claude-code/presentations/bfcours-latex-system",
              icon: Presentation,
              description: "Guide du package LaTeX"
            },
          ]
        },
      ]
    },
    {
      title: "Applications",
      href: "/claude-code/applications",
      icon: Settings,
      submenu: [
        {
          title: "Applications Éducatives",
          href: "/claude-code/applications/educatives",
          icon: GraduationCap,
          description: "Applications interactives pour les élèves"
        },
        {
          title: "Logiciels Enseignants",
          href: "/claude-code/applications/logiciels",
          icon: Package,
          description: "Outils de productivité pour enseignants"
        },
      ]
    },
    {
      title: "Téléchargements",
      href: "/claude-code/downloads",
      icon: Download,
      featured: true, // Item mis en avant
      submenu: [
        {
          title: "Tous les téléchargements",
          href: "/claude-code/downloads",
          icon: Download,
          description: "Configurations et ressources"
        },
      ]
    },
    {
      title: "Divers",
      href: "/about",
      icon: AlignJustify,
      submenu: [
        {
          title: "Qui suis-je ?",
          href: "/about",
          icon: BookOpen,
          description: "À propos de moi et de ce projet"
        },
        {
          title: "Changelog",
          href: "/changelog",
          icon: History,
          description: "Historique des modifications"
        },
      ]
    },
  ]

  // Logique simplifiée : une seule hitbox rectangulaire globale
  const clearCloseTimeout = () => {
    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current)
      closeTimeoutRef.current = null
    }
  }

  const handleMenuEnter = (title: string) => {
    clearCloseTimeout()
    setOpenMenu(title)
  }

  const handleCategoryEnter = (categoryTitle: string) => {
    clearCloseTimeout()
    setOpenCategory(categoryTitle)
  }

  const handleNavLeave = () => {
    // Délai court car on sort vraiment de la zone
    closeTimeoutRef.current = setTimeout(() => {
      setOpenMenu(null)
      setOpenCategory(null)
    }, 300)
  }

  // Fonction helper pour grouper les items par catégorie
  const groupItemsByCategory = (items: any[]) => {
    const grouped = new Map<string, any[]>()
    items.forEach(item => {
      const category = (item as any).category || 'Autre'
      if (!grouped.has(category)) {
        grouped.set(category, [])
      }
      grouped.get(category)!.push(item)
    })
    return grouped
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-cosmic-800/50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo et bouton animation */}
          <div className="flex items-center gap-2 sm:gap-3 flex-1 sm:flex-initial min-w-0">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl min-w-0">
              <div className="w-8 h-8 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <span className="hidden sm:inline-block glow-text truncate">
                IA & Enseignement
              </span>
            </Link>

            {/* Bouton pour changer l'animation de fond */}
            <button
              onClick={cycleAnimation}
              className="group relative flex items-center gap-2 px-2 sm:px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 text-muted-foreground hover:text-foreground hover:bg-cosmic-900/30 border border-transparent hover:border-cosmic-700/50 flex-shrink-0"
              title={""}
            >
              <Shuffle className="w-4 h-4 transition-transform group-hover:rotate-180 duration-500" />
              <span className="hidden lg:inline-block text-xs whitespace-nowrap">Animation</span>

              {/* Tooltip avec le nom de l'animation */}
              {currentAnimationInfo && (
                <div className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-3 py-2 bg-background/95 backdrop-blur-sm rounded-lg shadow-xl border border-cosmic-700/50 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
                  <div className="text-xs font-medium text-cosmic-300">Animation : {currentAnimationInfo.name}</div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">{currentAnimationInfo.secret}</div>
                </div>
              )}
            </button>
          </div>

          {/* Navigation Desktop avec zone globale */}
          <div
            className="hidden md:block relative"
            onMouseLeave={handleNavLeave}
          >
            <nav className="flex items-center gap-1">
            {navItems.map((item, itemIndex) => {
              const Icon = item.icon
              const isActive = pathname === item.href ||
                               (item.href !== "/" && pathname.startsWith(item.href))
              const hasSubmenu = item.submenu && item.submenu.length > 0
              const isFeatured = (item as any).featured

              // Déterminer si on est dans les derniers éléments (pour positionner à droite)
              const isLastItems = itemIndex >= navItems.length - 2
              const isFirstItems = itemIndex <= 2

              return (
                <div
                  key={item.href}
                  className="relative group"
                  onMouseEnter={() => hasSubmenu && handleMenuEnter(item.title)}
                >
                  <Link
                    href={item.href}
                    className={cn(
                      "inline-flex items-center gap-1 p-2 rounded-md text-sm font-medium transition-all duration-200 relative",
                      isActive
                        ? "bg-cosmic-900/50 text-cosmic-300 border border-cosmic-700"
                        : isFeatured
                        ? "text-foreground border border-cosmic-600/40 hover:border-cosmic-500/60 hover:bg-cosmic-900/30 hover:shadow-[0_0_12px_rgba(139,92,246,0.15)]"
                        : "text-muted-foreground hover:text-foreground hover:bg-cosmic-900/30"
                    )}
                    title={item.title}
                  >
                    <Icon className={cn("w-5 h-5", isFeatured && "text-cosmic-400")} />
                    {hasSubmenu && (
                      <ChevronDown
                        className={cn(
                          "w-3 h-3 transition-transform duration-200",
                          openMenu === item.title && "rotate-180"
                        )}
                      />
                    )}

                    {/* Tooltip au survol */}
                    {!hasSubmenu && (
                      <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 bg-background/95 backdrop-blur-sm rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 border border-cosmic-700/50">
                        {item.title}
                      </span>
                    )}
                  </Link>

                  {/* Submenu Dropdown */}
                  {hasSubmenu && openMenu === item.title && (
                    <div
                      className={cn(
                        "absolute top-full pt-2",
                        isLastItems ? "right-0" : "left-0"
                      )}
                    >
                      <div className={cn(
                        "w-72 bg-background/95 backdrop-blur-sm rounded-lg shadow-xl border border-cosmic-700/50 p-2 animate-in fade-in slide-in-from-top-2 duration-150",
                        (item as any).isMultiLevel ? "" : "max-h-[80vh] overflow-y-auto"
                      )}>
                      {/* Header du dropdown avec le titre de la catégorie */}
                      <div className="px-3 py-2 mb-2 border-b border-cosmic-800/50">
                        <div className="flex items-center gap-2">
                          <Icon className={cn("w-5 h-5", isFeatured && "text-cosmic-400")} />
                          <span className="font-semibold text-foreground">{item.title}</span>
                        </div>
                      </div>

                      {(item as any).isMultiLevel ? (
                        // Menu à 2 niveaux pour les présentations
                        <>
                          {item.submenu!.map((category: any, categoryIdx: number) => {
                            const CategoryIcon = category.icon
                            return (
                              <div
                                key={category.title}
                                className="relative"
                                onMouseEnter={() => handleCategoryEnter(category.title)}
                              >
                                <div
                                  className={cn(
                                    "flex items-start gap-3 px-3 py-2.5 rounded-md transition-colors cursor-pointer",
                                    openCategory === category.title
                                      ? "bg-cosmic-900/70 text-cosmic-300"
                                      : "hover:bg-cosmic-900/50"
                                  )}
                                >
                                  <CategoryIcon className="w-5 h-5 mt-0.5 flex-shrink-0 text-cosmic-400" />
                                  <div className="flex-1">
                                    <div className="font-medium text-sm">{category.title}</div>
                                    <div className="text-xs text-muted-foreground">
                                      {category.description}
                                    </div>
                                  </div>
                                  <ChevronDown className="w-4 h-4 mt-1 rotate-90 flex-shrink-0" />
                                </div>

                                {/* Sous-menu latéral pour les présentations de la catégorie */}
                                {openCategory === category.title && category.presentations && (
                                  <div
                                    className="absolute right-full top-0 pr-2"
                                  >
                                    <div className="w-72 bg-background/95 backdrop-blur-sm rounded-lg shadow-xl border border-cosmic-700/50 p-2 animate-in fade-in slide-in-from-right-2 duration-150 max-h-[80vh] overflow-y-auto z-[100]">

                                    {category.presentations.map((presentation: any) => {
                                      const PresIcon = presentation.icon
                                      const isPresActive = pathname === presentation.href

                                      return (
                                        <Link
                                          key={presentation.href}
                                          href={presentation.href}
                                          className={cn(
                                            "flex items-start gap-3 px-3 py-2.5 rounded-md transition-colors",
                                            isPresActive
                                              ? "bg-cosmic-900/70 text-cosmic-300"
                                              : "hover:bg-cosmic-900/50"
                                          )}
                                        >
                                          <PresIcon className="w-5 h-5 mt-0.5 flex-shrink-0 text-cosmic-400" />
                                          <div>
                                            <div className="font-medium text-sm">{presentation.title}</div>
                                            <div className="text-xs text-muted-foreground">
                                              {presentation.description}
                                            </div>
                                          </div>
                                        </Link>
                                      )
                                    })}
                                    </div>
                                  </div>
                                )}
                              </div>
                            )
                          })}
                        </>
                      ) : (
                        // Menu standard avec groupement par catégories
                        <>
                          {(() => {
                            const groupedItems = groupItemsByCategory(item.submenu!)
                            const categories = Array.from(groupedItems.keys())

                            return categories.map((category, categoryIndex) => (
                              <div key={category}>
                                {categories.length > 1 && (
                                  <div className="px-3 py-2 text-xs font-semibold text-cosmic-400 uppercase tracking-wide">
                                    {category}
                                  </div>
                                )}
                                {groupedItems.get(category)!.map((subItem) => {
                                  const SubIcon = subItem.icon
                                  const isSubActive = pathname === subItem.href

                                  return (
                                    <Link
                                      key={subItem.href}
                                      href={subItem.href}
                                      className={cn(
                                        "flex items-start gap-3 px-3 py-2.5 rounded-md transition-colors",
                                        isSubActive
                                          ? "bg-cosmic-900/70 text-cosmic-300"
                                          : "hover:bg-cosmic-900/50"
                                      )}
                                    >
                                      <SubIcon className="w-5 h-5 mt-0.5 flex-shrink-0 text-cosmic-400" />
                                      <div>
                                        <div className="font-medium text-sm">{subItem.title}</div>
                                        <div className="text-xs text-muted-foreground">
                                          {subItem.description}
                                        </div>
                                      </div>
                                    </Link>
                                  )
                                })}
                                {categoryIndex < categories.length - 1 && (
                                  <div className="my-2 border-t border-cosmic-800/50" />
                                )}
                              </div>
                            ))
                          })()}
                        </>
                      )}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
            </nav>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => {
              setMobileMenuOpen(!mobileMenuOpen)
              if (mobileMenuOpen) {
                setOpenMobileSubmenu(null)
              }
            }}
            className="md:hidden p-2 text-muted-foreground hover:text-foreground"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-cosmic-800/50 animate-in slide-in-from-top duration-200 max-h-[calc(100vh-5rem)] overflow-y-auto">
            <nav className="flex flex-col gap-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = pathname === item.href ||
                                 (item.href !== "/" && pathname.startsWith(item.href))
                const hasSubmenu = item.submenu && item.submenu.length > 0
                const isFeatured = (item as any).featured
                const isMultiLevel = (item as any).isMultiLevel

                return (
                  <div key={item.href}>
                    {hasSubmenu ? (
                      <button
                        onClick={() => setOpenMobileSubmenu(openMobileSubmenu === item.title ? null : item.title)}
                        className={cn(
                          "w-full flex items-center justify-between gap-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200",
                          isActive
                            ? "bg-cosmic-900/50 text-cosmic-300 border border-cosmic-700"
                            : isFeatured
                            ? "text-foreground border border-cosmic-600/40 hover:border-cosmic-500/60 hover:bg-cosmic-900/30"
                            : "text-muted-foreground hover:text-foreground hover:bg-cosmic-900/30"
                        )}
                      >
                        <div className="flex items-center gap-2">
                          <Icon className={cn("w-4 h-4", isFeatured && "text-cosmic-400")} />
                          <span>{item.title}</span>
                        </div>
                        <ChevronDown
                          className={cn(
                            "w-4 h-4 transition-transform duration-200",
                            openMobileSubmenu === item.title && "rotate-180"
                          )}
                        />
                      </button>
                    ) : (
                      <Link
                        href={item.href}
                        onClick={() => setMobileMenuOpen(false)}
                        className={cn(
                          "flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200",
                          isActive
                            ? "bg-cosmic-900/50 text-cosmic-300 border border-cosmic-700"
                            : isFeatured
                            ? "text-foreground border border-cosmic-600/40 hover:border-cosmic-500/60 hover:bg-cosmic-900/30"
                            : "text-muted-foreground hover:text-foreground hover:bg-cosmic-900/30"
                        )}
                      >
                        <Icon className={cn("w-4 h-4", isFeatured && "text-cosmic-400")} />
                        <span>{item.title}</span>
                      </Link>
                    )}

                    {/* Mobile Submenu */}
                    {hasSubmenu && openMobileSubmenu === item.title && (
                      <div className="ml-4 mt-1 space-y-1 animate-in slide-in-from-top-2 duration-200">
                        {isMultiLevel ? (
                          // Menu à 2 niveaux pour les présentations
                          item.submenu!.map((category: any) => {
                            const CategoryIcon = category.icon
                            return (
                              <div key={category.title} className="mb-3">
                                {/* En-tête de catégorie */}
                                <div className="flex items-start gap-2 px-3 py-2 text-xs font-semibold text-cosmic-400 uppercase tracking-wide">
                                  <CategoryIcon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                  <div>
                                    <div>{category.title}</div>
                                    {category.description && (
                                      <div className="text-[10px] text-muted-foreground font-normal normal-case mt-0.5">
                                        {category.description}
                                      </div>
                                    )}
                                  </div>
                                </div>

                                {/* Présentations de la catégorie */}
                                <div className="ml-3 space-y-0.5">
                                  {category.presentations?.map((presentation: any) => {
                                    const PresIcon = presentation.icon
                                    const isPresActive = pathname === presentation.href

                                    return (
                                      <Link
                                        key={presentation.href}
                                        href={presentation.href}
                                        onClick={() => setMobileMenuOpen(false)}
                                        className={cn(
                                          "flex items-start gap-2 px-3 py-2 rounded-md text-sm transition-colors",
                                          isPresActive
                                            ? "bg-cosmic-900/70 text-cosmic-300"
                                            : "text-muted-foreground hover:bg-cosmic-900/50"
                                        )}
                                      >
                                        <PresIcon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                        <div className="flex-1 min-w-0">
                                          <div className="font-medium text-sm truncate">{presentation.title}</div>
                                          {presentation.description && (
                                            <div className="text-xs text-muted-foreground line-clamp-2">
                                              {presentation.description}
                                            </div>
                                          )}
                                        </div>
                                      </Link>
                                    )
                                  })}
                                </div>
                              </div>
                            )
                          })
                        ) : (
                          // Menu standard avec groupement par catégories
                          (() => {
                            const groupedItems = groupItemsByCategory(item.submenu!)
                            const categories = Array.from(groupedItems.keys())

                            return categories.map((category, categoryIndex) => (
                              <div key={category}>
                                {categories.length > 1 && (
                                  <div className="px-3 py-1.5 text-xs font-semibold text-cosmic-400 uppercase tracking-wide">
                                    {category}
                                  </div>
                                )}
                                {groupedItems.get(category)!.map((subItem) => {
                                  const SubIcon = subItem.icon
                                  const isSubActive = pathname === subItem.href

                                  return (
                                    <Link
                                      key={subItem.href}
                                      href={subItem.href}
                                      onClick={() => setMobileMenuOpen(false)}
                                      className={cn(
                                        "flex items-start gap-2 px-3 py-2 rounded-md text-sm transition-colors",
                                        isSubActive
                                          ? "bg-cosmic-900/70 text-cosmic-300"
                                          : "text-muted-foreground hover:bg-cosmic-900/50"
                                      )}
                                    >
                                      <SubIcon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                      <div className="flex-1 min-w-0">
                                        <div className="font-medium text-sm truncate">{subItem.title}</div>
                                        {subItem.description && (
                                          <div className="text-xs text-muted-foreground line-clamp-2">
                                            {subItem.description}
                                          </div>
                                        )}
                                      </div>
                                    </Link>
                                  )
                                })}
                                {categoryIndex < categories.length - 1 && (
                                  <div className="my-1 border-t border-cosmic-800/50" />
                                )}
                              </div>
                            ))
                          })()
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
