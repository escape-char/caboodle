/**
 * Tests for the form UI component
 */
import React from 'react';
import {waitFor, render, screen, fireEvent} from '@testing-library/react';
import { useFormContext, Controller } from "react-hook-form"
import userEvent from '@testing-library/user-event';
import Form from './Form';
import { act } from 'react-dom/test-utils';

const INPUT_NAME = "testing";
const DEFAULT_VALUE = "defaultvalue";

/**
 * mock TestInput component for testing controllers within form
 * @param props 
 * @returns react element of mock test input
 */
function TestInput(props:any): React.ReactElement{
  const { control, errors} = useFormContext();
  return (
    <Controller
      name={INPUT_NAME}
      control={control}
      defaultValue={DEFAULT_VALUE}
      rules={props.rules}
      render={(
        {onChange, value, name},
        {invalid}
      ) => {
        return (
          <>
            <input onChange={onChange} defaultValue={value} name={INPUT_NAME} role="input" type="text"/>
            {invalid && <p> {errors[name]}</p>  }
          </>
        );
      }}
    />
  );
}

test('test rendering of form', () => {
  render(<Form onSubmit={()=>{}}><TestInput/></Form>);

  //test form is rendered
  screen.getByRole("form");
  //test children are rendered
  screen.getByRole("input")
});

test('test submitting form', async ()=>{
  const handleSubmit = jest.fn();
  const VALUE:string = "value";

  render(<Form onSubmit={handleSubmit}><TestInput/><input role="submit" type="submit"/></Form>);

  await waitFor(()=>{
    fireEvent.submit(screen.getByRole("submit"))
  })
  expect(handleSubmit).toHaveBeenCalled();
  expect(handleSubmit.mock.calls[0][0]).toEqual({testing: DEFAULT_VALUE});

})
