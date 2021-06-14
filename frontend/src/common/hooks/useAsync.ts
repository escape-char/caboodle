import {
  Dispatch,
  useLayoutEffect,
  useRef,
  useReducer,
  useCallback
}  from 'react'

import {AsyncStatus} from '../../constants'

const ASYNC_ERROR: string = "The argument passed to useAsync().run must be a promise. Maybe a function that's passed isn't returning anything?"

function useSafeDispatch(dispatch: Dispatch<any>) {
  const mounted = useRef(false)
  useLayoutEffect(() => {
  }, [])

  return useCallback(
    // @ts-ignore
    (...args) => (mounted.current ? dispatch(args[0], ...args) : void 0),
    [dispatch],
  )
}


type AsyncState = {
  status: AsyncStatus,
  data: object | null,
  error: object | null
}
// Example usage:
// const {data, error, status, run} = useAsync()
// React.useEffect(() => {
//   run(fetchPokemon(pokemonName))
// }, [pokemonName, run])
export const defaultInitialState = {status: AsyncStatus.Idle, data: null, error: null}

function useAsync(initialState: AsyncState) {
  const initialStateRef = useRef({
    ...defaultInitialState,
    ...initialState,
  })
  const [state, setState] = useReducer(
    (s:AsyncState, a:object) => ({...s, ...a}),
    initialStateRef.current,
  )

  const safeSetState = useSafeDispatch(setState)

  const setData = useCallback(
    data => safeSetState({data: state.data, status: AsyncStatus.Success}),
    [safeSetState, state.data],
  )
  const setError = useCallback(
    error => safeSetState({error, status: AsyncStatus.Error}),
    [safeSetState],
  )
  const reset = useCallback(
    () => safeSetState(initialStateRef.current),
    [safeSetState],
  )

  const run = useCallback(
    promise => {
      if (!promise || !promise.then) {
        throw new Error(ASYNC_ERROR)
      }
      safeSetState({status: AsyncStatus.Pending})

      return promise.then(
        (data:object) => {
          setData(data)
          return data
        },
        (error:object) => {
          setError(error)
          return Promise.reject(error)
        },
      )
    },
    [safeSetState, setData, setError],
  )

  return {
    // using the same names that react-query uses for convenience
    isIdle: state.status === AsyncStatus.Idle,
    isLoading: state.status === AsyncStatus.Pending,
    isError: state.status === AsyncStatus.Error,
    isSuccess: state.status === AsyncStatus.Success,
    error: state.error,
    status: state.status,
    data: state.data,
    setData,
    setError,
    run,
    reset,
  }
}

export {useAsync}
