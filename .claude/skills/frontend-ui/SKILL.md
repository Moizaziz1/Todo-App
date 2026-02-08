---
name: frontend-ui
description: Build frontend pages and reusable components with layouts and styling. Use for web application interfaces.
---

# Frontend UI Development

## Instructions

1. **Page structure**
   - Define clear layout sections (header, main, footer)
   - Use semantic HTML
   - Organize content logically

2. **Components**
   - Create reusable UI components
   - Pass data via props
   - Keep components small and focused

3. **Layout & styling**
   - Use Flexbox or Grid for layout
   - Apply consistent spacing and typography
   - Use responsive units (%, rem, vh, vw)

4. **Responsiveness**
   - Design mobile-first
   - Add breakpoints for tablets and desktops
   - Ensure accessibility

## Best Practices
- Reuse components instead of duplicating code
- Keep styles consistent across pages
- Avoid inline styles
- Use meaningful class names
- Test UI on multiple screen sizes

## Example Structure
```html
<main class="page">
  <header class="navbar">
    <h1 class="logo">My App</h1>
  </header>

  <section class="content">
    <div class="card">
      <h2 class="card-title">Title</h2>
      <p class="card-text">Description text</p>
      <button class="btn-primary">Click Me</button>
    </div>
  </section>

  <footer class="footer">
    <p>© 2026 My App</p>
  </footer>
</main>
 