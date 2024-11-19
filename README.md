## ITSM ticketing tool - POC

## Steps to create a react project

1. npm create vite@latest

2. Project name: … my-vite-react-app
   Select a framework: › React
   Select a variant: › JavaScript

3. Move into the newly created project directory
   cd Ticketing

4. Install Dependencies
   npm install

5. Start the Development Server
   npm run dev
6. Open the Application in a Browser
   http://localhost:5173

Ticketing/
├── public/ # Static files (e.g., favicon, assets)
├── src/ # Main source code
│ ├──Asset #
│ ├──Component # This file carries the main structure of the app
│ │ ├──Header.jsx # This component will always be stick to the Top of our screen helping us in navigating, userinfo , Logout , Themechange and more .
│ │ ├──Home.jsx # It is the parent component working as an container to hold header , Sidebar and the main content .
│ │ ├──Login.jsx # It let's the user login using Username and Password after authenticating with the backend if the user is present ot not .
│ │ ├──Sidebar.jsx # User support activities
│ │ ├──TicketCreation.jsx # Let's the User create new ticket using form having fields like owner , assign to , type , Description , Severity.
│ │ ├──Tickets.jsx # It is a table that shows all the present tickets .
├──pages # This carries all the sub-components required for our main components ex: Comment , TicketCreation , TicketView , TicketViewForm
│ │ ├──ProtectedRoutes.jsx # Help us protect our route form users who are not logged in and protect our data getting disclosed.
│ │ ├──TicketViewForm.jsx # This component will let the user get all the details about that particular ticket .
│ │ ├──Comment.jsx # Let the Users,Developer and admin discuss about the particular ticket .
├── App.jsx # Main React component carries the routing part
├── main.jsx # Entry point for the React app and the rendering is happening here
└── index.css # Global styles
├── package.json # Project dependencies and scripts
├── vite.config.js # Vite configuration
└── README.md # Documentation for the project
