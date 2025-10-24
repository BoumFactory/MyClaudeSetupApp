"use client"

import { useState } from "react"
import {
  Folder,
  FolderOpen,
  File,
  ChevronRight,
  ChevronDown,
  CheckSquare,
  Square,
  MinusSquare,
  Ban,
} from "lucide-react"
import { DownloadableItem } from "@/types"
import { cn } from "@/lib/utils"
import { formatSize } from "@/lib/file-scanner"

interface FileTreeItemProps {
  item: DownloadableItem
  onToggle: (path: string) => void
  level: number
}

/**
 * Item de l'arbre de fichiers
 */
export function FileTreeItem({ item, onToggle, level }: FileTreeItemProps) {
  const [isOpen, setIsOpen] = useState(false)

  const isDirectory = item.type === "directory"
  const hasChildren = isDirectory && item.children && item.children.length > 0

  // Déterminer l'état de sélection (complet, partiel, ou aucun)
  const getSelectionState = (): "all" | "some" | "none" => {
    if (item.isIgnored) return "none"
    if (!isDirectory) return item.isSelected ? "all" : "none"

    if (!item.children || item.children.length === 0) {
      return item.isSelected ? "all" : "none"
    }

    const selectedChildren = item.children.filter((c) => c.isSelected && !c.isIgnored)
    if (selectedChildren.length === 0) return "none"
    if (selectedChildren.length === item.children.filter(c => !c.isIgnored).length) return "all"
    return "some"
  }

  const selectionState = getSelectionState()

  const handleToggle = () => {
    if (!item.isIgnored) {
      onToggle(item.path)
    }
  }

  const handleExpand = () => {
    if (hasChildren) {
      setIsOpen(!isOpen)
    }
  }

  return (
    <div>
      {/* Item principal */}
      <div
        className={cn(
          "flex items-center gap-2 py-1.5 px-2 rounded-md hover:bg-cosmic-900/30 transition-colors group",
          item.isIgnored && "opacity-50"
        )}
        style={{ paddingLeft: `${level * 1.5 + 0.5}rem` }}
      >
        {/* Chevron d'expansion */}
        {hasChildren ? (
          <button
            onClick={handleExpand}
            className="p-0.5 hover:bg-cosmic-800/50 rounded"
          >
            {isOpen ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </button>
        ) : (
          <div className="w-5" />
        )}

        {/* Checkbox de sélection */}
        <button
          onClick={handleToggle}
          disabled={item.isIgnored}
          className={cn(
            "p-0.5 hover:bg-cosmic-800/50 rounded",
            item.isIgnored && "cursor-not-allowed"
          )}
        >
          {item.isIgnored ? (
            <Ban className="w-4 h-4 text-destructive" />
          ) : selectionState === "all" ? (
            <CheckSquare className="w-4 h-4 text-cosmic-400" />
          ) : selectionState === "some" ? (
            <MinusSquare className="w-4 h-4 text-cosmic-400" />
          ) : (
            <Square className="w-4 h-4" />
          )}
        </button>

        {/* Icône de fichier/dossier */}
        {isDirectory ? (
          isOpen ? (
            <FolderOpen className="w-4 h-4 text-cosmic-400" />
          ) : (
            <Folder className="w-4 h-4 text-cosmic-400" />
          )
        ) : (
          <File className="w-4 h-4 text-muted-foreground" />
        )}

        {/* Nom */}
        <button
          onClick={isDirectory ? handleExpand : handleToggle}
          className="flex-1 text-left text-sm truncate"
        >
          {item.name}
        </button>

        {/* Taille (pour les fichiers) */}
        {!isDirectory && item.size !== undefined && (
          <span className="text-xs text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
            {formatSize(item.size)}
          </span>
        )}
      </div>

      {/* Enfants (si dossier ouvert) */}
      {isDirectory && isOpen && hasChildren && (
        <div>
          {item.children!.map((child) => (
            <FileTreeItem
              key={child.path}
              item={child}
              onToggle={onToggle}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
}
