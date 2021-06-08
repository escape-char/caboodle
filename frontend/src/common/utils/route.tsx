import React from 'react';
import { Route, RouteProps as RouterRouteProps } from 'react-router-dom';


export interface RouteProps extends RouterRouteProps {
  routes?: RouteProps[]
}

export function RouteWithSubRoutes(route: any) {
  return (
    <Route
      path={route.path}
      render={(props) => {
        return (
          <route.component {...props} routes={route.routes} />
        );
      }}
    />
  );
}
