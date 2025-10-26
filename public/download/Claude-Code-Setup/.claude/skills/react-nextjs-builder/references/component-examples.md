# Exemples Complets de Composants

## 1. Dashboard Layout Complet

```tsx
// components/layouts/DashboardLayout.tsx
import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { ThemeProvider } from './ThemeProvider'

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto bg-muted/10 p-6">
            {children}
          </main>
        </div>
      </div>
    </ThemeProvider>
  )
}
```

```tsx
// components/layouts/Sidebar.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Home, FileText, Settings, Users } from 'lucide-react'

const navigation = [
  { name: 'Accueil', href: '/dashboard', icon: Home },
  { name: 'Articles', href: '/dashboard/posts', icon: FileText },
  { name: 'Utilisateurs', href: '/dashboard/users', icon: Users },
  { name: 'Paramètres', href: '/dashboard/settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-card border-r flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Button
              key={item.name}
              asChild
              variant={isActive ? 'secondary' : 'ghost'}
              className={cn(
                'w-full justify-start',
                isActive && 'bg-secondary'
              )}
            >
              <Link href={item.href}>
                <item.icon className="mr-2 h-4 w-4" />
                {item.name}
              </Link>
            </Button>
          )
        })}
      </nav>

      <div className="p-4 border-t">
        <p className="text-sm text-muted-foreground">
          Version 1.0.0
        </p>
      </div>
    </aside>
  )
}
```

```tsx
// components/layouts/Header.tsx
import { UserNav } from './UserNav'
import { ThemeToggle } from './ThemeToggle'
import { getUser } from '@/lib/actions/auth'

export async function Header() {
  const user = await getUser()

  return (
    <header className="border-b bg-card">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <h2 className="text-lg font-semibold">Tableau de bord</h2>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />
          <UserNav user={user} />
        </div>
      </div>
    </header>
  )
}
```

## 2. Data Table avec shadcn/ui

```tsx
'use client'

// components/tables/DataTable.tsx
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  SortingState,
  ColumnFiltersState,
} from '@tanstack/react-table'
import { useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  searchKey?: string
}

export function DataTable<TData, TValue>({
  columns,
  data,
  searchKey,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    state: {
      sorting,
      columnFilters,
    },
  })

  return (
    <div className="space-y-4">
      {searchKey && (
        <Input
          placeholder="Rechercher..."
          value={(table.getColumn(searchKey)?.getFilterValue() as string) ?? ''}
          onChange={(e) =>
            table.getColumn(searchKey)?.setFilterValue(e.target.value)
          }
          className="max-w-sm"
        />
      )}

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && 'selected'}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  Aucun résultat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          {table.getFilteredRowModel().rows.length} résultat(s)
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Précédent
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Suivant
          </Button>
        </div>
      </div>
    </div>
  )
}
```

```tsx
// app/dashboard/users/columns.tsx
'use client'

import { ColumnDef } from '@tanstack/react-table'
import { Button } from '@/components/ui/button'
import { ArrowUpDown, MoreHorizontal } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

export type User = {
  id: string
  name: string
  email: string
  role: string
}

export const columns: ColumnDef<User>[] = [
  {
    accessorKey: 'name',
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
        >
          Nom
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
  },
  {
    accessorKey: 'email',
    header: 'Email',
  },
  {
    accessorKey: 'role',
    header: 'Rôle',
  },
  {
    id: 'actions',
    cell: ({ row }) => {
      const user = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>Modifier</DropdownMenuItem>
            <DropdownMenuItem className="text-destructive">
              Supprimer
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]
```

## 3. Modal/Dialog Complet

```tsx
'use client'

// components/modals/CreatePostModal.tsx
import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { PostForm } from '@/components/forms/PostForm'
import { createPost } from '@/lib/actions/posts'
import { toast } from 'sonner'

export function CreatePostModal() {
  const [open, setOpen] = useState(false)

  async function handleSubmit(values: any) {
    try {
      await createPost(values)
      toast.success('Article créé avec succès')
      setOpen(false)
    } catch (error) {
      toast.error('Erreur lors de la création')
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Nouvel article</Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Créer un article</DialogTitle>
          <DialogDescription>
            Remplissez le formulaire pour créer un nouvel article
          </DialogDescription>
        </DialogHeader>
        <PostForm onSubmit={handleSubmit} />
      </DialogContent>
    </Dialog>
  )
}
```

