# Todo Application Frontend

This is the frontend for the Todo application built with Next.js, TypeScript, and Tailwind CSS.

## Features

- User authentication (login/signup)
- Todo management (create, read, update, delete)
- Responsive design
- Context-based state management
- Type-safe with TypeScript

## Tech Stack

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- React Context API for state management

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables by copying `.env.local.example` to `.env.local` and updating the values

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   └── dashboard/         # Dashboard page
├── components/            # Reusable components
│   ├── ui/                # Base UI components
│   ├── auth/              # Authentication components
│   └── todos/             # Todo-specific components
├── lib/                   # Utilities and API client
├── providers/             # React context providers
└── styles/                # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter