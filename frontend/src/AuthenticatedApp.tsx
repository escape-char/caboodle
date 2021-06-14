import {Switch} from 'react-router-dom'
import {authenticatedRoutes} from './routes'
import {RouteWithSubRoutes} from './common/utils/route'


export default function AuthenticatedApp(props:object){
  return (
    <Switch>
      {authenticatedRoutes.map((route, i) => (
        <RouteWithSubRoutes key={i} {...route} />
      ))}
    </Switch>
  )
}
