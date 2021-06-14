import {Switch} from 'react-router-dom'
import {unauthenticatedRoutes} from './routes'
import {RouteWithSubRoutes} from './common/utils/route'


export default function UnauthenticatedApp(props:object){
  return (
    <Switch>
      {unauthenticatedRoutes.map((route, i) => (
        <RouteWithSubRoutes key={i} {...route} />
      ))}
    </Switch>
  )
}
