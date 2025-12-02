## Hackathon-Future-City Frontend

### How to use it

- First run `npm install` to install all dependencies
- Create a `.env` file based on [.env.example](.env.example) and add your Google Maps API key:
  - Get your API key from [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/credentials)
  - Make sure to enable the Maps JavaScript API
  - Add it to `.env` as `VITE_GOOGLE_MAPS_API_KEY=your-api-key-here`
- Then run `npm run dev` to start the development server
- The frontend will be available at http://localhost:5173

## Structure

```
frontend/
├── src/                       # Source code
│   ├── pages/                # Page components
│   ├── components/           # Reusable componens
│   ├── services/             # API service layer
│   ├── App.tsx               # Main app component with routing
│   ├── main.tsx              # Application entry point
│   ├── index.css             # Global styles
│   └── color-palette.css     # Color palette definitions
├── public/                   # Static assets
├── index.html                # HTML entry point
├── package.json              # Project dependencies and scripts
├── vite.config.ts            # Vite configuration
└── .env                      # Environment variables (API keys)
```
