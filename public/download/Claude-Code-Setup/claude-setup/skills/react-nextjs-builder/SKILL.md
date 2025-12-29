---
name: react-nextjs-builder
description: Skill complet pour créer des composants React/Next.js avec App Router, Server Actions et shadcn/ui. Expertise en architecture fullstack moderne, composants réutilisables et standardisation de présentation.
---

# React Next.js Builder - Expert en Développement Next.js 13+

## Vue d'ensemble

Ce skill fournit une expertise complète pour le développement d'applications Next.js modernes utilisant l'App Router, les Server Actions et les composants shadcn/ui. Il couvre la création de composants, pages, layouts et l'architecture fullstack.

## Objectifs

1. Créer des composants React réutilisables et typés (TypeScript)
2. Développer des pages Next.js avec App Router
3. Implémenter des Server Actions pour les mutations de données
4. Intégrer des composants shadcn/ui de manière cohérente
5. Maintenir une standardisation de présentation professionnelle
6. Optimiser les performances (RSC, streaming, suspense)

## Architecture App Router Next.js 13+

### Structure de Projet Standard

```
app/
├── (routes)/                  # Groupes de routes
│   ├── (marketing)/          # Routes publiques
│   │   ├── page.tsx         # Page d'accueil
│   │   └── layout.tsx       # Layout marketing
│   ├── (dashboard)/         # Routes authentifiées
│   │   ├── dashboard/
│   │   │   ├── page.tsx    # Page dashboard
│   │   │   └── loading.tsx # État de chargement
│   │   └── layout.tsx      # Layout dashboard
│   └── api/                 # Route handlers (si nécessaire)
│       └── [...]/
│           └── route.ts
├── layout.tsx               # Layout racine
├── loading.tsx             # Loading UI global
├── error.tsx               # Error boundary
├── not-found.tsx           # Page 404
└── globals.css             # Styles globaux

components/
├── ui/                     # Composants shadcn/ui
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   └── ...
├── forms/                  # Composants de formulaires
│   ├── auth-form.tsx
│   └── ...
├── layouts/               # Composants de layout
│   ├── header.tsx
│   ├── footer.tsx
│   └── sidebar.tsx
└── shared/                # Composants partagés
    ├── loader.tsx
    └── ...

lib/
├── actions/               # Server Actions
│   ├── auth.ts
│   ├── users.ts
│   └── ...
├── db/                    # Configuration BDD
│   └── client.ts
├── validations/           # Schémas Zod
│   └── auth.ts
└── utils.ts              # Utilitaires

types/
└── index.ts              # Définitions TypeScript
```

## Conventions et Bonnes Pratiques

### 1. Nomenclature des Fichiers

**Pages et Routes** :
- `page.tsx` : Page de route
- `layout.tsx` : Layout partagé
- `loading.tsx` : UI de chargement
- `error.tsx` : Gestion des erreurs
- `not-found.tsx` : Page 404
- `route.ts` : Route handler API

**Composants** :
- `kebab-case` pour les dossiers : `auth-form/`
- `PascalCase` pour les fichiers : `AuthForm.tsx`
- Noms descriptifs et explicites

**Actions** :
- `kebab-case` : `auth-actions.ts`
- Préfixe `use` pour les hooks : `useAuth.ts`

### 2. Organisation des Composants

#### Composants Client vs Server

**Server Component (par défaut)** :
```tsx
// components/posts/PostList.tsx
import { getPosts } from '@/lib/actions/posts'

export default async function PostList() {
  const posts = await getPosts()

  return (
    <div className="grid gap-4">
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}
```

**Client Component (interactif)** :
```tsx
'use client'

// components/forms/CommentForm.tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { createComment } from '@/lib/actions/comments'

export function CommentForm({ postId }: { postId: string }) {
  const [isLoading, setIsLoading] = useState(false)

  async function handleSubmit(formData: FormData) {
    setIsLoading(true)
    try {
      await createComment(formData)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form action={handleSubmit}>
      <input type="hidden" name="postId" value={postId} />
      <textarea name="content" />
      <Button type="submit" disabled={isLoading}>
        Publier
      </Button>
    </form>
  )
}
```

### 3. Server Actions - Patterns Essentiels

#### Structure d'une Server Action

