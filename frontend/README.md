# NBA Newsletter Frontend

This is the frontend application for the NBA Newsletter service.  
Users can subscribe to the newsletter and select their favorite NBA teams.

## Tech Stack

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- Axios for API requests

## Features

- Email subscription form
- Favorite team selection
- Calls backend API at `/api/...`
- Mobile-friendly UI

## Development

```bash
cd frontend
npm install
npm run dev
```

## API Proxy

Vite proxy is configured to forward `/api` to `http://localhost:8000`:

```ts
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## Example APIs Used

- `POST /api/users/subscribe`
- `PATCH /api/users/{email}/teams`
- `GET /api/teams`

## Project Structure

```
frontend/
├── public/
├── src/
│   └── App.tsx
├── index.html
├── vite.config.ts
└── ...
```
