# Patterns Avancés React/Next.js

## 1. Parallel Routes

Afficher plusieurs pages en parallèle dans le même layout.

```
app/
├── @analytics/
│   └── page.tsx
├── @team/
│   └── page.tsx
├── layout.tsx
└── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <>
      {children}
      <div className="grid grid-cols-2 gap-4">
        {team}
        {analytics}
      </div>
    </>
  )
}
```

## 2. Intercepting Routes

Intercepter une route pour l'afficher dans un modal.

```
app/
├── @modal/
│   └── (.)photo/
│       └── [id]/
│           └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
└── layout.tsx
```

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/ui/modal'
import { getPhoto } from '@/lib/data/photos'

export default async function PhotoModal({
  params
}: {
  params: { id: string }
}) {
  const photo = await getPhoto(params.id)

  return (
    <Modal>
      <img src={photo.url} alt={photo.title} />
    </Modal>
  )
}
```

## 3. Route Handlers avec Middleware

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { auth } from '@/lib/auth'

const postSchema = z.object({
  title: z.string().min(5),
  content: z.string().min(20)
})

// Middleware pour vérifier l'authentification
async function withAuth(handler: Function) {
  return async (req: NextRequest) => {
    const session = await auth()

    if (!session) {
      return NextResponse.json(
        { error: 'Non authentifié' },
        { status: 401 }
      )
    }

    return handler(req, session)
  }
}

// GET /api/posts
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')

  const posts = await db.post.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' }
  })

  return NextResponse.json({
    posts,
    page,
    hasMore: posts.length === limit
  })
}

// POST /api/posts
export const POST = withAuth(async (req: NextRequest, session: any) => {
  try {
    const body = await req.json()
    const data = postSchema.parse(body)

    const post = await db.post.create({
      data: {
        ...data,
        authorId: session.user.id
      }
    })

    return NextResponse.json(post, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    )
  }
})

// DELETE /api/posts/[id]
export const DELETE = withAuth(async (
  req: NextRequest,
  session: any,
  { params }: { params: { id: string } }
) => {
  const post = await db.post.findUnique({
    where: { id: params.id }
  })

  if (!post) {
    return NextResponse.json(
      { error: 'Post introuvable' },
      { status: 404 }
    )
  }

  if (post.authorId !== session.user.id) {
    return NextResponse.json(
      { error: 'Non autorisé' },
      { status: 403 }
    )
  }

  await db.post.delete({
    where: { id: params.id }
  })

  return NextResponse.json({ success: true })
})
```

## 4. Optimistic Updates

```tsx
'use client'

import { experimental_useOptimistic as useOptimistic } from 'react'
import { deletePost } from '@/lib/actions/posts'

export function PostsList({ initialPosts }: { initialPosts: Post[] }) {
  const [optimisticPosts, addOptimisticPost] = useOptimistic(
    initialPosts,
    (state, deletedId: string) => state.filter(post => post.id !== deletedId)
  )

  async function handleDelete(postId: string) {
    addOptimisticPost(postId)
    await deletePost(postId)
  }

  return (
    <div className="space-y-4">
      {optimisticPosts.map(post => (
        <PostCard
          key={post.id}
          post={post}
          onDelete={() => handleDelete(post.id)}
        />
      ))}
    </div>
  )
}
```

## 5. Pagination avec Server Components

```tsx
// app/posts/page.tsx
import { getPosts } from '@/lib/data/posts'
import { Pagination } from '@/components/ui/pagination'

export default async function PostsPage({
  searchParams
}: {
  searchParams: { page?: string }
}) {
  const page = parseInt(searchParams.page || '1')
  const limit = 10

  const { posts, total } = await getPosts({ page, limit })
  const totalPages = Math.ceil(total / limit)

  return (
    <div className="space-y-6">
      <div className="grid gap-4">
        {posts.map(post => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>

      <Pagination currentPage={page} totalPages={totalPages} />
    </div>
  )
}
```

```tsx
// components/ui/pagination.tsx
import Link from 'next/link'
import { Button } from './button'

export function Pagination({
  currentPage,
  totalPages
}: {
  currentPage: number
  totalPages: number
}) {
  return (
    <div className="flex items-center justify-center gap-2">
      <Button
        variant="outline"
        asChild
        disabled={currentPage === 1}
      >
        <Link href={`?page=${currentPage - 1}`}>Précédent</Link>
      </Button>

      <span className="text-sm text-muted-foreground">
        Page {currentPage} sur {totalPages}
      </span>

      <Button
        variant="outline"
        asChild
        disabled={currentPage === totalPages}
      >
        <Link href={`?page=${currentPage + 1}`}>Suivant</Link>
      </Button>
    </div>
  )
}
```

## 6. Search avec URL State

