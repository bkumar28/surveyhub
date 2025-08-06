# SurveyHub Frontend

A modern, scalable React TypeScript application for survey management.

## 🚀 Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn
- TypeScript knowledge

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

### Build

```bash
npm run build
```

### Type Checking

```bash
npm run type-check
```

## 📁 Project Structure

This project follows a feature-based architecture with TypeScript:

- `src/features/` - Feature modules (auth, surveys, billing, etc.)
- `src/shared/` - Shared components, hooks, utilities, and types
- `src/app/` - App-level configuration (store, router, providers)
- `src/config/` - Configuration files

## 🛠️ Technologies

- **React 18** - UI Library
- **TypeScript** - Type Safety
- **Redux Toolkit** - State Management
- **React Router** - Routing
- **React Hook Form** - Form Management
- **Axios** - HTTP Client
- **SCSS** - Styling

## 🎯 Features

- 🔐 Authentication & Authorization
- 📊 Survey Management
- 💳 Billing & Subscriptions
- 👥 User Management
- 📈 Analytics & Reporting
- ⚙️ Settings & Preferences
- 🌙 Dark/Light Theme
- 📱 Responsive Design

## 📚 TypeScript Guidelines

- Use strict TypeScript configuration
- Define interfaces for all data structures
- Use proper typing for API responses
- Implement type guards where necessary
- Avoid `any` type usage

## 🧪 Testing

```bash
npm test
```

## 🔧 Code Quality

```bash
# Linting
npm run lint
npm run lint:fix

# Formatting
npm run format
```

## 🤝 Contributing

1. Follow the established folder structure
2. Use absolute imports with configured paths
3. Write tests for new components
4. Follow TypeScript best practices
5. Follow the coding standards (ESLint + Prettier)
