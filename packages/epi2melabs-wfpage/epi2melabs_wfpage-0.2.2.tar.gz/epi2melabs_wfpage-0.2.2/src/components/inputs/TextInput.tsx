import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const STR_INPUT = 'string';

export interface ITextProps {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue: string;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface ITextInput extends ITextProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const TextInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  minLength,
  maxLength,
  pattern,
  error,
  onChange,
  className
}: ITextInput): JSX.Element => (
  <div className={`TextInput ${className}`}>
    <h4>{label}</h4>
    <p>{description}</p>
    <label htmlFor={id}>
      <input
        id={id}
        type="text"
        placeholder={'Enter a value'}
        defaultValue={defaultValue}
        pattern={pattern}
        minLength={minLength}
        maxLength={maxLength}
        onChange={e => onChange(id, format, e.target.value)}
      />
    </label>
    {error.length ? (
      <div className="error">
        {error.map(Error => (
          <p>Error: {Error}</p>
        ))}
      </div>
    ) : (
      ''
    )}
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledTextInput = styled(TextInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  input {
    box-sizing: border-box;
    width: 100%;
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  input:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledTextInput;
