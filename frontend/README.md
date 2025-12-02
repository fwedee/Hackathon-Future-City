## Hackathon-Future-City Frontend

### How to use it

- First run `npm install` to install all dependencies
- Create a `.env` file based on [.env.example](.env.example) and add your Google Maps API key:
  - Get your API key from [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/credentials)
  - Make sure to enable the Maps JavaScript API
  - Add it to `.env` as `VITE_GOOGLE_MAPS_API_KEY=your-api-key-here`
- Then run `npm run dev` to start the development server
- The frontend will be available at http://localhost:5173