```tsx
'use server'

// lib/actions/users.ts
import { z } from 'zod'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

// Schéma de validation
const userSchema = z.object({
  name: z.string().min(2, 'Le nom doit contenir au moins 2 caractères'),
  email: z.string().email('Email invalide'),
  age: z.number().min(18, 'Vous devez avoir au moins 18 ans')
})

// Type pour le résultat
type ActionResult = {
  success: boolean
  message?: string
  errors?: Record<string, string[]>
  data?: any
}

/**
 * Créer un nouvel utilisateur
 */
export async function createUser(
  prevState: ActionResult | null,
  formData: FormData
): Promise<ActionResult> {
  try {
    // 1. Extraire et valider les données
    const rawData = {
      name: formData.get('name'),
      email: formData.get('email'),
      age: Number(formData.get('age'))
    }

    const validatedData = userSchema.parse(rawData)

    // 2. Effectuer l'opération
    const user = await db.user.create({
      data: validatedData
    })

    // 3. Revalider le cache si nécessaire
    revalidatePath('/users')

    // 4. Retourner le résultat
    return {
      success: true,
      message: 'Utilisateur créé avec succès',
      data: user
    }
  } catch (error) {
    // Gestion des erreurs de validation
    if (error instanceof z.ZodError) {
      return {
        success: false,
        errors: error.flatten().fieldErrors
      }
    }

    // Autres erreurs
    return {
      success: false,
      message: 'Une erreur est survenue'
    }
  }
}

/**
 * Supprimer un utilisateur et rediriger
 */
export async function deleteUser(userId: string) {
  try {
    await db.user.delete({
      where: { id: userId }
    })

    revalidatePath('/users')
    redirect('/users')
  } catch (error) {
    throw new Error('Impossible de supprimer l\'utilisateur')
  }
}
```

#### Utilisation avec useFormState (React 19)

```tsx
'use client'

// components/forms/UserForm.tsx
import { useFormState } from 'react-dom'
import { useFormStatus } from 'react-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { createUser } from '@/lib/actions/users'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <Button type="submit" disabled={pending}>
      {pending ? 'Création...' : 'Créer'}
    </Button>
  )
}

export function UserForm() {
  const [state, formAction] = useFormState(createUser, null)

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <Label htmlFor="name">Nom</Label>
        <Input
          id="name"
          name="name"
          required
        />
        {state?.errors?.name && (
          <p className="text-sm text-destructive">{state.errors.name[0]}</p>
        )}
      </div>

      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          required
        />
        {state?.errors?.email && (
          <p className="text-sm text-destructive">{state.errors.email[0]}</p>
        )}
      </div>

      <div>
        <Label htmlFor="age">Âge</Label>
        <Input
          id="age"
          name="age"
          type="number"
          required
        />
        {state?.errors?.age && (
          <p className="text-sm text-destructive">{state.errors.age[0]}</p>
        )}
      </div>

      {state?.message && (
        <p className={state.success ? 'text-green-600' : 'text-destructive'}>
          {state.message}
        </p>
      )}

      <SubmitButton />
    </form>
  )
}
```

### 4. Composants shadcn/ui - Standards d'Utilisation

#### Installation de shadcn/ui

```bash
# Initialiser shadcn/ui
pnpm dlx shadcn-ui@latest init

# Ajouter des composants
pnpm dlx shadcn-ui@latest add button
pnpm dlx shadcn-ui@latest add card
pnpm dlx shadcn-ui@latest add input
pnpm dlx shadcn-ui@latest add form
```

#### Configuration components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

#### Patterns de Composition

**Card Component avec shadcn/ui** :

```tsx
// components/posts/PostCard.tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import type { Post } from '@/types'

interface PostCardProps {
  post: Post
}

export function PostCard({ post }: PostCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-2xl">{post.title}</CardTitle>
          <Badge variant={post.published ? 'default' : 'secondary'}>
            {post.published ? 'Publié' : 'Brouillon'}
          </Badge>
        </div>
        <CardDescription>{post.excerpt}</CardDescription>
      </CardHeader>

      <CardContent>
        <p className="text-muted-foreground line-clamp-3">
          {post.content}
        </p>
      </CardContent>

      <CardFooter className="flex justify-between">
        <p className="text-sm text-muted-foreground">
          {new Date(post.createdAt).toLocaleDateString('fr-FR')}
        </p>
        <Button variant="outline" size="sm">
          Lire plus
        </Button>
      </CardFooter>
    </Card>
  )
}
```

**Form avec shadcn/ui et react-hook-form** :

