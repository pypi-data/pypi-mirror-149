import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const BOOL_INPUT = 'boolean';

export interface IBooleanProps {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue?: boolean;
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IBooleanInput extends IBooleanProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const BooleanInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  error,
  onChange,
  className
}: IBooleanInput): JSX.Element => {
  const [isChecked, setIsChecked] = useState(defaultValue);

  return (
    <div
      className={`BooleanInput ${className} ${
        isChecked ? 'checked' : 'unchecked'
      }`}
    >
      <h4>{label}</h4>
      <p>{description}</p>
      <label htmlFor={id}>
        <input
          id={id}
          className="boolInput"
          type="checkbox"
          defaultChecked={defaultValue}
          onChange={(e: any) => {
            setIsChecked(e.target.checked ? true : false);
            onChange(id, format, e.target.checked ? true : false);
          }}
        />
        <span>
          <FontAwesomeIcon icon={isChecked ? faCheck : faTimes} />
        </span>
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
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledBooleanInput = styled(BooleanInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    position: relative;
    display: inline-block;
  }

  label span {
    box-sizing: border-box;
    min-width: 75px;
    margin: 0;
    padding: 15px 25px;
    display: block;

    text-align: center;
    font-size: 16px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    cursor: pointer;
    transition: 0.2s ease-in-out all;
    -moz-appearance: textfield;
  }

  input {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  label span:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  input:checked + span {
    background-color: #005c75;
    color: white;
  }
`;

export default StyledBooleanInput;
