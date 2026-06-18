# ASHA - Data Management System

## Overview

ASHA is a data management system designed for ASHA (Accredited Social Health Activists) workers who manage pregnancy, medication, vaccination, birth, and death records for populations in their area. ASHA workers typically manage records for 1000+ individuals, making manual book-based record management impractical.

This system provides a user-friendly interface for ASHA workers to query their data using natural language instead of SQL, while ensuring data integrity through role-based access control.

## Key Features

- **Natural Language to SQL**: ASHA workers can query data using plain language without SQL knowledge
- **Multi-modal Input**: Voice and image-based query support
- **Role-Based Access Control**: ASHA workers can only read data; ANM (Auxiliary Nurse Midwife) workers have write/update/delete permissions
- **JWT Authentication**: Secure user authentication with JWT tokens
- **Session Management**: Automatic logout after session completion
- **Favorites**: Save frequently used queries for quick access
- **Admin Queries**: Admin-defined queries available to all ASHA workers
- **Password Reset**: OTP-based password reset via registered email (using Brevo SMTP)
- **Query Results Display**: Shows generated SQL, row count, and formatted data

## Tech Stack

**Frontend:**
- React 19
- Vite
- Tailwind CSS
- React Router
- Axios
- React Hook Form
- Framer Motion

**Backend:**
- FastAPI
- SQLAlchemy
- Pydantic
- Python 3.x

## Backend Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd asha/backend
   ```

2. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or for Windows:
   ```bash
   powershell -ExecutionPolicy BypassUser -Command "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install project dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   - Create a `.env` file in the backend directory with the following variables:
     ```
     # PostgreSQL Database Configuration
     DB_USER=postgres
     DB_PASSWORD=your-password
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=asha
     
     # LLM Configuration (Groq)
     GROQ_API_KEY=your-groq-api-key
     
     # JWT Configuration
     JWT_SECRET_KEY=your-secret-key-here
     JWT_ALGORITHM=HS256
     JWT_EXPIRE_MINUTES=60
     
     # Email Configuration (Brevo SMTP)
     SENDER_EMAIL=your-email@example.com
     SMTP_HOST=smtp-relay.brevo.com
     SMTP_PORT=587
     SMTP_USER=your-brevo-smtp-user
     SMTP_PASSWORD=your-brevo-smtp-password
     ```

5. **Set up the database**
   - Create the database and run the schema (see `schema.sql` for 3NF normalized database structure)
   ```bash
   createdb -U postgres asha
   psql -U postgres -d asha -f schema.sql
   ```

6. **Run the backend server**
   ```bash
   uv run uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

## Frontend Setup

### Prerequisites
- Node.js 16 or higher
- npm or yarn
- Git

### Installation Steps

1. **Navigate to frontend directory**
   ```bash
   cd asha/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   - Create a `.env.local` file in the frontend directory with:
     ```
     VITE_API_URL=http://localhost:8000
     ```

4. **Run the development server**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`

5. **Build for production** (optional)
   ```bash
   npm run build
   ```

## Project Structure

# File Tree: asha

```
├── 📁 backend
│   ├── 📁 core
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 config.py
│   │   ├── 🐍 database.py
│   │   ├── 🐍 email.py
│   │   ├── 🐍 llm.py
│   │   └── 🐍 security.py
│   ├── 📁 routers
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 chat.py
│   │   ├── 🐍 favorites.py
│   │   ├── 🐍 login.py
│   │   ├── 🐍 password_reset.py
│   │   └── 🐍 voice_query.py
│   ├── ⚙️ .gitignore
│   ├── 🐍 __init__.py
│   ├── 🐍 main.py
│   ├── ⚙️ pyproject.toml
│   └── 📄 uv.lock
├── 📁 frontend
│   ├── 📁 public
│   │   ├── 🖼️ favicon.svg
│   │   ├── 🖼️ icons.svg
│   │   └── 🖼️ image.png
│   ├── 📁 src
│   │   ├── 📁 assets
│   │   │   ├── 🖼️ hero.png
│   │   │   ├── 🖼️ react.svg
│   │   │   └── 🖼️ vite.svg
│   │   ├── 📁 components
│   │   │   ├── 📄 AssistantResponse.jsx
│   │   │   ├── 📄 AssistantSidebar.jsx
│   │   │   ├── 📄 ChatInput.jsx
│   │   │   ├── 📄 ErrorResponse.jsx
│   │   │   ├── 📄 Features.jsx
│   │   │   ├── 📄 Footer.jsx
│   │   │   ├── 📄 Hero.jsx
│   │   │   ├── 📄 Mission.jsx
│   │   │   ├── 📄 Navbar.jsx
│   │   │   ├── 📄 ProtectedRoute.jsx
│   │   │   ├── 📄 ResultsTable.jsx
│   │   │   ├── 📄 SqlCard.jsx
│   │   │   └── 📄 UserMessage.jsx
│   │   ├── 📁 pages
│   │   │   ├── 📄 Assistant.jsx
│   │   │   ├── 📄 ForgotPassword.jsx
│   │   │   ├── 📄 Landing.jsx
│   │   │   └── 📄 Login.jsx
│   │   ├── 📁 services
│   │   │   └── 📄 api.js
│   │   ├── 📄 App.jsx
│   │   ├── 🎨 index.css
│   │   └── 📄 main.jsx
│   ├── ⚙️ .gitignore
│   ├── 📄 eslint.config.js
│   ├── 🌐 index.html
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   └── 📄 vite.config.js
├── 📝 README.md
├── 🎵 english.mp3
├── 📄 schema.sql
└── 🖼️ what is the sex ratio in my area.png
```

## Future Enhancements

- **SQL Query Validation**: Implement validation for LLM-generated SQL queries by executing them against the database. If errors occur, send the error details back to the LLM along with the original question to regenerate valid SQL.