## 4. Composant de Drag & Drop

```tsx
'use client'

// components/upload/DropZone.tsx
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DropZoneProps {
  onDrop: (files: File[]) => void
  accept?: Record<string, string[]>
  maxSize?: number
}

export function DropZone({ onDrop, accept, maxSize }: DropZoneProps) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    maxSize,
  })

  return (
    <div
      {...getRootProps()}
      className={cn(
        'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition',
        isDragActive
          ? 'border-primary bg-primary/10'
          : 'border-muted-foreground/25 hover:border-muted-foreground/50'
      )}
    >
      <input {...getInputProps()} />
      <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
      {isDragActive ? (
        <p>Déposez les fichiers ici...</p>
      ) : (
        <div>
          <p className="text-lg mb-2">
            Glissez-déposez vos fichiers ici
          </p>
          <p className="text-sm text-muted-foreground">
            ou cliquez pour sélectionner
          </p>
        </div>
      )}
    </div>
  )
}
```

## 5. Composant de Statistiques

```tsx
// components/dashboard/StatsCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface StatsCardProps {
  title: string
  value: string | number
  description?: string
  icon: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
}

export function StatsCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
}: StatsCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {(description || trend) && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
            {trend && (
              <span
                className={cn(
                  'font-medium',
                  trend.isPositive ? 'text-green-600' : 'text-red-600'
                )}
              >
                {trend.isPositive ? '+' : ''}
                {trend.value}%
              </span>
            )}
            {description && <span>{description}</span>}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

```tsx
// app/dashboard/page.tsx
import { StatsCard } from '@/components/dashboard/StatsCard'
import { Users, FileText, TrendingUp, DollarSign } from 'lucide-react'
import { getStats } from '@/lib/data/stats'

export default async function DashboardPage() {
  const stats = await getStats()

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Tableau de bord</h1>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Utilisateurs"
          value={stats.totalUsers}
          icon={Users}
          trend={{ value: 12, isPositive: true }}
          description="vs. mois dernier"
        />
        <StatsCard
          title="Articles"
          value={stats.totalPosts}
          icon={FileText}
          trend={{ value: 5, isPositive: true }}
        />
        <StatsCard
          title="Vues"
          value={stats.totalViews}
          icon={TrendingUp}
          trend={{ value: -2, isPositive: false }}
        />
        <StatsCard
          title="Revenus"
          value={`${stats.revenue}€`}
          icon={DollarSign}
          trend={{ value: 8, isPositive: true }}
        />
      </div>
    </div>
  )
}
```

## 6. Composant de Commentaires

```tsx
// components/comments/CommentsList.tsx
import { getComments } from '@/lib/data/comments'
import { CommentCard } from './CommentCard'
import { CommentForm } from './CommentForm'

export async function CommentsList({ postId }: { postId: string }) {
  const comments = await getComments(postId)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">
          Commentaires ({comments.length})
        </h3>
      </div>

      <CommentForm postId={postId} />

      <div className="space-y-4">
        {comments.map(comment => (
          <CommentCard key={comment.id} comment={comment} />
        ))}
      </div>
    </div>
  )
}
```

```tsx
// components/comments/CommentCard.tsx
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { formatDistanceToNow } from 'date-fns'
import { fr } from 'date-fns/locale'

export function CommentCard({ comment }: { comment: Comment }) {
  return (
    <div className="flex gap-4">
      <Avatar>
        <AvatarImage src={comment.author.image} />
        <AvatarFallback>{comment.author.name[0]}</AvatarFallback>
      </Avatar>

      <div className="flex-1 space-y-1">
        <div className="flex items-center gap-2">
          <p className="font-medium">{comment.author.name}</p>
          <p className="text-xs text-muted-foreground">
            {formatDistanceToNow(new Date(comment.createdAt), {
              addSuffix: true,
              locale: fr,
            })}
          </p>
        </div>
        <p className="text-sm">{comment.content}</p>
      </div>
    </div>
  )
}
```
