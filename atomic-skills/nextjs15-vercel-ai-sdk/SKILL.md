---
name: nextjs15-vercel-ai-sdk
description: This skill should be used when building Next.js 15 App Router applications with Vercel AI SDK, React Server Components, Server Actions, TanStack Query, Tailwind CSS, shadcn/ui (Radix UI), Zustand, and TypeScript — covering streaming chat UIs, NATS integration, AI-powered features, and modern frontend patterns.
metadata:
  category: frontend
  source:
    repository: https://github.com/PatrickJS/awesome-cursorrules
    path: rules/nextjs15-react19-vercelai-tailwind-cursorrules-prompt-file
---

# Next.js 15 + Vercel AI SDK + shadcn/ui

## Source

- **awesome-cursorrules** — GitHub: [PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) (38.8k stars, 3.3k forks)
- **Vercel AI SDK** — GitHub: [vercel/ai](https://github.com/vercel/ai) (11k+ stars)
- **shadcn/ui** — GitHub: [shadcn-ui/ui](https://github.com/shadcn-ui/ui) (80k+ stars)

## Trigger Keywords

`next.js 15`, `app router`, `vercel ai sdk`, `ai sdk`, `shadcn`, `radix ui`, `tailwind`, `server components`, `RSC`, `server actions`, `tanstack query`, `zustand`, `streaming`, `chat UI`, `seadragon`

## Code Style & Structure

### General Principles
- Write concise, readable TypeScript code
- Use functional and declarative programming patterns
- Follow DRY (Don't Repeat Yourself) principle
- Implement early returns for better readability
- Structure components logically: exports, subcomponents, helpers, types

### Naming Conventions
- Use descriptive names with auxiliary verbs: `isLoading`, `hasError`
- Prefix event handlers with "handle": `handleClick`, `handleSubmit`
- Use lowercase with dashes for directories: `components/auth-wizard`
- Favor named exports for components

### TypeScript Usage
- Use TypeScript for all code
- Prefer interfaces over types
- Avoid enums; use const maps instead
- Implement proper type safety and inference
- Use `satisfies` operator for type validation

## React & Next.js 15 Patterns

### Component Architecture
- Favor React Server Components (RSC) where possible
- Minimize `'use client'` directives
- Implement proper error boundaries
- Use Suspense for async operations
- Optimize for performance and Web Vitals

### State Management
- Use `useActionState` instead of deprecated `useFormState`
- Leverage enhanced `useFormStatus` with new properties (data, method, action)
- Minimize client-side state; use URL state management with `nuqs` where applicable
- Use Zustand for complex client-side state
- TanStack Query for server state management

### Async Request APIs (Next.js 15)
```typescript
// Always use async versions of runtime APIs
const cookieStore = await cookies();
const headersList = await headers();
const { isEnabled } = await draftMode();

// Handle async params in layouts/pages
const params = await props.params;
const searchParams = await props.searchParams;
```

### Data Fetching
```typescript
// Server component data fetching
async function Page() {
  const data = await fetchData();
  return <Component data={data} />;
}

// Client-side with TanStack Query
const { data, isLoading } = useQuery({
  queryKey: ['messages', chatId],
  queryFn: () => api.getMessages(chatId),
});
```

## Vercel AI SDK Integration

### Streaming Chat Pattern
```typescript
import { useChat } from '@ai-sdk/react';

function ChatComponent() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    streamProtocol: 'text',
  });

  return (
    <form onSubmit={handleSubmit}>
      {messages.map(m => <Message key={m.id} message={m} />)}
      <input value={input} onChange={handleInputChange} />
    </form>
  );
}
```

### Server-side AI Route
```typescript
import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: openai('gpt-4o'),
    messages,
  });
  return result.toDataStreamResponse();
}
```

### NATS Streaming Integration (Dumatel Pattern)
The Seadragon frontend uses NATS JetStream for real-time message streaming:
- Client subscribes to NATS subject for chat responses
- Messages are chunked and streamed from Python backend through NATS
- Frontend assembles chunks into complete responses
- Use `nats` npm package for WebSocket-based NATS connections

## UI Components (shadcn/ui + Radix UI)

### Component Pattern
```typescript
import { cn } from '@/shared/lib/utils';
import { Button } from '@/shared/ui/button';
import { Dialog, DialogContent, DialogTrigger } from '@/shared/ui/dialog';

interface Props extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
}

export function MyComponent({ title, className, ...props }: Props) {
  return (
    <div className={cn('flex flex-col gap-4', className)} {...props}>
      <h2 className="text-lg font-semibold">{title}</h2>
    </div>
  );
}
```

### Tailwind Best Practices
- Use Tailwind CSS for all styling
- Prefer `cn()` utility for conditional classes
- Use CSS variables for theming (defined in `tailwind.config.ts`)
- Implement responsive design with mobile-first approach
- Use `tailwindcss-animate` for transitions

## Testing

### Vitest for Unit Tests
```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

describe('Component', () => {
  it('renders correctly', () => {
    render(<Component title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

### Playwright for E2E
```typescript
import { test, expect } from '@playwright/test';

test('chat flow', async ({ page }) => {
  await page.goto('/chat');
  await page.fill('[data-testid="chat-input"]', 'Hello');
  await page.click('[data-testid="send-button"]');
  await expect(page.locator('[data-testid="message"]')).toBeVisible();
});
```

## Performance Optimization
- Implement route-based code splitting
- Use `dynamic()` for lazy loading heavy components
- Optimize images with `next/image` and WebP format
- Minimize bundle size with tree-shaking
- Use `React.memo()` and `useCallback()` for expensive re-renders
- Implement virtual scrolling with `@tanstack/react-virtual` for long lists

## When NOT to Use
- For Python backend services → use `fastapi-expert`, `python-dev`
- For pure API design → use `api-designer`
- For infrastructure → use `devops-engineer`
