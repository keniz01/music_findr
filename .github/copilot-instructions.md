# AI Coding Assistant Instructions

## Project Overview
Music Findr is a full-stack application for exploring music data through a modern web interface. It consists of:

1. **Backend (`data_accessor`)**:
   - Python-based PostgreSQL data access layer
   - Strict read-only interface (SELECT queries only)
   - Semantic schema exploration using vector embeddings
   - Clean architecture: Controller → Service → Repository layers

2. **Frontend (`music-findr-app`)**:
   - React + TypeScript + Vite application
   - Ant Design component library
   - TailwindCSS for styling
   - Testing with Vitest

## Key Architecture Patterns

### Backend Architecture

```
┌─ Application Layer ─┐
│    (Controller)     │ → Public API, request handling
├────────┬───────────┤
│  Domain Layer      │ → Business logic, interfaces
├────────┬───────────┤
│ Infrastructure     │ → Data access, configuration
└────────┬───────────┘
         ▼
    PostgreSQL DB
```

- **Only** import `MusicQueryController` from package root
- Internal modules are prefixed with `_` and raise ImportError if imported directly
- All database operations are async/await based
- Strict SQL safety checks prevent non-SELECT operations

### Frontend Architecture
- Vite-based React application with TypeScript
- Component-based architecture with Ant Design
- ESLint with strict TypeScript checking
- Test-driven development with Vitest

## Development Workflow

### Backend Development
1. **Environment Setup**:
   ```bash
   cd back-end/data_accessor
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install -e .
   ```

2. **Running Tests**:
   ```bash
   python tests/run_tests.py  # Includes coverage report
   ```

3. **Package Building**:
   ```bash
   uv build  # Creates distributable in dist/
   ```

### Frontend Development
1. **Setup**:
   ```bash
   cd front-end/music-findr-app
   npm install
   ```

2. **Development Server**:
   ```bash
   npm run dev
   ```

3. **Testing**:
   ```bash
   npm run test
   ```

## Key Integration Points

1. **Database Schema Access**:
   ```python
   # Example: Semantic schema search
   embeddings = [0.1, -0.2, ...]  # 384-dim vector
   schema = await controller.fetch_database_schema(embeddings)
   ```

2. **SQL Query Execution**:
   ```python
   # Only SELECT queries allowed
   try:
       results = await controller.execute_sql("SELECT * FROM music_table")
   except ForbiddenSqlStatementException:
       # Handle non-SELECT query error
   ```

## Project Conventions

### Backend
1. **Error Handling**:
   - Custom exceptions in `domain/exceptions/`
   - Always handle `ForbiddenSqlStatementException` and `SqlStatementExecutionException`
   - Use proper async context management

2. **SQL Safety**:
   - Only SELECT statements allowed
   - No CTEs (WITH clauses)
   - No comments in queries
   - No transaction control statements

3. **Testing**:
   - Use `unittest.IsolatedAsyncioTestCase` for async tests
   - Mock external dependencies (database, services)
   - Test both success and error paths

### Frontend
1. **Component Structure**:
   - Functional components with hooks
   - TypeScript for type safety
   - Ant Design for UI components
   - TailwindCSS for custom styling

2. **Testing**:
   - Test files colocated with components
   - Use React Testing Library patterns
   - Vitest as test runner

## Debugging Tips
1. **Backend**:
   - Check coverage reports in `coverage_html_report/`
   - Use logging for tracing (configured in each layer)
   - Validate SQL safety with `DefaultSqlSafetyChecker`

2. **Frontend**:
   - Use React DevTools for component debugging
   - ESLint with TypeScript for static analysis
   - Vite HMR for rapid development

## Common Gotchas
1. Don't import internal modules directly (they start with `_`)
2. Always handle async operations properly
3. Remember SQL restrictions (SELECT only)
4. Use vector embeddings for schema exploration
5. Configure Python path: `PYTHONPATH=src`
6. Frontend requires Node.js 19+ for React 19

## Configuration Files
- Backend: `secrets.toml` for database config
- Frontend: `tsconfig.json` for TypeScript
- ESLint: `eslint.config.js`
- Vite: `vite.config.ts`