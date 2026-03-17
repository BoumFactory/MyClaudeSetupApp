import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Tutoriels - Claude Code",
  description:
    "Parcours de formation pour maîtriser Claude Desktop, Claude Code CLI et l'architecture agentique. Guides interactifs avec suivi de progression.",
}

export default function TutorialsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <>{children}</>
}