```tsx
'use client'

// components/forms/PostForm.tsx
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'

const formSchema = z.object({
  title: z.string().min(5, 'Le titre doit contenir au moins 5 caractères'),
  content: z.string().min(20, 'Le contenu doit contenir au moins 20 caractères'),
  published: z.boolean().default(false)
})

type FormValues = z.infer<typeof formSchema>

interface PostFormProps {
  defaultValues?: Partial<FormValues>
  onSubmit: (values: FormValues) => Promise<void>
}

export function PostForm({ defaultValues, onSubmit }: PostFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: '',
      content: '',
      published: false,
      ...defaultValues
    }
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Titre</FormLabel>
              <FormControl>
                <Input placeholder="Titre de l'article" {...field} />
              </FormControl>
              <FormDescription>
                Le titre principal de votre article
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="content"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Contenu</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Écrivez votre article ici..."
                  className="min-h-[200px]"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="published"
          render={({ field }) => (
            <FormItem className="flex items-center justify-between rounded-lg border p-4">
              <div className="space-y-0.5">
                <FormLabel className="text-base">Publier</FormLabel>
                <FormDescription>
                  Rendre cet article visible publiquement
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={form.formState.isSubmitting}
          className="w-full"
        >
          {form.formState.isSubmitting ? 'Enregistrement...' : 'Enregistrer'}
        </Button>
      </form>
    </Form>
  )
}
```

### 5. Layouts et Pages App Router

#### Layout Racine (app/layout.tsx)

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: {
    default: 'Mon Application',
    template: '%s | Mon Application'
  },
  description: 'Description de mon application',
  icons: {
    icon: '/favicon.ico'
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className={cn(
        'min-h-screen bg-background font-sans antialiased',
        inter.className
      )}>
        {children}
      </body>
    </html>
  )
}
```

#### Layout avec Navigation

```tsx
// app/(dashboard)/layout.tsx
import { Header } from '@/components/layouts/Header'
import { Sidebar } from '@/components/layouts/Sidebar'
import { getUser } from '@/lib/actions/auth'
import { redirect } from 'next/navigation'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const user = await getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar user={user} />
      <div className="flex-1 flex flex-col">
        <Header user={user} />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

#### Page avec Loading et Error States

```tsx
// app/(dashboard)/posts/page.tsx
import { Suspense } from 'react'
import { PostsList } from '@/components/posts/PostsList'
import { PostsLoading } from '@/components/posts/PostsLoading'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export const metadata = {
  title: 'Articles'
}

export default function PostsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Articles</h1>
        <Button asChild>
          <Link href="/posts/new">Nouvel article</Link>
        </Button>
      </div>

      <Suspense fallback={<PostsLoading />}>
        <PostsList />
      </Suspense>
    </div>
  )
}
```

```tsx
// app/(dashboard)/posts/loading.tsx
export default function Loading() {
  return (
    <div className="space-y-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="h-32 bg-muted rounded-lg" />
        </div>
      ))}
    </div>
  )
}
```

```tsx
// app/(dashboard)/posts/error.tsx
'use client'

import { Button } from '@/components/ui/button'
import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
      <h2 className="text-2xl font-bold">Une erreur est survenue</h2>
      <p className="text-muted-foreground">
        Impossible de charger les articles
      </p>
      <Button onClick={reset}>Réessayer</Button>
    </div>
  )
}
```

### 6. Patterns de Données et Caching

#### Data Fetching avec React Server Components

```tsx
// lib/data/posts.ts
import 'server-only'
import { cache } from 'react'
import { db } from '@/lib/db/client'

// Cache automatique avec React cache()
export const getPosts = cache(async () => {
  const posts = await db.post.findMany({
    orderBy: { createdAt: 'desc' },
    include: {
      author: {
        select: {
          name: true,
          image: true
        }
      }
    }
  })

  return posts
})

export const getPost = cache(async (id: string) => {
  const post = await db.post.findUnique({
    where: { id },
    include: {
      author: true,
      comments: {
        include: {
          author: true
        }
      }
    }
  })

  return post
})
```

#### Revalidation Stratégies

```tsx
// app/posts/[id]/page.tsx

// Revalidation toutes les heures
export const revalidate = 3600

// Ou ISR avec fetch
async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: {
      revalidate: 3600,
      tags: ['posts']
    }
  })
  return res.json()
}

// Revalidation à la demande dans une Server Action
'use server'
import { revalidateTag, revalidatePath } from 'next/cache'

export async function updatePost(id: string, data: any) {
  await db.post.update({ where: { id }, data })

  // Revalider par tag
  revalidateTag('posts')

  // Ou par path
  revalidatePath('/posts')
  revalidatePath(`/posts/${id}`)
}
```

