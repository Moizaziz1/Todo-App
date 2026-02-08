---
name: database-schema-design
description: Design relational database schemas with tables, migrations, and constraints. Use for backend data modeling.
---

# Database Schema Design

## Instructions

1. **Table creation**
   - Define primary keys
   - Use appropriate data types
   - Normalize data where possible

2. **Relationships**
   - One-to-one, one-to-many, many-to-many
   - Use foreign keys
   - Enforce referential integrity

3. **Migrations**
   - Version-controlled schema changes
   - Separate up and down migrations
   - Never edit old migrations after production

4. **Indexes & Constraints**
   - Add indexes for frequently queried columns
   - Use unique constraints where required
   - Apply NOT NULL and CHECK constraints

## Best Practices
- Use clear, consistent naming (snake_case or camelCase)
- Avoid storing duplicate data
- Keep tables focused on a single responsibility
- Always use migrations instead of manual edits
- Document schema decisions

## Example Structure
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
