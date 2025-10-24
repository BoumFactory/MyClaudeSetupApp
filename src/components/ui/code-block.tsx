"use client"

import { useState } from "react"
import { Check, Copy } from "lucide-react"
import { Button } from "@/components/ui/button"

interface CodeBlockProps {
  code: string
  language?: string
  filename?: string
}

export function CodeBlock({ code, language = "json", filename }: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Erreur lors de la copie:", err)
    }
  }

  return (
    <div className="rounded-lg overflow-hidden border border-border">
      {filename && (
        <div className="bg-muted/50 px-4 py-2 flex items-center justify-between">
          <span className="text-sm font-medium">{filename}</span>
          <Button
            variant="ghost"
            size="sm"
            onClick={copyToClipboard}
            className={`h-8 gap-2 transition-all ${copied ? "text-green-500" : ""}`}
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                <span className="text-xs font-semibold">Copié !</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span className="text-xs">Copier</span>
              </>
            )}
          </Button>
        </div>
      )}
      <div className="relative">
        {!filename && (
          <Button
            variant="ghost"
            size="sm"
            onClick={copyToClipboard}
            className={`absolute top-2 right-2 h-8 gap-2 z-10 transition-all ${copied ? "text-green-500" : ""}`}
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                <span className="text-xs font-semibold">Copié !</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span className="text-xs">Copier</span>
              </>
            )}
          </Button>
        )}
        <pre className="p-4 overflow-x-auto text-sm bg-slate-950/50">
          <code className="text-slate-200">{code}</code>
        </pre>
      </div>
    </div>
  )
}
