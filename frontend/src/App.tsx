import React, {Suspense} from 'react';
import {useAuth} from './features/auth/context'
import './App.css';

const AuthenticatedApp = React.lazy(() =>
  import('./AuthenticatedApp')
)
const UnauthenticatedApp = React.lazy(() => import('./UnauthenticatedApp'))

function App() {
  const {isAuthenticated} = useAuth()
  return (
    <Suspense fallback={<p>loading</p>}>
      {isAuthenticated() ? <AuthenticatedApp/> : <UnauthenticatedApp/>}
    </Suspense>
  );
}

export default App;
