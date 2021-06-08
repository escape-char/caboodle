/**
 * Tests for the input UI component
 */
import React from 'react';
import { render, screen, fireEvent} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Input from './Input';

const NAME="input1";
const VALUE="defaultvalue";
const LABEL="label"

test('test rendering of input', () => {
  
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE}/>);

  const input:HTMLElement = screen.getByRole("input");

  //check label is rendered
  screen.getByText(LABEL)

  //the form control group should exist
  screen.getByRole("group");

  //must have passed in value and default to text
  expect(input.getAttribute("value")).toEqual(VALUE);
  expect(input.getAttribute("type")).toEqual("text");

});

test('test rendering of required input', () => {
  
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} required/>);

  expect(screen.getByRole("label").closest('label')).toHaveClass("Mui-required");
  expect(screen.getByText("*")).toBeInTheDocument();
  expect(screen.getByRole("input").closest('input')).toBeRequired();
});

test('test rendering of error with message input', () => {
  const HELPER_TEXT = "this field has an error";
  
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} error helperText={HELPER_TEXT}/>);

  expect(screen.getByRole("label").closest('label')).toHaveClass("Mui-error");
  expect(screen.getByRole('input').parentElement).toHaveClass('Mui-error');
  expect(screen.getByText(HELPER_TEXT).closest("p")).toHaveClass("Mui-error");

});
test('test rendering of message input', () => {
  const HELPER_TEXT = "this field has a message";
  
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} helperText={HELPER_TEXT}/>);

  screen.getByText(HELPER_TEXT)

});

test('test rendering of disabled input', () => {
  const HELPER_TEXT = "this field has a message";
  
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} disabled/>);

  const input:HTMLElement = screen.getByRole("input");

  expect(screen.getByRole("label").closest('label')).toHaveClass("Mui-disabled");
  expect(input.closest("input")).toHaveClass("Mui-disabled");
  expect(input.closest("input")).toBeDisabled();
  expect(input.closest("input")?.parentElement).toHaveClass("Mui-disabled")

});

test('test value changing in input', ()=>{
  const handleChange = jest.fn();
  const CHANGED_VALUE = "test change";
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} onChange={handleChange}/>);

  //typing adds to existing value in input
  userEvent.type(screen.getByRole('input'), CHANGED_VALUE);

  expect(handleChange).toHaveBeenCalled();
  expect(handleChange.mock.calls[0][0].target.value).toEqual(`${VALUE}${CHANGED_VALUE}`);


})

test('test value blur event in input', ()=>{
  const handleBlur = jest.fn();
  const CHANGED_VALUE = "test change";
  render(<Input label={LABEL} name={NAME} defaultValue={VALUE} onBlur={handleBlur}/>);

  //typing adds to existing value in input
  fireEvent.blur(screen.getByRole('input'))

  expect(handleBlur).toHaveBeenCalled();
  expect(handleBlur.mock.calls[0][0].target.value).toEqual(`${VALUE}`);
})

