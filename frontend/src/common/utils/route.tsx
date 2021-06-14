import React from 'react';
import { Route, RouteProps as RouterRouteProps } from 'react-router-dom';


export interface RouteProps extends RouterRouteProps {
  routes?: RouteProps[]
}

export function RouteWithSubRoutes(route: any) {
  const renderRoute = (props: object) =>{
    return (<route.component {...props} routes={route.routes} />)
  }
  const render = route.render ||  renderRoute
  
  return (
    <Route
      path={route.path}
      render={render}
    />
  );
}
