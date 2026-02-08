---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication System

## Instructions

1. **User Registration (Signup)**
   - Validate user input (email, password)
   - Hash passwords before storing
   - Save user data securely in database

2. **User Login (Signin)**
   - Verify email and password
   - Compare hashed passwords
   - Generate access tokens on success

3. **Password Security**
   - Use bcrypt or argon2 for hashing
   - Never store plain text passwords
   - Apply salting and proper hash rounds

4. **JWT Token Handling**
   - Generate JWT on login
   - Include user ID and role in payload
   - Set token expiration time
   - Verify JWT on protected routes

5. **Better Auth Integration**
   - Configure Better Auth providers
   - Enable session and token management
   - Integrate with backend API routes
   - Support OAuth and credentials login

## Best Practices
- Enforce strong password rules
- Use HTTPS only
- Store JWT in HTTP-only cookies
- Rotate secrets regularly
- Implement refresh tokens
- Protect routes with middleware
- Rate-limit login attempts

## Example Structure
```ts
// Signup
const hashedPassword = await bcrypt.hash(password, 10);

await db.user.create({
  data: { email, password: hashedPassword }
});

// Signin
const isValid = await bcrypt.compare(password, user.password);

if (!isValid) throw new Error("Invalid credentials");

// JWT
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "1h" }
);
