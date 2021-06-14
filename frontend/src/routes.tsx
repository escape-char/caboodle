import {Redirect} from 'react-router-dom'
import { RouteProps } from './common/utils/route';
import SignIn from './features/auth/SignIn';
import { getURLPathWithParams } from './common/utils';
import PlaceholderPage from './features/pages/PlaceholderPage'

export const authenticatedRoutes: RouteProps[] = [
  {
    path: "/",
    render: (props)=>{
      return(
        <PlaceholderPage {...props} title="Home"/>
      )
    }
  }

];
export const unauthenticatedRoutes: RouteProps[] = [
  {
    path: "/signin",
    component: SignIn,
  },
  {
    path: "/signup",
    render: (props)=>{
      return(
        <PlaceholderPage {...props} title="Sign Up"/>
      )
    }
  },
  {
    path: "/forgot-password",
    render: (props)=>{
      return(
        <PlaceholderPage {...props} title="Forgot Password"/>
      )
    }
  },
  {
    render: (props)=>{
      console.log("inside catch all unauthenticated")
      const to: string = getURLPathWithParams()
      console.log("to: ", to)
      return (<Redirect to={`/signin?to=${to}`}/>)
    }
  }
];
