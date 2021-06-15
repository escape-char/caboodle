import {Switch} from 'react-router-dom'
import {authenticatedRoutes} from './routes'
import {RouteWithSubRoutes} from './common/utils/route'
import {AppBar} from './features/appbar'
import {Sidebar} from './features/sidebar'


export default function AuthenticatedApp(props:object){
  return (
    <>
      <AppBar header="Cabool"/>
      <Sidebar/>
      <Switch>
        {authenticatedRoutes.map((route, i) => (
          <RouteWithSubRoutes key={i} {...route} />
        ))}
      </Switch>
    </>
  )
}