### 7. Standardisation de Présentation

#### Thème et Design System

**Configuration Tailwind (tailwind.config.ts)** :

```typescript
import type { Config } from 'tailwindcss'

const config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
} satisfies Config

export default config
```

**Variables CSS (app/globals.css)** :

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

#### Composants de Layout Standards

**Container** :
```tsx
// components/layouts/Container.tsx
import { cn } from '@/lib/utils'

interface ContainerProps {
  children: React.ReactNode
  className?: string
}

export function Container({ children, className }: ContainerProps) {
  return (
    <div className={cn('container mx-auto px-4 sm:px-6 lg:px-8', className)}>
      {children}
    </div>
  )
}
```

**Section** :
```tsx
// components/layouts/Section.tsx
import { cn } from '@/lib/utils'

interface SectionProps {
  children: React.ReactNode
  className?: string
  title?: string
  description?: string
}

export function Section({ children, className, title, description }: SectionProps) {
  return (
    <section className={cn('py-12', className)}>
      {(title || description) && (
        <div className="mb-8">
          {title && (
            <h2 className="text-3xl font-bold tracking-tight">{title}</h2>
          )}
          {description && (
            <p className="mt-2 text-lg text-muted-foreground">{description}</p>
          )}
        </div>
      )}
      {children}
    </section>
  )
}
```

### 8. TypeScript - Types et Interfaces

#### Types de Base

```typescript
// types/index.ts

// Utilisateur
export interface User {
  id: string
  name: string
  email: string
  image?: string
  role: 'admin' | 'user'
  createdAt: Date
  updatedAt: Date
}

// Post
export interface Post {
  id: string
  title: string
  content: string
  excerpt: string
  published: boolean
  authorId: string
  author?: User
  createdAt: Date
  updatedAt: Date
}

// Types utilitaires
export type ApiResponse<T> = {
  success: boolean
  data?: T
  error?: string
}

export type PaginatedResponse<T> = {
  items: T[]
  total: number
  page: number
  pageSize: number
  hasMore: boolean
}

// Props génériques
export interface PageProps<T = {}> {
  params: T
  searchParams: { [key: string]: string | string[] | undefined }
}
```

### 9. Optimisations Performance

#### Images

```tsx
import Image from 'next/image'

export function OptimizedImage({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      className="rounded-lg"
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
      priority // Pour les images above the fold
    />
  )
}
```

#### Dynamic Imports

```tsx
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(
  () => import('@/components/HeavyComponent'),
  {
    loading: () => <p>Chargement...</p>,
    ssr: false // Si le composant ne doit pas être rendu côté serveur
  }
)
```

#### Streaming avec Suspense

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <Header />

      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>

      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>
    </div>
  )
}
```

## Checklist de Qualité

Avant de livrer un composant ou une page :

- [ ] TypeScript : Tous les types sont définis
- [ ] Accessibilité : Labels, aria-attributes
- [ ] Responsive : Mobile, tablet, desktop
- [ ] Loading states : Suspense, loading.tsx
- [ ] Error handling : error.tsx, try/catch
- [ ] Validation : Zod schemas pour les formulaires
- [ ] Performance : Images optimisées, dynamic imports
- [ ] SEO : Metadata, semantic HTML
- [ ] shadcn/ui : Composants utilisés correctement
- [ ] Server Actions : Validés, avec revalidation
- [ ] Commentaires : Code documenté en français

## Ressources et Références

### Documentation Officielle
- [Next.js App Router](https://nextjs.org/docs/app)
- [React Server Components](https://react.dev/reference/react/use-server)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)

### Outils Recommandés
- **TypeScript** : Typage statique
- **Zod** : Validation de schémas
- **react-hook-form** : Gestion de formulaires
- **Prisma** : ORM pour la BDD
- **NextAuth.js** : Authentification

## Conclusion

Ce skill fournit tous les patterns, conventions et bonnes pratiques pour développer des applications Next.js modernes et performantes. L'agent qui utilise ce skill doit :

1. Respecter l'architecture App Router
2. Utiliser les Server Actions pour les mutations
3. Intégrer shadcn/ui de manière cohérente
4. Maintenir une standardisation de présentation
5. Optimiser les performances (RSC, streaming, caching)
6. Écrire du code TypeScript typé et documenté

L'objectif est de livrer du code de qualité production, maintenable et performant.
