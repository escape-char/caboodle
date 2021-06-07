import React from 'react';
import { Theme, createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { Switch, BrowserRouter as Router } from 'react-router-dom';
import { RouteWithSubRoutes } from './common/utils/route';
import CssBaseline from '@material-ui/core/CssBaseline';
import defaultTheme from './common/theme';
import routes from './routes';
import {AppBar} from './appbar';
import {Sidebar} from './sidebar';
import './App.css';

const theme: Theme = createMuiTheme(defaultTheme);

function App() {
  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="App">
          <AppBar header="Caboodle"/>
          <Sidebar/>
          <Router>
            <Switch>
              {routes.map((route, i) => (
                <RouteWithSubRoutes key={i} {...route} />
              ))}
            </Switch>

          </Router>

        </div>
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