```tsx
'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { Input } from '@/components/ui/input'
import { useDebouncedCallback } from 'use-debounce'

export function SearchInput() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const handleSearch = useDebouncedCallback((term: string) => {
    const params = new URLSearchParams(searchParams)

    if (term) {
      params.set('q', term)
    } else {
      params.delete('q')
    }

    router.replace(`/posts?${params.toString()}`)
  }, 300)

  return (
    <Input
      placeholder="Rechercher..."
      defaultValue={searchParams.get('q') || ''}
      onChange={(e) => handleSearch(e.target.value)}
    />
  )
}
```

```tsx
// app/posts/page.tsx
import { Suspense } from 'react'
import { SearchInput } from '@/components/SearchInput'
import { PostsList } from '@/components/posts/PostsList'

export default function PostsPage({
  searchParams
}: {
  searchParams: { q?: string }
}) {
  return (
    <div className="space-y-6">
      <SearchInput />

      <Suspense fallback={<PostsSkeleton />}>
        <PostsList query={searchParams.q} />
      </Suspense>
    </div>
  )
}
```

## 7. Infinite Scroll

```tsx
'use client'

import { useEffect, useRef } from 'react'
import { useInView } from 'react-intersection-observer'

export function InfinitePostsList({ initialPosts }: { initialPosts: Post[] }) {
  const [posts, setPosts] = useState(initialPosts)
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const { ref, inView } = useInView()

  useEffect(() => {
    if (inView && hasMore) {
      loadMore()
    }
  }, [inView])

  async function loadMore() {
    const nextPage = page + 1
    const newPosts = await fetch(`/api/posts?page=${nextPage}`).then(r => r.json())

    if (newPosts.length === 0) {
      setHasMore(false)
    } else {
      setPosts(prev => [...prev, ...newPosts])
      setPage(nextPage)
    }
  }

  return (
    <div className="space-y-4">
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasMore && (
        <div ref={ref} className="py-4">
          <Spinner />
        </div>
      )}
    </div>
  )
}
```

## 8. File Upload avec Server Actions

```tsx
'use client'

// components/forms/UploadForm.tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { uploadFile } from '@/lib/actions/upload'

export function UploadForm() {
  const [isUploading, setIsUploading] = useState(false)

  async function handleSubmit(formData: FormData) {
    setIsUploading(true)
    try {
      const result = await uploadFile(formData)
      console.log('Fichier uploadé:', result)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <form action={handleSubmit}>
      <input
        type="file"
        name="file"
        accept="image/*"
        required
      />
      <Button type="submit" disabled={isUploading}>
        {isUploading ? 'Upload...' : 'Uploader'}
      </Button>
    </form>
  )
}
```

```tsx
'use server'

// lib/actions/upload.ts
import { writeFile } from 'fs/promises'
import { join } from 'path'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File

  if (!file) {
    throw new Error('Aucun fichier fourni')
  }

  // Valider le type de fichier
  if (!file.type.startsWith('image/')) {
    throw new Error('Le fichier doit être une image')
  }

  // Valider la taille (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    throw new Error('Le fichier est trop volumineux (max 5MB)')
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // Générer un nom unique
  const uniqueName = `${Date.now()}-${file.name}`
  const path = join(process.cwd(), 'public', 'uploads', uniqueName)

  await writeFile(path, buffer)

  return {
    success: true,
    url: `/uploads/${uniqueName}`
  }
}
```

## 9. Middleware pour Auth et Redirections

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(request: NextRequest) {
  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET
  })

  const isAuthPage = request.nextUrl.pathname.startsWith('/login')
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard')

  // Rediriger si connecté et sur page auth
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Rediriger si non connecté et sur page protégée
  if (isProtectedPage && !token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', request.nextUrl.pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register']
}
```

## 10. Real-time avec Server-Sent Events

```tsx
// app/api/notifications/route.ts
export async function GET(req: NextRequest) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      // Envoyer des notifications en temps réel
      const sendNotification = (data: any) => {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify(data)}\n\n`)
        )
      }

      // Exemple : écouter des événements
      const interval = setInterval(() => {
        sendNotification({
          type: 'notification',
          message: 'Nouvelle notification',
          timestamp: Date.now()
        })
      }, 5000)

      // Nettoyer à la fermeture
      req.signal.addEventListener('abort', () => {
        clearInterval(interval)
        controller.close()
      })
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  })
}
```

```tsx
'use client'

// components/Notifications.tsx
import { useEffect, useState } from 'react'

export function Notifications() {
  const [notifications, setNotifications] = useState<any[]>([])

  useEffect(() => {
    const eventSource = new EventSource('/api/notifications')

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setNotifications(prev => [data, ...prev].slice(0, 10))
    }

    return () => eventSource.close()
  }, [])

  return (
    <div className="space-y-2">
      {notifications.map((notif, i) => (
        <div key={i} className="p-2 bg-muted rounded">
          {notif.message}
        </div>
      ))}
    </div>
  )
}
```
