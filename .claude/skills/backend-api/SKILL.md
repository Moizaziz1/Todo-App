---
name: backend-api
description: Build backend APIs with routes, request/response handling, and database connectivity. Use for server-side application logic.
---

# Backend API Development

## Instructions

1. **Route structure**
   - Define RESTful endpoints
   - Group routes by resource
   - Use clear URL naming

2. **Request & response handling**
   - Parse request bodies and query params
   - Validate incoming data
   - Return proper HTTP status codes

3. **Database connection**
   - Configure database client
   - Use connection pooling
   - Handle connection errors safely

4. **Business logic**
   - Implement CRUD operations
   - Separate controllers and services
   - Handle edge cases

## Best Practices
- Keep routes thin and logic in services
- Always validate user input
- Use async/await for database operations
- Never expose sensitive errors
- Follow REST conventions

## Example Structure
```js
import express from "express";
import { connectDB } from "./db.js";

const app = express();
app.use(express.json());

app.get("/users", async (req, res) => {
  const users = await db.query("SELECT * FROM users");
  res.status(200).json(users.rows);
});

app.post("/users", async (req, res) => {
  const { name, email } = req.body;
  const result = await db.query(
    "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
    [name, email]
  );
  res.status(201).json(result.rows[0]);
});

connectDB();
app.listen(3000);
