import React from 'react';
import ReactDOM from 'react-dom';
import { Theme, createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import {BrowserRouter as Router } from 'react-router-dom';
import reportWebVitals from './reportWebVitals';
import {AuthProvider} from './features/auth/context'
import GlobalAlertProvider from './features/globalalert/context'
import CssBaseline from '@material-ui/core/CssBaseline';
import defaultTheme from './common/theme';
import App from './App';
import './index.css';

const theme: Theme = createMuiTheme(defaultTheme);

export function AppProviders({children}: {children: React.ReactNode}) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
      <Router>
          <GlobalAlertProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </GlobalAlertProvider>
      </Router>
    </ThemeProvider>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <AppProviders>
        <App />
    </AppProviders>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
