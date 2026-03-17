# PIPPF - Pre-Indexing Phishing Prevention Framework

B.Tech Final Year Cybersecurity Project

## Project Overview

PIPPF is a web-based phishing detection system that analyzes URLs before they are indexed by search engines. The system uses machine learning algorithms (Random Forest and Gradient Boosting) to classify websites as SAFE, SUSPICIOUS, or PHISHING based on multiple security indicators.

## Features

- **URL Verification**: Real-time analysis of URLs with risk scoring
- **Secure Search Engine**: Pre-filtered search results showing only verified safe websites
- **Admin Dashboard**: Monitoring and analytics with filterable URL database
- **System Architecture**: Detailed explanation of ML models and detection workflow

## Tech Stack

- **Frontend**: React.js
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Animations**: CSS3 Animations

## Project Structure

```
pippf-project/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js          # Navigation component
│   │   └── StatusBadge.js     # Reusable status indicator
│   ├── pages/
│   │   ├── Landing.js         # Home page
│   │   ├── VerifyUrl.js       # URL verification page
│   │   ├── SecureSearch.js    # Search engine page
│   │   ├── Dashboard.js       # Admin dashboard
│   │   └── Architecture.js    # System architecture page
│   ├── data/
│   │   └── mockData.js        # Mock database (simulates backend)
│   ├── utils/
│   │   └── helpers.js         # Utility functions
│   ├── App.js                 # Main app component
│   ├── App.css                # Custom styles
│   ├── index.js               # Entry point
│   └── index.css              # Global styles
├── package.json
├── tailwind.config.js
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Steps

1. **Navigate to project directory**
   ```bash
   cd pippf-project
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

## How It Works

### Frontend (Current Implementation)
- Pure React application with simulated ML predictions
- Mock data stored in `src/data/mockData.js`
- Client-side filtering and analysis simulation
- No backend required for demonstration

### Backend (Future Implementation)
To make this production-ready, you would need:

1. **Backend API** (Python Flask/FastAPI)
   - URL feature extraction
   - ML model integration (Random Forest, Gradient Boosting)
   - Database connection (PostgreSQL/MongoDB)

2. **Machine Learning Pipeline**
   - Real URL analysis
   - SSL certificate validation
   - WHOIS lookup
   - DNS checks
   - Domain age verification

3. **Search Integration**
   - Web crawler
   - Indexing system
   - Real-time filtering

## Key Components Explained

### 1. Header.js
Navigation component with responsive mobile menu

### 2. mockData.js
Contains sample URL database with:
- URL
- Status (SAFE/SUSPICIOUS/PHISHING)
- Risk score (0-100%)
- SSL status
- Domain age
- URL complexity

### 3. helpers.js
Utility functions for:
- Status color coding
- Risk assessment
- Data filtering
- Analysis simulation

### 4. Individual Pages
- **Landing**: Hero section, features, and stats
- **VerifyUrl**: URL input with detailed risk analysis
- **SecureSearch**: Search with pre-filtered results
- **Dashboard**: Statistics and URL table with filters
- **Architecture**: System workflow and ML model details

## Customization

### Changing Mock Data
Edit `src/data/mockData.js` to modify sample URLs and statistics

### Styling
- Modify Tailwind classes directly in components
- Edit `src/App.css` for custom animations
- Update `tailwind.config.js` for theme changes

### Adding New Pages
1. Create new page component in `src/pages/`
2. Import in `App.js`
3. Add navigation button in `Header.js`
4. Update routing logic in `App.js`

## Deployment

### Build for production
```bash
npm run build
```

This creates an optimized production build in the `build` folder.

### Deploy options
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## Future Enhancements

1. **Backend Integration**
   - Connect to real ML models
   - Database implementation
   - API endpoints

2. **Real-time Features**
   - Live URL scanning
   - WebSocket updates
   - Notification system

3. **Advanced Analytics**
   - Charts and graphs
   - Historical trends
   - Threat intelligence feeds

4. **User Management**
   - Authentication
   - Role-based access
   - Activity logs

## Notes for Presentation

- This is a **demonstration frontend** showing the UI/UX concept
- ML predictions are **simulated** using random selection from mock data
- All data is **client-side** - no actual security analysis occurs
- Perfect for presenting the system design and user interface
- Backend implementation would be required for production use

## License

This is an academic project for educational purposes.

## Contact

For questions or suggestions, please contact your project guide or supervisor.
