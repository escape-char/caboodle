import React, {useState, useEffect} from 'react';
import {useForm} from 'react-hook-form'
import { useHistory } from 'react-router';
import { RouteComponentProps } from 'react-router-dom';
import * as yup from 'yup';
import { SplashPage } from '../pages';
import {Form, FormInput, FormFooter, FormFooterItem} from '../../common/components/forms';
import { InputType } from '../../common/components/inputs/constants';
import {useYupValidationResolver} from '../../common/utils/validation'
import {useAuth} from './context'
import { getURLParams } from '../../common/utils';
import {default as Button, ButtonSize, ButtonVariant, ButtonColor} from '../../common/components/inputs/Button';

const signInSchema = yup.object({
  username: yup.string().required(),
  password: yup.string().required()

})
export default function SignIn(props: RouteComponentProps): React.ReactElement{
    const {login} = useAuth()
    const [redirectTo, setRedirectTo] = useState<string>('/')
    const [isAuthenticating, setIsAuthenticating] = useState(false)
    const history = useHistory()

    const resolver = useYupValidationResolver(signInSchema)
    const methods = useForm({mode: 'onBlur', resolver: resolver})

    useEffect(()=>{
      const params: Record<string, any>  = getURLParams()
      console.log("params: ", params)
      if(params.to){
        setRedirectTo(params.to)
      }
    }, [setRedirectTo])

    async function handleSubmit(values:any){
      setIsAuthenticating(true)

      login(values.username, values.password).finally(()=>{
        window.location.replace(redirectTo)
      })

    }
    return (
      <SplashPage 
          header="Sign In"
          subheader="Sign in to begin managing your bookmarks"
          splashHeader="Welcome to Caboodle"
          splashSubheader="Where we meet all your bookmarking needs"
          splashContent={()=>{
            return (
              <>
                <p>You are just a few seconds away from managing your bookmarks. 
                  You will need to sign up for an account or sign in with an existing account to continue
                </p>
                <Button 
                  onClick={()=>history.push('/signup')}
                  variant={ButtonVariant.CONTAINED} 
                  color={ButtonColor.SECONDARY} 
                  size={ButtonSize.LARGE}
                >
                    Sign Up
                </Button>
              </>

            );
          }}
        >
        <Form onSubmit={handleSubmit} disableGutters useFormResult={methods}>
          <FormInput 
            label="Username" 
            name="username" 
            rules={{required:true}}
            placeholder="Enter username..."
            required
            inputProps={{fullWidth:true}}/>
          <FormInput 
            label="Password" 
            name="password" 
            placeholder="Enter password..."
            type={InputType.PASSWORD}
            inputProps={{fullWidth:true}}/>

          <FormFooter>
            <FormFooterItem>
              <Button 
                disabled={!methods.formState.isValid || isAuthenticating}
                loading={isAuthenticating}
                fullWidth={true} 
                type="submit"
                variant={ButtonVariant.CONTAINED} 
                color={ButtonColor.PRIMARY}>
                  Sign In
               </Button>
            </FormFooterItem>
            <FormFooterItem>
              <Button 
                onClick={()=>history.push("/forgot-password")}
                fullWidth={true} size={ButtonSize.SMALL}>
                Forgot Your Password?</Button>
            </FormFooterItem>
            <FormFooterItem>
              <Button 
                onClick={()=>history.push("/signup")}
                fullWidth={true} size={ButtonSize.SMALL}>Don't Have an Account?</Button>
            </FormFooterItem>
          </FormFooter>
        </Form>
      </SplashPage>
    );
}
