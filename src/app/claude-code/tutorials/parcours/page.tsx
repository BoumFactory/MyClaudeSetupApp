import { redirect } from 'next/navigation'

/**
 * /claude-code/tutorials/parcours → redirige vers parcours-libre
 */
export default function ParcoursIndexPage() {
  redirect('/claude-code/tutorials/parcours-libre')
}
